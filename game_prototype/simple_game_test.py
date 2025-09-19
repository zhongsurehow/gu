#!/usr/bin/env python3
"""
简化的游戏测试脚本
直接使用游戏的实际结构进行测试
"""

import sys
import random
import time
from typing import Dict, List, Any
from game_state import GameState, Player, Avatar, AvatarName, Zone

class SimpleGameTester:
    """简化的游戏测试器"""
    
    def __init__(self):
        self.test_results = []
        self.performance_data = []
        
    def run_tests(self, num_games: int = 100):
        """运行指定数量的游戏测试"""
        print(f"🎮 开始运行 {num_games} 次游戏测试...")
        print("=" * 60)
        
        successful_games = 0
        
        for i in range(num_games):
            try:
                print(f"进度: {i+1}/{num_games} ({((i+1)/num_games)*100:.1f}%)")
                
                start_time = time.time()
                result = self._simulate_single_game()
                end_time = time.time()
                
                if result:
                    self.test_results.append(result)
                    self.performance_data.append({
                        'game_id': i + 1,
                        'duration': end_time - start_time,
                        'turns': result.get('turns', 0),
                        'winner': result.get('winner', 'unknown')
                    })
                    successful_games += 1
                    print(f"✅ 游戏 {i+1} 完成: {result['winner']} 获胜 ({result['turns']} 回合)")
                else:
                    print(f"❌ 游戏 {i+1} 失败")
                    
            except Exception as e:
                print(f"❌ 游戏 {i+1} 出现错误: {str(e)}")
                continue
        
        print(f"\n✅ 完成 {successful_games} 次游戏测试")
        
        if successful_games > 0:
            self._analyze_results()
        else:
            print("❌ 没有成功完成的游戏，无法进行分析")
    
    def _simulate_single_game(self) -> Dict[str, Any]:
        """模拟单次游戏"""
        # 创建玩家
        avatars = [
            Avatar(AvatarName.EMPEROR, "帝王", "统治者"),
            Avatar(AvatarName.HERMIT, "隐士", "修行者"),
        ]
        
        players = [
            Player("玩家1", avatars[0]),
            Player("玩家2", avatars[1])
        ]
        
        # 创建游戏状态，传入players参数
        game_state = GameState(players)
        
        # 模拟游戏进行
        max_turns = 50
        for turn in range(max_turns):
            current_player = game_state.get_current_player()
            
            # 简单的行动模拟
            action_type = random.choice(["学习", "冥想", "变卦", "移动"])
            
            if action_type == "学习":
                # 增加道行和气 (提高获取速度)
                current_player.dao_xing += random.randint(2, 4)
                current_player.qi += random.randint(2, 3)
            elif action_type == "冥想":
                # 增加诚意和气 (提高获取速度)
                current_player.cheng_yi += random.randint(2, 3)
                current_player.qi += random.randint(2, 4)
                current_player.dao_xing += random.randint(1, 2)
                # 模拟阴阳平衡变化
                balance_change = random.randint(-2, 2)
                if balance_change > 0:
                    current_player.yin_yang_balance.yang_points += abs(balance_change)
                else:
                    current_player.yin_yang_balance.yin_points += abs(balance_change)
            elif action_type == "变卦":
                # 变卦行动：消耗诚意，获得道行和气
                if current_player.cheng_yi >= 2:
                    current_player.cheng_yi -= 2
                    current_player.dao_xing += random.randint(2, 3)
                    current_player.qi += random.randint(1, 2)
            elif action_type == "移动":
                # 随机移动到不同区域
                zones = list(Zone)
                current_player.position = random.choice(zones)
            
            # 检查胜利条件
            winner = self._check_victory_conditions(game_state)
            if winner:
                return {
                    'winner': winner.name,
                    'turns': turn + 1,
                    'victory_type': self._determine_victory_type(winner),
                    'final_scores': self._calculate_scores(game_state)
                }
            
            # 切换玩家
            game_state.current_player_index = (game_state.current_player_index + 1) % len(game_state.players)
        
        # 如果达到最大回合数，判断得分胜利
        scores = self._calculate_scores(game_state)
        winner_name = max(scores, key=scores.get)
        winner = next(p for p in game_state.players if p.name == winner_name)
        
        return {
            'winner': winner_name,
            'turns': max_turns,
            'victory_type': 'score',
            'final_scores': scores
        }
    
    def _check_victory_conditions(self, game_state: GameState) -> Player:
        """检查胜利条件"""
        for player in game_state.players:
            # 道行胜利 (提高阈值以降低其优势)
            if player.dao_xing >= 25:
                return player
            
            # 诚意胜利 (降低阈值以增强竞争力)
            if player.cheng_yi >= 12:
                return player
            
            # 气的积累胜利 (降低阈值以增强竞争力)
            if player.qi >= 25:
                return player
        
        return None
    
    def _determine_victory_type(self, winner: Player) -> str:
        """确定胜利类型"""
        if winner.dao_xing >= 25:
            return "道行胜利"
        elif winner.cheng_yi >= 12:
            return "诚意胜利"
        elif winner.qi >= 25:
            return "气胜利"
        else:
            return "综合胜利"
    
    def _calculate_scores(self, game_state: GameState) -> Dict[str, int]:
        """计算玩家得分"""
        scores = {}
        for player in game_state.players:
            score = (
                player.dao_xing * 10 +
                player.cheng_yi * 8 +
                player.qi * 5 +
                abs(player.yin_yang_balance.balance_ratio) * -5  # 平衡越好得分越高
            )
            scores[player.name] = score
        return scores
    
    def _analyze_results(self):
        """分析测试结果"""
        print("\n" + "=" * 60)
        print("🔍 游戏分析报告")
        print("=" * 60)
        
        # 基本统计
        total_games = len(self.test_results)
        total_turns = sum(result['turns'] for result in self.test_results)
        avg_turns = total_turns / total_games if total_games > 0 else 0
        
        print(f"\n📊 基本统计:")
        print(f"总游戏数: {total_games}")
        print(f"平均回合数: {avg_turns:.1f}")
        print(f"最短游戏: {min(result['turns'] for result in self.test_results)} 回合")
        print(f"最长游戏: {max(result['turns'] for result in self.test_results)} 回合")
        
        # 胜利类型分析
        victory_types = {}
        for result in self.test_results:
            victory_type = result['victory_type']
            victory_types[victory_type] = victory_types.get(victory_type, 0) + 1
        
        print(f"\n🏆 胜利类型分布:")
        for victory_type, count in victory_types.items():
            percentage = (count / total_games) * 100
            print(f"{victory_type}: {count} 次 ({percentage:.1f}%)")
        
        # 玩家胜率分析
        winners = {}
        for result in self.test_results:
            winner = result['winner']
            winners[winner] = winners.get(winner, 0) + 1
        
        print(f"\n👑 玩家胜率:")
        for player, wins in winners.items():
            win_rate = (wins / total_games) * 100
            print(f"{player}: {wins} 胜 ({win_rate:.1f}%)")
        
        # 性能分析
        if self.performance_data:
            avg_duration = sum(data['duration'] for data in self.performance_data) / len(self.performance_data)
            print(f"\n⚡ 性能统计:")
            print(f"平均游戏时长: {avg_duration:.3f} 秒")
            print(f"每回合平均时间: {(avg_duration / avg_turns):.3f} 秒")
        
        # 优化建议
        self._generate_optimization_suggestions(victory_types, avg_turns, winners)
    
    def _generate_optimization_suggestions(self, victory_types: Dict, avg_turns: float, winners: Dict):
        """生成优化建议"""
        print(f"\n💡 优化建议:")
        print("-" * 40)
        
        # 游戏平衡性建议
        if len(winners) > 1:
            win_rates = [count / len(self.test_results) for count in winners.values()]
            max_win_rate = max(win_rates)
            min_win_rate = min(win_rates)
            
            if max_win_rate - min_win_rate > 0.2:  # 胜率差距超过20%
                print("⚠️  玩家胜率不平衡，建议调整角色能力或初始资源")
        
        # 游戏时长建议
        if avg_turns < 10:
            print("⚠️  游戏时长过短，建议增加胜利条件难度")
        elif avg_turns > 40:
            print("⚠️  游戏时长过长，建议降低胜利条件难度或增加资源获取速度")
        
        # 胜利类型多样性建议
        if len(victory_types) < 3:
            print("⚠️  胜利类型单一，建议平衡各种胜利路径的可行性")
        
        # 具体优化建议
        dominant_victory = max(victory_types, key=victory_types.get) if victory_types else None
        if dominant_victory and victory_types[dominant_victory] / len(self.test_results) > 0.6:
            print(f"⚠️  {dominant_victory} 过于强势，建议调整相关机制")
        
        print("\n✅ 分析完成！")

def main():
    """主函数"""
    print("🎯 天机变游戏优化测试")
    print("=" * 60)
    
    tester = SimpleGameTester()
    tester.run_tests(100)

if __name__ == "__main__":
    main()