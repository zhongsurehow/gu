#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真实爻辞系统测试脚本
验证基于真实易经爻辞的任务生成和特殊效果系统
"""

from authentic_yao_ci_generator import (
    AuthenticYaoCiGenerator, 
    GameContext, 
    YaoCiEffectProcessor,
    generate_authentic_yao_ci_tasks
)
from authentic_yao_ci import AUTHENTIC_YAO_CI_DATA
from generate_64_guas import generate_all_64_guas

def test_authentic_yao_ci_data():
    """测试真实爻辞数据的完整性"""
    print("=== 测试真实爻辞数据 ===")
    
    for gua_name, yao_ci_list in AUTHENTIC_YAO_CI_DATA.items():
        print(f"\n【{gua_name}】包含 {len(yao_ci_list)} 个爻辞:")
        for yao_ci in yao_ci_list:
            print(f"  {yao_ci.position}: {yao_ci.original_text}")
            print(f"    解读: {yao_ci.interpretation[:30]}...")
            print(f"    奖励: 道行{yao_ci.reward_dao_xing}, 诚意{yao_ci.reward_cheng_yi}")
    
    print(f"\n总计实现了 {len(AUTHENTIC_YAO_CI_DATA)} 个卦的真实爻辞")

def test_contextual_task_generation():
    """测试基于上下文的任务生成"""
    print("\n=== 测试上下文任务生成 ===")
    
    generator = AuthenticYaoCiGenerator()
    
    # 测试不同的游戏上下文
    contexts = [
        GameContext(
            player_dao_xing=10,
            player_cheng_yi=5,
            player_yin=3,
            player_yang=7,
            other_players_dao_xing=[15, 8],
            turn_number=3,
            recent_actions=["占卜", "修炼", "交流"],
            negative_states=[]
        ),
        GameContext(
            player_dao_xing=80,
            player_cheng_yi=20,
            player_yin=5,
            player_yang=5,
            other_players_dao_xing=[60, 70],
            turn_number=10,
            recent_actions=["保守", "保守", "等待"],
            negative_states=["困顿"]
        ),
        GameContext(
            player_dao_xing=30,
            player_cheng_yi=10,
            player_yin=1,
            player_yang=9,
            other_players_dao_xing=[25, 35],
            turn_number=5,
            recent_actions=["激进", "冒险"],
            negative_states=["失衡", "焦虑"]
        )
    ]
    
    for i, context in enumerate(contexts, 1):
        print(f"\n--- 上下文 {i} ---")
        print(f"玩家状态: 道行{context.player_dao_xing}, 诚意{context.player_cheng_yi}")
        print(f"阴阳: {context.player_yin}/{context.player_yang}")
        print(f"其他玩家道行: {context.other_players_dao_xing}")
        print(f"负面状态: {context.negative_states}")
        
        generator.set_game_context(context)
        
        # 测试几个主要卦的任务生成
        for gua_name in ["乾为天", "坤为地", "震为雷"]:
            tasks = generator.generate_contextual_yao_ci_tasks(gua_name)
            print(f"\n{gua_name} 生成了 {len(tasks)} 个任务:")
            for task in tasks[:2]:  # 只显示前两个任务
                print(f"  {task.name}")
                print(f"    {task.description.split('【')[1].split('】')[1][:50]}...")

def test_special_effects():
    """测试爻辞特殊效果处理"""
    print("\n=== 测试特殊效果处理 ===")
    
    processor = YaoCiEffectProcessor()
    player_state = {
        'dao_xing': 30,
        'cheng_yi': 10,
        'yin': 5,
        'yang': 5
    }
    
    # 测试不同的特殊效果
    effects_to_test = [
        "获得2点阴气和2点阳气，下回合行动效果+1",
        "免疫所有负面效果和攻击，但不能主动行动",
        "行动精准度+100%",
        "效果翻倍",
        "获得'智者'称号，之后的占卜结果准确率+50%"
    ]
    
    print("应用特殊效果:")
    for effect in effects_to_test:
        print(f"\n应用效果: {effect}")
        old_state = player_state.copy()
        new_state = processor.apply_special_effect(effect, player_state)
        
        # 显示状态变化
        for key in new_state:
            if new_state[key] != old_state.get(key, 0):
                print(f"  {key}: {old_state.get(key, 0)} -> {new_state[key]}")
        
        # 显示激活的效果
        active_effects = processor.process_turn_start()
        if active_effects:
            print(f"  激活效果: {active_effects}")

def test_integration_with_64_guas():
    """测试与64卦系统的集成"""
    print("\n=== 测试与64卦系统集成 ===")
    
    all_guas = generate_all_64_guas()
    
    # 统计使用真实爻辞的卦
    authentic_count = 0
    fallback_count = 0
    
    print("检查各卦的爻辞任务类型:")
    for gua_name, gua_card in all_guas.items():
        tasks = gua_card.tasks
        
        # 检查是否使用了真实爻辞（通过任务名称判断）
        if any("初九" in task.name or "六二" in task.name or "九三" in task.name for task in tasks):
            authentic_count += 1
            status = "✓ 真实爻辞"
        else:
            fallback_count += 1
            status = "○ 模板任务"
        
        print(f"  {gua_name}: {status} ({len(tasks)}个任务)")
    
    print(f"\n统计结果:")
    print(f"  使用真实爻辞: {authentic_count} 个卦")
    print(f"  使用模板任务: {fallback_count} 个卦")
    print(f"  覆盖率: {authentic_count/64*100:.1f}%")

def test_yao_ci_content_quality():
    """测试爻辞内容质量"""
    print("\n=== 测试爻辞内容质量 ===")
    
    # 展示几个典型的真实爻辞任务
    sample_guas = ["乾为天", "坤为地", "震为雷"]
    
    for gua_name in sample_guas:
        print(f"\n【{gua_name}】爻辞示例:")
        tasks = generate_authentic_yao_ci_tasks(gua_name)
        
        if tasks:
            # 显示第一个任务的完整内容
            task = tasks[0]
            print(f"任务名称: {task.name}")
            print(f"任务描述:")
            for line in task.description.split('\n'):
                if line.strip():
                    print(f"  {line.strip()}")
            print(f"奖励: 道行+{task.reward_dao_xing}, 诚意+{task.reward_cheng_yi}")
            
            # 特殊效果已包含在任务描述中

def main():
    """运行所有测试"""
    print("真实爻辞系统测试开始")
    print("=" * 50)
    
    try:
        test_authentic_yao_ci_data()
        test_contextual_task_generation()
        test_special_effects()
        test_integration_with_64_guas()
        test_yao_ci_content_quality()
        
        print("\n" + "=" * 50)
        print("✓ 所有测试完成，真实爻辞系统运行正常")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()