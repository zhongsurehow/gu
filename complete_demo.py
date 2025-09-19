#!/usr/bin/env python3
"""
天机变·易经哲学游戏 - 完整功能演示
展示所有易经机制的集成效果和游戏体验
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_prototype.game_state import GameState, Player
from game_prototype.game_data import EMPEROR_AVATAR, HERMIT_AVATAR
from game_prototype.yijing_actions import (
    enhanced_play_card, enhanced_meditate, enhanced_study,
    biangua_transformation, check_victory_conditions_enhanced,
    display_yijing_status
)
from game_prototype.yijing_mechanics import (
    YinYangBalance, WuXingCycle, BianguaTransformation, TaijiMechanism
)
from game_prototype.generate_64_guas import generate_all_64_guas

def print_section(title: str):
    """打印章节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_subsection(title: str):
    """打印子章节标题"""
    print(f"\n{'-'*40}")
    print(f"  {title}")
    print(f"{'-'*40}")

def demo_game_setup():
    """演示游戏初始化和64卦系统"""
    print_section("🎮 游戏初始化与64卦系统")
    
    # 创建玩家
    player1 = Player(name="道德天尊", avatar=EMPEROR_AVATAR)
    player2 = Player(name="太上老君", avatar=HERMIT_AVATAR)
    
    # 创建游戏状态
    game_state = GameState(players=[player1, player2])
    
    # 获取64卦卡组
    gua_dict = generate_all_64_guas()
    gua_deck = list(gua_dict.values())
    
    print(f"✅ 创建玩家: {player1.name} vs {player2.name}")
    print(f"✅ 64卦卡组生成完成，共 {len(gua_deck)} 张卡牌")
    
    # 展示部分卦牌
    print("\n📚 部分卦牌展示:")
    for i, card in enumerate(gua_deck[:8]):
        first_task = card.tasks[0] if card.tasks else None
        task_desc = first_task.description[:30] + "..." if first_task else "无任务描述"
        print(f"  {i+1}. {card.name} - {task_desc}")
    
    # 给玩家发牌
    for i, player in enumerate(game_state.players):
        for j in range(5):
            if j < len(gua_deck):
                player.hand.append(gua_deck[j + i*5])
        player.qi = 10
        player.cheng_yi = 5
        player.dao_xing = 3
    
    print(f"\n✅ 初始资源分配完成")
    print(f"  玩家手牌: {len(game_state.players[0].hand)} 张")
    print(f"  初始气: {game_state.players[0].qi}")
    print(f"  初始诚意: {game_state.players[0].cheng_yi}")
    print(f"  初始道行: {game_state.players[0].dao_xing}")
    
    return game_state

def demo_yijing_mechanics():
    """演示易经核心机制"""
    print_section("☯️ 易经核心机制演示")
    
    # 阴阳平衡演示
    print_subsection("阴阳平衡系统")
    balance = YinYangBalance()
    
    print(f"初始状态: 阴={balance.yin_points}, 阳={balance.yang_points}")
    
    balance.yin_points += 3
    print(f"增加阴气后: 阴={balance.yin_points}, 阳={balance.yang_points}")
    print(f"平衡比例: {balance.balance_ratio:.2f}")
    print(f"平衡奖励: {balance.get_balance_bonus()} 点")
    
    balance.yang_points += 2
    print(f"增加阳气后: 阴={balance.yin_points}, 阳={balance.yang_points}")
    print(f"平衡比例: {balance.balance_ratio:.2f}")
    print(f"平衡奖励: {balance.get_balance_bonus()} 点")
    
    # 五行相生相克演示
    print_subsection("五行相生相克系统")
    wuxing = WuXingCycle()
    
    from game_prototype.yijing_mechanics import WuXing
    elements = [WuXing.JIN, WuXing.MU, WuXing.SHUI, WuXing.HUO, WuXing.TU]
    print("五行相生关系:")
    for element in elements:
        sheng_target = wuxing.get_sheng_target(element)
        print(f"  {element.value} 生 {sheng_target.value}")
    
    print("\n五行相克关系:")
    for element in elements:
        ke_target = wuxing.get_ke_target(element)
        print(f"  {element.value} 克 {ke_target.value}")
    
    # 测试相生相克判断
    print(f"\n相生相克判断示例:")
    print(f"  木生火: {wuxing.is_sheng_relationship(WuXing.MU, WuXing.HUO)}")
    print(f"  水克火: {wuxing.is_ke_relationship(WuXing.SHUI, WuXing.HUO)}")
    print(f"  金生水: {wuxing.is_sheng_relationship(WuXing.JIN, WuXing.SHUI)}")
    
    # 变卦机制演示
    print_subsection("变卦转换系统")
    print("变卦示例:")
    biangua_example = BianguaTransformation(
        original_gua="乾为天",
        transformed_gua="坤为地",
        trigger_condition="阴阳失衡时",
        effect_description="从刚健转为柔顺，体现变化之道"
    )
    print(f"  {biangua_example.original_gua} → {biangua_example.transformed_gua}")
    print(f"  触发条件: {biangua_example.trigger_condition}")
    print(f"  效果: {biangua_example.effect_description}")
    
    # 太极机制演示
    print_subsection("太极转化概率")
    taiji = TaijiMechanism()
    
    # 创建不同的阴阳平衡状态进行测试
    test_balances = [
        YinYangBalance(yin_points=1, yang_points=10),  # 极阳
        YinYangBalance(yin_points=10, yang_points=1),  # 极阴
        YinYangBalance(yin_points=5, yang_points=5),   # 平衡
    ]
    
    for balance in test_balances:
        prob = taiji.calculate_transformation_probability(balance)
        print(f"  阴={balance.yin_points}, 阳={balance.yang_points} → 转化概率 {prob:.1%}")

def demo_enhanced_actions(game_state: GameState):
    """演示增强动作系统"""
    print_section("🎯 增强动作系统演示")
    
    player = game_state.players[0]
    
    # 显示玩家状态
    print_subsection("玩家修行状态")
    display_yijing_status(player)
    
    # 增强冥想演示
    print_subsection("增强冥想 (Enhanced Meditate)")
    print(f"冥想前: 气={player.qi}, 道行={player.dao_xing}")
    
    new_state = enhanced_meditate(game_state)
    if new_state:
        game_state = new_state
        player = game_state.players[0]
        print(f"冥想后: 气={player.qi}, 道行={player.dao_xing}")
        print("✅ 增强冥想成功，获得位置修行奖励")
    
    # 增强学习演示
    print_subsection("增强学习 (Enhanced Study)")
    print(f"学习前: 诚意={player.cheng_yi}, 道行={player.dao_xing}")
    
    new_state = enhanced_study(game_state)
    if new_state:
        game_state = new_state
        player = game_state.players[0]
        print(f"学习后: 诚意={player.cheng_yi}, 道行={player.dao_xing}")
        print("✅ 增强学习成功，体现学而时习之")
    
    # 变卦转换演示
    print_subsection("变卦转换 (Biangua Transformation)")
    print(f"变卦前状态: 气={player.qi}, 诚意={player.cheng_yi}")
    
    # 确保玩家有biangua_history属性
    if not hasattr(player, 'biangua_history'):
        player.biangua_history = []
    print(f"变卦历史: {len(player.biangua_history)} 次")
    
    new_state = biangua_transformation(game_state, "乾为天", "坤为地")
    if new_state:
        game_state = new_state
        player = game_state.players[0]
        print(f"变卦后状态: 气={player.qi}, 诚意={player.cheng_yi}")
        print(f"变卦历史: {len(player.biangua_history)} 次")
        print("✅ 变卦成功，体现变化之道")
    else:
        print("❌ 变卦失败，资源不足或条件不满足")
    
    return game_state

def demo_victory_conditions(game_state: GameState):
    """演示多元胜利条件"""
    print_section("🏆 多元胜利条件演示")
    
    player = game_state.players[0]
    
    # 模拟不同的胜利条件
    print_subsection("传统胜利条件")
    original_dao_xing = player.dao_xing
    player.dao_xing = 15
    
    winner = check_victory_conditions_enhanced(game_state)
    if winner:
        print(f"✅ {winner.name} 通过传统路径获胜 (道行达到15)")
    
    # 恢复原始道行
    player.dao_xing = original_dao_xing
    
    print_subsection("阴阳大师路径")
    # 模拟高平衡状态
    player.yin_yang_balance.yin_points = 8
    player.yin_yang_balance.yang_points = 7
    player.dao_xing = 12
    
    winner = check_victory_conditions_enhanced(game_state)
    if winner:
        print(f"✅ {winner.name} 通过阴阳大师路径获胜")
    else:
        balance_ratio = player.yin_yang_balance.balance_ratio
        print(f"阴阳平衡: {balance_ratio:.2f} (需要≥0.8且道行≥12)")
    
    print_subsection("五行宗师路径")
    # 模拟五行亲和力
    from game_prototype.yijing_mechanics import WuXing
    for element in WuXing:
        player.wuxing_affinities[element.value] = 3
    player.dao_xing = 10
    
    winner = check_victory_conditions_enhanced(game_state)
    if winner:
        print(f"✅ {winner.name} 通过五行宗师路径获胜")
    else:
        total_affinity = sum(player.wuxing_affinities.values())
        print(f"五行亲和力总和: {total_affinity} (需要≥15且道行≥10)")
    
    print_subsection("变化之道路径")
    # 模拟多次变卦
    if not hasattr(player, 'biangua_history'):
        player.biangua_history = []
    player.biangua_history = ["乾→坤", "坤→震", "震→巽", "巽→坎", "坎→离", "离→艮"]
    player.dao_xing = 8
    
    winner = check_victory_conditions_enhanced(game_state)
    if winner:
        print(f"✅ {winner.name} 通过变化之道路径获胜")
    else:
        print(f"变卦次数: {len(player.biangua_history)} (需要≥5且道行≥8)")

def demo_educational_value():
    """演示教育价值"""
    print_section("📖 教育价值演示")
    
    print_subsection("易经知识学习")
    print("🎓 通过游戏，玩家可以学习到:")
    print("  • 64卦的名称、含义和象征")
    print("  • 阴阳平衡的哲学思想")
    print("  • 五行相生相克的自然规律")
    print("  • 变化之道的智慧")
    print("  • 中庸之道的实践")
    
    print_subsection("智慧格言系统")
    wisdom_sayings = [
        "天行健，君子以自强不息",
        "地势坤，君子以厚德载物",
        "学而时习之，不亦说乎",
        "知者不惑，仁者不忧，勇者不惧",
        "穷则变，变则通，通则久"
    ]
    
    print("💡 游戏中的智慧格言:")
    for i, saying in enumerate(wisdom_sayings, 1):
        print(f"  {i}. {saying}")
    
    print_subsection("策略思维培养")
    print("🧠 游戏培养的思维能力:")
    print("  • 平衡思维: 在阴阳之间寻找和谐")
    print("  • 系统思维: 理解五行相生相克的循环")
    print("  • 变化思维: 适应不同情况的灵活性")
    print("  • 长远思维: 多种胜利路径的规划")
    print("  • 资源管理: 气、诚意、道行的合理分配")

def main():
    """主演示函数"""
    print("🌟 欢迎体验《天机变·易经哲学游戏》完整演示")
    print("本演示将展示游戏的所有核心功能和教育价值")
    
    try:
        # 1. 游戏初始化演示
        game_state = demo_game_setup()
        
        # 2. 易经机制演示
        demo_yijing_mechanics()
        
        # 3. 增强动作演示
        game_state = demo_enhanced_actions(game_state)
        
        # 4. 胜利条件演示
        demo_victory_conditions(game_state)
        
        # 5. 教育价值演示
        demo_educational_value()
        
        print_section("🎉 演示完成")
        print("✅ 所有易经机制已成功集成到游戏中")
        print("✅ 游戏具备完整的教育价值和策略深度")
        print("✅ 传统文化与现代游戏完美融合")
        
        print(f"\n🚀 要开始游戏，请运行:")
        print(f"   python -m game_prototype.main")
        
        print(f"\n📚 要了解更多，请查看:")
        print(f"   README.md - 项目介绍")
        print(f"   YIJING_GUIDE.md - 易经知识背景")
        print(f"   PROJECT_SUMMARY.md - 项目总结")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()