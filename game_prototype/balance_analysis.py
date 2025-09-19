#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏平衡性分析和调整工具
分析当前游戏平衡问题并提供调整建议
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
from typing import Dict, List, Any
from config_manager import ConfigManager

def analyze_current_balance():
    """分析当前游戏平衡状况"""
    print("🔍 === 游戏平衡性分析 ===\n")
    
    config_manager = ConfigManager()
    balance_config = config_manager.get_balance_config()
    
    # 分析初始资源
    initial_resources = balance_config.get("initial_resources", {})
    print("📊 初始资源分析:")
    print(f"  气: {initial_resources.get('qi', 0)}")
    print(f"  道行: {initial_resources.get('dao_xing', 0)}")
    print(f"  诚意: {initial_resources.get('cheng_yi', 0)}")
    print(f"  初始手牌: {initial_resources.get('initial_hand_size', 0)}张")
    
    # 分析资源上限
    resource_limits = balance_config.get("resource_limits", {})
    print(f"\n📈 资源上限分析:")
    print(f"  最大气: {resource_limits.get('max_qi', 0)}")
    print(f"  最大道行: {resource_limits.get('max_dao_xing', 0)}")
    print(f"  最大诚意: {resource_limits.get('max_cheng_yi', 0)}")
    print(f"  最大手牌: {resource_limits.get('max_hand_size', 0)}张")
    
    # 分析动作成本
    action_costs = balance_config.get("action_costs", {})
    print(f"\n⚡ 动作成本分析:")
    print(f"  冥想气消耗: {action_costs.get('meditate_qi_cost', 0)}")
    print(f"  学习道行消耗: {action_costs.get('study_dao_xing_cost', 0)}")
    print(f"  变卦诚意消耗: {action_costs.get('transform_cheng_yi_cost', 0)}")
    
    # 分析胜利条件
    victory_conditions = balance_config.get("victory_conditions", {})
    print(f"\n🏆 胜利条件分析:")
    print(f"  传统道行胜利: {victory_conditions.get('traditional_dao_xing', 0)}")
    print(f"  太极大师平衡要求: {victory_conditions.get('taiji_master_balance', 0)}")
    print(f"  资源大师要求: 气{victory_conditions.get('resource_master_qi', 0)}, 诚意{victory_conditions.get('resource_master_cheng_yi', 0)}, 道行{victory_conditions.get('resource_master_dao_xing', 0)}")
    
    return balance_config

def identify_balance_issues(balance_config: Dict[str, Any]) -> List[str]:
    """识别平衡性问题"""
    print("\n⚠️ === 平衡性问题识别 ===\n")
    
    issues = []
    
    # 检查初始资源
    initial_resources = balance_config.get("initial_resources", {})
    qi = initial_resources.get("qi", 0)
    dao_xing = initial_resources.get("dao_xing", 0)
    cheng_yi = initial_resources.get("cheng_yi", 0)
    
    if qi < 5:
        issues.append("初始气值过低，可能导致前期行动受限")
    if dao_xing < 1:
        issues.append("初始道行过低，影响游戏进程")
    if cheng_yi < 2:
        issues.append("初始诚意不足，变卦机制难以启动")
    
    # 检查动作成本
    action_costs = balance_config.get("action_costs", {})
    meditate_cost = action_costs.get("meditate_qi_cost", 0)
    transform_cost = action_costs.get("transform_cheng_yi_cost", 0)
    
    if meditate_cost >= qi // 2:
        issues.append("冥想成本过高，相对于初始气值")
    if transform_cost >= cheng_yi * 2:
        issues.append("变卦成本过高，相对于初始诚意")
    
    # 检查胜利条件
    victory_conditions = balance_config.get("victory_conditions", {})
    traditional_dao_xing = victory_conditions.get("traditional_dao_xing", 0)
    resource_master_qi = victory_conditions.get("resource_master_qi", 0)
    
    resource_limits = balance_config.get("resource_limits", {})
    max_qi = resource_limits.get("max_qi", 0)
    max_dao_xing = resource_limits.get("max_dao_xing", 0)
    
    if traditional_dao_xing >= max_dao_xing * 0.8:
        issues.append("传统胜利条件过于接近道行上限")
    if resource_master_qi >= max_qi * 0.9:
        issues.append("资源大师胜利条件过于接近气上限")
    
    # 检查游戏流程
    game_flow = balance_config.get("game_flow", {})
    max_turns = game_flow.get("max_turns", 0)
    ap_per_turn = game_flow.get("ap_per_turn", 0)
    
    if max_turns < 30:
        issues.append("最大回合数可能过少，限制策略深度")
    if ap_per_turn < 2:
        issues.append("每回合行动点过少，可能导致游戏节奏过慢")
    
    # 输出问题
    for i, issue in enumerate(issues, 1):
        print(f"{i}. {issue}")
    
    if not issues:
        print("✅ 未发现明显的平衡性问题")
    
    return issues

def generate_balance_adjustments(issues: List[str]) -> Dict[str, Any]:
    """生成平衡性调整建议"""
    print(f"\n🔧 === 平衡性调整建议 ===\n")
    
    adjustments = {
        "initial_resources": {},
        "action_costs": {},
        "victory_conditions": {},
        "game_flow": {},
        "new_mechanics": []
    }
    
    # 基于问题生成调整建议
    if any("初始气值过低" in issue for issue in issues):
        adjustments["initial_resources"]["qi"] = 10
        print("📈 建议调整: 初始气值从8提升到10")
    
    if any("初始诚意不足" in issue for issue in issues):
        adjustments["initial_resources"]["cheng_yi"] = 3
        print("📈 建议调整: 初始诚意从2提升到3")
    
    if any("冥想成本过高" in issue for issue in issues):
        adjustments["action_costs"]["meditate_qi_cost"] = 1
        print("📉 建议调整: 冥想气消耗从2降低到1")
    
    if any("变卦成本过高" in issue for issue in issues):
        adjustments["action_costs"]["transform_cheng_yi_cost"] = 2
        print("📉 建议调整: 变卦诚意消耗从3降低到2")
    
    if any("传统胜利条件过于接近" in issue for issue in issues):
        adjustments["victory_conditions"]["traditional_dao_xing"] = 15
        print("📈 建议调整: 传统道行胜利条件从12提升到15")
    
    if any("最大回合数可能过少" in issue for issue in issues):
        adjustments["game_flow"]["max_turns"] = 60
        print("📈 建议调整: 最大回合数从50提升到60")
    
    # 新增平衡机制建议
    adjustments["new_mechanics"] = [
        "动态难度调整: 根据玩家表现调整AI难度",
        "资源回收机制: 失败的行动返还部分资源",
        "平衡奖励系统: 维持平衡状态获得额外奖励",
        "策略多样性激励: 使用不同策略获得奖励",
        "后期加速机制: 游戏后期增加资源获得速度"
    ]
    
    print(f"\n🆕 新增机制建议:")
    for i, mechanic in enumerate(adjustments["new_mechanics"], 1):
        print(f"{i}. {mechanic}")
    
    return adjustments

def create_balanced_config(original_config: Dict[str, Any], adjustments: Dict[str, Any]) -> Dict[str, Any]:
    """创建平衡调整后的配置"""
    print(f"\n⚙️ === 生成平衡调整配置 ===\n")
    
    balanced_config = original_config.copy()
    game_balance = balanced_config.get("game_balance", {})
    
    # 应用初始资源调整
    if adjustments["initial_resources"]:
        initial_resources = game_balance.get("initial_resources", {})
        initial_resources.update(adjustments["initial_resources"])
        game_balance["initial_resources"] = initial_resources
        print("✅ 已应用初始资源调整")
    
    # 应用动作成本调整
    if adjustments["action_costs"]:
        action_costs = game_balance.get("action_costs", {})
        action_costs.update(adjustments["action_costs"])
        game_balance["action_costs"] = action_costs
        print("✅ 已应用动作成本调整")
    
    # 应用胜利条件调整
    if adjustments["victory_conditions"]:
        victory_conditions = game_balance.get("victory_conditions", {})
        victory_conditions.update(adjustments["victory_conditions"])
        game_balance["victory_conditions"] = victory_conditions
        print("✅ 已应用胜利条件调整")
    
    # 应用游戏流程调整
    if adjustments["game_flow"]:
        game_flow = game_balance.get("game_flow", {})
        game_flow.update(adjustments["game_flow"])
        game_balance["game_flow"] = game_flow
        print("✅ 已应用游戏流程调整")
    
    # 添加新的平衡机制配置
    game_balance["balance_mechanics"] = {
        "dynamic_difficulty": True,
        "resource_recovery_rate": 0.3,
        "balance_reward_multiplier": 1.2,
        "strategy_diversity_bonus": 0.1,
        "late_game_acceleration": True,
        "late_game_threshold": 0.7
    }
    print("✅ 已添加新平衡机制配置")
    
    balanced_config["game_balance"] = game_balance
    return balanced_config

def simulate_balance_impact(balanced_config: Dict[str, Any]):
    """模拟平衡调整的影响"""
    print(f"\n🎮 === 平衡调整影响模拟 ===\n")
    
    game_balance = balanced_config.get("game_balance", {})
    
    # 模拟游戏开局
    initial_resources = game_balance.get("initial_resources", {})
    action_costs = game_balance.get("action_costs", {})
    
    qi = initial_resources.get("qi", 8)
    cheng_yi = initial_resources.get("cheng_yi", 2)
    meditate_cost = action_costs.get("meditate_qi_cost", 2)
    transform_cost = action_costs.get("transform_cheng_yi_cost", 3)
    
    print("🎯 开局资源分析:")
    print(f"  可进行冥想次数: {qi // meditate_cost}")
    print(f"  可进行变卦次数: {cheng_yi // transform_cost}")
    print(f"  资源利用率: {((qi // meditate_cost) + (cheng_yi // transform_cost)) / 10 * 100:.1f}%")
    
    # 模拟胜利条件达成难度
    victory_conditions = game_balance.get("victory_conditions", {})
    resource_limits = game_balance.get("resource_limits", {})
    
    traditional_dao_xing = victory_conditions.get("traditional_dao_xing", 12)
    max_dao_xing = resource_limits.get("max_dao_xing", 20)
    
    print(f"\n🏆 胜利条件分析:")
    print(f"  传统胜利难度: {traditional_dao_xing / max_dao_xing * 100:.1f}% 道行上限")
    print(f"  胜利条件合理性: {'合理' if 0.6 <= traditional_dao_xing / max_dao_xing <= 0.8 else '需要调整'}")
    
    # 模拟游戏节奏
    game_flow = game_balance.get("game_flow", {})
    max_turns = game_flow.get("max_turns", 50)
    ap_per_turn = game_flow.get("ap_per_turn", 2)
    
    total_actions = max_turns * ap_per_turn
    print(f"\n⏱️ 游戏节奏分析:")
    print(f"  总行动次数: {total_actions}")
    print(f"  平均每回合决策复杂度: {'高' if ap_per_turn >= 3 else '中' if ap_per_turn >= 2 else '低'}")
    print(f"  游戏长度评估: {'长' if max_turns >= 60 else '中' if max_turns >= 40 else '短'}")

def run_balance_analysis():
    """运行完整的平衡性分析"""
    print("🎯 开始游戏平衡性分析...\n")
    
    try:
        # 1. 分析当前平衡状况
        balance_config = analyze_current_balance()
        
        # 2. 识别平衡性问题
        issues = identify_balance_issues(balance_config)
        
        # 3. 生成调整建议
        adjustments = generate_balance_adjustments(issues)
        
        # 4. 创建平衡调整配置
        config_manager = ConfigManager()
        original_config = config_manager._config
        balanced_config = create_balanced_config(original_config, adjustments)
        
        # 5. 模拟调整影响
        simulate_balance_impact(balanced_config)
        
        # 6. 保存平衡调整配置
        with open("game_config_balanced.json", "w", encoding="utf-8") as f:
            json.dump(balanced_config, f, ensure_ascii=False, indent=2)
        
        print(f"\n" + "="*60)
        print("🎉 平衡性分析完成！")
        print("📁 平衡调整配置已保存到: game_config_balanced.json")
        print("🔧 建议应用这些调整以改善游戏平衡性")
        
        return balanced_config
        
    except Exception as e:
        print(f"\n❌ 平衡性分析失败: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    run_balance_analysis()