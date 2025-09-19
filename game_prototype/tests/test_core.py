"""
核心模块单元测试
测试游戏核心组件的功能和接口
"""

import unittest
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 现在可以正常导入
from core.interfaces import *
from core.base_types import *
from core.constants import *
from core.events import *
from core.game_engine import *
from core.logging_system import *
from core.exceptions import *

class TestInterfaces(unittest.TestCase):
    """测试核心接口"""
    
    def test_position_creation(self):
        """测试位置创建"""
        pos = Position(5, 10)
        self.assertEqual(pos.x, 5)
        self.assertEqual(pos.y, 10)
    
    def test_position_equality(self):
        """测试位置相等性"""
        pos1 = Position(3, 7)
        pos2 = Position(3, 7)
        pos3 = Position(4, 7)
        
        self.assertEqual(pos1, pos2)
        self.assertNotEqual(pos1, pos3)
    
    def test_validation_result(self):
        """测试验证结果"""
        # 成功的验证
        success_result = ValidationResult(True, "操作成功")
        self.assertTrue(success_result.is_valid)
        self.assertEqual(success_result.message, "操作成功")
        
        # 失败的验证
        fail_result = ValidationResult(False, "操作失败")
        self.assertFalse(fail_result.is_valid)
        self.assertEqual(fail_result.message, "操作失败")
    
    def test_action_result(self):
        """测试行动结果"""
        result = ActionResult(
            success=True,
            message="行动成功",
            effects={"health": -10, "mana": 5}
        )
        
        self.assertTrue(result.success)
        self.assertEqual(result.message, "行动成功")
        self.assertEqual(result.effects["health"], -10)
        self.assertEqual(result.effects["mana"], 5)

class TestBaseTypes(unittest.TestCase):
    """测试基础类型"""
    
    def test_player_type_enum(self):
        """测试玩家类型枚举"""
        self.assertEqual(PlayerType.HUMAN.value, "human")
        self.assertEqual(PlayerType.AI.value, "ai")
        self.assertEqual(PlayerType.SPECTATOR.value, "spectator")
    
    def test_action_type_enum(self):
        """测试行动类型枚举"""
        self.assertEqual(ActionType.MOVE.value, "move")
        self.assertEqual(ActionType.PLACE_PIECE.value, "place_piece")
        self.assertEqual(ActionType.CULTIVATE.value, "cultivate")

class TestConstants(unittest.TestCase):
    """测试常量定义"""
    
    def test_game_constants(self):
        """测试游戏常量"""
        # 测试棋盘大小
        self.assertIsInstance(BOARD_SIZE, int)
        self.assertGreater(BOARD_SIZE, 0)
        
        # 测试最大玩家数
        self.assertIsInstance(MAX_PLAYERS, int)
        self.assertGreater(MAX_PLAYERS, 0)
    
    def test_resource_constants(self):
        """测试资源常量"""
        # 测试初始资源
        self.assertIsInstance(INITIAL_RESOURCES, dict)
        self.assertIn("qi", INITIAL_RESOURCES)
        self.assertIn("spirit", INITIAL_RESOURCES)

class TestEvents(unittest.TestCase):
    """测试事件系统"""
    
    def setUp(self):
        """设置测试环境"""
        self.event_manager = EventManager()
        self.received_events = []
    
    def event_handler(self, event):
        """事件处理器"""
        self.received_events.append(event)
    
    def test_event_registration(self):
        """测试事件注册"""
        self.event_manager.register_handler("test_event", self.event_handler)
        
        # 检查处理器是否注册成功
        self.assertIn("test_event", self.event_manager.handlers)
        self.assertIn(self.event_handler, self.event_manager.handlers["test_event"])
    
    def test_event_emission(self):
        """测试事件发射"""
        self.event_manager.register_handler("test_event", self.event_handler)
        
        test_event = GameEvent("test_event", {"data": "test_data"})
        self.event_manager.emit_event(test_event)
        
        # 检查事件是否被接收
        self.assertEqual(len(self.received_events), 1)
        self.assertEqual(self.received_events[0].event_type, "test_event")
        self.assertEqual(self.received_events[0].data["data"], "test_data")
    
    def test_event_unregistration(self):
        """测试事件注销"""
        self.event_manager.register_handler("test_event", self.event_handler)
        self.event_manager.unregister_handler("test_event", self.event_handler)
        
        # 检查处理器是否被移除
        if "test_event" in self.event_manager.handlers:
            self.assertNotIn(self.event_handler, self.event_manager.handlers["test_event"])

class TestGameEngine(unittest.TestCase):
    """测试游戏引擎"""
    
    def setUp(self):
        """设置测试环境"""
        self.engine = GameEngine()
    
    def test_engine_initialization(self):
        """测试引擎初始化"""
        self.assertIsNotNone(self.engine.event_manager)
        self.assertIsNotNone(self.engine.logger)
        self.assertFalse(self.engine.is_running)
    
    def test_engine_start_stop(self):
        """测试引擎启动和停止"""
        # 启动引擎
        self.engine.start()
        self.assertTrue(self.engine.is_running)
        
        # 停止引擎
        self.engine.stop()
        self.assertFalse(self.engine.is_running)

class TestLoggingSystem(unittest.TestCase):
    """测试日志系统"""
    
    def setUp(self):
        """设置测试环境"""
        self.logger = GameLogger("test_logger")
    
    def test_logger_creation(self):
        """测试日志器创建"""
        self.assertEqual(self.logger.name, "test_logger")
        self.assertIsNotNone(self.logger.logger)
    
    def test_logging_methods(self):
        """测试日志方法"""
        # 这些方法不应该抛出异常
        try:
            self.logger.debug("Debug message")
            self.logger.info("Info message")
            self.logger.warning("Warning message")
            self.logger.error("Error message")
            self.logger.critical("Critical message")
        except Exception as e:
            self.fail(f"日志方法抛出了异常: {e}")

class TestExceptions(unittest.TestCase):
    """测试异常类"""
    
    def test_game_exception(self):
        """测试游戏异常"""
        with self.assertRaises(GameException):
            raise GameException("测试异常")
    
    def test_validation_error(self):
        """测试验证错误"""
        with self.assertRaises(ValidationError):
            raise ValidationError("验证失败")
    
    def test_action_error(self):
        """测试行动错误"""
        with self.assertRaises(ActionError):
            raise ActionError("行动失败")
    
    def test_state_error(self):
        """测试状态错误"""
        with self.assertRaises(StateError):
            raise StateError("状态错误")

if __name__ == '__main__':
    unittest.main()