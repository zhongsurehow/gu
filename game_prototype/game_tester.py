"""
游戏自动化测试框架
用于批量测试游戏平衡性和机制有效性
"""

import random
import json
import time
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from game_state import GameState, Player, AvatarName, Zone
from core_engine import CoreGameEngine, ActionType
from balance_analyzer import BalanceAnalyzer, GameAnalysis
from config_manager import get_config

class TestStrategy(Enum):
    """测试策略类型"""
    RANDOM = "random"
    AGGRESSIVE = "aggressive"
    DEFENSIVE = "defensive"
    BALANCED = "balanced"
    DAO_XING_FOCUSED = "dao_xing_focused"
    CHENG_YI_FOCUSED = "cheng_yi_focused"
    INTERACTION_HEAVY = "interaction_heavy"

class TestDifficulty(Enum):
    """测试难度"""
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"
    EXPERT = "expert"

@dataclass
class TestConfiguration:
    """测试配置"""
    num_games: int = 100
    max_turns: int = 50
    player_strategies: List[TestStrategy] = None
    difficulty: TestDifficulty = TestDifficulty.NORMAL
    enable_logging: bool = False
    parallel_games: int = 4
    seed: Optional[int] = None
    
    def __post_init__(self):
        if self.player_strategies is None:
            self.player_strategies = [TestStrategy.BALANCED, TestStrategy.BALANCED]

@dataclass
class TestResult:
    """单次测试结果"""
    game_id: str
    duration: int
    winner: str
    victory_type: str
    strategies_used: List[TestStrategy]
    final_scores: Dict[str, Dict[str, int]]
    balance_issues: List[str]
    execution_time: float

class AIPlayer:
    """AI玩家实现"""
    
    def __init__(self, name: str, strategy: TestStrategy, difficulty: TestDifficulty):
        self.name = name
        self.strategy = strategy
        self.difficulty = difficulty
        self.logger = logging.getLogger(f"AIPlayer.{name}")
        
        # 策略权重配置
        self.strategy_weights = self._get_strategy_weights()
        self.difficulty_modifiers = self._get_difficulty_modifiers()
    
    def choose_action(self, game_state: GameState, available_actions: List[ActionType]) -> ActionType:
        """选择动作"""
        if not available_actions:
            return ActionType.PASS
        
        # 根据策略和难度选择动作
        action_scores = {}
        
        for action in available_actions:
            score = self._evaluate_action(action, game_state)
            action_scores[action] = score
        
        # 应用难度修正
        if self.difficulty == TestDifficulty.EASY:
            # 简单难度：随机性更高
            return random.choice(available_actions)
        elif self.difficulty == TestDifficulty.EXPERT:
            # 专家难度：总是选择最优动作
            return max(action_scores.items(), key=lambda x: x[1])[0]
        else:
            # 普通和困难难度：基于权重的概率选择
            weights = list(action_scores.values())
            if self.difficulty == TestDifficulty.NORMAL:
                # 增加随机性
                weights = [w + random.uniform(-0.2, 0.2) for w in weights]
            
            # 确保权重为正数
            min_weight = min(weights)
            if min_weight <= 0:
                weights = [w - min_weight + 0.1 for w in weights]
            
            return random.choices(available_actions, weights=weights)[0]
    
    def _evaluate_action(self, action: ActionType, game_state: GameState) -> float:
        """评估动作价值"""
        player = self._get_player(game_state)
        if not player:
            return 0.0
        
        base_score = 0.5
        
        # 根据策略调整评分
        if self.strategy == TestStrategy.RANDOM:
            return random.uniform(0, 1)
        
        elif self.strategy == TestStrategy.AGGRESSIVE:
            if action in [ActionType.PLAY_CARD, ActionType.TRANSFORM]:
                base_score += 0.3
            elif action == ActionType.MOVE:
                base_score += 0.2
        
        elif self.strategy == TestStrategy.DEFENSIVE:
            if action in [ActionType.MEDITATE, ActionType.STUDY]:
                base_score += 0.3
            elif action == ActionType.DIVINE:
                base_score += 0.1
        
        elif self.strategy == TestStrategy.DAO_XING_FOCUSED:
            if action in [ActionType.STUDY, ActionType.MEDITATE]:
                base_score += 0.4
            # 如果接近道行胜利，优先相关动作
            if player.dao_xing >= 15:
                base_score += 0.2
        
        elif self.strategy == TestStrategy.CHENG_YI_FOCUSED:
            if action in [ActionType.PLAY_CARD, ActionType.TRANSFORM]:
                base_score += 0.4
            # 如果接近诚意胜利，优先相关动作
            if player.cheng_yi >= 10:
                base_score += 0.2
        
        elif self.strategy == TestStrategy.INTERACTION_HEAVY:
            if action in [ActionType.PLAY_CARD, ActionType.MOVE, ActionType.TRANSFORM]:
                base_score += 0.3
        
        # 考虑当前游戏状态
        base_score += self._evaluate_game_state(action, player, game_state)
        
        return max(0, min(1, base_score))
    
    def _evaluate_game_state(self, action: ActionType, player: Player, game_state: GameState) -> float:
        """基于游戏状态评估动作"""
        modifier = 0.0
        
        # 资源状态考虑
        if player.qi < 3 and action == ActionType.MEDITATE:
            modifier += 0.2  # 气不足时优先冥想
        
        if len(player.hand) < 3 and action == ActionType.STUDY:
            modifier += 0.15  # 手牌不足时优先学习
        
        # 胜利条件接近度
        if player.dao_xing >= 15 and action in [ActionType.STUDY, ActionType.MEDITATE]:
            modifier += 0.25  # 接近道行胜利
        
        if player.cheng_yi >= 10 and action in [ActionType.PLAY_CARD, ActionType.TRANSFORM]:
            modifier += 0.25  # 接近诚意胜利
        
        # 阴阳平衡考虑
        balance_ratio = player.yin_yang_balance.balance_ratio
        if balance_ratio < 0.3 or balance_ratio > 0.7:
            # 失衡时优先平衡动作
            if action in [ActionType.MEDITATE, ActionType.TRANSFORM]:
                modifier += 0.1
        
        return modifier
    
    def _get_player(self, game_state: GameState) -> Optional[Player]:
        """获取当前AI玩家对象"""
        for player in game_state.players:
            if player.name == self.name:
                return player
        return None
    
    def _get_strategy_weights(self) -> Dict[ActionType, float]:
        """获取策略权重"""
        base_weights = {
            ActionType.STUDY: 0.2,
            ActionType.MEDITATE: 0.2,
            ActionType.PLAY_CARD: 0.2,
            ActionType.MOVE: 0.15,
            ActionType.TRANSFORM: 0.15,
            ActionType.DIVINE: 0.1,
            ActionType.PASS: 0.05
        }
        
        # 根据策略调整权重
        if self.strategy == TestStrategy.AGGRESSIVE:
            base_weights[ActionType.PLAY_CARD] += 0.2
            base_weights[ActionType.TRANSFORM] += 0.15
            base_weights[ActionType.MOVE] += 0.1
        elif self.strategy == TestStrategy.DEFENSIVE:
            base_weights[ActionType.MEDITATE] += 0.2
            base_weights[ActionType.STUDY] += 0.15
            base_weights[ActionType.DIVINE] += 0.1
        
        return base_weights
    
    def _get_difficulty_modifiers(self) -> Dict[str, float]:
        """获取难度修正值"""
        return {
            TestDifficulty.EASY: 0.7,
            TestDifficulty.NORMAL: 1.0,
            TestDifficulty.HARD: 1.3,
            TestDifficulty.EXPERT: 1.5
        }

class GameTester:
    """游戏测试器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.balance_analyzer = BalanceAnalyzer()
        self.test_results: List[TestResult] = []
    
    def run_test_suite(self, config: TestConfiguration) -> Dict[str, Any]:
        """运行测试套件"""
        self.logger.info(f"开始运行测试套件：{config.num_games}局游戏")
        
        if config.seed:
            random.seed(config.seed)
        
        start_time = time.time()
        
        # 并行执行测试
        if config.parallel_games > 1:
            results = self._run_parallel_tests(config)
        else:
            results = self._run_sequential_tests(config)
        
        execution_time = time.time() - start_time
        
        # 分析结果
        analysis = self._analyze_test_results(results, execution_time)
        
        # 生成报告
        report = self._generate_test_report(analysis, config)
        
        self.logger.info(f"测试套件完成，耗时 {execution_time:.2f} 秒")
        
        return report
    
    def _run_parallel_tests(self, config: TestConfiguration) -> List[TestResult]:
        """并行运行测试"""
        results = []
        
        with ThreadPoolExecutor(max_workers=config.parallel_games) as executor:
            # 提交所有测试任务
            futures = []
            for i in range(config.num_games):
                future = executor.submit(self._run_single_test, i, config)
                futures.append(future)
            
            # 收集结果
            for future in as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                except Exception as e:
                    self.logger.error(f"测试执行失败: {e}")
        
        return results
    
    def _run_sequential_tests(self, config: TestConfiguration) -> List[TestResult]:
        """顺序运行测试"""
        results = []
        
        for i in range(config.num_games):
            try:
                result = self._run_single_test(i, config)
                if result:
                    results.append(result)
                
                # 进度报告
                if (i + 1) % 10 == 0:
                    self.logger.info(f"已完成 {i + 1}/{config.num_games} 局测试")
            
            except Exception as e:
                self.logger.error(f"第 {i+1} 局测试失败: {e}")
        
        return results
    
    def _run_single_test(self, game_id: int, config: TestConfiguration) -> Optional[TestResult]:
        """运行单次测试"""
        start_time = time.time()
        
        try:
            # 创建游戏引擎
            engine = CoreGameEngine()
            
            # 创建AI玩家
            ai_players = []
            for i, strategy in enumerate(config.player_strategies):
                player_name = f"Player_{i+1}"
                ai_player = AIPlayer(player_name, strategy, config.difficulty)
                ai_players.append(ai_player)
            
            # 初始化游戏
            game_state = self._create_test_game_state(ai_players)
            game_history = []
            
            # 游戏主循环
            turn = 0
            while turn < config.max_turns:
                current_player_idx = turn % len(ai_players)
                current_ai = ai_players[current_player_idx]
                
                # 获取可用动作
                available_actions = engine.get_available_actions(game_state, current_ai.name)
                
                if not available_actions:
                    break
                
                # AI选择动作
                chosen_action = current_ai.choose_action(game_state, available_actions)
                
                # 执行动作
                action_result = engine.execute_action(game_state, current_ai.name, chosen_action)
                
                # 记录历史
                game_history.append({
                    "turn": turn,
                    "player": current_ai.name,
                    "action": chosen_action.value,
                    "result": action_result.success,
                    "message": action_result.message
                })
                
                # 检查胜利条件
                if engine.check_victory_condition(game_state):
                    break
                
                turn += 1
            
            # 分析游戏结果
            game_analysis = self.balance_analyzer.analyze_game(game_state, game_history)
            
            # 创建测试结果
            execution_time = time.time() - start_time
            
            result = TestResult(
                game_id=f"test_{game_id}",
                duration=turn,
                winner=game_analysis.winner,
                victory_type=game_analysis.victory_type,
                strategies_used=config.player_strategies,
                final_scores=game_analysis.player_stats,
                balance_issues=game_analysis.critical_issues,
                execution_time=execution_time
            )
            
            return result
        
        except Exception as e:
            self.logger.error(f"测试 {game_id} 执行失败: {e}")
            return None
    
    def _create_test_game_state(self, ai_players: List[AIPlayer]) -> GameState:
        """创建测试游戏状态"""
        players = []
        
        for i, ai_player in enumerate(ai_players):
            # 创建玩家
            avatar = list(AvatarName)[i % len(AvatarName)]
            position = list(Zone)[i % len(Zone)]
            
            player = Player(
                name=ai_player.name,
                avatar=avatar,
                position=position
            )
            
            players.append(player)
        
        # 创建游戏状态
        game_state = GameState(players=players)
        
        return game_state
    
    def _analyze_test_results(self, results: List[TestResult], execution_time: float) -> Dict[str, Any]:
        """分析测试结果"""
        if not results:
            return {"error": "没有有效的测试结果"}
        
        analysis = {
            "summary": {
                "total_games": len(results),
                "successful_games": len([r for r in results if r.winner != "无"]),
                "total_execution_time": execution_time,
                "average_game_time": execution_time / len(results)
            },
            "game_length": {
                "average": sum(r.duration for r in results) / len(results),
                "min": min(r.duration for r in results),
                "max": max(r.duration for r in results),
                "distribution": self._get_duration_distribution(results)
            },
            "victory_analysis": self._analyze_victories(results),
            "strategy_performance": self._analyze_strategy_performance(results),
            "balance_issues": self._analyze_balance_issues(results),
            "performance_metrics": self._calculate_performance_metrics(results)
        }
        
        return analysis
    
    def _get_duration_distribution(self, results: List[TestResult]) -> Dict[str, int]:
        """获取游戏时长分布"""
        distribution = {
            "very_short": 0,  # < 10回合
            "short": 0,       # 10-15回合
            "normal": 0,      # 16-25回合
            "long": 0,        # 26-35回合
            "very_long": 0    # > 35回合
        }
        
        for result in results:
            duration = result.duration
            if duration < 10:
                distribution["very_short"] += 1
            elif duration <= 15:
                distribution["short"] += 1
            elif duration <= 25:
                distribution["normal"] += 1
            elif duration <= 35:
                distribution["long"] += 1
            else:
                distribution["very_long"] += 1
        
        return distribution
    
    def _analyze_victories(self, results: List[TestResult]) -> Dict[str, Any]:
        """分析胜利情况"""
        victory_types = {}
        winner_distribution = {}
        
        for result in results:
            # 胜利类型统计
            victory_type = result.victory_type
            victory_types[victory_type] = victory_types.get(victory_type, 0) + 1
            
            # 获胜者分布
            winner = result.winner
            winner_distribution[winner] = winner_distribution.get(winner, 0) + 1
        
        return {
            "victory_types": victory_types,
            "winner_distribution": winner_distribution,
            "completion_rate": len([r for r in results if r.winner != "无"]) / len(results)
        }
    
    def _analyze_strategy_performance(self, results: List[TestResult]) -> Dict[str, Any]:
        """分析策略表现"""
        strategy_stats = {}
        
        for result in results:
            for i, strategy in enumerate(result.strategies_used):
                strategy_name = strategy.value
                
                if strategy_name not in strategy_stats:
                    strategy_stats[strategy_name] = {
                        "games_played": 0,
                        "wins": 0,
                        "total_duration": 0,
                        "total_dao_xing": 0,
                        "total_cheng_yi": 0
                    }
                
                stats = strategy_stats[strategy_name]
                stats["games_played"] += 1
                stats["total_duration"] += result.duration
                
                # 检查是否获胜
                player_name = f"Player_{i+1}"
                if result.winner == player_name:
                    stats["wins"] += 1
                
                # 累计分数
                if player_name in result.final_scores:
                    player_scores = result.final_scores[player_name]
                    stats["total_dao_xing"] += player_scores.get("final_dao_xing", 0)
                    stats["total_cheng_yi"] += player_scores.get("final_cheng_yi", 0)
        
        # 计算平均值和胜率
        for strategy_name, stats in strategy_stats.items():
            games = stats["games_played"]
            if games > 0:
                stats["win_rate"] = stats["wins"] / games
                stats["average_duration"] = stats["total_duration"] / games
                stats["average_dao_xing"] = stats["total_dao_xing"] / games
                stats["average_cheng_yi"] = stats["total_cheng_yi"] / games
        
        return strategy_stats
    
    def _analyze_balance_issues(self, results: List[TestResult]) -> Dict[str, Any]:
        """分析平衡性问题"""
        all_issues = []
        issue_frequency = {}
        
        for result in results:
            all_issues.extend(result.balance_issues)
        
        for issue in all_issues:
            issue_frequency[issue] = issue_frequency.get(issue, 0) + 1
        
        # 按频率排序
        sorted_issues = sorted(issue_frequency.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "total_issues": len(all_issues),
            "unique_issues": len(issue_frequency),
            "most_common_issues": sorted_issues[:10],
            "issue_rate": len(all_issues) / len(results) if results else 0
        }
    
    def _calculate_performance_metrics(self, results: List[TestResult]) -> Dict[str, float]:
        """计算性能指标"""
        if not results:
            return {}
        
        execution_times = [r.execution_time for r in results]
        durations = [r.duration for r in results]
        
        return {
            "average_execution_time": sum(execution_times) / len(execution_times),
            "min_execution_time": min(execution_times),
            "max_execution_time": max(execution_times),
            "games_per_second": len(results) / sum(execution_times),
            "average_turns_per_second": sum(durations) / sum(execution_times)
        }
    
    def _generate_test_report(self, analysis: Dict[str, Any], config: TestConfiguration) -> Dict[str, Any]:
        """生成测试报告"""
        report = {
            "test_configuration": asdict(config),
            "analysis": analysis,
            "recommendations": self._generate_recommendations(analysis),
            "timestamp": time.time()
        }
        
        return report
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """生成优化建议"""
        recommendations = []
        
        # 游戏时长建议
        avg_duration = analysis.get("game_length", {}).get("average", 0)
        if avg_duration < 10:
            recommendations.append("游戏时间过短，建议增加游戏复杂度或调整胜利条件")
        elif avg_duration > 30:
            recommendations.append("游戏时间过长，建议加快游戏节奏或提供更多胜利路径")
        
        # 胜利分析建议
        victory_analysis = analysis.get("victory_analysis", {})
        completion_rate = victory_analysis.get("completion_rate", 0)
        if completion_rate < 0.8:
            recommendations.append("游戏完成率较低，可能存在死锁或平衡问题")
        
        # 策略平衡建议
        strategy_performance = analysis.get("strategy_performance", {})
        win_rates = [stats.get("win_rate", 0) for stats in strategy_performance.values()]
        if win_rates and (max(win_rates) - min(win_rates)) > 0.3:
            recommendations.append("策略间胜率差异过大，需要平衡调整")
        
        # 平衡性问题建议
        balance_issues = analysis.get("balance_issues", {})
        issue_rate = balance_issues.get("issue_rate", 0)
        if issue_rate > 2:
            recommendations.append("平衡性问题频发，建议重点关注核心机制设计")
        
        return recommendations
    
    def export_test_results(self, filename: str = "test_results.json"):
        """导出测试结果"""
        try:
            export_data = {
                "test_results": [asdict(result) for result in self.test_results],
                "balance_analysis": self.balance_analyzer.export_analysis_data()
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2, default=str)
            
            self.logger.info(f"测试结果已导出到 {filename}")
        
        except Exception as e:
            self.logger.error(f"导出测试结果失败: {e}")

# 便捷函数
def run_quick_test(num_games: int = 10, strategies: List[TestStrategy] = None) -> Dict[str, Any]:
    """快速测试函数"""
    if strategies is None:
        strategies = [TestStrategy.BALANCED, TestStrategy.BALANCED]
    
    config = TestConfiguration(
        num_games=num_games,
        player_strategies=strategies,
        parallel_games=2,
        enable_logging=False
    )
    
    tester = GameTester()
    return tester.run_test_suite(config)

def run_balance_test() -> Dict[str, Any]:
    """平衡性测试"""
    strategies_to_test = [
        [TestStrategy.AGGRESSIVE, TestStrategy.DEFENSIVE],
        [TestStrategy.DAO_XING_FOCUSED, TestStrategy.CHENG_YI_FOCUSED],
        [TestStrategy.BALANCED, TestStrategy.INTERACTION_HEAVY],
        [TestStrategy.RANDOM, TestStrategy.BALANCED]
    ]
    
    all_results = []
    tester = GameTester()
    
    for strategies in strategies_to_test:
        config = TestConfiguration(
            num_games=25,
            player_strategies=strategies,
            parallel_games=4
        )
        
        result = tester.run_test_suite(config)
        all_results.append(result)
    
    return {
        "individual_tests": all_results,
        "overall_analysis": tester.balance_analyzer.get_optimization_suggestions()
    }