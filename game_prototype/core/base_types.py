"""
天机变游戏基础类型定义

统一管理所有枚举类型和数据结构，为游戏系统提供类型安全的基础。
包含游戏阶段、玩家类型、行动类型、资源类型、易学系统相关类型等。

主要组件：
- 游戏基础枚举：GamePhase, PlayerType, ActionType, ResourceType
- 易学系统枚举：WuxingElement, BaguaType, YinyangType, CultivationLevel
- 数据结构：Position, ActionResult, GameState, PlayerState
- 工厂函数：create_default_position, create_empty_action_result

作者: 游戏开发团队
版本: 1.0.0
"""

from enum import Enum, auto, IntEnum
from typing import Dict, List, Optional, Any, Union, Tuple, NamedTuple, TypeVar, Generic
from dataclasses import dataclass, field
import uuid
from datetime import datetime

# 类型变量
T = TypeVar('T')
StateType = TypeVar('StateType')

# ==================== 游戏基础枚举 ====================

class GamePhase(Enum):
    """
    游戏阶段枚举
    
    定义游戏进行的各个阶段，用于控制游戏流程和状态转换。
    每个阶段都有特定的规则和允许的操作。
    """
    SETUP = "设置阶段"      # 游戏初始化，玩家准备
    MAIN = "主要阶段"       # 主要游戏阶段，大部分操作发生在此
    ACTION = "行动阶段"     # 玩家执行行动
    RESOLUTION = "结算阶段"  # 行动结果计算和应用
    END = "结束阶段"        # 游戏结束，计算最终结果
    
    def __str__(self) -> str:
        """返回阶段的中文名称"""
        return self.value
    
    @classmethod
    def get_next_phase(cls, current_phase: 'GamePhase') -> 'GamePhase':
        """
        获取下一个游戏阶段
        
        Args:
            current_phase: 当前游戏阶段
            
        Returns:
            GamePhase: 下一个游戏阶段
        """
        phase_order = [cls.SETUP, cls.MAIN, cls.ACTION, cls.RESOLUTION, cls.END]
        try:
            current_index = phase_order.index(current_phase)
            if current_index < len(phase_order) - 1:
                return phase_order[current_index + 1]
            return cls.END
        except ValueError:
            return cls.SETUP

class PlayerType(Enum):
    """
    玩家类型枚举
    
    区分不同类型的游戏参与者，用于确定行为模式和权限。
    """
    HUMAN = "人类玩家"      # 真实玩家
    AI = "AI玩家"          # 人工智能玩家
    OBSERVER = "观察者"     # 观察者，不参与游戏
    
    def __str__(self) -> str:
        """返回玩家类型的中文名称"""
        return self.value
    
    @property
    def is_active_player(self) -> bool:
        """判断是否为活跃玩家（可以执行游戏操作）"""
        return self in (PlayerType.HUMAN, PlayerType.AI)

class ActionType(Enum):
    """
    行动类型枚举
    
    定义玩家可以执行的各种行动类型。
    每种行动类型都有对应的成本和效果。
    """
    MOVE = "移动"           # 移动到新位置
    ATTACK = "攻击"         # 攻击其他玩家或目标
    DEFEND = "防御"         # 防御姿态，提高防御力
    MEDITATE = "冥想"       # 冥想恢复资源
    DIVINATION = "占卜"     # 占卜获取信息
    PLAY_CARD = "出牌"      # 使用卡牌
    TRANSFORM = "变卦"      # 八卦变换
    SPECIAL = "特殊行动"    # 特殊技能或能力
    
    def __str__(self) -> str:
        """返回行动类型的中文名称"""
        return self.value
    
    @property
    def base_cost(self) -> int:
        """获取行动的基础成本"""
        cost_map = {
            ActionType.MOVE: 1,
            ActionType.ATTACK: 2,
            ActionType.DEFEND: 1,
            ActionType.MEDITATE: 1,
            ActionType.DIVINATION: 2,
            ActionType.PLAY_CARD: 1,
            ActionType.TRANSFORM: 3,
            ActionType.SPECIAL: 2,
        }
        return cost_map.get(self, 1)

class ResourceType(Enum):
    """
    资源类型枚举
    
    定义游戏中的各种资源类型。
    资源用于执行行动、购买物品、提升能力等。
    """
    # 五行资源
    GOLD = "金"             # 金属性资源
    WOOD = "木"             # 木属性资源
    WATER = "水"            # 水属性资源
    FIRE = "火"             # 火属性资源
    EARTH = "土"            # 土属性资源
    
    # 阴阳资源
    YIN = "阴气"            # 阴性能量
    YANG = "阳气"           # 阳性能量
    
    # 特殊资源
    WISDOM = "智慧"         # 智慧点数
    INFLUENCE = "影响力"    # 影响力点数
    ACTION_POINTS = "行动点" # 行动点数
    
    def __str__(self) -> str:
        """返回资源类型的中文名称"""
        return self.value
    
    @property
    def is_wuxing_resource(self) -> bool:
        """判断是否为五行资源"""
        return self in (ResourceType.GOLD, ResourceType.WOOD, ResourceType.WATER, 
                       ResourceType.FIRE, ResourceType.EARTH)
    
    @property
    def is_yinyang_resource(self) -> bool:
        """判断是否为阴阳资源"""
        return self in (ResourceType.YIN, ResourceType.YANG)

# ==================== 易学系统枚举 ====================

class WuxingElement(Enum):
    """
    五行元素枚举
    
    传统五行理论的数字化实现，包含相生相克关系。
    用于游戏中的元素系统和平衡机制。
    """
    GOLD = "金"     # 金：收敛、肃杀、坚固
    WOOD = "木"     # 木：生长、条达、仁慈
    WATER = "水"    # 水：润下、智慧、流动
    FIRE = "火"     # 火：炎上、礼仪、光明
    EARTH = "土"    # 土：稼穑、信用、承载
    
    def __str__(self) -> str:
        """返回五行元素的中文名称"""
        return self.value
    
    def generates(self) -> 'WuxingElement':
        """
        获取当前元素相生的元素
        
        五行相生：金生水，水生木，木生火，火生土，土生金
        
        Returns:
            WuxingElement: 被当前元素生成的元素
        """
        generation_map = {
            WuxingElement.GOLD: WuxingElement.WATER,
            WuxingElement.WATER: WuxingElement.WOOD,
            WuxingElement.WOOD: WuxingElement.FIRE,
            WuxingElement.FIRE: WuxingElement.EARTH,
            WuxingElement.EARTH: WuxingElement.GOLD,
        }
        return generation_map[self]
    
    def destroys(self) -> 'WuxingElement':
        """
        获取当前元素相克的元素
        
        五行相克：金克木，木克土，土克水，水克火，火克金
        
        Returns:
            WuxingElement: 被当前元素克制的元素
        """
        destruction_map = {
            WuxingElement.GOLD: WuxingElement.WOOD,
            WuxingElement.WOOD: WuxingElement.EARTH,
            WuxingElement.EARTH: WuxingElement.WATER,
            WuxingElement.WATER: WuxingElement.FIRE,
            WuxingElement.FIRE: WuxingElement.GOLD,
        }
        return destruction_map[self]
    
    def get_relationship(self, other: 'WuxingElement') -> str:
        """
        获取与另一个元素的关系
        
        Args:
            other: 另一个五行元素
            
        Returns:
            str: 关系类型（"相生"、"相克"、"被生"、"被克"、"同类"）
        """
        if self == other:
            return "同类"
        elif self.generates() == other:
            return "相生"
        elif self.destroys() == other:
            return "相克"
        elif other.generates() == self:
            return "被生"
        elif other.destroys() == self:
            return "被克"
        else:
            return "无关"

class BaguaType(Enum):
    """
    八卦类型枚举
    
    传统八卦理论的数字化实现，每个卦象都有特定的属性和含义。
    用于游戏中的策略系统和状态变化。
    """
    QIAN = "乾"     # 乾卦：天，创造力，领导力
    KUN = "坤"      # 坤卦：地，包容性，支持力
    ZHEN = "震"     # 震卦：雷，行动力，震撼力
    XUN = "巽"      # 巽卦：风，渗透力，灵活性
    KAN = "坎"      # 坎卦：水，智慧，危险
    LI = "离"       # 离卦：火，光明，美丽
    GEN = "艮"      # 艮卦：山，稳定，停止
    DUI = "兑"      # 兑卦：泽，喜悦，交流
    
    def __str__(self) -> str:
        """返回八卦的中文名称"""
        return self.value
    
    @property
    def element(self) -> WuxingElement:
        """获取八卦对应的五行元素"""
        element_map = {
            BaguaType.QIAN: WuxingElement.GOLD,
            BaguaType.DUI: WuxingElement.GOLD,
            BaguaType.LI: WuxingElement.FIRE,
            BaguaType.ZHEN: WuxingElement.WOOD,
            BaguaType.XUN: WuxingElement.WOOD,
            BaguaType.KAN: WuxingElement.WATER,
            BaguaType.GEN: WuxingElement.EARTH,
            BaguaType.KUN: WuxingElement.EARTH,
        }
        return element_map[self]
    
    @property
    def yinyang(self) -> str:
        """获取八卦的阴阳属性"""
        yang_guas = {BaguaType.QIAN, BaguaType.ZHEN, BaguaType.KAN, BaguaType.GEN}
        return "阳" if self in yang_guas else "阴"
    
    @property
    def attributes(self) -> Dict[str, Any]:
        """获取八卦的详细属性"""
        attributes_map = {
            BaguaType.QIAN: {"方位": "西北", "季节": "秋冬之交", "特性": "刚健"},
            BaguaType.KUN: {"方位": "西南", "季节": "夏秋之交", "特性": "柔顺"},
            BaguaType.ZHEN: {"方位": "东", "季节": "春", "特性": "动"},
            BaguaType.XUN: {"方位": "东南", "季节": "春夏之交", "特性": "入"},
            BaguaType.KAN: {"方位": "北", "季节": "冬", "特性": "陷"},
            BaguaType.LI: {"方位": "南", "季节": "夏", "特性": "丽"},
            BaguaType.GEN: {"方位": "东北", "季节": "冬春之交", "特性": "止"},
            BaguaType.DUI: {"方位": "西", "季节": "秋", "特性": "悦"},
        }
        return attributes_map[self]

class YinyangType(Enum):
    """
    阴阳类型枚举
    
    阴阳理论的数字化实现，表示对立统一的两种基本力量。
    用于游戏中的平衡系统和能量管理。
    """
    YIN = "阴"      # 阴：柔、静、暗、冷、下
    YANG = "阳"     # 阳：刚、动、明、热、上
    
    def __str__(self) -> str:
        """返回阴阳类型的中文名称"""
        return self.value
    
    def opposite(self) -> 'YinyangType':
        """获取相对的阴阳类型"""
        return YinyangType.YANG if self == YinyangType.YIN else YinyangType.YIN
    
    @property
    def characteristics(self) -> List[str]:
        """获取阴阳特征"""
        if self == YinyangType.YIN:
            return ["柔", "静", "暗", "冷", "下", "内", "收"]
        else:
            return ["刚", "动", "明", "热", "上", "外", "放"]

class CultivationLevel(IntEnum):
    """
    修为等级枚举
    
    修仙体系的等级划分，使用IntEnum便于比较大小。
    数值越大表示修为越高。
    """
    MORTAL = 0          # 凡人
    QI_REFINING = 1     # 练气期
    FOUNDATION = 2      # 筑基期
    GOLDEN_CORE = 3     # 金丹期
    NASCENT_SOUL = 4    # 元婴期
    SPIRIT_TRANSFORM = 5 # 化神期
    VOID_REFINING = 6   # 炼虚期
    BODY_INTEGRATION = 7 # 合体期
    MAHAYANA = 8        # 大乘期
    TRIBULATION = 9     # 渡劫期
    
    def __str__(self) -> str:
        """返回修为等级的中文名称"""
        names = {
            0: "凡人", 1: "练气期", 2: "筑基期", 3: "金丹期", 4: "元婴期",
            5: "化神期", 6: "炼虚期", 7: "合体期", 8: "大乘期", 9: "渡劫期"
        }
        return names[self.value]
    
    @property
    def power_multiplier(self) -> float:
        """获取修为等级对应的力量倍数"""
        return 1.0 + (self.value * 0.5)
    
    @property
    def breakthrough_difficulty(self) -> float:
        """获取突破到下一级的难度系数"""
        return 1.0 + (self.value * 0.3)

# ==================== 数据结构 ====================

@dataclass(frozen=True)
class Position:
    """
    位置数据类
    
    表示游戏中的二维坐标位置，支持基本的位置运算。
    使用frozen=True确保位置不可变。
    """
    x: int
    y: int
    
    def __post_init__(self) -> None:
        """初始化后验证"""
        if not isinstance(self.x, int) or not isinstance(self.y, int):
            raise ValueError("坐标必须是整数")
    
    def distance_to(self, other: 'Position') -> float:
        """
        计算到另一个位置的欧几里得距离
        
        Args:
            other: 目标位置
            
        Returns:
            float: 距离值
        """
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    
    def manhattan_distance_to(self, other: 'Position') -> int:
        """
        计算到另一个位置的曼哈顿距离
        
        Args:
            other: 目标位置
            
        Returns:
            int: 曼哈顿距离
        """
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def move(self, dx: int, dy: int) -> 'Position':
        """
        移动到新位置
        
        Args:
            dx: x轴偏移量
            dy: y轴偏移量
            
        Returns:
            Position: 新位置
        """
        return Position(self.x + dx, self.y + dy)
    
    def is_adjacent_to(self, other: 'Position') -> bool:
        """
        判断是否与另一个位置相邻（8方向）
        
        Args:
            other: 目标位置
            
        Returns:
            bool: 是否相邻
        """
        return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1 and self != other

@dataclass
class ActionResult:
    """
    行动结果数据类
    
    记录行动执行的结果，包括成功状态、效果和消息。
    """
    success: bool
    message: str = ""
    effects: Dict[str, Any] = field(default_factory=dict)
    cost: Dict[ResourceType, int] = field(default_factory=dict)
    rewards: Dict[ResourceType, int] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self) -> None:
        """初始化后处理"""
        if not isinstance(self.success, bool):
            raise ValueError("success必须是布尔值")
        
        # 确保effects、cost、rewards是字典
        if not isinstance(self.effects, dict):
            self.effects = {}
        if not isinstance(self.cost, dict):
            self.cost = {}
        if not isinstance(self.rewards, dict):
            self.rewards = {}
    
    def add_effect(self, key: str, value: Any) -> None:
        """添加效果"""
        self.effects[key] = value
    
    def add_cost(self, resource: ResourceType, amount: int) -> None:
        """添加成本"""
        self.cost[resource] = self.cost.get(resource, 0) + amount
    
    def add_reward(self, resource: ResourceType, amount: int) -> None:
        """添加奖励"""
        self.rewards[resource] = self.rewards.get(resource, 0) + amount
    
    @property
    def net_resource_change(self) -> Dict[ResourceType, int]:
        """计算净资源变化（奖励 - 成本）"""
        all_resources = set(self.cost.keys()) | set(self.rewards.keys())
        return {
            resource: self.rewards.get(resource, 0) - self.cost.get(resource, 0)
            for resource in all_resources
        }

@dataclass
class GameState:
    """
    游戏状态数据类
    
    记录游戏的当前状态，包括阶段、回合、玩家等信息。
    """
    phase: GamePhase = GamePhase.SETUP
    round_number: int = 1
    current_player_id: Optional[str] = None
    active_players: List[str] = field(default_factory=list)
    game_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    start_time: datetime = field(default_factory=datetime.now)
    last_update: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self) -> None:
        """初始化后验证"""
        if self.round_number < 1:
            raise ValueError("回合数必须大于0")
        
        if not isinstance(self.active_players, list):
            self.active_players = []
    
    def advance_round(self) -> None:
        """推进到下一回合"""
        self.round_number += 1
        self.last_update = datetime.now()
    
    def set_phase(self, new_phase: GamePhase) -> None:
        """设置游戏阶段"""
        self.phase = new_phase
        self.last_update = datetime.now()
    
    def add_player(self, player_id: str) -> None:
        """添加玩家"""
        if player_id not in self.active_players:
            self.active_players.append(player_id)
            self.last_update = datetime.now()
    
    def remove_player(self, player_id: str) -> None:
        """移除玩家"""
        if player_id in self.active_players:
            self.active_players.remove(player_id)
            if self.current_player_id == player_id:
                self.current_player_id = None
            self.last_update = datetime.now()
    
    @property
    def player_count(self) -> int:
        """获取玩家数量"""
        return len(self.active_players)
    
    @property
    def game_duration(self) -> float:
        """获取游戏持续时间（秒）"""
        return (datetime.now() - self.start_time).total_seconds()

@dataclass
class PlayerState:
    """
    玩家状态数据类
    
    记录单个玩家的状态信息，包括资源、位置、属性等。
    """
    player_id: str
    player_type: PlayerType
    position: Position = field(default_factory=lambda: Position(0, 0))
    resources: Dict[ResourceType, int] = field(default_factory=dict)
    cultivation_level: CultivationLevel = CultivationLevel.MORTAL
    wuxing_affinity: Dict[WuxingElement, float] = field(default_factory=dict)
    bagua_state: Optional[BaguaType] = None
    yinyang_balance: float = 0.5  # 0.0=纯阴, 1.0=纯阳, 0.5=平衡
    is_active: bool = True
    last_action_time: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self) -> None:
        """初始化后处理"""
        # 初始化资源
        if not self.resources:
            self.resources = {resource: 0 for resource in ResourceType}
        
        # 初始化五行亲和度
        if not self.wuxing_affinity:
            self.wuxing_affinity = {element: 0.2 for element in WuxingElement}
        
        # 验证阴阳平衡值
        if not 0.0 <= self.yinyang_balance <= 1.0:
            raise ValueError("阴阳平衡值必须在0.0到1.0之间")
    
    def get_resource(self, resource_type: ResourceType) -> int:
        """获取指定资源数量"""
        return self.resources.get(resource_type, 0)
    
    def add_resource(self, resource_type: ResourceType, amount: int) -> None:
        """增加资源"""
        self.resources[resource_type] = self.get_resource(resource_type) + amount
        self.last_action_time = datetime.now()
    
    def consume_resource(self, resource_type: ResourceType, amount: int) -> bool:
        """
        消耗资源
        
        Args:
            resource_type: 资源类型
            amount: 消耗数量
            
        Returns:
            bool: 是否成功消耗
        """
        current_amount = self.get_resource(resource_type)
        if current_amount >= amount:
            self.resources[resource_type] = current_amount - amount
            self.last_action_time = datetime.now()
            return True
        return False
    
    def can_afford(self, costs: Dict[ResourceType, int]) -> bool:
        """检查是否能承担指定成本"""
        return all(
            self.get_resource(resource) >= amount
            for resource, amount in costs.items()
        )
    
    def move_to(self, new_position: Position) -> None:
        """移动到新位置"""
        self.position = new_position
        self.last_action_time = datetime.now()
    
    def set_cultivation_level(self, level: CultivationLevel) -> None:
        """设置修为等级"""
        self.cultivation_level = level
        self.last_action_time = datetime.now()
    
    def adjust_yinyang_balance(self, delta: float) -> None:
        """调整阴阳平衡"""
        self.yinyang_balance = max(0.0, min(1.0, self.yinyang_balance + delta))
        self.last_action_time = datetime.now()
    
    @property
    def dominant_yinyang(self) -> YinyangType:
        """获取主导的阴阳类型"""
        return YinyangType.YANG if self.yinyang_balance > 0.5 else YinyangType.YIN
    
    @property
    def total_resources(self) -> int:
        """获取总资源数量"""
        return sum(self.resources.values())

# ==================== 工厂函数 ====================

def create_default_position() -> Position:
    """创建默认位置（原点）"""
    return Position(0, 0)

def create_empty_action_result() -> ActionResult:
    """创建空的行动结果"""
    return ActionResult(success=False, message="未执行任何行动")

def create_default_game_state() -> GameState:
    """创建默认游戏状态"""
    return GameState()

def create_player_state(player_id: str, player_type: PlayerType) -> PlayerState:
    """
    创建玩家状态
    
    Args:
        player_id: 玩家ID
        player_type: 玩家类型
        
    Returns:
        PlayerState: 新的玩家状态
    """
    return PlayerState(player_id=player_id, player_type=player_type)

# ==================== 类型别名 ====================

# 资源字典类型
ResourceDict = Dict[ResourceType, int]

# 位置元组类型
PositionTuple = Tuple[int, int]

# 玩家ID类型
PlayerId = str

# 游戏ID类型
GameId = str

# 时间戳类型
Timestamp = datetime

# ==================== 导出列表 ====================

__all__ = [
    # 枚举类型
    'GamePhase',
    'PlayerType', 
    'ActionType',
    'ResourceType',
    'WuxingElement',
    'BaguaType',
    'YinyangType',
    'CultivationLevel',
    
    # 数据类
    'Position',
    'ActionResult',
    'GameState',
    'PlayerState',
    
    # 工厂函数
    'create_default_position',
    'create_empty_action_result',
    'create_default_game_state',
    'create_player_state',
    
    # 类型别名
    'ResourceDict',
    'PositionTuple',
    'PlayerId',
    'GameId',
    'Timestamp',
    
    # 类型变量
    'T',
    'StateType',
]