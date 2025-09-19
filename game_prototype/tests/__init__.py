"""
天机变游戏测试模块
包含所有单元测试、集成测试和性能测试
"""

from .test_core import *
from .test_models import *
from .test_systems import *
from .test_utils import *
from .test_integration import *

__all__ = [
    # 核心测试
    'TestInterfaces', 'TestBaseTypes', 'TestConstants',
    'TestEventSystem', 'TestGameEngine', 'TestLoggingSystem',
    
    # 模型测试
    'TestPlayerModel', 'TestActionModel', 'TestGameStateModel',
    
    # 系统测试
    'TestConfigSystem', 'TestYixueSystem',
    
    # 工具测试
    'TestGameUtils', 'TestValidationUtils', 'TestYixueUtils',
    
    # 集成测试
    'TestGameIntegration', 'TestSystemIntegration'
]

__version__ = "1.0.0"