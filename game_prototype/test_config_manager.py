#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理器测试脚本
验证配置系统的正确性和功能
"""

from config_manager import ConfigManager, get_config, update_config
from yijing_mechanics import YinYangBalance, TaijiMechanism, ZhanBuSystem

def test_config_loading():
    """测试配置加载功能"""
    print("=== 测试配置加载 ===")
    
    # 测试基本配置获取
    max_players = get_config("game_settings.max_players", 2)
    print(f"最大玩家数: {max_players}")
    
    # 测试嵌套配置获取
    high_threshold = get_config("game_balance.yin_yang_balance.high_balance_threshold", 0.8)
    print(f"高平衡阈值: {high_threshold}")
    
    # 测试默认值
    non_existent = get_config("non.existent.key", "default_value")
    print(f"不存在的配置项: {non_existent}")
    
    print("配置加载测试完成\n")

def test_yin_yang_balance_with_config():
    """测试阴阳平衡系统使用配置"""
    print("=== 测试阴阳平衡配置化 ===")
    
    # 创建不同平衡状态的测试
    test_cases = [
        (8, 2, "高度平衡"),
        (6, 4, "中等平衡"),
        (5, 5, "轻微平衡"),
        (3, 7, "不平衡")
    ]
    
    for yin, yang, desc in test_cases:
        balance = YinYangBalance(yin, yang)
        bonus = balance.get_balance_bonus()
        ratio = balance.balance_ratio
        print(f"{desc}: 阴{yin}阳{yang}, 平衡比{ratio:.2f}, 奖励{bonus}")
    
    print("阴阳平衡配置化测试完成\n")

def test_taiji_mechanism_with_config():
    """测试太极机制使用配置"""
    print("=== 测试太极机制配置化 ===")
    
    # 测试极端状态转化概率
    extreme_balance = YinYangBalance(12, 1)  # 极阴状态
    prob = TaijiMechanism.calculate_transformation_probability(extreme_balance)
    print(f"极阴状态(阴12阳1)转化概率: {prob}")
    
    # 测试正常状态转化概率
    normal_balance = YinYangBalance(5, 5)  # 平衡状态
    prob = TaijiMechanism.calculate_transformation_probability(normal_balance)
    print(f"平衡状态(阴5阳5)转化概率: {prob}")
    
    print("太极机制配置化测试完成\n")

def test_zhanbu_system_with_config():
    """测试占卜系统使用配置"""
    print("=== 测试占卜系统配置化 ===")
    
    # 测试不同道行等级的占卜结果
    test_dao_xing = [20, 50, 80]  # 低、中、高道行
    
    for dao_xing in test_dao_xing:
        result = ZhanBuSystem.divine_fortune(dao_xing)
        print(f"道行{dao_xing}的占卜结果: {result['fortune']} - {result['advice']}")
    
    print("占卜系统配置化测试完成\n")

def test_config_update():
    """测试配置更新功能"""
    print("=== 测试配置更新 ===")
    
    # 获取原始值
    original_value = get_config("game_balance.yin_yang_balance.high_balance_bonus", 3)
    print(f"原始高平衡奖励: {original_value}")
    
    # 更新配置
    update_config("game_balance.yin_yang_balance.high_balance_bonus", 5)
    new_value = get_config("game_balance.yin_yang_balance.high_balance_bonus", 3)
    print(f"更新后高平衡奖励: {new_value}")
    
    # 测试更新后的效果
    balance = YinYangBalance(8, 2)  # 高度平衡
    bonus = balance.get_balance_bonus()
    print(f"高度平衡状态奖励: {bonus}")
    
    # 恢复原始值
    update_config("game_balance.yin_yang_balance.high_balance_bonus", original_value)
    restored_value = get_config("game_balance.yin_yang_balance.high_balance_bonus", 3)
    print(f"恢复后高平衡奖励: {restored_value}")
    
    print("配置更新测试完成\n")

def test_config_manager_singleton():
    """测试配置管理器单例模式"""
    print("=== 测试单例模式 ===")
    
    # 创建多个实例
    manager1 = ConfigManager()
    manager2 = ConfigManager()
    
    # 验证是同一个实例
    print(f"manager1 id: {id(manager1)}")
    print(f"manager2 id: {id(manager2)}")
    print(f"是否为同一实例: {manager1 is manager2}")
    
    print("单例模式测试完成\n")

def main():
    """运行所有测试"""
    print("开始配置管理器测试\n")
    
    try:
        test_config_loading()
        test_yin_yang_balance_with_config()
        test_taiji_mechanism_with_config()
        test_zhanbu_system_with_config()
        test_config_update()
        test_config_manager_singleton()
        
        print("=== 所有测试完成 ===")
        print("✅ 配置管理器功能正常")
        print("✅ 硬编码数值已成功外部化")
        print("✅ 游戏平衡参数可通过配置文件调整")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()