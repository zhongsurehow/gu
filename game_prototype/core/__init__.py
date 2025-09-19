"""
天机变游戏核心模块
提供游戏的基础架构和抽象接口
"""

from .base_types import *
from .interfaces import *
from .exceptions import *
from .constants import *

__version__ = "1.0.0"
__author__ = "天机变开发团队"

__all__ = [
    # 基础类型
    'GamePhase', 'PlayerType', 'ActionType', 'ResourceType',
    
    # 接口
    'IGameAction', 'IGameSystem', 'IPlayer', 'IGameState',
    
    # 异常
    'GameException', 'InvalidActionException', 'ResourceException',
    
    # 常量
    'GAME_CONSTANTS', 'UI_CONSTANTS', 'BALANCE_CONSTANTS'
]