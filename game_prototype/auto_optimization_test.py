#!/usr/bin/env python3
"""
自动化游戏测试脚本 - 运行100次游戏并收集优化数据
"""

import random
import time
import json
import statistics
from typing import Dict, List, Any, Tuple
from collections import defaultdict, Counter
import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_state import GameState, Player, Zone
from main import setup_game
from bot_player import get_bot_choice
from yijing_actions import check_victory_conditions_enhanced
from enhanced_victory import check_enhanced_victory_conditions

class GameAnalyzer:
    """游戏分析器 - 收集和分析游戏数据"""
    
    def __init__(self):
        self.game_results = []
        self.performance_data = []
        self.balance_issues = []
        self.ai_decisions = []
        
    def run_automated_tests(self, num_games: int = 100):
        """运行自动化测试"""
        print(f"🎮 开始运行 {num_games} 次自动化游戏测试...")
        print("=" * 60)
        
        for game_num in range(1, num_games + 1):
            print(f"\r进度: {game_num}/{num_games} ({game_num/num_games*100:.1f}%)", end="", flush=True)
            
            try:
                result = self._run_single_game(game_num)
                self.game_results.append(result)
                
                # 每10局输出一次中间统计
                if game_num % 10 == 0:
                    self._print_intermediate_stats(game_num)
                    
            except Exception as e:
                print(f"\n❌ 游戏 {game_num} 出现错误: {e}")
                self.balance_issues.append({
                    'game_num': game_num,
                    'error': str(e),
                    'type': 'runtime_error'
                })
        
        print(f"\n\n✅ 完成 {len(self.game_results)} 次游戏测试")
        self._analyze_results()
        
    def _run_single_game(self, game_num: int) -> Dict[str, Any]:
        """运行单次游戏并收集数据"""
        start_time = time.time()
        
        # 随机选择玩家数量 (2-4人)
        num_players = random.choice([2, 3, 4])
        game_state = setup_game(num_players)
        
        # 游戏数据收集
        game_data = {
            'game_num': game_num,
            'num_players': num_players,
            'turns': 0,
            'winner': None,
            'victory_type': None,
            'game_duration': 0,
            'final_scores': {},
            'resource_distribution': {},
            'ai_performance': {},
            'balance_metrics': {}
        }
        
        # 模拟游戏进行
        max_turns = 100  # 防止无限循环
        turn_count = 0
        
        while turn_count < max_turns:
            turn_count += 1
            
            # 检查胜利条件
            victory_result = self._check_all_victory_conditions(game_state)
            if victory_result['winner']:
                game_data['winner'] = victory_result['winner'].name
                game_data['victory_type'] = victory_result['type']
                break
            
            # 执行回合
            self._simulate_turn(game_state, game_data)
            
            # 检查游戏是否陷入僵局
            if self._is_stalemate(game_state, turn_count):
                game_data['victory_type'] = 'stalemate'
                break
        
        # 记录最终数据
        game_data['turns'] = turn_count
        game_data['game_duration'] = time.time() - start_time
        game_data['final_scores'] = self._calculate_final_scores(game_state)
        game_data['resource_distribution'] = self._analyze_resource_distribution(game_state)
        
        return game_data
    
    def _simulate_turn(self, game_state: GameState, game_data: Dict):
        """模拟一个回合"""
        for player in game_state.players:
            if not player.is_active:
                continue
                
            # 模拟AI决策
            actions_taken = 0
            max_actions = 3  # 每回合最多3个行动
            
            while actions_taken < max_actions and player.ap > 0:
                # 简化的AI决策逻辑
                action_choice = self._make_ai_decision(player, game_state)
                
                if action_choice == 'play_card' and player.hand:
                    self._simulate_play_card(player, game_state)
                elif action_choice == 'meditate':
                    self._simulate_meditate(player)
                elif action_choice == 'move':
                    self._simulate_move(player)
                else:
                    break  # 无法执行更多行动
                
                actions_taken += 1
        
        # 回合结束处理
        self._end_turn_processing(game_state)
    
    def _make_ai_decision(self, player: Player, game_state: GameState) -> str:
        """简化的AI决策逻辑"""
        if player.ap <= 0:
            return 'pass'
        
        # 基于当前状态做决策
        if player.hand and player.ap >= 2:
            return 'play_card'
        elif player.qi < 5:
            return 'meditate'
        elif random.random() < 0.3:
            return 'move'
        else:
            return 'play_card' if player.hand else 'meditate'
    
    def _simulate_play_card(self, player: Player, game_state: GameState):
        """模拟打牌行动"""
        if not player.hand or player.ap < 2:
            return
        
        card = random.choice(player.hand)
        player.hand.remove(card)
        player.ap -= 2
        
        # 简化的卡牌效果
        if hasattr(card, 'qi_cost'):
            player.qi = max(0, player.qi - getattr(card, 'qi_cost', 1))
        
        # 增加影响力
        zone = random.choice(list(Zone))
        if not hasattr(player, 'influence'):
            player.influence = {}
        if zone not in player.influence:
            player.influence[zone] = 0
        player.influence[zone] += random.randint(1, 3)
    
    def _simulate_meditate(self, player: Player):
        """模拟冥想行动"""
        if player.ap < 1:
            return
        
        player.ap -= 1
        player.qi += random.randint(2, 4)
        player.dao_xing += random.randint(0, 1)
    
    def _simulate_move(self, player: Player):
        """模拟移动行动"""
        if player.ap < 1:
            return
        
        player.ap -= 1
        # 简化的移动逻辑
        new_zone = random.choice(list(Zone))
        player.current_zone = new_zone
    
    def _end_turn_processing(self, game_state: GameState):
        """回合结束处理"""
        for player in game_state.players:
            # 恢复行动点
            player.ap = min(3, player.ap + 2)
            
            # 资源自然恢复
            if player.qi < 10:
                player.qi += 1
    
    def _check_all_victory_conditions(self, game_state: GameState) -> Dict[str, Any]:
        """检查所有胜利条件"""
        # 检查道行胜利
        for player in game_state.players:
            if player.dao_xing >= 20:
                return {'winner': player, 'type': 'dao_xing'}
        
        # 检查区域控制胜利
        for player in game_state.players:
            controlled_zones = 0
            if hasattr(player, 'influence') and isinstance(player.influence, dict):
                controlled_zones = sum(1 for zone in Zone if 
                                     zone in player.influence and 
                                     player.influence[zone] >= 5)
            if controlled_zones >= 5:
                return {'winner': player, 'type': 'zone_control'}
        
        # 检查文化胜利
        for player in game_state.players:
            yin_qi = getattr(player, 'yin_qi', 0)
            yang_qi = getattr(player, 'yang_qi', 0)
            wuxing_total = 0
            if hasattr(player, 'wuxing_affinities') and isinstance(player.wuxing_affinities, dict):
                wuxing_total = sum(player.wuxing_affinities.values())
            
            total_culture = yin_qi + yang_qi + wuxing_total
            if total_culture >= 50:
                return {'winner': player, 'type': 'culture'}
        
        return {'winner': None, 'type': None}
    
    def _is_stalemate(self, game_state: GameState, turn_count: int) -> bool:
        """检查是否陷入僵局"""
        if turn_count > 80:  # 超过80回合认为是僵局
            return True
        
        # 检查是否所有玩家都无法行动
        active_players = sum(1 for p in game_state.players if p.is_active and p.ap > 0)
        return active_players == 0
    
    def _calculate_final_scores(self, game_state: GameState) -> Dict[str, int]:
        """计算最终分数"""
        scores = {}
        for player in game_state.players:
            # 安全地获取影响力总和
            influence_total = 0
            if hasattr(player, 'influence') and isinstance(player.influence, dict):
                influence_total = sum(player.influence.values())
            elif hasattr(player, 'influence_markers'):
                influence_total = player.influence_markers
            
            # 安全地获取阴阳气
            yin_qi = getattr(player, 'yin_qi', 0)
            yang_qi = getattr(player, 'yang_qi', 0)
            
            score = (player.dao_xing * 5 + 
                    player.qi + 
                    influence_total +
                    (yin_qi + yang_qi) * 2)
            scores[player.name] = score
        return scores
    
    def _analyze_resource_distribution(self, game_state: GameState) -> Dict[str, Any]:
        """分析资源分布"""
        influence_totals = []
        for p in game_state.players:
            if hasattr(p, 'influence') and isinstance(p.influence, dict):
                influence_totals.append(sum(p.influence.values()))
            elif hasattr(p, 'influence_markers'):
                influence_totals.append(p.influence_markers)
            else:
                influence_totals.append(0)
        
        resources = {
            'qi_distribution': [p.qi for p in game_state.players],
            'dao_xing_distribution': [p.dao_xing for p in game_state.players],
            'influence_distribution': influence_totals
        }
        return resources
    
    def _print_intermediate_stats(self, completed_games: int):
        """打印中间统计信息"""
        if not self.game_results:
            return
        
        print(f"\n\n📊 中间统计 ({completed_games} 局):")
        
        # 胜利类型分布
        victory_types = [r['victory_type'] for r in self.game_results if r['victory_type']]
        if victory_types:
            victory_counter = Counter(victory_types)
            print("胜利类型分布:")
            for vtype, count in victory_counter.most_common():
                print(f"  {vtype}: {count} 次 ({count/len(victory_types)*100:.1f}%)")
        
        # 平均游戏时长
        durations = [r['game_duration'] for r in self.game_results]
        avg_duration = statistics.mean(durations)
        print(f"平均游戏时长: {avg_duration:.2f} 秒")
        
        # 平均回合数
        turns = [r['turns'] for r in self.game_results]
        avg_turns = statistics.mean(turns)
        print(f"平均回合数: {avg_turns:.1f}")
    
    def _analyze_results(self):
        """分析测试结果并生成优化建议"""
        print("\n" + "="*60)
        print("🔍 游戏分析报告")
        print("="*60)
        
        self._analyze_game_balance()
        self._analyze_performance()
        self._analyze_ai_behavior()
        self._generate_optimization_suggestions()
        
        # 保存详细报告
        self._save_analysis_report()
    
    def _analyze_game_balance(self):
        """分析游戏平衡性"""
        print("\n📊 游戏平衡性分析:")
        
        # 胜利条件分析
        victory_types = [r['victory_type'] for r in self.game_results if r['victory_type']]
        victory_counter = Counter(victory_types)
        
        print("胜利条件分布:")
        total_victories = len(victory_types)
        for vtype, count in victory_counter.most_common():
            percentage = count / total_victories * 100
            print(f"  {vtype}: {count} 次 ({percentage:.1f}%)")
            
            # 标记平衡问题
            if percentage > 60:
                self.balance_issues.append({
                    'type': 'victory_imbalance',
                    'issue': f"{vtype} 胜利条件过于容易达成 ({percentage:.1f}%)",
                    'severity': 'high'
                })
            elif percentage < 10 and total_victories > 20:
                self.balance_issues.append({
                    'type': 'victory_underused',
                    'issue': f"{vtype} 胜利条件很少被使用 ({percentage:.1f}%)",
                    'severity': 'medium'
                })
        
        # 游戏时长分析
        turns = [r['turns'] for r in self.game_results]
        avg_turns = statistics.mean(turns)
        max_turns = max(turns)
        min_turns = min(turns)
        
        print(f"\n回合数统计:")
        print(f"  平均: {avg_turns:.1f} 回合")
        print(f"  最长: {max_turns} 回合")
        print(f"  最短: {min_turns} 回合")
        
        if avg_turns > 50:
            self.balance_issues.append({
                'type': 'game_too_long',
                'issue': f"游戏平均时长过长 ({avg_turns:.1f} 回合)",
                'severity': 'medium'
            })
        elif avg_turns < 10:
            self.balance_issues.append({
                'type': 'game_too_short',
                'issue': f"游戏结束过快 ({avg_turns:.1f} 回合)",
                'severity': 'high'
            })
    
    def _analyze_performance(self):
        """分析性能问题"""
        print("\n⚡ 性能分析:")
        
        durations = [r['game_duration'] for r in self.game_results]
        avg_duration = statistics.mean(durations)
        max_duration = max(durations)
        
        print(f"平均游戏时长: {avg_duration:.2f} 秒")
        print(f"最长游戏时长: {max_duration:.2f} 秒")
        
        if avg_duration > 5:
            self.balance_issues.append({
                'type': 'performance_slow',
                'issue': f"游戏运行较慢 (平均 {avg_duration:.2f} 秒)",
                'severity': 'low'
            })
    
    def _analyze_ai_behavior(self):
        """分析AI行为"""
        print("\n🤖 AI行为分析:")
        
        # 统计僵局情况
        stalemates = sum(1 for r in self.game_results if r['victory_type'] == 'stalemate')
        stalemate_rate = stalemates / len(self.game_results) * 100
        
        print(f"僵局率: {stalemate_rate:.1f}% ({stalemates}/{len(self.game_results)})")
        
        if stalemate_rate > 20:
            self.balance_issues.append({
                'type': 'ai_stalemate',
                'issue': f"AI容易陷入僵局 ({stalemate_rate:.1f}%)",
                'severity': 'high'
            })
    
    def _generate_optimization_suggestions(self):
        """生成优化建议"""
        print("\n💡 优化建议:")
        
        if not self.balance_issues:
            print("  ✅ 未发现明显的平衡性问题")
            return
        
        # 按严重程度排序
        high_priority = [issue for issue in self.balance_issues if issue.get('severity') == 'high']
        medium_priority = [issue for issue in self.balance_issues if issue.get('severity') == 'medium']
        low_priority = [issue for issue in self.balance_issues if issue.get('severity') == 'low']
        
        if high_priority:
            print("\n  🔴 高优先级问题:")
            for issue in high_priority:
                print(f"    • {issue['issue']}")
        
        if medium_priority:
            print("\n  🟡 中优先级问题:")
            for issue in medium_priority:
                print(f"    • {issue['issue']}")
        
        if low_priority:
            print("\n  🟢 低优先级问题:")
            for issue in low_priority:
                print(f"    • {issue['issue']}")
    
    def _save_analysis_report(self):
        """保存分析报告到文件"""
        report = {
            'summary': {
                'total_games': len(self.game_results),
                'avg_turns': statistics.mean([r['turns'] for r in self.game_results]),
                'avg_duration': statistics.mean([r['game_duration'] for r in self.game_results]),
                'victory_distribution': dict(Counter([r['victory_type'] for r in self.game_results if r['victory_type']]))
            },
            'balance_issues': self.balance_issues,
            'detailed_results': self.game_results
        }
        
        with open('game_analysis_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 详细报告已保存到: game_analysis_report.json")

def main():
    """主函数"""
    print("🎯 天机变游戏自动化优化测试")
    print("="*60)
    
    # 设置随机种子以便复现
    random.seed(42)
    
    analyzer = GameAnalyzer()
    
    try:
        analyzer.run_automated_tests(100)
    except KeyboardInterrupt:
        print("\n\n⏹️ 测试被用户中断")
        if analyzer.game_results:
            print("正在分析已完成的游戏...")
            analyzer._analyze_results()
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()