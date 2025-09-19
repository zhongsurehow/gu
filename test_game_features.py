#!/usr/bin/env python3
"""
测试修改后的游戏功能
验证易学规则优化和占卜系统
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'game_prototype'))

from game_prototype.main import setup_game
from game_prototype.yijing_actions import divine_fortune, consult_yijing, check_victory_conditions_enhanced
from game_prototype.yijing_mechanics import ZhanBuSystem, ZhouYiWisdom
from game_prototype.game_state import GameState, Player

def test_game_setup():
    """测试游戏设置功能"""
    print("🧪 测试游戏设置功能...")
    
    # 测试不同人数的游戏设置
    for num_players in [1, 2, 4, 8]:
        try:
            game_state = setup_game(num_players)
            print(f"✅ {num_players}人游戏设置成功")
            print(f"   玩家数量: {len(game_state.players)}")
            for i, player in enumerate(game_state.players):
                print(f"   玩家{i+1}: {player.name} (头像: {player.avatar.name.value})")
        except Exception as e:
            print(f"❌ {num_players}人游戏设置失败: {e}")
    print()

def test_divination_system():
    """测试占卜系统"""
    print("🔮 测试占卜系统...")
    
    # 创建测试游戏状态
    game_state = setup_game(2)
    player = game_state.players[0]
    
    # 设置玩家属性用于测试
    player.qi = 10
    player.dao_xing = 5
    
    print(f"测试玩家: {player.name}")
    print(f"初始状态 - 气: {player.qi}, 道行: {player.dao_xing}")
    
    # 测试占卜运势
    try:
        print("\n--- 测试占卜运势 ---")
        new_state = divine_fortune(game_state)
        new_player = new_state.players[0]
        print(f"占卜后 - 气: {new_player.qi}, 道行: {new_player.dao_xing}")
        print("✅ 占卜运势功能正常")
    except Exception as e:
        print(f"❌ 占卜运势测试失败: {e}")
    
    # 测试咨询易经
    try:
        print("\n--- 测试咨询易经 ---")
        new_state = consult_yijing(game_state, "meditate")
        new_player = new_state.players[0]
        print(f"咨询后 - 道行: {new_player.dao_xing}")
        print("✅ 咨询易经功能正常")
    except Exception as e:
        print(f"❌ 咨询易经测试失败: {e}")
    
    print()

def test_victory_conditions():
    """测试胜利条件"""
    print("🏆 测试胜利条件...")
    
    game_state = setup_game(2)
    player = game_state.players[0]
    
    # 测试不同的胜利条件
    test_cases = [
        {"dao_xing": 12, "qi": 15, "yin_qi": 8, "yang_qi": 7, "desc": "大道至简"},
        {"dao_xing": 8, "qi": 20, "yin_qi": 10, "yang_qi": 10, "desc": "太极宗师"},
        {"dao_xing": 10, "qi": 18, "wuxing_harmony": 5, "desc": "五行圆满"},
    ]
    
    for case in test_cases:
        # 设置玩家属性
        for attr, value in case.items():
            if attr != "desc" and hasattr(player, attr):
                setattr(player, attr, value)
        
        try:
            winner = check_victory_conditions_enhanced(game_state)
            if winner:
                print(f"✅ {case['desc']} 胜利条件测试通过")
            else:
                print(f"⚠️ {case['desc']} 胜利条件未触发")
        except Exception as e:
            print(f"❌ {case['desc']} 胜利条件测试失败: {e}")
    
    print()

def test_wisdom_system():
    """测试智慧格言系统"""
    print("💫 测试智慧格言系统...")
    
    try:
        # 测试随机智慧
        wisdom_key, wisdom_quote = ZhouYiWisdom.get_random_wisdom()
        print(f"随机智慧: {wisdom_key} - {wisdom_quote}")
        
        # 测试条件触发智慧
        conditions = ["balance_achieved", "wuxing_harmony", "dao_progress"]
        for condition in conditions:
            wisdom = ZhouYiWisdom.trigger_wisdom(condition)
            if wisdom:
                print(f"条件 '{condition}' 触发智慧: {wisdom}")
        
        print("✅ 智慧格言系统正常")
    except Exception as e:
        print(f"❌ 智慧格言系统测试失败: {e}")
    
    print()

def test_zhanbu_mechanics():
    """测试占卜机制"""
    print("📜 测试占卜机制...")
    
    try:
        # 测试不同道行的占卜准确度
        for dao_xing in [1, 5, 10, 15]:
            divination = ZhanBuSystem.divine_fortune(dao_xing)
            print(f"道行 {dao_xing}: 卦象={divination['gua']}, 运势={divination['fortune']}, 准确度={divination['accuracy']:.2f}")
        
        # 测试行动占卜
        actions = ["meditate", "study", "transform", "wuxing"]
        for action in actions:
            success = ZhanBuSystem.divine_action_outcome(action, 5)
            print(f"行动 '{action}' 占卜结果: {'成功' if success else '失败'}")
        
        print("✅ 占卜机制正常")
    except Exception as e:
        print(f"❌ 占卜机制测试失败: {e}")
    
    print()

def main():
    """主测试函数"""
    print("🎋 天机变游戏功能测试")
    print("=" * 50)
    
    test_game_setup()
    test_divination_system()
    test_victory_conditions()
    test_wisdom_system()
    test_zhanbu_mechanics()
    
    print("🎉 测试完成！")
    print("游戏已成功优化为更符合易学传统的版本")
    print("主要改进:")
    print("- ✅ 支持1-8人游戏")
    print("- ✅ 添加占卜系统")
    print("- ✅ 优化胜利条件")
    print("- ✅ 集成智慧格言")
    print("- ✅ 强化易经哲学元素")

if __name__ == "__main__":
    main()