"""
游戏平衡性分析系统
用于分析游戏机制的平衡性，提供优化建议
"""

import json
import statistics
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import logging

from config_manager import get_config
from game_state import GameState, Player, Zone
from yijing_mechanics import YinYangBalance, WuXing

class BalanceMetric(Enum):
    """平衡性指标"""
    RESOURCE_DISTRIBUTION = "resource_distribution"
    ACTION_EFFICIENCY = "action_efficiency"
    VICTORY_PATH_VIABILITY = "victory_path_viability"
    PLAYER_INTERACTION = "player_interaction"
    GAME_LENGTH = "game_length"
    STRATEGY_DIVERSITY = "strategy_diversity"
    LUCK_VS_SKILL = "luck_vs_skill"

@dataclass
class BalanceReport:
    """平衡性报告"""
    metric: BalanceMetric
    score: float  # 0-100分
    issues: List[str]
    recommendations: List[str]
    data: Dict[str, Any]

@dataclass
class GameAnalysis:
    """游戏分析结果"""
    game_id: str
    duration: int  # 回合数
    winner: str
    victory_type: str
    player_stats: Dict[str, Dict[str, Any]]
    balance_scores: Dict[BalanceMetric, float]
    critical_issues: List[str]

class BalanceAnalyzer:
    """游戏平衡性分析器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.game_history: List[GameAnalysis] = []
        self.balance_thresholds = {
            "excellent": 85,
            "good": 70,
            "acceptable": 55,
            "poor": 40,
            "critical": 25
        }
    
    def analyze_game(self, game_state: GameState, game_history: List[Dict]) -> GameAnalysis:
        """分析单局游戏的平衡性"""
        
        # 基础统计
        duration = game_state.turn
        winner = self._determine_winner(game_state)
        victory_type = self._determine_victory_type(game_state, winner)
        
        # 玩家统计
        player_stats = {}
        for player in game_state.players:
            player_stats[player.name] = self._analyze_player_performance(player, game_history)
        
        # 平衡性评分
        balance_scores = {}
        for metric in BalanceMetric:
            balance_scores[metric] = self._calculate_balance_score(metric, game_state, game_history)
        
        # 关键问题识别
        critical_issues = self._identify_critical_issues(balance_scores, player_stats)
        
        analysis = GameAnalysis(
            game_id=f"game_{len(self.game_history)}",
            duration=duration,
            winner=winner.name if winner else "无",
            victory_type=victory_type,
            player_stats=player_stats,
            balance_scores=balance_scores,
            critical_issues=critical_issues
        )
        
        self.game_history.append(analysis)
        return analysis
    
    def generate_balance_report(self, metric: BalanceMetric) -> BalanceReport:
        """生成特定指标的平衡性报告"""
        
        if not self.game_history:
            return BalanceReport(
                metric=metric,
                score=0,
                issues=["没有足够的游戏数据"],
                recommendations=["需要更多游戏数据来进行分析"],
                data={}
            )
        
        scores = [game.balance_scores[metric] for game in self.game_history]
        avg_score = statistics.mean(scores)
        
        issues = []
        recommendations = []
        data = {}
        
        if metric == BalanceMetric.RESOURCE_DISTRIBUTION:
            issues, recommendations, data = self._analyze_resource_distribution()
        elif metric == BalanceMetric.ACTION_EFFICIENCY:
            issues, recommendations, data = self._analyze_action_efficiency()
        elif metric == BalanceMetric.VICTORY_PATH_VIABILITY:
            issues, recommendations, data = self._analyze_victory_paths()
        elif metric == BalanceMetric.PLAYER_INTERACTION:
            issues, recommendations, data = self._analyze_player_interaction()
        elif metric == BalanceMetric.GAME_LENGTH:
            issues, recommendations, data = self._analyze_game_length()
        elif metric == BalanceMetric.STRATEGY_DIVERSITY:
            issues, recommendations, data = self._analyze_strategy_diversity()
        elif metric == BalanceMetric.LUCK_VS_SKILL:
            issues, recommendations, data = self._analyze_luck_vs_skill()
        
        return BalanceReport(
            metric=metric,
            score=avg_score,
            issues=issues,
            recommendations=recommendations,
            data=data
        )
    
    def get_optimization_suggestions(self) -> Dict[str, List[str]]:
        """获取优化建议"""
        suggestions = {
            "immediate": [],  # 立即修复
            "short_term": [],  # 短期优化
            "long_term": []   # 长期改进
        }
        
        if not self.game_history:
            suggestions["immediate"].append("收集更多游戏数据进行分析")
            return suggestions
        
        # 分析各项指标
        for metric in BalanceMetric:
            report = self.generate_balance_report(metric)
            
            if report.score < self.balance_thresholds["critical"]:
                suggestions["immediate"].extend(report.recommendations)
            elif report.score < self.balance_thresholds["poor"]:
                suggestions["short_term"].extend(report.recommendations)
            elif report.score < self.balance_thresholds["good"]:
                suggestions["long_term"].extend(report.recommendations)
        
        return suggestions
    
    def export_analysis_data(self, filename: str = "balance_analysis.json"):
        """导出分析数据"""
        export_data = {
            "summary": {
                "total_games": len(self.game_history),
                "average_duration": statistics.mean([g.duration for g in self.game_history]) if self.game_history else 0,
                "victory_distribution": self._get_victory_distribution(),
                "overall_balance_score": self._calculate_overall_balance_score()
            },
            "detailed_reports": [self.generate_balance_report(metric) for metric in BalanceMetric],
            "optimization_suggestions": self.get_optimization_suggestions(),
            "game_history": [asdict(game) for game in self.game_history]
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2, default=str)
            self.logger.info(f"分析数据已导出到 {filename}")
        except Exception as e:
            self.logger.error(f"导出分析数据失败: {e}")
    
    # 私有方法 - 分析功能
    def _determine_winner(self, game_state: GameState) -> Optional[Player]:
        """确定获胜者"""
        # 简化的胜利判定逻辑
        for player in game_state.players:
            if player.dao_xing >= 20 or player.cheng_yi >= 15:
                return player
        return None
    
    def _determine_victory_type(self, game_state: GameState, winner: Optional[Player]) -> str:
        """确定胜利类型"""
        if not winner:
            return "未结束"
        
        if winner.dao_xing >= 20:
            return "道行胜利"
        elif winner.cheng_yi >= 15:
            return "诚意胜利"
        else:
            return "其他胜利"
    
    def _analyze_player_performance(self, player: Player, game_history: List[Dict]) -> Dict[str, Any]:
        """分析玩家表现"""
        return {
            "final_dao_xing": player.dao_xing,
            "final_cheng_yi": player.cheng_yi,
            "final_qi": player.qi,
            "yin_yang_balance": player.yin_yang_balance.balance_ratio,
            "hand_size": len(player.hand),
            "position": player.position.value,
            "actions_taken": len([action for action in game_history if action.get("player") == player.name])
        }
    
    def _calculate_balance_score(self, metric: BalanceMetric, game_state: GameState, game_history: List[Dict]) -> float:
        """计算特定指标的平衡性评分"""
        
        if metric == BalanceMetric.RESOURCE_DISTRIBUTION:
            return self._score_resource_distribution(game_state)
        elif metric == BalanceMetric.ACTION_EFFICIENCY:
            return self._score_action_efficiency(game_history)
        elif metric == BalanceMetric.VICTORY_PATH_VIABILITY:
            return self._score_victory_path_viability(game_state)
        elif metric == BalanceMetric.PLAYER_INTERACTION:
            return self._score_player_interaction(game_history)
        elif metric == BalanceMetric.GAME_LENGTH:
            return self._score_game_length(game_state.turn)
        elif metric == BalanceMetric.STRATEGY_DIVERSITY:
            return self._score_strategy_diversity(game_history)
        elif metric == BalanceMetric.LUCK_VS_SKILL:
            return self._score_luck_vs_skill(game_state, game_history)
        
        return 50.0  # 默认中等评分
    
    def _score_resource_distribution(self, game_state: GameState) -> float:
        """评分资源分配平衡性"""
        if len(game_state.players) < 2:
            return 50.0
        
        # 计算各种资源的分布方差
        dao_xing_values = [p.dao_xing for p in game_state.players]
        cheng_yi_values = [p.cheng_yi for p in game_state.players]
        qi_values = [p.qi for p in game_state.players]
        
        # 方差越小，分布越均匀，评分越高
        dao_xing_variance = statistics.variance(dao_xing_values) if len(dao_xing_values) > 1 else 0
        cheng_yi_variance = statistics.variance(cheng_yi_values) if len(cheng_yi_values) > 1 else 0
        qi_variance = statistics.variance(qi_values) if len(qi_values) > 1 else 0
        
        # 归一化评分（方差越小评分越高）
        max_variance = 100  # 假设的最大方差
        avg_variance = (dao_xing_variance + cheng_yi_variance + qi_variance) / 3
        score = max(0, 100 - (avg_variance / max_variance) * 100)
        
        return min(100, score)
    
    def _score_action_efficiency(self, game_history: List[Dict]) -> float:
        """评分动作效率平衡性"""
        if not game_history:
            return 50.0
        
        # 分析不同动作的使用频率
        action_counts = {}
        for action in game_history:
            action_type = action.get("action", "unknown")
            action_counts[action_type] = action_counts.get(action_type, 0) + 1
        
        if len(action_counts) < 2:
            return 30.0  # 动作多样性不足
        
        # 计算动作分布的均匀性
        total_actions = sum(action_counts.values())
        frequencies = [count / total_actions for count in action_counts.values()]
        
        # 使用熵来衡量分布均匀性
        import math
        entropy = -sum(f * math.log2(f) for f in frequencies if f > 0)
        max_entropy = math.log2(len(action_counts))
        
        # 归一化到0-100分
        score = (entropy / max_entropy) * 100 if max_entropy > 0 else 50
        return min(100, score)
    
    def _score_victory_path_viability(self, game_state: GameState) -> float:
        """评分胜利路径可行性"""
        viable_paths = 0
        total_paths = 3  # 道行、诚意、区域控制
        
        for player in game_state.players:
            # 检查道行胜利路径
            if player.dao_xing >= 10:  # 接近胜利条件的一半
                viable_paths += 1
            
            # 检查诚意胜利路径
            if player.cheng_yi >= 7:
                viable_paths += 1
            
            # 检查区域控制（简化）
            # TODO: 实现区域控制检查
        
        # 计算可行路径比例
        viability_ratio = viable_paths / (len(game_state.players) * total_paths)
        return min(100, viability_ratio * 100)
    
    def _score_player_interaction(self, game_history: List[Dict]) -> float:
        """评分玩家互动程度"""
        # 简化的互动评分：基于影响其他玩家的动作数量
        interaction_actions = 0
        total_actions = len(game_history)
        
        for action in game_history:
            action_type = action.get("action", "")
            # 某些动作类型被认为是互动性的
            if action_type in ["play_card", "move", "transform"]:
                interaction_actions += 1
        
        if total_actions == 0:
            return 50.0
        
        interaction_ratio = interaction_actions / total_actions
        return min(100, interaction_ratio * 100)
    
    def _score_game_length(self, turns: int) -> float:
        """评分游戏长度合理性"""
        ideal_length = get_config("game_balance.game_flow.ideal_game_length", 15)
        min_length = get_config("game_balance.game_flow.min_game_length", 8)
        max_length = get_config("game_balance.game_flow.max_game_length", 25)
        
        if min_length <= turns <= max_length:
            # 在合理范围内，越接近理想长度评分越高
            distance_from_ideal = abs(turns - ideal_length)
            max_distance = max(ideal_length - min_length, max_length - ideal_length)
            score = 100 - (distance_from_ideal / max_distance) * 30
            return max(70, score)
        else:
            # 超出合理范围
            if turns < min_length:
                return max(20, 50 - (min_length - turns) * 5)
            else:
                return max(20, 50 - (turns - max_length) * 3)
    
    def _score_strategy_diversity(self, game_history: List[Dict]) -> float:
        """评分策略多样性"""
        # 基于动作序列的多样性来评估
        if len(game_history) < 5:
            return 30.0
        
        # 分析动作模式
        action_patterns = {}
        for i in range(len(game_history) - 2):
            pattern = tuple(action.get("action", "") for action in game_history[i:i+3])
            action_patterns[pattern] = action_patterns.get(pattern, 0) + 1
        
        # 计算模式多样性
        total_patterns = sum(action_patterns.values())
        unique_patterns = len(action_patterns)
        
        if total_patterns == 0:
            return 30.0
        
        # 多样性评分
        diversity_ratio = unique_patterns / total_patterns
        return min(100, diversity_ratio * 200)  # 放大系数
    
    def _score_luck_vs_skill(self, game_state: GameState, game_history: List[Dict]) -> float:
        """评分运气与技巧的平衡"""
        # 简化的评分：基于玩家决策的复杂性和随机性影响
        decision_complexity = 0
        random_events = 0
        
        for action in game_history:
            action_type = action.get("action", "")
            
            # 复杂决策动作
            if action_type in ["play_card", "transform", "divine"]:
                decision_complexity += 1
            
            # 随机性动作
            if action_type in ["divine", "meditate"]:
                random_events += 1
        
        total_actions = len(game_history)
        if total_actions == 0:
            return 50.0
        
        skill_ratio = decision_complexity / total_actions
        luck_ratio = random_events / total_actions
        
        # 理想的技巧与运气比例是7:3
        ideal_skill_ratio = 0.7
        balance_score = 100 - abs(skill_ratio - ideal_skill_ratio) * 200
        
        return max(20, min(100, balance_score))
    
    # 私有方法 - 详细分析
    def _analyze_resource_distribution(self) -> Tuple[List[str], List[str], Dict[str, Any]]:
        """分析资源分配问题"""
        issues = []
        recommendations = []
        data = {}
        
        if not self.game_history:
            return issues, recommendations, data
        
        # 分析资源差距
        resource_gaps = []
        for game in self.game_history:
            dao_xing_values = [stats["final_dao_xing"] for stats in game.player_stats.values()]
            cheng_yi_values = [stats["final_cheng_yi"] for stats in game.player_stats.values()]
            
            if len(dao_xing_values) > 1:
                dao_xing_gap = max(dao_xing_values) - min(dao_xing_values)
                cheng_yi_gap = max(cheng_yi_values) - min(cheng_yi_values)
                resource_gaps.append({"dao_xing_gap": dao_xing_gap, "cheng_yi_gap": cheng_yi_gap})
        
        if resource_gaps:
            avg_dao_xing_gap = statistics.mean([gap["dao_xing_gap"] for gap in resource_gaps])
            avg_cheng_yi_gap = statistics.mean([gap["cheng_yi_gap"] for gap in resource_gaps])
            
            data["average_dao_xing_gap"] = avg_dao_xing_gap
            data["average_cheng_yi_gap"] = avg_cheng_yi_gap
            
            if avg_dao_xing_gap > 10:
                issues.append("道行差距过大，可能导致游戏失衡")
                recommendations.append("调整道行获取机制，增加追赶机制")
            
            if avg_cheng_yi_gap > 8:
                issues.append("诚意差距过大，影响游戏平衡")
                recommendations.append("平衡诚意获取途径，避免单一策略过强")
        
        return issues, recommendations, data
    
    def _analyze_action_efficiency(self) -> Tuple[List[str], List[str], Dict[str, Any]]:
        """分析动作效率问题"""
        issues = []
        recommendations = []
        data = {}
        
        # 统计动作使用频率
        action_usage = {}
        for game in self.game_history:
            # 这里需要从游戏历史中提取动作数据
            # 简化实现
            pass
        
        data["action_usage"] = action_usage
        
        # 基于使用频率识别问题
        if "study" in action_usage and action_usage["study"] > 0.5:
            issues.append("学习动作使用过于频繁，可能过于强力")
            recommendations.append("增加学习动作的成本或减少奖励")
        
        return issues, recommendations, data
    
    def _analyze_victory_paths(self) -> Tuple[List[str], List[str], Dict[str, Any]]:
        """分析胜利路径问题"""
        issues = []
        recommendations = []
        data = {}
        
        # 统计胜利类型分布
        victory_types = {}
        for game in self.game_history:
            victory_type = game.victory_type
            victory_types[victory_type] = victory_types.get(victory_type, 0) + 1
        
        data["victory_distribution"] = victory_types
        
        total_games = len(self.game_history)
        if total_games > 0:
            for victory_type, count in victory_types.items():
                ratio = count / total_games
                if ratio > 0.7:
                    issues.append(f"{victory_type}过于主导，占比{ratio:.1%}")
                    recommendations.append(f"平衡{victory_type}的难度和其他胜利路径")
        
        return issues, recommendations, data
    
    def _analyze_player_interaction(self) -> Tuple[List[str], List[str], Dict[str, Any]]:
        """分析玩家互动问题"""
        issues = []
        recommendations = []
        data = {}
        
        # 分析互动程度
        avg_interaction_score = statistics.mean([
            game.balance_scores.get(BalanceMetric.PLAYER_INTERACTION, 50)
            for game in self.game_history
        ]) if self.game_history else 50
        
        data["average_interaction_score"] = avg_interaction_score
        
        if avg_interaction_score < 40:
            issues.append("玩家互动不足，游戏偏向单机体验")
            recommendations.append("增加更多需要玩家互动的机制")
            recommendations.append("强化区域争夺和资源竞争")
        
        return issues, recommendations, data
    
    def _analyze_game_length(self) -> Tuple[List[str], List[str], Dict[str, Any]]:
        """分析游戏长度问题"""
        issues = []
        recommendations = []
        data = {}
        
        if not self.game_history:
            return issues, recommendations, data
        
        durations = [game.duration for game in self.game_history]
        avg_duration = statistics.mean(durations)
        duration_variance = statistics.variance(durations) if len(durations) > 1 else 0
        
        data["average_duration"] = avg_duration
        data["duration_variance"] = duration_variance
        data["min_duration"] = min(durations)
        data["max_duration"] = max(durations)
        
        if avg_duration < 8:
            issues.append("游戏时间过短，可能缺乏深度")
            recommendations.append("增加游戏复杂度或调整胜利条件")
        elif avg_duration > 25:
            issues.append("游戏时间过长，可能影响体验")
            recommendations.append("加快游戏节奏或提供更多胜利路径")
        
        if duration_variance > 50:
            issues.append("游戏时长变化过大，缺乏一致性")
            recommendations.append("平衡各种策略的效率")
        
        return issues, recommendations, data
    
    def _analyze_strategy_diversity(self) -> Tuple[List[str], List[str], Dict[str, Any]]:
        """分析策略多样性问题"""
        issues = []
        recommendations = []
        data = {}
        
        # 简化的策略多样性分析
        avg_diversity_score = statistics.mean([
            game.balance_scores.get(BalanceMetric.STRATEGY_DIVERSITY, 50)
            for game in self.game_history
        ]) if self.game_history else 50
        
        data["average_diversity_score"] = avg_diversity_score
        
        if avg_diversity_score < 40:
            issues.append("策略多样性不足，存在主导策略")
            recommendations.append("平衡各种策略的效果")
            recommendations.append("增加策略间的相互制约")
        
        return issues, recommendations, data
    
    def _analyze_luck_vs_skill(self) -> Tuple[List[str], List[str], Dict[str, Any]]:
        """分析运气与技巧平衡问题"""
        issues = []
        recommendations = []
        data = {}
        
        avg_luck_skill_score = statistics.mean([
            game.balance_scores.get(BalanceMetric.LUCK_VS_SKILL, 50)
            for game in self.game_history
        ]) if self.game_history else 50
        
        data["average_luck_skill_score"] = avg_luck_skill_score
        
        if avg_luck_skill_score < 40:
            issues.append("运气与技巧平衡不佳")
            recommendations.append("调整随机性元素的影响程度")
            recommendations.append("增加技巧性决策的重要性")
        
        return issues, recommendations, data
    
    # 辅助方法
    def _identify_critical_issues(self, balance_scores: Dict[BalanceMetric, float], player_stats: Dict[str, Dict[str, Any]]) -> List[str]:
        """识别关键问题"""
        critical_issues = []
        
        for metric, score in balance_scores.items():
            if score < self.balance_thresholds["critical"]:
                critical_issues.append(f"{metric.value}评分过低({score:.1f})")
        
        return critical_issues
    
    def _get_victory_distribution(self) -> Dict[str, int]:
        """获取胜利类型分布"""
        distribution = {}
        for game in self.game_history:
            victory_type = game.victory_type
            distribution[victory_type] = distribution.get(victory_type, 0) + 1
        return distribution
    
    def _calculate_overall_balance_score(self) -> float:
        """计算总体平衡评分"""
        if not self.game_history:
            return 0.0
        
        all_scores = []
        for game in self.game_history:
            game_scores = list(game.balance_scores.values())
            if game_scores:
                all_scores.extend(game_scores)
        
        return statistics.mean(all_scores) if all_scores else 0.0