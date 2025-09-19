#!/usr/bin/env python3
"""
交互式演示：展示天机变游戏的双人模式
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_prototype.main import setup_game, get_current_modifiers
from game_prototype.game_state import Zone
import game_prototype.actions as actions

def interactive_demo():
    """交互式双人游戏演示"""
    print("=== 天机变游戏双人模式交互演示 ===\n")
    
    # 初始化游戏
    game_state = setup_game()
    print("🎮 游戏开始！")
    print(f"👑 玩家1: {game_state.players[0].name} ({game_state.players[0].avatar.name.value})")
    print(f"🧙 玩家2: {game_state.players[1].name} ({game_state.players[1].avatar.name.value})")
    print()
    
    # 显示游戏规则
    print("📋 游戏规则简介:")
    print("- 每个玩家每回合有2点行动点数(AP)")
    print("- 可以打牌到对应卦区获得影响力")
    print("- 可以移动到不同区域(消耗气)")
    print("- 可以冥想获得气，学习抽取卡牌")
    print("- 目标是获得道行，率先达到胜利条件获胜")
    print()
    
    # 预设一些动作来演示
    demo_actions = [
        (0, 4),  # Player1 打牌
        (1, 6),  # Player2 冥想
        (0, 8),  # Player1 冥想
        (1, 5),  # Player2 学习
        (0, 1),  # Player1 跳过
        (1, 1),  # Player2 跳过
    ]
    
    action_index = 0
    max_turns = 3
    
    for turn in range(1, max_turns + 1):
        print(f"🔄 === 第 {turn} 回合 ===")
        
        for player_idx, player in enumerate(game_state.players):
            print(f"\n⚡ --- {player.name} 的回合 ---")
            
            # 显示玩家状态
            print(f"📍 位置: {player.position.value}")
            print(f"💨 气: {player.qi}")
            print(f"✨ 道行: {player.dao_xing}")
            print(f"🃏 手牌: {len(player.hand)}张")
            if player.hand:
                print(f"   卡牌: {', '.join(card.name for card in player.hand)}")
            
            # 获取修正值和行动点
            mods = get_current_modifiers(player, game_state)
            ap = 2 + mods.extra_ap
            print(f"⚡ 行动点数: {ap}")
            
            # 获取可用动作
            flags = {"task": False, "freestudy": False, "scry": False, "ask_heart": False}
            valid_actions = actions.get_valid_actions(game_state, player, ap, mods, **flags)
            
            print("\n🎯 可用动作:")
            for action_id, action_data in valid_actions.items():
                cost = action_data['cost']
                desc = action_data['description']
                print(f"  {action_id}: {desc} (消耗: {cost} AP)")
            
            # 使用预设动作或默认动作
            if action_index < len(demo_actions) and demo_actions[action_index][0] == player_idx:
                chosen_action = demo_actions[action_index][1]
                action_index += 1
            else:
                # 默认选择第一个非pass动作，如果没有就pass
                non_pass_actions = [aid for aid, data in valid_actions.items() if data['action'] != "pass"]
                chosen_action = non_pass_actions[0] if non_pass_actions else 1
            
            # 确保选择的动作存在
            if chosen_action not in valid_actions:
                chosen_action = 1  # 默认pass
            
            action_data = valid_actions[chosen_action]
            print(f"\n🎯 选择动作: {action_data['description']}")
            
            # 执行动作
            if action_data['action'] == "pass":
                print("⏭️ 跳过回合")
            else:
                try:
                    action_func = action_data['action']
                    args = action_data.get('args', [])
                    new_state = action_func(game_state, *args, mods)
                    if new_state:
                        game_state = new_state
                        print("✅ 动作执行成功！")
                        
                        # 显示动作结果
                        updated_player = new_state.get_current_player() if player_idx == new_state.current_player_index else new_state.players[player_idx]
                        if "Play" in action_data['description']:
                            print(f"🃏 在卦区放置了影响力标记")
                        elif "Move" in action_data['description']:
                            print(f"📍 移动到: {updated_player.position.value}")
                        elif "Meditate" in action_data['description']:
                            print(f"💨 获得气，当前气: {updated_player.qi}")
                        elif "Study" in action_data['description']:
                            print(f"🃏 抽取卡牌，当前手牌: {len(updated_player.hand)}张")
                    else:
                        print("❌ 动作执行失败")
                except Exception as e:
                    print(f"💥 动作执行出错: {e}")
            
            print(f"🏁 {player.name} 回合结束")
            print("─" * 50)
        
        # 显示当前棋盘状态
        print(f"\n🏁 第 {turn} 回合结束")
        print("🗺️ 当前棋盘状态:")
        for zone_name, zone_data in game_state.board.gua_zones.items():
            controller = zone_data.get("controller") or "无人控制"
            markers = zone_data.get("markers", {})
            if markers:
                markers_str = ", ".join(f"{name}:{count}" for name, count in markers.items())
                print(f"  【{zone_name}】控制者: {controller} | 影响力: {markers_str}")
            else:
                print(f"  【{zone_name}】控制者: {controller} | 影响力: 无")
        print()
    
    print("🎉 === 演示结束 ===")
    print("这就是天机变游戏的双人模式！")
    print("🎯 游戏特色:")
    print("- 策略性的卡牌打法")
    print("- 区域控制机制")
    print("- 资源管理(气、道行)")
    print("- 回合制对战")
    print("\n要开始真正的游戏，请运行: python -m game_prototype.main")

if __name__ == "__main__":
    interactive_demo()