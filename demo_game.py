#!/usr/bin/env python3
"""
演示脚本：展示天机变游戏的双人模式
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_prototype.main import setup_game, get_current_modifiers, run_action_phase
from game_prototype.game_state import Zone
import game_prototype.actions as actions

def demo_two_player_game():
    """演示双人游戏模式"""
    print("=== 天机变游戏双人模式演示 ===\n")
    
    # 初始化游戏
    game_state = setup_game()
    print("游戏初始化完成！")
    print(f"玩家1: {game_state.players[0].name} ({game_state.players[0].avatar.name.value})")
    print(f"玩家2: {game_state.players[1].name} ({game_state.players[1].avatar.name.value})")
    print()
    
    # 显示初始状态
    print("=== 初始游戏状态 ===")
    for i, player in enumerate(game_state.players, 1):
        print(f"玩家{i} ({player.name}):")
        print(f"  - 位置: {player.position.value}")
        print(f"  - 气: {player.qi}")
        print(f"  - 道行: {player.dao_xing}")
        print(f"  - 手牌数量: {len(player.hand)}")
        if player.hand:
            print(f"  - 手牌: {[card.name for card in player.hand]}")
        print()
    
    # 显示棋盘状态
    print("=== 棋盘状态 ===")
    for zone_name, zone_data in game_state.board.gua_zones.items():
        controller = zone_data.get("controller", "无人控制")
        markers = zone_data.get("markers", {})
        markers_str = ", ".join(f"{name}: {count}" for name, count in markers.items()) if markers else "无"
        print(f"【{zone_name}】- 控制者: {controller}, 影响力标记: {markers_str}")
    print()
    
    # 演示几个回合
    max_demo_turns = 3
    for turn in range(1, max_demo_turns + 1):
        print(f"=== 第 {turn} 回合 ===")
        
        for player_idx, player in enumerate(game_state.players):
            print(f"\n--- {player.name} 的回合 ---")
            print(f"当前状态: 位置={player.position.value}, 气={player.qi}, 道行={player.dao_xing}, 手牌={len(player.hand)}张")
            
            # 获取修正值
            mods = get_current_modifiers(player, game_state)
            ap = 2 + mods.extra_ap
            print(f"行动点数: {ap}")
            
            # 获取可用动作
            flags = {"task": False, "freestudy": False, "scry": False, "ask_heart": False}
            valid_actions = actions.get_valid_actions(game_state, player, ap, mods, **flags)
            
            print("可用动作:")
            for action_id, action_data in valid_actions.items():
                print(f"  {action_id}: {action_data['description']} (消耗: {action_data['cost']} AP)")
            
            # 自动选择一个动作进行演示
            if len(valid_actions) > 1:  # 如果有除了pass之外的动作
                # 优先选择打牌动作
                play_actions = [aid for aid, data in valid_actions.items() 
                              if "Play" in data.get('description', '')]
                if play_actions:
                    chosen_action = play_actions[0]
                else:
                    # 选择冥想或学习
                    other_actions = [aid for aid, data in valid_actions.items() 
                                   if aid != 1]  # 排除pass
                    chosen_action = other_actions[0] if other_actions else 1
            else:
                chosen_action = 1  # pass
            
            action_data = valid_actions[chosen_action]
            print(f"\n选择动作: {action_data['description']}")
            
            # 执行动作
            if action_data['action'] == "pass":
                print("跳过回合")
            else:
                try:
                    action_func = action_data['action']
                    args = action_data.get('args', [])
                    new_state = action_func(game_state, *args, mods)
                    if new_state:
                        game_state = new_state
                        print("动作执行成功！")
                    else:
                        print("动作执行失败")
                except Exception as e:
                    print(f"动作执行出错: {e}")
            
            print(f"{player.name} 回合结束")
            print("-" * 40)
        
        print(f"第 {turn} 回合结束\n")
    
    print("=== 演示结束 ===")
    print("这就是天机变游戏的双人模式！")
    print("玩家轮流进行回合，可以打牌、移动、冥想、学习等动作。")
    print("目标是通过控制卦区、完成任务来获得道行，率先达到胜利条件的玩家获胜！")

if __name__ == "__main__":
    demo_two_player_game()