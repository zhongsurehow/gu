#!/usr/bin/env python3
"""
基本游戏功能测试脚本
测试游戏的核心功能是否正常工作
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试所有必要的模块是否能正常导入"""
    print("🔍 测试模块导入...")
    
    try:
        from game_state import GameState, Player
        from game_data import EMPEROR_AVATAR, HERMIT_AVATAR
        from main import setup_game
        print("[完成] 核心模块导入成功")
        return True
    except ImportError as e:
        print(f"[错误] 模块导入失败: {e}")
        return False

def test_game_setup():
    """测试游戏初始化"""
    print("\n[游戏] 测试游戏初始化...")
    
    try:
        from main import setup_game
        game_state = setup_game(num_players=2)
        
        # 检查游戏状态
        assert len(game_state.players) == 2, "玩家数量不正确"
        assert all(len(player.hand) > 0 for player in game_state.players), "玩家手牌为空"
        assert all(player.qi > 0 for player in game_state.players), "玩家气值为0"
        
        print("[完成] 游戏初始化成功")
        print(f"   - 玩家数量: {len(game_state.players)}")
        print(f"   - 玩家1手牌数: {len(game_state.players[0].hand)}")
        print(f"   - 玩家1气值: {game_state.players[0].qi}")
        return True
    except Exception as e:
        print(f"[错误] 游戏初始化失败: {e}")
        return False

def test_player_creation():
    """测试玩家创建"""
    print("\n[玩家] 测试玩家创建...")
    
    try:
        from game_state import Player
        from game_data import EMPEROR_AVATAR
        
        player = Player(name="测试玩家", avatar=EMPEROR_AVATAR)
        
        assert player.name == "测试玩家", "玩家名称不正确"
        assert player.avatar == EMPEROR_AVATAR, "玩家头像不正确"
        assert hasattr(player, 'qi'), "玩家缺少气属性"
        assert hasattr(player, 'dao_xing'), "玩家缺少道行属性"
        
        print("[完成] 玩家创建成功")
        print(f"   - 玩家名称: {player.name}")
        print(f"   - 玩家头像: {player.avatar.name.value}")
        return True
    except Exception as e:
        print(f"[错误] 玩家创建失败: {e}")
        return False

def test_card_system():
    """测试卡牌系统"""
    print("\n[卡牌] 测试卡牌系统...")
    
    try:
        from game_data import GAME_DECK
        
        assert len(GAME_DECK) > 0, "游戏卡组为空"
        
        # 检查第一张卡牌的属性
        first_card = GAME_DECK[0]
        assert hasattr(first_card, 'name'), "卡牌缺少名称属性"
        assert hasattr(first_card, 'associated_guas'), "卡牌缺少关联卦属性"
        assert hasattr(first_card, 'tasks'), "卡牌缺少任务属性"
        
        print("[完成] 卡牌系统正常")
        print(f"   - 卡组大小: {len(GAME_DECK)}")
        print(f"   - 第一张卡牌: {first_card.name}")
        return True
    except Exception as e:
        print(f"[错误] 卡牌系统测试失败: {e}")
        return False

def main():
    """运行所有测试"""
    print("[启动] 开始天机变游戏基本功能测试")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_player_creation,
        test_card_system,
        test_game_setup,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"[统计] 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("[成功] 所有测试通过！游戏基本功能正常")
        return True
    else:
        print("[警告]  部分测试失败，请检查相关功能")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)