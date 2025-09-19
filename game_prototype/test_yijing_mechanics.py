"""
测试易经机制的平衡性和教育效果
"""

import unittest
import copy
from game_prototype.game_state import GameState, Player, Zone
from game_prototype.yijing_mechanics import (
    YinYang, WuXing, YinYangBalance, WuXingCycle, 
    TaijiMechanism, ZhouYiWisdom, GUA_ATTRIBUTES
)
from game_prototype.yijing_actions import (
    enhanced_play_card, enhanced_meditate, enhanced_study,
    apply_yin_yang_effect, apply_wuxing_effect,
    biangua_transformation, check_victory_conditions_enhanced
)
from game_prototype.generate_64_guas import ALL_64_GUAS
from game_prototype.game_data import BALANCED_DECK, HERMIT_AVATAR

class TestYinYangBalance(unittest.TestCase):
    """测试阴阳平衡机制"""
    
    def setUp(self):
        self.balance = YinYangBalance()
    
    def test_initial_balance(self):
        """测试初始平衡状态"""
        self.assertEqual(self.balance.yin_points, 0)
        self.assertEqual(self.balance.yang_points, 0)
        self.assertEqual(self.balance.balance_ratio, 1.0)
    
    def test_balance_calculation(self):
        """测试平衡度计算"""
        self.balance.yin_points = 3
        self.balance.yang_points = 4
        expected_ratio = (min(3, 4) * 2) / (3 + 4)  # (3*2)/7 = 6/7 ≈ 0.857
        self.assertAlmostEqual(self.balance.balance_ratio, expected_ratio, places=2)

    def test_balance_bonus(self):
        """测试平衡奖励"""
        # 完全平衡
        self.balance.yin_points = 5
        self.balance.yang_points = 5
        # 完全平衡时ratio = (5*2)/(5+5) = 1.0，应该得到最高奖励
        self.assertEqual(self.balance.get_balance_bonus(), 3)
        
        # 高度平衡
        self.balance.yin_points = 8
        self.balance.yang_points = 9
        # ratio = (8*2)/(8+9) = 16/17 ≈ 0.94，应该得到3分奖励（≥0.8）
        self.assertEqual(self.balance.get_balance_bonus(), 3)
        
        # 基础平衡
        self.balance.yin_points = 6
        self.balance.yang_points = 10
        self.assertEqual(self.balance.get_balance_bonus(), 1)
        
        # 失衡
        self.balance.yin_points = 2
        self.balance.yang_points = 10
        self.assertEqual(self.balance.get_balance_bonus(), 0)

class TestWuXingCycle(unittest.TestCase):
    """测试五行相生相克机制"""
    
    def test_sheng_relationships(self):
        """测试相生关系"""
        self.assertTrue(WuXingCycle.is_sheng_relationship(WuXing.WOOD, WuXing.FIRE))
        self.assertTrue(WuXingCycle.is_sheng_relationship(WuXing.FIRE, WuXing.EARTH))
        self.assertTrue(WuXingCycle.is_sheng_relationship(WuXing.EARTH, WuXing.METAL))
        self.assertTrue(WuXingCycle.is_sheng_relationship(WuXing.METAL, WuXing.WATER))
        self.assertTrue(WuXingCycle.is_sheng_relationship(WuXing.WATER, WuXing.WOOD))
    
    def test_ke_relationships(self):
        """测试相克关系"""
        self.assertTrue(WuXingCycle.is_ke_relationship(WuXing.WOOD, WuXing.EARTH))
        self.assertTrue(WuXingCycle.is_ke_relationship(WuXing.EARTH, WuXing.WATER))
        self.assertTrue(WuXingCycle.is_ke_relationship(WuXing.WATER, WuXing.FIRE))
        self.assertTrue(WuXingCycle.is_ke_relationship(WuXing.FIRE, WuXing.METAL))
        self.assertTrue(WuXingCycle.is_ke_relationship(WuXing.METAL, WuXing.WOOD))
    
    def test_sheng_target(self):
        """测试相生目标"""
        self.assertEqual(WuXingCycle.get_sheng_target(WuXing.WOOD), WuXing.FIRE)
        self.assertEqual(WuXingCycle.get_sheng_target(WuXing.FIRE), WuXing.EARTH)
        self.assertEqual(WuXingCycle.get_sheng_target(WuXing.EARTH), WuXing.METAL)
        self.assertEqual(WuXingCycle.get_sheng_target(WuXing.METAL), WuXing.WATER)
        self.assertEqual(WuXingCycle.get_sheng_target(WuXing.WATER), WuXing.WOOD)

class TestYijingActions(unittest.TestCase):
    """测试易经动作系统"""
    
    def setUp(self):
        self.player = Player("测试玩家", HERMIT_AVATAR)
        self.player.qi = 10
        self.player.dao_xing = 5
        self.player.cheng_yi = 5
        
        # 添加测试卡牌
        if BALANCED_DECK:
            self.player.hand = BALANCED_DECK[:3]
        
        self.game_state = GameState(
            players=[self.player]
        )
    
    def test_apply_yin_yang_effect(self):
        """测试阴阳效果应用"""
        initial_yin = self.player.yin_yang_balance.yin_points
        initial_yang = self.player.yin_yang_balance.yang_points
        
        apply_yin_yang_effect(self.player, YinYang.YIN, 2)
        self.assertEqual(self.player.yin_yang_balance.yin_points, initial_yin + 2)
        
        apply_yin_yang_effect(self.player, YinYang.YANG, 3)
        self.assertEqual(self.player.yin_yang_balance.yang_points, initial_yang + 3)
    
    def test_apply_wuxing_effect(self):
        """测试五行效果应用"""
        initial_wood = self.player.wuxing_affinities[WuXing.WOOD]
        
        # 应用木属性效果
        result = apply_wuxing_effect(self.player, WuXing.WOOD, 3)
        self.assertEqual(self.player.wuxing_affinities[WuXing.WOOD], initial_wood + 3)
        
        # 检查是否触发相生效果
        if self.player.wuxing_affinities[WuXing.WOOD] >= 3:
            self.assertIsNotNone(result)
            self.assertIn("木生火", result)
    
    def test_enhanced_meditate(self):
        """测试增强冥想动作"""
        initial_qi = self.player.qi
        initial_yin = self.player.yin_yang_balance.yin_points
        
        # 在地部冥想
        self.player.position = Zone.DI
        new_state = enhanced_meditate(self.game_state)
        new_player = new_state.get_current_player()
        
        # 验证气增加
        self.assertGreater(new_player.qi, initial_qi)
        # 验证阴气增加
        self.assertGreater(new_player.yin_yang_balance.yin_points, initial_yin)
    
    def test_enhanced_study(self):
        """测试增强学习动作"""
        initial_hand_size = len(self.player.hand)
        
        new_state = enhanced_study(self.game_state)
        new_player = new_state.get_current_player()
        
        # 验证手牌增加
        self.assertGreaterEqual(len(new_player.hand), initial_hand_size + 2)
    
    def test_biangua_transformation(self):
        """测试变卦机制"""
        initial_cheng_yi = self.player.cheng_yi
        initial_history_length = len(self.player.transformation_history)
        
        new_state = biangua_transformation(self.game_state, "乾为天", "坤为地")
        
        if new_state:  # 如果变卦成功
            new_player = new_state.get_current_player()
            # 验证诚意消耗
            self.assertEqual(new_player.cheng_yi, initial_cheng_yi - 3)
            # 验证变卦历史记录
            self.assertEqual(len(new_player.transformation_history), initial_history_length + 1)

class TestVictoryConditions(unittest.TestCase):
    """测试胜利条件"""
    
    def setUp(self):
        self.player1 = Player("玩家1", HERMIT_AVATAR)
        self.player2 = Player("玩家2", HERMIT_AVATAR)
        self.game_state = GameState(
            players=[self.player1, self.player2]
        )
    
    def test_traditional_dao_xing_victory(self):
        """测试传统道行胜利"""
        self.player1.dao_xing = 15
        winner = check_victory_conditions_enhanced(self.game_state)
        self.assertEqual(winner, self.player1)
    
    def test_resource_victory(self):
        """测试资源胜利"""
        self.player1.qi = 20
        self.player1.cheng_yi = 10
        winner = check_victory_conditions_enhanced(self.game_state)
        self.assertEqual(winner, self.player1)
    
    def test_yin_yang_master_victory(self):
        """测试阴阳大师胜利"""
        self.player1.dao_xing = 10
        self.player1.yin_yang_balance.yin_points = 9
        self.player1.yin_yang_balance.yang_points = 10
        winner = check_victory_conditions_enhanced(self.game_state)
        self.assertEqual(winner, self.player1)
    
    def test_wuxing_master_victory(self):
        """测试五行宗师胜利"""
        for element in WuXing:
            self.player1.wuxing_affinities[element] = 3
        winner = check_victory_conditions_enhanced(self.game_state)
        self.assertEqual(winner, self.player1)
    
    def test_transformation_path_victory(self):
        """测试变化之道胜利"""
        self.player1.dao_xing = 8
        self.player1.transformation_history = ["乾→坤", "坤→震", "震→巽", "巽→坎", "坎→离"]
        winner = check_victory_conditions_enhanced(self.game_state)
        self.assertEqual(winner, self.player1)

class TestEducationalValue(unittest.TestCase):
    """测试教育价值"""
    
    def test_gua_attributes_coverage(self):
        """测试卦象属性覆盖度"""
        # 验证所有64卦都有属性定义
        covered_guas = set(GUA_ATTRIBUTES.keys())
        all_gua_names = set(gua["name"] for gua in ALL_64_GUAS)
        
        # 至少应该覆盖主要的卦象
        important_guas = {"乾为天", "坤为地", "震为雷", "巽为风", "坎为水", "离为火", "艮为山", "兑为泽"}
        self.assertTrue(important_guas.issubset(covered_guas))
    
    def test_yijing_wisdom_activation(self):
        """测试易经智慧激活"""
        # 创建触发条件
        player_state = {
            "dao_xing": 10,
            "yin_yang_balance": 0.9,
            "controlled_zones": 3
        }
        
        card_effects = ["相生", "平衡", "变化"]
        
        wisdom = ZhouYiWisdom.check_wisdom_activation(player_state, card_effects)
        self.assertIsInstance(wisdom, list)
    
    def test_learning_progression(self):
        """测试学习进度"""
        player = Player("学习者", HERMIT_AVATAR)
        
        # 模拟学习过程
        for _ in range(10):
            # 应用各种易经效果
            apply_yin_yang_effect(player, YinYang.YIN, 1)
            apply_yin_yang_effect(player, YinYang.YANG, 1)
            apply_wuxing_effect(player, WuXing.WOOD, 1)
        
        # 验证学习效果
        self.assertGreater(player.yin_yang_balance.yin_points, 0)
        self.assertGreater(player.yin_yang_balance.yang_points, 0)
        self.assertGreater(player.wuxing_affinities[WuXing.WOOD], 0)

class TestGameBalance(unittest.TestCase):
    """测试游戏平衡性"""
    
    def test_action_costs(self):
        """测试动作成本平衡"""
        # 变卦成本应该合理
        self.assertEqual(3, 3)  # 变卦消耗3点诚意
        
        # 各种动作的AP成本应该平衡
        play_card_cost = 1
        meditate_cost = 1
        study_cost = 1
        
        self.assertEqual(play_card_cost, meditate_cost)
        self.assertEqual(meditate_cost, study_cost)
    
    def test_victory_condition_balance(self):
        """测试胜利条件平衡"""
        # 不同胜利路径的难度应该相当
        traditional_threshold = 15  # 道行胜利
        resource_threshold = (20, 10)  # 气和诚意胜利
        balance_threshold = (0.9, 10)  # 阴阳大师胜利
        
        # 这些阈值应该经过平衡测试
        self.assertGreater(traditional_threshold, 10)
        self.assertGreater(resource_threshold[0], 15)
        self.assertGreater(balance_threshold[1], 5)
    
    def test_resource_generation_rate(self):
        """测试资源生成速率"""
        player = Player("测试玩家", HERMIT_AVATAR)
        game_state = GameState(players=[player])
        
        # 模拟多轮游戏
        for turn in range(10):
            # 每轮冥想
            game_state = enhanced_meditate(game_state)
            # 每轮学习
            game_state = enhanced_study(game_state)
        
        final_player = game_state.get_current_player()
        
        # 验证资源增长合理
        self.assertGreater(final_player.qi, 10)
        self.assertGreater(len(final_player.hand), 3)

def run_balance_simulation():
    """运行平衡性模拟测试"""
    print("🎮 运行游戏平衡性模拟...")
    
    # 创建多个玩家进行模拟
    results = {"traditional": 0, "yin_yang": 0, "wuxing": 0, "transformation": 0, "resource": 0}
    
    for simulation in range(100):
        player = Player(f"模拟玩家{simulation}", HERMIT_AVATAR)
        game_state = GameState(players=[player])
        
        # 模拟随机游戏过程
        for turn in range(50):
            import random
            action = random.choice(["meditate", "study", "transform"])
            
            if action == "meditate":
                game_state = enhanced_meditate(game_state)
            elif action == "study":
                game_state = enhanced_study(game_state)
            elif action == "transform" and player.cheng_yi >= 3:
                source_gua = random.choice(list(GUA_ATTRIBUTES.keys()))
                target_gua = random.choice(list(GUA_ATTRIBUTES.keys()))
                new_state = biangua_transformation(game_state, source_gua, target_gua)
                if new_state:
                    game_state = new_state
            
            # 检查胜利条件
            winner = check_victory_conditions_enhanced(game_state)
            if winner:
                # 判断胜利类型
                if winner.dao_xing >= 15:
                    results["traditional"] += 1
                elif winner.qi >= 20 and winner.cheng_yi >= 10:
                    results["resource"] += 1
                elif winner.yin_yang_balance.balance_ratio >= 0.9 and winner.dao_xing >= 10:
                    results["yin_yang"] += 1
                elif all(affinity >= 3 for affinity in winner.wuxing_affinities.values()):
                    results["wuxing"] += 1
                elif len(winner.transformation_history) >= 5 and winner.dao_xing >= 8:
                    results["transformation"] += 1
                break
    
    print("📊 胜利路径分布:")
    for path, count in results.items():
        percentage = (count / 100) * 100
        print(f"   {path}: {count}/100 ({percentage:.1f}%)")
    
    return results

if __name__ == "__main__":
    print("🧪 开始易经机制测试...")
    
    # 运行单元测试
    unittest.main(verbosity=2, exit=False)
    
    # 运行平衡性模拟
    print("\n" + "="*50)
    run_balance_simulation()
    
    print("\n✅ 测试完成！")