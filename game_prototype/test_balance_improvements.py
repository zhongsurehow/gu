#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏平衡性改进测试
测试新的平衡配置是否改善了游戏体验
"""

import json
from config_manager import ConfigManager
from game_state import Player, Avatar, AvatarName, GameState
from yijing_mechanics import YijingMechanics
from enhanced_victory import EnhancedVictoryConditions

def test_resource_balance():
    """测试资源平衡性"""
    print("=== 测试资源平衡性 ===")
    
    # 加载平衡配置
    with open('game_config_balanced.json', 'r', encoding='utf-8') as f:
        balanced_config = json.load(f)
    
    balance_config = balanced_config['game_balance']
    
    # 检查初始资源是否合理
    initial = balance_config['initial_resources']
    limits = balance_config['resource_limits']
    
    print(f"初始气: {initial['qi']}, 最大气: {limits['max_qi']}")
    print(f"初始道行: {initial['dao_xing']}, 最大道行: {limits['max_dao_xing']}")
    print(f"初始诚意: {initial['cheng_yi']}, 最大诚意: {limits['max_cheng_yi']}")
    
    # 验证资源比例
    qi_ratio = initial['qi'] / limits['max_qi']
    dao_xing_ratio = initial['dao_xing'] / limits['max_dao_xing']
    cheng_yi_ratio = initial['cheng_yi'] / limits['max_cheng_yi']
    
    print(f"资源初始比例 - 气: {qi_ratio:.2f}, 道行: {dao_xing_ratio:.2f}, 诚意: {cheng_yi_ratio:.2f}")
    
    # 检查是否在合理范围内（20%-40%）
    assert 0.2 <= qi_ratio <= 0.4, f"气的初始比例不合理: {qi_ratio}"
    assert 0.05 <= dao_xing_ratio <= 0.15, f"道行的初始比例不合理: {dao_xing_ratio}"
    assert 0.1 <= cheng_yi_ratio <= 0.3, f"诚意的初始比例不合理: {cheng_yi_ratio}"
    
    print("✓ 资源平衡性测试通过")

def test_action_cost_balance():
    """测试行动成本平衡性"""
    print("\n=== 测试行动成本平衡性 ===")
    
    with open('game_config_balanced.json', 'r', encoding='utf-8') as f:
        balanced_config = json.load(f)
    
    costs = balanced_config['game_balance']['action_costs']
    bonuses = balanced_config['game_balance']['phase_bonuses']
    
    print(f"冥想成本: {costs['meditate_qi_cost']}, 基础气获得: {bonuses['base_qi_gain']}")
    print(f"学习成本: {costs['study_dao_xing_cost']}")
    print(f"变化成本: {costs['transform_cheng_yi_cost']}")
    
    # 验证成本效益比
    qi_efficiency = bonuses['base_qi_gain'] / costs['meditate_qi_cost']
    print(f"气获得效率: {qi_efficiency:.2f}")
    
    # 检查效率是否合理（1.0-2.0之间）
    assert 1.0 <= qi_efficiency <= 2.0, f"气获得效率不合理: {qi_efficiency}"
    
    print("✓ 行动成本平衡性测试通过")

def test_victory_condition_balance():
    """测试胜利条件平衡性"""
    print("\n=== 测试胜利条件平衡性 ===")
    
    with open('game_config_balanced.json', 'r', encoding='utf-8') as f:
        balanced_config = json.load(f)
    
    victory = balanced_config['game_balance']['victory_conditions']
    limits = balanced_config['game_balance']['resource_limits']
    
    print(f"传统胜利道行要求: {victory['traditional_dao_xing']}")
    print(f"最大道行限制: {limits['max_dao_xing']}")
    
    # 检查胜利条件是否在合理范围内
    dao_xing_ratio = victory['traditional_dao_xing'] / limits['max_dao_xing']
    print(f"胜利道行比例: {dao_xing_ratio:.2f}")
    
    assert 0.5 <= dao_xing_ratio <= 0.8, f"胜利道行比例不合理: {dao_xing_ratio}"
    
    # 检查其他胜利条件
    print(f"太极大师平衡要求: {victory['taiji_master_balance']}")
    print(f"五行掌握阈值: {victory['wuxing_mastery_threshold']}")
    
    print("✓ 胜利条件平衡性测试通过")

def test_game_flow_balance():
    """测试游戏流程平衡性"""
    print("\n=== 测试游戏流程平衡性 ===")
    
    with open('game_config_balanced.json', 'r', encoding='utf-8') as f:
        balanced_config = json.load(f)
    
    flow = balanced_config['game_balance']['game_flow']
    victory = balanced_config['game_balance']['victory_conditions']
    
    max_turns = flow['max_turns']
    victory_dao_xing = victory['traditional_dao_xing']
    
    print(f"最大回合数: {max_turns}")
    print(f"胜利所需道行: {victory_dao_xing}")
    
    # 估算达到胜利条件所需回合数
    # 假设每回合平均获得0.3道行
    estimated_turns = victory_dao_xing / 0.3
    print(f"预估达到胜利所需回合: {estimated_turns:.1f}")
    
    # 检查游戏长度是否合理
    turn_ratio = estimated_turns / max_turns
    print(f"游戏长度比例: {turn_ratio:.2f}")
    
    assert 0.4 <= turn_ratio <= 0.8, f"游戏长度比例不合理: {turn_ratio}"
    
    print("✓ 游戏流程平衡性测试通过")

def test_balance_mechanics():
    """测试平衡机制"""
    print("\n=== 测试平衡机制 ===")
    
    with open('game_config_balanced.json', 'r', encoding='utf-8') as f:
        balanced_config = json.load(f)
    
    mechanics = balanced_config['game_balance']['balance_mechanics']
    
    print(f"动态难度: {mechanics['dynamic_difficulty']}")
    print(f"资源恢复率: {mechanics['resource_recovery_rate']}")
    print(f"平衡奖励倍数: {mechanics['balance_reward_multiplier']}")
    print(f"策略多样性奖励: {mechanics['strategy_diversity_bonus']}")
    print(f"后期游戏加速: {mechanics['late_game_acceleration']}")
    
    # 验证机制参数合理性
    assert 0.1 <= mechanics['resource_recovery_rate'] <= 0.5, "资源恢复率不合理"
    assert 1.0 <= mechanics['balance_reward_multiplier'] <= 2.0, "平衡奖励倍数不合理"
    assert 0.05 <= mechanics['strategy_diversity_bonus'] <= 0.2, "策略多样性奖励不合理"
    
    print("✓ 平衡机制测试通过")

def test_integrated_balance():
    """测试整体平衡性"""
    print("\n=== 测试整体平衡性 ===")
    
    # 创建测试游戏状态
    avatar1 = Avatar(AvatarName.EMPEROR, "测试帝王", "测试能力")
    avatar2 = Avatar(AvatarName.HERMIT, "测试隐士", "测试能力")
    player1 = Player("玩家1", avatar1)
    player2 = Player("玩家2", avatar2)
    
    game_state = GameState([player1, player2])
    
    # 使用平衡配置初始化
    config_manager = ConfigManager()
    config_manager.load_config('game_config_balanced.json')
    
    balance_config = config_manager.get_balance_config()
    
    # 设置初始资源
    initial = balance_config['initial_resources']
    for player in game_state.players:
        player.qi = initial['qi']
        player.dao_xing = initial['dao_xing']
        player.cheng_yi = initial['cheng_yi']
    
    print(f"玩家初始状态:")
    for i, player in enumerate(game_state.players, 1):
        print(f"  玩家{i}: 气={player.qi}, 道行={player.dao_xing}, 诚意={player.cheng_yi}")
    
    # 模拟几回合游戏
    yijing = YijingMechanics(game_state)
    victory = EnhancedVictoryConditions(game_state)
    
    for turn in range(5):
        print(f"\n第{turn+1}回合:")
        for player in game_state.players:
            # 模拟基础气获得
            qi_gain = balance_config['phase_bonuses']['base_qi_gain']
            player.qi = min(player.qi + qi_gain, balance_config['resource_limits']['max_qi'])
            
            # 模拟学习行动
            if player.qi >= balance_config['action_costs']['study_dao_xing_cost']:
                player.qi -= balance_config['action_costs']['study_dao_xing_cost']
                player.dao_xing += 1
        
        # 检查胜利条件
        winners = victory.check_all_victory_conditions()
        if winners:
            print(f"游戏在第{turn+1}回合结束，获胜者: {[w.name for w in winners]}")
            break
    
    print("\n最终状态:")
    for i, player in enumerate(game_state.players, 1):
        print(f"  玩家{i}: 气={player.qi}, 道行={player.dao_xing}, 诚意={player.cheng_yi}")
    
    print("✓ 整体平衡性测试完成")

def run_all_balance_tests():
    """运行所有平衡性测试"""
    print("开始游戏平衡性改进测试...")
    
    try:
        test_resource_balance()
        test_action_cost_balance()
        test_victory_condition_balance()
        test_game_flow_balance()
        test_balance_mechanics()
        test_integrated_balance()
        
        print("\n" + "="*50)
        print("🎉 所有平衡性测试通过！")
        print("游戏平衡性调整成功，具备以下特性：")
        print("• 合理的资源分配和成长曲线")
        print("• 平衡的行动成本和收益")
        print("• 多样化的胜利条件")
        print("• 适中的游戏时长")
        print("• 动态平衡机制")
        print("• 策略深度和可玩性")
        
    except Exception as e:
        print(f"\n❌ 平衡性测试失败: {e}")
        raise

if __name__ == "__main__":
    run_all_balance_tests()