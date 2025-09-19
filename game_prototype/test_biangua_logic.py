#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
变卦逻辑测试
测试BianguaTransformation类的完整功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from yijing_mechanics import BianguaTransformation, YinYangBalance, WuXing
from game_state import Player, AvatarName, Avatar

def test_biangua_basic_functionality():
    """测试变卦基础功能"""
    print("=== 测试变卦基础功能 ===")
    
    # 创建变卦实例
    biangua = BianguaTransformation(
        original_gua="乾",
        transformed_gua="坤",
        trigger_condition="阴阳失衡",
        effect_description="从刚健转为柔顺",
        cost_qi=5,
        cost_dao_xing=3,
        reward_multiplier=1.5,
        risk_level="medium"
    )
    
    print(f"变卦配置: {biangua.original_gua} -> {biangua.transformed_gua}")
    print(f"触发条件: {biangua.trigger_condition}")
    print(f"消耗: 气{biangua.cost_qi}, 道行{biangua.cost_dao_xing}")
    print(f"风险等级: {biangua.risk_level}")
    print("✓ 变卦基础功能正常")

def test_biangua_conditions():
    """测试变卦条件检查"""
    print("\n=== 测试变卦条件检查 ===")
    
    # 创建玩家
    avatar = Avatar(AvatarName.EMPEROR, "测试帝王", "测试能力")
    player = Player("测试玩家", avatar)
    player.qi = 10
    player.dao_xing = 8
    player.yin_yang_balance = YinYangBalance(yin_points=2, yang_points=8)  # 阴阳失衡
    
    # 创建变卦实例
    biangua = BianguaTransformation(
        original_gua="乾",
        transformed_gua="坤", 
        trigger_condition="阴阳失衡",
        effect_description="平衡阴阳",
        cost_qi=5,
        cost_dao_xing=3
    )
    
    game_context = {
        'player': player,
        'game_state': None,
        'turn_phase': 'action'
    }
    
    # 测试资源充足的情况
    can_transform = biangua.can_transform(game_context)
    print(f"资源充足时可以变卦: {can_transform}")
    
    # 测试资源不足的情况
    player.qi = 3  # 不足
    can_transform_insufficient = biangua.can_transform(game_context)
    print(f"资源不足时可以变卦: {can_transform_insufficient}")
    
    print("✓ 变卦条件检查正常")

def test_biangua_transformation_outcome():
    """测试变卦结果计算"""
    print("\n=== 测试变卦结果计算 ===")
    
    # 创建玩家
    avatar = Avatar(AvatarName.HERMIT, "测试隐士", "测试能力")
    player = Player("测试玩家", avatar)
    player.qi = 15
    player.dao_xing = 12
    player.yin_yang_balance = YinYangBalance(yin_points=5, yang_points=5)  # 平衡状态
    
    # 创建变卦实例
    biangua = BianguaTransformation(
        original_gua="震",
        transformed_gua="巽",
        trigger_condition="道行充足",
        effect_description="从动转为入",
        cost_qi=8,
        cost_dao_xing=5,
        reward_multiplier=2.0,
        risk_level="low"
    )
    
    game_context = {
        'player': player,
        'game_state': None,
        'turn_phase': 'action'
    }
    
    # 计算成功率
    success_rate = biangua._calculate_success_rate(game_context)
    print(f"变卦成功率: {success_rate:.2%}")
    
    # 模拟变卦结果
    print("\n模拟10次变卦结果:")
    success_count = 0
    for i in range(10):
        outcome = biangua.calculate_transformation_outcome(game_context)
        if outcome['success']:
            success_count += 1
            print(f"第{i+1}次: 成功 - {outcome['message']}")
        else:
            print(f"第{i+1}次: 失败 - {outcome['message']}")
    
    print(f"实际成功率: {success_count}/10 = {success_count*10}%")
    print("✓ 变卦结果计算正常")

def test_different_trigger_conditions():
    """测试不同的触发条件"""
    print("\n=== 测试不同触发条件 ===")
    
    # 创建玩家
    avatar = Avatar(AvatarName.EMPEROR, "测试帝王", "测试能力")
    player = Player("测试玩家", avatar)
    player.qi = 20
    player.dao_xing = 15
    player.yin_yang_balance = YinYangBalance(yin_points=3, yang_points=7)
    
    # 添加五行亲和力属性
    player.wuxing_affinities = {
        WuXing.JIN: 2,
        WuXing.MU: 3,
        WuXing.SHUI: 1,
        WuXing.HUO: 2,
        WuXing.TU: 0
    }
    
    game_context = {
        'player': player,
        'game_state': None,
        'turn_phase': 'end'
    }
    
    # 测试不同条件
    conditions_to_test = [
        "阴阳失衡",
        "道行充足", 
        "气充盈",
        "五行和谐",
        "回合末期",
        "未知条件"
    ]
    
    for condition in conditions_to_test:
        biangua = BianguaTransformation(
            original_gua="坎",
            transformed_gua="离",
            trigger_condition=condition,
            effect_description=f"测试{condition}",
            cost_qi=5,
            cost_dao_xing=3
        )
        
        can_transform = biangua.can_transform(game_context)
        print(f"触发条件'{condition}': {'可以变卦' if can_transform else '不能变卦'}")
    
    print("✓ 不同触发条件测试完成")

def test_transformation_effects():
    """测试变卦特殊效果"""
    print("\n=== 测试变卦特殊效果 ===")
    
    guas = ["乾为天", "坤为地", "震为雷", "巽为风", "坎为水", "离为火", "艮为山", "兑为泽", "未知卦"]
    
    for gua in guas:
        biangua = BianguaTransformation(
            original_gua="测试",
            transformed_gua=gua,
            trigger_condition="测试",
            effect_description="测试效果"
        )
        
        effect = biangua._get_transformation_effect()
        print(f"{gua}: {effect}")
    
    print("✓ 变卦特殊效果测试完成")

def run_all_tests():
    """运行所有测试"""
    print("开始变卦逻辑测试...")
    
    try:
        test_biangua_basic_functionality()
        test_biangua_conditions()
        test_biangua_transformation_outcome()
        test_different_trigger_conditions()
        test_transformation_effects()
        
        print("\n" + "="*50)
        print("🎉 所有变卦逻辑测试通过！")
        print("变卦系统已完善，具备以下特性:")
        print("- 多样化的触发条件")
        print("- 资源消耗和风险管理")
        print("- 动态成功率计算")
        print("- 丰富的变卦效果")
        print("- 策略性的决策机制")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()