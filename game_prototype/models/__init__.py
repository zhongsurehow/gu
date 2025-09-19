"""
天机变游戏数据模型模块

包含所有游戏数据模型的定义，包括：
- 玩家模型
- 游戏状态模型
- 行动模型
- 易学相关模型
"""

from .player_model import Player, PlayerState, PlayerStats
from .game_model import GameState, GameSession, GameHistory
from .action_model import GameAction, ActionResult, ActionHistory
from .yixue_model import HexagramState, WuxingState, YinyangState, CultivationLevel

__all__ = [
    # 玩家模型
    'Player',
    'PlayerState', 
    'PlayerStats',
    
    # 游戏模型
    'GameState',
    'GameSession',
    'GameHistory',
    
    # 行动模型
    'GameAction',
    'ActionResult',
    'ActionHistory',
    
    # 易学模型
    'HexagramState',
    'WuxingState',
    'YinyangState',
    'CultivationLevel'
]

__version__ = "1.0.0"