#!/usr/bin/env python3
"""
天机变游戏AI决策逻辑优化
实现智能AI策略和决策优化
"""

import random
import sys
import os
from typing import Dict, List, Tuple, Optional
from enum import Enum

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class AIStrategy(Enum):
    """AI策略类型"""
    AGGRESSIVE = "aggressive"      # 激进型：快速获胜
    BALANCED = "balanced"         # 平衡型：均衡发展
    DEFENSIVE = "defensive"       # 防守型：稳健发展
    ADAPTIVE = "adaptive"         # 自适应：根据情况调整

class AIDecisionMaker:
    """AI决策制定器"""
    
    def __init__(self, strategy: AIStrategy = AIStrategy.BALANCED):
        self.strategy = strategy
        self.decision_history = []
        self.performance_metrics = {
            'wins': 0,
            'losses': 0,
            'avg_turns': 0,
            'strategy_effectiveness': {}
        }
        
    def evaluate_game_state(self, player, opponent) -> Dict[str, float]:
        """评估当前游戏状态"""
        evaluation = {
            'dao_xing_advantage': (player.dao_xing - opponent.dao_xing) / 25.0,
            'cheng_yi_advantage': (player.cheng_yi - opponent.cheng_yi) / 12.0,
            'qi_advantage': (player.qi - opponent.qi) / 25.0,
            'balance_stability': self._evaluate_balance_stability(player),
            'victory_proximity': self._calculate_victory_proximity(player),
            'opponent_threat': self._calculate_opponent_threat(opponent)
        }
        
        # 计算总体优势
        evaluation['overall_advantage'] = (
            evaluation['dao_xing_advantage'] * 0.3 +
            evaluation['cheng_yi_advantage'] * 0.25 +
            evaluation['qi_advantage'] * 0.25 +
            evaluation['balance_stability'] * 0.1 +
            evaluation['victory_proximity'] * 0.1
        )
        
        return evaluation
        
    def _evaluate_balance_stability(self, player) -> float:
        """评估阴阳平衡稳定性"""
        if hasattr(player, 'yin_yang_balance'):
            balance_ratio = player.yin_yang_balance.balance_ratio
            # 平衡度越接近0.5越好
            stability = 1.0 - abs(balance_ratio - 0.5) * 2
            return max(0.0, stability)
        return 0.5
        
    def _calculate_victory_proximity(self, player) -> float:
        """计算胜利接近度"""
        dao_xing_progress = min(player.dao_xing / 25.0, 1.0)
        cheng_yi_progress = min(player.cheng_yi / 12.0, 1.0)
        qi_progress = min(player.qi / 25.0, 1.0)
        
        return max(dao_xing_progress, cheng_yi_progress, qi_progress)
        
    def _calculate_opponent_threat(self, opponent) -> float:
        """计算对手威胁度"""
        return self._calculate_victory_proximity(opponent)
        
    def choose_action(self, player, opponent, available_actions: List[str]) -> str:
        """选择最佳行动"""
        evaluation = self.evaluate_game_state(player, opponent)
        
        # 根据策略选择行动
        if self.strategy == AIStrategy.AGGRESSIVE:
            action = self._aggressive_strategy(player, opponent, available_actions, evaluation)
        elif self.strategy == AIStrategy.DEFENSIVE:
            action = self._defensive_strategy(player, opponent, available_actions, evaluation)
        elif self.strategy == AIStrategy.ADAPTIVE:
            action = self._adaptive_strategy(player, opponent, available_actions, evaluation)
        else:  # BALANCED
            action = self._balanced_strategy(player, opponent, available_actions, evaluation)
            
        # 记录决策
        self.decision_history.append({
            'action': action,
            'evaluation': evaluation,
            'strategy': self.strategy.value
        })
        
        return action
        
    def _aggressive_strategy(self, player, opponent, actions: List[str], eval_data: Dict) -> str:
        """激进策略：优先快速获胜"""
        # 如果接近胜利，专注于最接近的胜利条件
        if eval_data['victory_proximity'] > 0.7:
            if player.dao_xing >= 20:
                return "学习"  # 冲刺道行胜利
            elif player.cheng_yi >= 10:
                return "冥想"  # 冲刺诚意胜利
            elif player.qi >= 20:
                return "变卦"  # 冲刺气胜利
                
        # 对手威胁高时，加快发展
        if eval_data['opponent_threat'] > 0.6:
            return random.choice(["学习", "冥想", "变卦"])
            
        # 默认快速发展
        return random.choice(["学习", "冥想"])
        
    def _defensive_strategy(self, player, opponent, actions: List[str], eval_data: Dict) -> str:
        """防守策略：稳健发展"""
        # 平衡发展，避免过度专精
        if player.dao_xing < 15 and player.cheng_yi < 8:
            return "学习"  # 基础发展
        elif player.cheng_yi < 8:
            return "冥想"  # 补充诚意
        elif eval_data['balance_stability'] < 0.3:
            return "冥想"  # 调整平衡
        else:
            return "变卦"  # 稳步提升
            
    def _adaptive_strategy(self, player, opponent, actions: List[str], eval_data: Dict) -> str:
        """自适应策略：根据情况调整"""
        # 根据优势情况调整策略
        if eval_data['overall_advantage'] > 0.3:
            # 优势时采用激进策略
            return self._aggressive_strategy(player, opponent, actions, eval_data)
        elif eval_data['overall_advantage'] < -0.3:
            # 劣势时采用防守策略
            return self._defensive_strategy(player, opponent, actions, eval_data)
        else:
            # 均势时采用平衡策略
            return self._balanced_strategy(player, opponent, actions, eval_data)
            
    def _balanced_strategy(self, player, opponent, actions: List[str], eval_data: Dict) -> str:
        """平衡策略：均衡发展"""
        # 根据当前状态选择最需要的发展方向
        scores = {
            "学习": self._calculate_action_value(player, "学习", eval_data),
            "冥想": self._calculate_action_value(player, "冥想", eval_data),
            "变卦": self._calculate_action_value(player, "变卦", eval_data)
        }
        
        # 选择价值最高的行动
        best_action = max(scores.items(), key=lambda x: x[1])[0]
        return best_action
        
    def _calculate_action_value(self, player, action: str, eval_data: Dict) -> float:
        """计算行动价值"""
        value = 0.0
        
        if action == "学习":
            # 道行价值
            dao_need = max(0, 25 - player.dao_xing) / 25.0
            value += dao_need * 0.6
            # 气价值
            qi_need = max(0, 25 - player.qi) / 25.0
            value += qi_need * 0.4
            
        elif action == "冥想":
            # 诚意价值
            cheng_need = max(0, 12 - player.cheng_yi) / 12.0
            value += cheng_need * 0.5
            # 气价值
            qi_need = max(0, 25 - player.qi) / 25.0
            value += qi_need * 0.3
            # 平衡调整价值
            balance_need = 1.0 - eval_data['balance_stability']
            value += balance_need * 0.2
            
        elif action == "变卦":
            # 需要足够诚意
            if player.cheng_yi >= 2:
                # 道行和气的综合价值
                dao_need = max(0, 25 - player.dao_xing) / 25.0
                qi_need = max(0, 25 - player.qi) / 25.0
                value += (dao_need + qi_need) * 0.4
            else:
                value = 0.0  # 诚意不足，无法变卦
                
        return value
        
    def update_performance(self, won: bool, turns: int):
        """更新性能指标"""
        if won:
            self.performance_metrics['wins'] += 1
        else:
            self.performance_metrics['losses'] += 1
            
        # 更新平均回合数
        total_games = self.performance_metrics['wins'] + self.performance_metrics['losses']
        self.performance_metrics['avg_turns'] = (
            (self.performance_metrics['avg_turns'] * (total_games - 1) + turns) / total_games
        )
        
        # 更新策略效果
        strategy_name = self.strategy.value
        if strategy_name not in self.performance_metrics['strategy_effectiveness']:
            self.performance_metrics['strategy_effectiveness'][strategy_name] = {
                'wins': 0, 'games': 0, 'avg_turns': 0
            }
            
        strategy_stats = self.performance_metrics['strategy_effectiveness'][strategy_name]
        strategy_stats['games'] += 1
        if won:
            strategy_stats['wins'] += 1
        strategy_stats['avg_turns'] = (
            (strategy_stats['avg_turns'] * (strategy_stats['games'] - 1) + turns) / strategy_stats['games']
        )

class AIOptimizationTester:
    """AI优化测试器"""
    
    def __init__(self):
        self.test_results = {}
        
    def test_strategy_performance(self, strategy: AIStrategy, games: int = 100):
        """测试策略性能"""
        print(f"🤖 测试AI策略: {strategy.value} ({games}局游戏)")
        
        ai_player = AIDecisionMaker(strategy)
        wins = 0
        total_turns = 0
        
        for game in range(games):
            result = self._simulate_ai_game(ai_player)
            if result['winner'] == 'ai':
                wins += 1
            total_turns += result['turns']
            
            ai_player.update_performance(result['winner'] == 'ai', result['turns'])
            
        win_rate = wins / games
        avg_turns = total_turns / games
        
        self.test_results[strategy.value] = {
            'win_rate': win_rate,
            'avg_turns': avg_turns,
            'games': games
        }
        
        print(f"  胜率: {win_rate:.1%}")
        print(f"  平均回合数: {avg_turns:.1f}")
        print(f"  性能评分: {self._calculate_performance_score(win_rate, avg_turns):.2f}")
        
        return ai_player.performance_metrics
        
    def _simulate_ai_game(self, ai_player: AIDecisionMaker) -> Dict:
        """模拟AI游戏"""
        # 简化的游戏模拟
        class MockPlayer:
            def __init__(self, name):
                self.name = name
                self.dao_xing = 0
                self.cheng_yi = 0
                self.qi = 0
                self.yin_yang_balance = MockBalance()
                
        class MockBalance:
            def __init__(self):
                self.yin_points = 50
                self.yang_points = 50
                
            @property
            def balance_ratio(self):
                total = self.yin_points + self.yang_points
                return self.yin_points / total if total > 0 else 0.5
        
        ai = MockPlayer("AI")
        opponent = MockPlayer("对手")
        
        max_turns = 50
        for turn in range(max_turns):
            # AI回合
            action = ai_player.choose_action(ai, opponent, ["学习", "冥想", "变卦"])
            self._apply_action(ai, action)
            
            if self._check_victory(ai):
                return {'winner': 'ai', 'turns': turn + 1}
                
            # 对手回合（随机策略）
            opponent_action = random.choice(["学习", "冥想", "变卦"])
            self._apply_action(opponent, opponent_action)
            
            if self._check_victory(opponent):
                return {'winner': 'opponent', 'turns': turn + 1}
                
        # 平局，按分数判断
        ai_score = ai.dao_xing + ai.cheng_yi + ai.qi
        opp_score = opponent.dao_xing + opponent.cheng_yi + opponent.qi
        
        winner = 'ai' if ai_score > opp_score else 'opponent'
        return {'winner': winner, 'turns': max_turns}
        
    def _apply_action(self, player, action: str):
        """应用行动效果"""
        if action == "学习":
            player.dao_xing += random.randint(2, 4)
            player.qi += random.randint(2, 3)
        elif action == "冥想":
            player.cheng_yi += random.randint(2, 3)
            player.qi += random.randint(2, 4)
            player.dao_xing += random.randint(1, 2)
        elif action == "变卦":
            if player.cheng_yi >= 2:
                player.cheng_yi -= 2
                player.dao_xing += random.randint(1, 3)
                player.qi += random.randint(2, 4)
                
    def _check_victory(self, player) -> bool:
        """检查胜利条件"""
        return (player.dao_xing >= 25 or 
                player.cheng_yi >= 12 or 
                player.qi >= 25)
                
    def _calculate_performance_score(self, win_rate: float, avg_turns: float) -> float:
        """计算性能评分"""
        # 胜率权重70%，效率权重30%
        efficiency_score = max(0, (50 - avg_turns) / 50)  # 回合数越少越好
        return win_rate * 0.7 + efficiency_score * 0.3
        
    def compare_strategies(self):
        """比较不同策略"""
        print("\n" + "=" * 60)
        print("🏆 AI策略性能对比")
        print("=" * 60)
        
        if not self.test_results:
            print("❌ 没有测试数据")
            return
            
        # 按性能评分排序
        sorted_strategies = sorted(
            self.test_results.items(),
            key=lambda x: self._calculate_performance_score(x[1]['win_rate'], x[1]['avg_turns']),
            reverse=True
        )
        
        print(f"{'策略':<12} {'胜率':<8} {'平均回合':<10} {'性能评分':<10}")
        print("-" * 50)
        
        for strategy, data in sorted_strategies:
            score = self._calculate_performance_score(data['win_rate'], data['avg_turns'])
            win_rate_str = f"{data['win_rate']:.1%}"
            print(f"{strategy:<12} {win_rate_str:<8} {data['avg_turns']:<10.1f} {score:<10.2f}")
            
        best_strategy = sorted_strategies[0][0]
        print(f"\n🥇 最佳策略: {best_strategy}")
        
        return best_strategy

def main():
    """主函数"""
    print("🧠 开始AI决策逻辑优化测试")
    print("=" * 60)
    
    tester = AIOptimizationTester()
    
    # 测试所有策略
    strategies = [
        AIStrategy.AGGRESSIVE,
        AIStrategy.BALANCED, 
        AIStrategy.DEFENSIVE,
        AIStrategy.ADAPTIVE
    ]
    
    for strategy in strategies:
        tester.test_strategy_performance(strategy, 50)
        print()
        
    # 比较策略性能
    best_strategy = tester.compare_strategies()
    
    print(f"\n💡 优化建议:")
    print("----------------------------------------")
    print(f"✅ 推荐使用 {best_strategy} 策略")
    print("✅ AI决策逻辑已优化完成")
    print("✅ 可根据实际游戏情况进一步调整参数")

if __name__ == "__main__":
    main()