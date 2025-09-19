"""
系统模块单元测试
测试配置系统、易学系统等核心系统组件
"""

import unittest
import sys
import os
from pathlib import Path
import tempfile
import json

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 现在可以正常导入
from systems.config_system import *
from systems.yixue_system import *

class TestConfigSystem(unittest.TestCase):
    """测试配置系统"""
    
    def setUp(self):
        """设置测试环境"""
        self.config_manager = ConfigManager()
        self.temp_file = None
    
    def tearDown(self):
        """清理测试环境"""
        if self.temp_file and os.path.exists(self.temp_file):
            os.remove(self.temp_file)
    
    def test_config_field_creation(self):
        """测试配置字段创建"""
        field = ConfigField(
            name="test_field",
            default_value=100,
            description="测试字段",
            validator=RangeValidator(0, 200)
        )
        
        self.assertEqual(field.name, "test_field")
        self.assertEqual(field.default_value, 100)
        self.assertEqual(field.description, "测试字段")
        self.assertIsInstance(field.validator, RangeValidator)
    
    def test_range_validator(self):
        """测试范围验证器"""
        validator = RangeValidator(0, 100)
        
        # 有效值
        self.assertTrue(validator.validate(50).is_valid)
        self.assertTrue(validator.validate(0).is_valid)
        self.assertTrue(validator.validate(100).is_valid)
        
        # 无效值
        self.assertFalse(validator.validate(-1).is_valid)
        self.assertFalse(validator.validate(101).is_valid)
    
    def test_choice_validator(self):
        """测试选择验证器"""
        validator = ChoiceValidator(["easy", "medium", "hard"])
        
        # 有效值
        self.assertTrue(validator.validate("easy").is_valid)
        self.assertTrue(validator.validate("medium").is_valid)
        self.assertTrue(validator.validate("hard").is_valid)
        
        # 无效值
        self.assertFalse(validator.validate("invalid").is_valid)
        self.assertFalse(validator.validate("").is_valid)
    
    def test_type_validator(self):
        """测试类型验证器"""
        validator = TypeValidator(int)
        
        # 有效值
        self.assertTrue(validator.validate(42).is_valid)
        self.assertTrue(validator.validate(0).is_valid)
        self.assertTrue(validator.validate(-10).is_valid)
        
        # 无效值
        self.assertFalse(validator.validate("42").is_valid)
        self.assertFalse(validator.validate(3.14).is_valid)
        self.assertFalse(validator.validate(True).is_valid)
    
    def test_config_registration(self):
        """测试配置注册"""
        field = ConfigField(
            name="test_config",
            default_value=50,
            description="测试配置",
            validator=RangeValidator(0, 100)
        )
        
        self.config_manager.register_field(field)
        
        # 检查配置是否注册成功
        self.assertIn("test_config", self.config_manager.fields)
        self.assertEqual(self.config_manager.get_value("test_config"), 50)
    
    def test_config_set_get(self):
        """测试配置设置和获取"""
        field = ConfigField(
            name="test_value",
            default_value=10,
            description="测试值",
            validator=RangeValidator(0, 100)
        )
        
        self.config_manager.register_field(field)
        
        # 设置有效值
        result = self.config_manager.set_value("test_value", 75)
        self.assertTrue(result.is_valid)
        self.assertEqual(self.config_manager.get_value("test_value"), 75)
        
        # 设置无效值
        result = self.config_manager.set_value("test_value", 150)
        self.assertFalse(result.is_valid)
        self.assertEqual(self.config_manager.get_value("test_value"), 75)  # 值不应该改变
    
    def test_config_save_load(self):
        """测试配置保存和加载"""
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            self.temp_file = f.name
        
        # 注册一些配置
        field1 = ConfigField("config1", 100, "配置1", RangeValidator(0, 200))
        field2 = ConfigField("config2", "medium", "配置2", ChoiceValidator(["easy", "medium", "hard"]))
        
        self.config_manager.register_field(field1)
        self.config_manager.register_field(field2)
        
        # 修改配置值
        self.config_manager.set_value("config1", 150)
        self.config_manager.set_value("config2", "hard")
        
        # 保存配置
        self.config_manager.save_config(self.temp_file)
        
        # 创建新的配置管理器并加载
        new_manager = ConfigManager()
        new_manager.register_field(field1)
        new_manager.register_field(field2)
        new_manager.load_config(self.temp_file)
        
        # 检查值是否正确加载
        self.assertEqual(new_manager.get_value("config1"), 150)
        self.assertEqual(new_manager.get_value("config2"), "hard")

class TestYixueSystem(unittest.TestCase):
    """测试易学系统"""
    
    def test_wuxing_creation(self):
        """测试五行创建"""
        wuxing = Wuxing(WuxingElement.WOOD, 80)
        
        self.assertEqual(wuxing.element, WuxingElement.WOOD)
        self.assertEqual(wuxing.strength, 80)
    
    def test_bagua_creation(self):
        """测试八卦创建"""
        bagua = Bagua(BaguaType.QIAN, 90)
        
        self.assertEqual(bagua.type, BaguaType.QIAN)
        self.assertEqual(bagua.power, 90)
    
    def test_yinyang_creation(self):
        """测试阴阳创建"""
        yinyang = Yinyang(YinyangType.YANG, 70)
        
        self.assertEqual(yinyang.type, YinyangType.YANG)
        self.assertEqual(yinyang.balance, 70)
    
    def test_cultivation_state(self):
        """测试修为状态"""
        state = CultivationState(
            realm=CultivationRealm.FOUNDATION,
            level=5,
            experience=1500,
            qi_capacity=2000
        )
        
        self.assertEqual(state.realm, CultivationRealm.FOUNDATION)
        self.assertEqual(state.level, 5)
        self.assertEqual(state.experience, 1500)
        self.assertEqual(state.qi_capacity, 2000)
    
    def test_wuxing_system(self):
        """测试五行系统"""
        system = WuxingSystem()
        
        # 测试生克关系
        wood = Wuxing(WuxingElement.WOOD, 100)
        fire = Wuxing(WuxingElement.FIRE, 100)
        
        # 木生火
        reaction = system.calculate_reaction(wood, fire)
        self.assertEqual(reaction, WuxingReaction.GENERATION)
        
        # 测试相互作用
        result = system.interact_elements(wood, fire)
        self.assertIsInstance(result, dict)
        self.assertIn("reaction", result)
        self.assertIn("bonus", result)
    
    def test_bagua_system(self):
        """测试八卦系统"""
        system = BaguaSystem()
        
        qian = Bagua(BaguaType.QIAN, 100)
        kun = Bagua(BaguaType.KUN, 100)
        
        # 测试八卦关系
        relationship = system.calculate_relationship(qian, kun)
        self.assertIsInstance(relationship, BaguaRelationship)
        
        # 测试相互作用
        result = system.interact_bagua(qian, kun)
        self.assertIsInstance(result, dict)
        self.assertIn("relationship", result)
        self.assertIn("effect", result)
    
    def test_yinyang_system(self):
        """测试阴阳系统"""
        system = YinyangSystem()
        
        yang = Yinyang(YinyangType.YANG, 80)
        yin = Yinyang(YinyangType.YIN, 60)
        
        # 测试平衡计算
        balance = system.calculate_balance(yang, yin)
        self.assertIsInstance(balance, float)
        self.assertGreaterEqual(balance, 0.0)
        self.assertLessEqual(balance, 1.0)
        
        # 测试调和
        result = system.harmonize(yang, yin)
        self.assertIsInstance(result, dict)
        self.assertIn("balance", result)
        self.assertIn("harmony_bonus", result)
    
    def test_cultivation_system(self):
        """测试修为系统"""
        system = CultivationSystem()
        
        state = CultivationState(
            realm=CultivationRealm.QI_REFINING,
            level=9,
            experience=4500,
            qi_capacity=1000
        )
        
        # 测试突破检查
        can_breakthrough = system.can_breakthrough(state)
        self.assertIsInstance(can_breakthrough, bool)
        
        # 测试经验增加
        new_state = system.add_experience(state, 500)
        self.assertEqual(new_state.experience, 5000)
        
        # 测试修为提升
        if can_breakthrough:
            advanced_state = system.advance_cultivation(state)
            self.assertGreaterEqual(advanced_state.level, state.level)
    
    def test_comprehensive_yixue_system(self):
        """测试综合易学系统"""
        system = YixueSystem()
        
        # 创建默认状态
        state = create_default_yixue_state()
        
        self.assertIsInstance(state["wuxing"], list)
        self.assertIsInstance(state["bagua"], list)
        self.assertIsInstance(state["yinyang"], dict)
        self.assertIsInstance(state["cultivation"], CultivationState)
        
        # 测试系统分析
        analysis = system.analyze_state(state)
        self.assertIsInstance(analysis, dict)
        self.assertIn("wuxing_balance", analysis)
        self.assertIn("bagua_harmony", analysis)
        self.assertIn("yinyang_balance", analysis)
        self.assertIn("cultivation_potential", analysis)

if __name__ == '__main__':
    unittest.main()