"""
天机变游戏常量定义

统一管理所有游戏常量，避免硬编码，提供类型安全的常量访问。
包含游戏基础常量、资源常量、易学系统常量、UI常量等。

主要组件：
- GAME_CONSTANTS: 游戏基础常量类
- RESOURCE_CONSTANTS: 资源相关常量类
- YIXUE_CONSTANTS: 易学系统常量类
- UI_CONSTANTS: 界面相关常量类
- BALANCE_CONSTANTS: 游戏平衡常量类

作者: 游戏开发团队
版本: 1.0.0
"""

from typing import Dict, Any, List, Tuple, Final, Union
from .base_types import (
    ResourceType, WuxingElement, BaguaType, YinyangType, 
    CultivationLevel, ActionType, GamePhase, PlayerType
)

# ==================== 游戏基础常量 ====================

class GAME_CONSTANTS:
    """
    游戏基础常量类
    
    定义游戏的核心参数和配置，包括版本信息、玩家限制、
    回合设置、胜利条件等基础游戏规则。
    """
    
    # 游戏版本信息
    VERSION: Final[str] = "1.0.0"
    BUILD_NUMBER: Final[int] = 1001
    RELEASE_DATE: Final[str] = "2024-01-01"
    
    # 玩家数量限制
    MIN_PLAYERS: Final[int] = 2
    MAX_PLAYERS: Final[int] = 4
    DEFAULT_PLAYERS: Final[int] = 2
    OPTIMAL_PLAYERS: Final[int] = 3
    
    # 游戏轮次设置
    MAX_ROUNDS: Final[int] = 50
    DEFAULT_ROUNDS: Final[int] = 20
    MIN_ROUNDS: Final[int] = 5
    QUICK_GAME_ROUNDS: Final[int] = 10
    
    # 行动点数配置
    DEFAULT_ACTION_POINTS: Final[int] = 3
    MAX_ACTION_POINTS: Final[int] = 10
    MIN_ACTION_POINTS: Final[int] = 1
    BONUS_ACTION_POINTS: Final[int] = 2
    
    # 胜利条件
    VICTORY_POINTS_TO_WIN: Final[int] = 100
    REGIONS_TO_WIN: Final[int] = 5
    CULTIVATION_LEVEL_TO_WIN: Final[CultivationLevel] = CultivationLevel.MAHAYANA
    ALTERNATIVE_WIN_POINTS: Final[int] = 80
    
    # 时间限制（秒）
    TURN_TIME_LIMIT: Final[int] = 120
    GAME_TIME_LIMIT: Final[int] = 3600
    MEDITATION_TIME: Final[int] = 30
    
    # 游戏难度系数
    EASY_DIFFICULTY: Final[float] = 0.8
    NORMAL_DIFFICULTY: Final[float] = 1.0
    HARD_DIFFICULTY: Final[float] = 1.2
    EXPERT_DIFFICULTY: Final[float] = 1.5

class RESOURCE_CONSTANTS:
    """
    资源相关常量类
    
    定义各种资源的初始值、上限、转换比率等配置。
    包括五行资源、阴阳资源、特殊资源的管理参数。
    """
    
    # 初始资源配置
    INITIAL_RESOURCES: Final[Dict[ResourceType, int]] = {
        ResourceType.GOLD: 10,
        ResourceType.WOOD: 8,
        ResourceType.WATER: 8,
        ResourceType.FIRE: 8,
        ResourceType.EARTH: 8,
        ResourceType.YIN: 5,
        ResourceType.YANG: 5,
        ResourceType.WISDOM: 0,
        ResourceType.INFLUENCE: 0,
        ResourceType.ACTION_POINTS: 3
    }
    
    # 资源上限
    MAX_RESOURCES: Final[Dict[ResourceType, int]] = {
        ResourceType.GOLD: 100,
        ResourceType.WOOD: 100,
        ResourceType.WATER: 100,
        ResourceType.FIRE: 100,
        ResourceType.EARTH: 100,
        ResourceType.YIN: 50,
        ResourceType.YANG: 50,
        ResourceType.WISDOM: 200,
        ResourceType.INFLUENCE: 150,
        ResourceType.ACTION_POINTS: 10
    }
    
    # 资源生产率（每回合）
    RESOURCE_GENERATION: Final[Dict[ResourceType, int]] = {
        ResourceType.GOLD: 2,
        ResourceType.WOOD: 2,
        ResourceType.WATER: 2,
        ResourceType.FIRE: 2,
        ResourceType.EARTH: 2,
        ResourceType.YIN: 1,
        ResourceType.YANG: 1,
        ResourceType.WISDOM: 0,
        ResourceType.INFLUENCE: 0,
        ResourceType.ACTION_POINTS: 3
    }
    
    # 资源转换比率（1:N）
    RESOURCE_CONVERSION_RATES: Final[Dict[Tuple[ResourceType, ResourceType], float]] = {
        # 五行资源互换
        (ResourceType.GOLD, ResourceType.WATER): 1.2,
        (ResourceType.WATER, ResourceType.WOOD): 1.2,
        (ResourceType.WOOD, ResourceType.FIRE): 1.2,
        (ResourceType.FIRE, ResourceType.EARTH): 1.2,
        (ResourceType.EARTH, ResourceType.GOLD): 1.2,
        
        # 阴阳转换
        (ResourceType.YIN, ResourceType.YANG): 1.0,
        (ResourceType.YANG, ResourceType.YIN): 1.0,
        
        # 特殊资源转换
        (ResourceType.WISDOM, ResourceType.INFLUENCE): 0.8,
        (ResourceType.INFLUENCE, ResourceType.WISDOM): 1.2,
    }
    
    # 资源价值权重（用于AI评估）
    RESOURCE_VALUES: Final[Dict[ResourceType, float]] = {
        ResourceType.GOLD: 1.0,
        ResourceType.WOOD: 1.0,
        ResourceType.WATER: 1.0,
        ResourceType.FIRE: 1.0,
        ResourceType.EARTH: 1.0,
        ResourceType.YIN: 1.5,
        ResourceType.YANG: 1.5,
        ResourceType.WISDOM: 3.0,
        ResourceType.INFLUENCE: 2.5,
        ResourceType.ACTION_POINTS: 4.0
    }

class YIXUE_CONSTANTS:
    """
    易学系统常量类
    
    定义五行、八卦、阴阳等易学系统的相关常量。
    包括相生相克关系、卦象属性、修为等级等配置。
    """
    
    # 五行相生关系强度
    WUXING_GENERATION_BONUS: Final[float] = 1.2
    WUXING_DESTRUCTION_PENALTY: Final[float] = 0.8
    WUXING_NEUTRAL_MULTIPLIER: Final[float] = 1.0
    
    # 八卦变换成本
    BAGUA_TRANSFORM_COSTS: Final[Dict[BaguaType, Dict[ResourceType, int]]] = {
        BaguaType.QIAN: {ResourceType.GOLD: 3, ResourceType.YANG: 2},
        BaguaType.KUN: {ResourceType.EARTH: 3, ResourceType.YIN: 2},
        BaguaType.ZHEN: {ResourceType.WOOD: 3, ResourceType.YANG: 1},
        BaguaType.XUN: {ResourceType.WOOD: 2, ResourceType.YIN: 1},
        BaguaType.KAN: {ResourceType.WATER: 3, ResourceType.YIN: 2},
        BaguaType.LI: {ResourceType.FIRE: 3, ResourceType.YANG: 2},
        BaguaType.GEN: {ResourceType.EARTH: 2, ResourceType.YANG: 1},
        BaguaType.DUI: {ResourceType.GOLD: 2, ResourceType.YIN: 1},
    }
    
    # 八卦效果加成
    BAGUA_EFFECTS: Final[Dict[BaguaType, Dict[str, float]]] = {
        BaguaType.QIAN: {"leadership": 1.3, "creativity": 1.2, "authority": 1.4},
        BaguaType.KUN: {"support": 1.4, "nurturing": 1.3, "stability": 1.2},
        BaguaType.ZHEN: {"action": 1.3, "movement": 1.4, "initiative": 1.2},
        BaguaType.XUN: {"flexibility": 1.3, "penetration": 1.2, "adaptation": 1.4},
        BaguaType.KAN: {"wisdom": 1.4, "danger_sense": 1.3, "flow": 1.2},
        BaguaType.LI: {"clarity": 1.3, "beauty": 1.2, "illumination": 1.4},
        BaguaType.GEN: {"stability": 1.4, "meditation": 1.3, "stopping": 1.2},
        BaguaType.DUI: {"joy": 1.2, "communication": 1.4, "exchange": 1.3},
    }
    
    # 修为等级突破需求
    CULTIVATION_BREAKTHROUGH_REQUIREMENTS: Final[Dict[CultivationLevel, Dict[str, Any]]] = {
        CultivationLevel.QI_REFINING: {
            "resources": {ResourceType.WISDOM: 10, ResourceType.YIN: 5, ResourceType.YANG: 5},
            "time": 3,
            "success_rate": 0.9
        },
        CultivationLevel.FOUNDATION: {
            "resources": {ResourceType.WISDOM: 25, ResourceType.INFLUENCE: 10},
            "time": 5,
            "success_rate": 0.8
        },
        CultivationLevel.GOLDEN_CORE: {
            "resources": {ResourceType.WISDOM: 50, ResourceType.INFLUENCE: 25},
            "time": 8,
            "success_rate": 0.7
        },
        CultivationLevel.NASCENT_SOUL: {
            "resources": {ResourceType.WISDOM: 100, ResourceType.INFLUENCE: 50},
            "time": 12,
            "success_rate": 0.6
        },
        CultivationLevel.SPIRIT_TRANSFORM: {
            "resources": {ResourceType.WISDOM: 200, ResourceType.INFLUENCE: 100},
            "time": 15,
            "success_rate": 0.5
        },
    }
    
    # 阴阳平衡效果
    YINYANG_BALANCE_EFFECTS: Final[Dict[str, Tuple[float, float]]] = {
        # (阴性效果, 阳性效果)
        "defense": (1.3, 0.8),      # 阴性增强防御，阳性减弱防御
        "attack": (0.8, 1.3),       # 阳性增强攻击，阴性减弱攻击
        "wisdom": (1.2, 1.0),       # 阴性略微增强智慧
        "action": (0.9, 1.2),       # 阳性增强行动力
        "meditation": (1.4, 0.7),   # 阴性大幅增强冥想效果
        "influence": (1.0, 1.3),    # 阳性增强影响力
    }

class UI_CONSTANTS:
    """
    界面相关常量类
    
    定义用户界面的各种常量，包括颜色、尺寸、动画等配置。
    """
    
    # 颜色配置
    COLORS: Final[Dict[str, str]] = {
        # 五行颜色
        "gold": "#FFD700",
        "wood": "#228B22",
        "water": "#4169E1",
        "fire": "#DC143C",
        "earth": "#8B4513",
        
        # 阴阳颜色
        "yin": "#2F4F4F",
        "yang": "#F5DEB3",
        
        # 界面颜色
        "background": "#1a1a1a",
        "primary": "#4a90e2",
        "secondary": "#7ed321",
        "accent": "#f5a623",
        "warning": "#d0021b",
        "success": "#50e3c2",
        "text": "#ffffff",
        "text_secondary": "#cccccc",
    }
    
    # 字体大小
    FONT_SIZES: Final[Dict[str, int]] = {
        "small": 12,
        "normal": 14,
        "large": 16,
        "title": 20,
        "header": 24,
        "display": 32,
    }
    
    # 动画时间（毫秒）
    ANIMATION_DURATIONS: Final[Dict[str, int]] = {
        "fast": 200,
        "normal": 400,
        "slow": 800,
        "card_flip": 600,
        "resource_change": 300,
        "phase_transition": 1000,
    }
    
    # 界面尺寸
    DIMENSIONS: Final[Dict[str, int]] = {
        "card_width": 120,
        "card_height": 180,
        "button_height": 40,
        "panel_width": 300,
        "sidebar_width": 250,
        "header_height": 60,
    }

class ACTION_CONSTANTS:
    """
    行动相关常量类
    
    定义各种行动的成本、效果、冷却时间等参数。
    """
    
    # 行动基础成本
    ACTION_COSTS: Final[Dict[ActionType, Dict[ResourceType, int]]] = {
        ActionType.MOVE: {ResourceType.ACTION_POINTS: 1},
        ActionType.ATTACK: {ResourceType.ACTION_POINTS: 2, ResourceType.YANG: 1},
        ActionType.DEFEND: {ResourceType.ACTION_POINTS: 1, ResourceType.YIN: 1},
        ActionType.MEDITATE: {ResourceType.ACTION_POINTS: 1},
        ActionType.DIVINATION: {ResourceType.ACTION_POINTS: 2, ResourceType.WISDOM: 5},
        ActionType.PLAY_CARD: {ResourceType.ACTION_POINTS: 1},
        ActionType.TRANSFORM: {ResourceType.ACTION_POINTS: 3, ResourceType.WISDOM: 10},
        ActionType.SPECIAL: {ResourceType.ACTION_POINTS: 2},
    }
    
    # 行动成功率
    ACTION_SUCCESS_RATES: Final[Dict[ActionType, float]] = {
        ActionType.MOVE: 1.0,
        ActionType.ATTACK: 0.8,
        ActionType.DEFEND: 0.9,
        ActionType.MEDITATE: 0.95,
        ActionType.DIVINATION: 0.7,
        ActionType.PLAY_CARD: 0.9,
        ActionType.TRANSFORM: 0.6,
        ActionType.SPECIAL: 0.75,
    }
    
    # 行动冷却时间（回合）
    ACTION_COOLDOWNS: Final[Dict[ActionType, int]] = {
        ActionType.MOVE: 0,
        ActionType.ATTACK: 1,
        ActionType.DEFEND: 0,
        ActionType.MEDITATE: 2,
        ActionType.DIVINATION: 3,
        ActionType.PLAY_CARD: 0,
        ActionType.TRANSFORM: 5,
        ActionType.SPECIAL: 3,
    }

class BALANCE_CONSTANTS:
    """
    游戏平衡常量类
    
    定义游戏平衡相关的参数，用于调整游戏难度和公平性。
    """
    
    # 经验值获取倍率
    EXPERIENCE_MULTIPLIERS: Final[Dict[str, float]] = {
        "victory": 2.0,
        "defeat": 0.5,
        "draw": 1.0,
        "early_game": 1.2,
        "late_game": 0.8,
        "perfect_play": 1.5,
    }
    
    # AI难度调整
    AI_DIFFICULTY_MODIFIERS: Final[Dict[str, Dict[str, float]]] = {
        "easy": {
            "resource_bonus": 0.8,
            "action_efficiency": 0.7,
            "decision_quality": 0.6,
        },
        "normal": {
            "resource_bonus": 1.0,
            "action_efficiency": 1.0,
            "decision_quality": 1.0,
        },
        "hard": {
            "resource_bonus": 1.2,
            "action_efficiency": 1.3,
            "decision_quality": 1.4,
        },
        "expert": {
            "resource_bonus": 1.5,
            "action_efficiency": 1.6,
            "decision_quality": 1.8,
        },
    }
    
    # 随机事件概率
    RANDOM_EVENT_PROBABILITIES: Final[Dict[str, float]] = {
        "positive_event": 0.15,
        "negative_event": 0.10,
        "neutral_event": 0.05,
        "rare_event": 0.02,
        "legendary_event": 0.005,
    }
    
    # 资源稀缺度调整
    RESOURCE_SCARCITY: Final[Dict[ResourceType, float]] = {
        ResourceType.GOLD: 1.0,
        ResourceType.WOOD: 1.0,
        ResourceType.WATER: 1.0,
        ResourceType.FIRE: 1.0,
        ResourceType.EARTH: 1.0,
        ResourceType.YIN: 1.2,
        ResourceType.YANG: 1.2,
        ResourceType.WISDOM: 2.0,
        ResourceType.INFLUENCE: 1.5,
        ResourceType.ACTION_POINTS: 3.0,
    }

class MESSAGE_CONSTANTS:
    """
    消息和文本常量类
    
    定义游戏中使用的各种消息模板和文本常量。
    """
    
    # 系统消息模板
    SYSTEM_MESSAGES: Final[Dict[str, str]] = {
        "game_start": "天机变游戏开始！愿智慧与你同在。",
        "game_end": "游戏结束！{winner} 获得了最终的胜利。",
        "round_start": "第 {round} 回合开始",
        "phase_change": "游戏阶段转换：{old_phase} → {new_phase}",
        "player_turn": "轮到 {player} 行动",
        "action_success": "{player} 成功执行了 {action}",
        "action_failed": "{player} 执行 {action} 失败：{reason}",
        "resource_gained": "{player} 获得了 {amount} {resource}",
        "resource_lost": "{player} 失去了 {amount} {resource}",
        "cultivation_breakthrough": "恭喜 {player} 突破到 {level}！",
        "bagua_transform": "{player} 变换八卦为 {bagua}",
    }
    
    # 错误消息
    ERROR_MESSAGES: Final[Dict[str, str]] = {
        "insufficient_resources": "资源不足，无法执行此操作",
        "invalid_action": "无效的行动类型",
        "action_on_cooldown": "此行动正在冷却中",
        "game_not_started": "游戏尚未开始",
        "game_already_ended": "游戏已经结束",
        "player_not_found": "找不到指定的玩家",
        "invalid_position": "无效的位置坐标",
        "permission_denied": "权限不足",
    }
    
    # 帮助文本
    HELP_TEXTS: Final[Dict[str, str]] = {
        "move": "移动到相邻的位置，消耗1行动点",
        "attack": "攻击目标，消耗2行动点和1阳气",
        "defend": "进入防御姿态，消耗1行动点和1阴气",
        "meditate": "冥想恢复资源，消耗1行动点",
        "divination": "占卜获取信息，消耗2行动点和5智慧",
        "transform": "变换八卦状态，消耗3行动点和10智慧",
    }

# ==================== 导出列表 ====================

__all__ = [
    'GAME_CONSTANTS',
    'RESOURCE_CONSTANTS',
    'YIXUE_CONSTANTS',
    'UI_CONSTANTS',
    'ACTION_CONSTANTS',
    'BALANCE_CONSTANTS',
    'MESSAGE_CONSTANTS',
]