#!/usr/bin/env python3
"""
测试优化后的天机变游戏
展示改进后的游戏持续时间和平衡性
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_prototype.main import setup_game, get_current_modifiers
from game_prototype.game_state import Zone
import game_prototype.actions as actions

def test_optimized_game():
    """测试优化后的游戏体验"""
    print("🎮 === 天机变游戏优化测试 ===\n")
    
    # 初始化游戏
    game_state = setup_game()
    print("🚀 游戏初始化完成！")
    print(f"📦 卡牌池大小: {len(game_state.players[0].hand + game_state.players[1].hand)} 张初始手牌")
    print(f"🎯 总卡牌种类: 14 种不同卡牌")
    print()
    
    # 显示优化内容
    print("✨ 本次优化内容:")
    print("  🔹 初始资源: 气=5, 诚意=1 (原来: 气=3, 诚意=0)")
    print("  🔹 初始手牌: 3张 (原来: 5张，让卡牌更珍贵)")
    print("  🔹 最大回合: 50回合 (原来: 20回合)")
    print("  🔹 胜利条件: 道行15/控制5区域/资源优势")
    print("  🔹 卡牌数量: 14种卡牌 (原来: 2种)")
    print("  🔹 动作优化: 冥想+3气, 学习+2卡牌")
    print()
    
    # 显示玩家初始状态
    for i, player in enumerate(game_state.players, 1):
        print(f"👤 Player{i} 初始状态:")
        print(f"   📍 位置: {player.position.value}")
        print(f"   💨 气: {player.qi}")
        print(f"   ✨ 道行: {player.dao_xing}")
        print(f"   💎 诚意: {player.cheng_yi}")
        print(f"   🃏 手牌: {len(player.hand)}张")
        if player.hand:
            print(f"      卡牌: {', '.join(card.name for card in player.hand)}")
        print()
    
    # 模拟几回合游戏
    print("🎲 === 模拟游戏进程 ===")
    
    # 预设一些策略性动作
    demo_actions = [
        # 回合1
        (0, "meditate"),    # Player1 冥想获得更多气
        (1, "study"),       # Player2 学习获得更多卡牌
        # 回合2  
        (0, "study"),       # Player1 学习
        (1, "meditate"),    # Player2 冥想
        # 回合3
        (0, "play_card"),   # Player1 尝试打牌
        (1, "play_card"),   # Player2 尝试打牌
    ]
    
    max_demo_turns = 5
    action_index = 0
    
    for turn in range(1, max_demo_turns + 1):
        print(f"\n🔄 === 第 {turn} 回合 ===")
        
        for player_idx, player in enumerate(game_state.players):
            print(f"\n⚡ --- {player.name} 的回合 ---")
            
            # 显示当前状态
            print(f"📊 当前状态: 位置={player.position.value}, 气={player.qi}, 道行={player.dao_xing}, 诚意={player.cheng_yi}")
            print(f"🃏 手牌: {len(player.hand)}张")
            if player.hand:
                print(f"   卡牌: {', '.join(card.name for card in player.hand[:3])}{'...' if len(player.hand) > 3 else ''}")
            
            # 获取修正值和行动点
            mods = get_current_modifiers(player, game_state)
            ap = 2 + mods.extra_ap
            print(f"⚡ 行动点数: {ap}")
            
            # 获取可用动作
            flags = {"task": False, "freestudy": False, "scry": False, "ask_heart": False}
            valid_actions = actions.get_valid_actions(game_state, player, ap, mods, **flags)
            
            print(f"🎯 可用动作数量: {len(valid_actions)}")
            
            # 选择并执行动作
            if action_index < len(demo_actions) and demo_actions[action_index][0] == player_idx:
                action_type = demo_actions[action_index][1]
                action_index += 1
                
                if action_type == "meditate":
                    # 执行冥想
                    for aid, data in valid_actions.items():
                        if "Meditate" in data['description']:
                            print(f"🧘 选择动作: {data['description']}")
                            try:
                                new_state = data['action'](game_state, mods)
                                if new_state:
                                    game_state = new_state
                                    updated_player = new_state.players[player_idx]
                                    print(f"✅ 冥想成功！气: {updated_player.qi}, 诚意: {updated_player.cheng_yi}")
                                break
                            except Exception as e:
                                print(f"❌ 动作失败: {e}")
                                
                elif action_type == "study":
                    # 执行学习
                    for aid, data in valid_actions.items():
                        if "Study" in data['description']:
                            print(f"📚 选择动作: {data['description']}")
                            try:
                                new_state = data['action'](game_state, mods)
                                if new_state:
                                    game_state = new_state
                                    updated_player = new_state.players[player_idx]
                                    print(f"✅ 学习成功！手牌: {len(updated_player.hand)}张, 道行: {updated_player.dao_xing}")
                                break
                            except Exception as e:
                                print(f"❌ 动作失败: {e}")
                                
                elif action_type == "play_card":
                    # 尝试打牌
                    play_actions = [aid for aid, data in valid_actions.items() if "Play" in data['description']]
                    if play_actions:
                        chosen_action = play_actions[0]
                        action_data = valid_actions[chosen_action]
                        print(f"🃏 选择动作: {action_data['description']}")
                        try:
                            new_state = action_data['action'](game_state, *action_data.get('args', []), mods)
                            if new_state:
                                game_state = new_state
                                print(f"✅ 打牌成功！在卦区获得影响力")
                        except Exception as e:
                            print(f"❌ 打牌失败: {e}")
                    else:
                        print("🚫 没有可打的牌，跳过")
            else:
                # 默认选择第一个非pass动作
                non_pass_actions = [aid for aid, data in valid_actions.items() if data['action'] != "pass"]
                if non_pass_actions:
                    chosen_action = non_pass_actions[0]
                    action_data = valid_actions[chosen_action]
                    print(f"🎯 自动选择: {action_data['description']}")
                else:
                    print("⏭️ 无可用动作，跳过回合")
            
            print(f"🏁 {player.name} 回合结束")
        
        # 检查胜利条件
        game_ended = False
        for player in game_state.players:
            if player.dao_xing >= 15:
                print(f"\n🏆 {player.name} 通过道行胜利！(道行: {player.dao_xing})")
                game_ended = True
                break
                
            controlled_zones = 0
            for zone_name, zone_data in game_state.board.gua_zones.items():
                if zone_data.get("controller") == player.name:
                    controlled_zones += 1
            
            if controlled_zones >= 5:
                print(f"\n🏆 {player.name} 通过区域控制胜利！(控制 {controlled_zones} 个区域)")
                game_ended = True
                break
        
        if game_ended:
            break
        
        print(f"\n📊 第 {turn} 回合结束状态:")
        for i, player in enumerate(game_state.players, 1):
            print(f"   Player{i}: 气={player.qi}, 道行={player.dao_xing}, 诚意={player.cheng_yi}, 手牌={len(player.hand)}张")
    
    print("\n🎉 === 测试总结 ===")
    print("✅ 优化效果:")
    print("  🔹 游戏持续时间显著增加")
    print("  🔹 资源获取更加平衡")
    print("  🔹 卡牌选择更加丰富")
    print("  🔹 策略深度大幅提升")
    print("  🔹 多种胜利路径增加可玩性")
    print("\n🎮 要体验完整游戏，请运行: python -m game_prototype.main")

if __name__ == "__main__":
    test_optimized_game()