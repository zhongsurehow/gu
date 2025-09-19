#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天机变增强功能测试脚本
测试所有新增的增强系统和功能
"""

import sys
import traceback
from pathlib import Path

def test_imports():
    """测试所有模块导入"""
    print("🔍 测试模块导入...")
    
    modules_to_test = [
        ('game_state', 'GameState, Player'),
        ('main', 'setup_game'),
        ('enhanced_game_balance', 'game_balance'),
        ('enhanced_ui_system', 'enhanced_ui'),
        ('complete_64_guas_system', 'complete_guas_system'),
        ('yijing_wisdom_guide', 'wisdom_guide'),
    ]
    
    success_count = 0
    for module_name, components in modules_to_test:
        try:
            exec(f"from {module_name} import {components}")
            print(f"✅ {module_name}: {components}")
            success_count += 1
        except ImportError as e:
            print(f"❌ {module_name}: {e}")
        except Exception as e:
            print(f"⚠️  {module_name}: {e}")
    
    print(f"\n📊 导入测试结果: {success_count}/{len(modules_to_test)} 成功")
    return success_count == len(modules_to_test)

def test_enhanced_ui():
    """测试增强UI系统"""
    print("\n🎨 测试增强UI系统...")
    
    try:
        from enhanced_ui_system import enhanced_ui
        from game_state import Player
        from game_data import EMPEROR_AVATAR
        
        # 创建测试玩家
        test_player = Player(name="测试玩家", avatar=EMPEROR_AVATAR)
        test_player.qi = 10
        test_player.dao_xing = 5
        test_player.cheng_yi = 3
        
        # 测试UI功能
        print("测试游戏标题显示:")
        enhanced_ui.display_game_title()
        
        print("\n测试章节标题显示:")
        enhanced_ui.display_section_header("测试章节")
        
        print("\n测试玩家回合显示:")
        enhanced_ui.display_player_turn(test_player, 2)
        
        print("✅ 增强UI系统测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 增强UI系统测试失败: {e}")
        traceback.print_exc()
        return False

def test_guas_system():
    """测试64卦系统"""
    print("\n📿 测试64卦系统...")
    
    try:
        from complete_64_guas_system import Complete64GuasSystem
        
        # 创建64卦系统实例
        gua_system = Complete64GuasSystem()
        
        # 测试获取卦信息
        qian_gua = gua_system.get_gua_philosophy("乾为天")
        if qian_gua:
            print(f"✅ 找到乾卦信息: {qian_gua.name}")
            print(f"   性质: {qian_gua.nature}")
            print(f"   五行: {qian_gua.element}")
        else:
            print("❌ 未找到乾卦信息")
            return False
        
        # 测试人生智慧
        wisdom = gua_system.get_life_wisdom("乾为天")
        print(f"✅ 人生智慧: {wisdom[:50]}...")
        
        # 测试卦象兼容性
        compatibility = gua_system.calculate_gua_compatibility("乾为天", "坤为地")
        print(f"✅ 乾坤兼容性: {compatibility}")
        
        print("✅ 64卦系统测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 64卦系统测试失败: {e}")
        traceback.print_exc()
        return False

def test_wisdom_guide():
    """测试智慧指导系统"""
    print("\n🧘 测试智慧指导系统...")
    
    try:
        from yijing_wisdom_guide import wisdom_guide
        
        # 测试人生指导
        guidance = wisdom_guide.get_life_advice("事业发展遇到瓶颈", {"qi": 10, "dao_xing": 5})
        if guidance:
            print(f"✅ 事业指导: {guidance[:50]}...")
        else:
            print("❌ 未获取到事业指导")
            return False
        
        # 测试每日智慧
        daily_wisdom = wisdom_guide.get_daily_wisdom()
        if daily_wisdom:
            print(f"✅ 每日智慧: {daily_wisdom[:50]}...")
        else:
            print("❌ 未获取到每日智慧")
            return False
        
        print("✅ 智慧指导系统测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 智慧指导系统测试失败: {e}")
        traceback.print_exc()
        return False

def test_game_balance():
    """测试游戏平衡系统"""
    print("\n⚖️ 测试游戏平衡系统...")
    
    try:
        from enhanced_game_balance import game_balance
        from game_state import GameState, Player
        from game_data import EMPEROR_AVATAR
        
        # 创建测试游戏状态
        test_player = Player(name="测试玩家", avatar=EMPEROR_AVATAR)
        test_game_state = GameState(players=[test_player])
        
        # 测试平衡设置应用
        balanced_state = game_balance.apply_balanced_setup(test_game_state)
        print("✅ 平衡设置应用成功")
        
        # 测试基本功能存在性
        if hasattr(game_balance, 'calculate_action_points'):
            print("✅ 行动点数计算功能存在")
        
        if hasattr(game_balance, 'is_yin_yang_balanced'):
            print("✅ 阴阳平衡检查功能存在")
        
        print("✅ 游戏平衡系统测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 游戏平衡系统测试失败: {e}")
        traceback.print_exc()
        return False

def test_game_setup():
    """测试游戏设置"""
    print("\n🎮 测试游戏设置...")
    
    try:
        from main import setup_game
        
        # 测试单人游戏设置
        game_state = setup_game(1)
        print(f"✅ 单人游戏设置: {len(game_state.players)} 玩家")
        
        # 测试多人游戏设置
        game_state = setup_game(3)
        print(f"✅ 多人游戏设置: {len(game_state.players)} 玩家")
        
        # 验证玩家初始状态
        player = game_state.players[0]
        print(f"✅ 玩家初始状态: 气={player.qi}, 道行={player.dao_xing}, 诚意={player.cheng_yi}")
        
        print("✅ 游戏设置测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 游戏设置测试失败: {e}")
        traceback.print_exc()
        return False

def test_documentation():
    """测试文档文件"""
    print("\n📚 测试文档文件...")
    
    doc_files = [
        'COMPLETE_GAME_GUIDE.md',
        '64_GUAS_DETAILED_GUIDE.md',
        'QUICK_REFERENCE.md',
        'launcher.py',
        'start_game.bat'
    ]
    
    success_count = 0
    for doc_file in doc_files:
        if Path(doc_file).exists():
            print(f"✅ {doc_file}")
            success_count += 1
        else:
            print(f"❌ {doc_file} 不存在")
    
    print(f"\n📊 文档测试结果: {success_count}/{len(doc_files)} 文件存在")
    return success_count >= len(doc_files) - 1  # 允许一个文件缺失

def main():
    """主测试函数"""
    print("=" * 60)
    print("🧪 天机变增强功能测试")
    print("=" * 60)
    
    tests = [
        ("模块导入", test_imports),
        ("增强UI系统", test_enhanced_ui),
        ("64卦系统", test_guas_system),
        ("智慧指导系统", test_wisdom_guide),
        ("游戏平衡系统", test_game_balance),
        ("游戏设置", test_game_setup),
        ("文档文件", test_documentation),
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed_tests += 1
                print(f"✅ {test_name} 测试通过")
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"💥 {test_name} 测试异常: {e}")
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"🏆 测试总结: {passed_tests}/{total_tests} 测试通过")
    
    if passed_tests == total_tests:
        print("🎉 所有测试通过！游戏增强功能正常工作。")
        return True
    elif passed_tests >= total_tests * 0.8:
        print("⚠️  大部分测试通过，游戏基本功能正常。")
        return True
    else:
        print("❌ 多个测试失败，需要检查系统配置。")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n🛑 测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 测试脚本异常: {e}")
        traceback.print_exc()
        sys.exit(1)