#!/usr/bin/env python3
"""
易经哲学游戏机制演示
展示阴阳平衡、五行相生相克、变卦等核心机制
"""

from game_prototype.yijing_mechanics import YinYangBalance, WuXing, WuXingCycle
from game_prototype.game_state import Player, GameState
from game_prototype.game_data import HERMIT_AVATAR, BALANCED_DECK
from game_prototype.yijing_actions import (
    enhanced_play_card, enhanced_meditate, enhanced_study,
    biangua_transformation, check_victory_conditions_enhanced,
    display_yijing_status
)
import random

def demo_yin_yang_balance():
    """演示阴阳平衡机制"""
    print("🌟 === 阴阳平衡机制演示 ===")
    balance = YinYangBalance()
    
    print(f"初始状态: 阴{balance.yin_points} 阳{balance.yang_points} 平衡度{balance.balance_ratio:.2f}")
    
    # 模拟阴阳变化
    balance.yin_points = 3
    balance.yang_points = 7
    print(f"阳盛阴衰: 阴{balance.yin_points} 阳{balance.yang_points} 平衡度{balance.balance_ratio:.2f} 奖励{balance.get_balance_bonus()}")
    
    balance.yin_points = 5
    balance.yang_points = 5
    print(f"阴阳平衡: 阴{balance.yin_points} 阳{balance.yang_points} 平衡度{balance.balance_ratio:.2f} 奖励{balance.get_balance_bonus()}")
    
    print()

def demo_wuxing_cycle():
    """演示五行相生相克"""
    print("🌟 === 五行相生相克演示 ===")
    
    # 相生演示
    print("五行相生:")
    for element in WuXing:
        generated = WuXingCycle.get_sheng_target(element)
        print(f"  {element.value} 生 {generated.value}")
    
    print("\n五行相克:")
    for element in WuXing:
        restrained = WuXingCycle.get_ke_target(element)
        print(f"  {element.value} 克 {restrained.value}")
    
    # 相生相克关系判断
    print(f"\n金对木的关系: {'相克' if WuXingCycle.is_ke_relationship(WuXing.JIN, WuXing.MU) else '无直接关系'}")
    print(f"水对木的关系: {'相生' if WuXingCycle.is_sheng_relationship(WuXing.SHUI, WuXing.MU) else '无直接关系'}")
    print()

def demo_enhanced_actions():
    """演示增强动作系统"""
    print("🌟 === 增强动作系统演示 ===")
    
    # 创建测试玩家
    player = Player("易经修行者", HERMIT_AVATAR)
    player.qi = 10
    player.dao_xing = 5
    player.cheng_yi = 3
    player.hand = BALANCED_DECK[:3]  # 给玩家一些卡牌
    
    game_state = GameState(players=[player])
    
    print("玩家初始状态:")
    display_yijing_status(player)
    
    # 演示增强冥想
    print("\n🧘 执行增强冥想...")
    new_state = enhanced_meditate(game_state)
    new_player = new_state.get_current_player()
    print(f"冥想后: 气{new_player.qi} 道行{new_player.dao_xing} 诚意{new_player.cheng_yi}")
    display_yijing_status(new_player)
    
    # 演示增强学习
    print("\n📚 执行增强学习...")
    new_state = enhanced_study(new_state)
    new_player = new_state.get_current_player()
    print(f"学习后: 手牌数{len(new_player.hand)} 道行{new_player.dao_xing}")
    display_yijing_status(new_player)
    
    print()

def demo_biangua_transformation():
    """演示变卦机制"""
    print("🌟 === 变卦机制演示 ===")
    
    player = Player("变卦大师", HERMIT_AVATAR)
    player.dao_xing = 10
    player.cheng_yi = 8
    player.hand = BALANCED_DECK[:5]
    
    game_state = GameState(players=[player])
    
    print("变卦前状态:")
    print(f"道行: {player.dao_xing}, 诚意: {player.cheng_yi}")
    print(f"手牌数: {len(player.hand)}")
    
    # 执行变卦
    print("\n🔄 执行变卦转换...")
    new_state = biangua_transformation(game_state, "乾", "坤")
    if new_state:
        new_player = new_state.get_current_player()
    else:
        print("变卦失败：资源不足")
        return
    
    print("变卦后状态:")
    print(f"道行: {new_player.dao_xing}, 诚意: {new_player.cheng_yi}")
    print(f"手牌数: {len(new_player.hand)}")
    print(f"变卦历史: {new_player.transformation_history}")
    
    print()

def demo_victory_conditions():
    """演示增强胜利条件"""
    print("🌟 === 增强胜利条件演示 ===")
    
    # 创建接近胜利的玩家
    player = Player("胜利者", HERMIT_AVATAR)
    
    # 测试不同胜利条件
    scenarios = [
        ("道行胜利", {"dao_xing": 15, "cheng_yi": 5}),
        ("阴阳平衡胜利", {"dao_xing": 8, "cheng_yi": 12, "yin_yang": (10, 10)}),
        ("五行大师胜利", {"dao_xing": 10, "cheng_yi": 8, "wuxing_mastery": True}),
        ("变卦智者胜利", {"dao_xing": 12, "cheng_yi": 10, "transformations": 5})
    ]
    
    for scenario_name, conditions in scenarios:
        test_player = Player("测试者", HERMIT_AVATAR)
        test_player.dao_xing = conditions.get("dao_xing", 0)
        test_player.cheng_yi = conditions.get("cheng_yi", 0)
        
        if "yin_yang" in conditions:
            yin, yang = conditions["yin_yang"]
            test_player.yin_yang_balance.yin_points = yin
            test_player.yin_yang_balance.yang_points = yang
        
        if "wuxing_mastery" in conditions:
            # 设置五行精通
            for element in WuXing:
                test_player.wuxing_affinities[element] = 8
        
        if "transformations" in conditions:
            test_player.transformation_history = ["变卦"] * conditions["transformations"]
        
        game_state = GameState(players=[test_player])
        winner = check_victory_conditions_enhanced(game_state)
        
        print(f"{scenario_name}: {'✅ 胜利' if winner else '❌ 未胜利'}")
        if winner:
            print(f"  胜利者: {winner.name}")
    
    print()

def main():
    """主演示函数"""
    print("🎮 === 天机变·易经哲学游戏机制演示 ===\n")
    
    demo_yin_yang_balance()
    demo_wuxing_cycle()
    demo_enhanced_actions()
    demo_biangua_transformation()
    demo_victory_conditions()
    
    print("🌟 === 演示完成 ===")
    print("易经哲学机制已成功集成到游戏中！")
    print("- ☯️  阴阳平衡系统：体现中庸之道")
    print("- 🌊 五行相生相克：展现自然规律")
    print("- 🔄 变卦机制：诠释变化之道")
    print("- 🎯 多元胜利条件：鼓励不同修行路径")
    print("- 📚 教育价值：在游戏中学习易经智慧")

if __name__ == "__main__":
    main()