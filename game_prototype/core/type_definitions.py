"""
类型定义模块
定义项目中使用的所有自定义类型，确保类型安全
"""

from typing import (
    Dict, List, Optional, Any, Union, Tuple, Set, Callable, 
    TypeVar, Generic, Protocol, runtime_checkable, Literal,
    Awaitable, AsyncIterator, Iterator, NamedTuple
)
from typing_extensions import TypedDict, NotRequired
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import time

# ==================== 基础类型别名 ====================

# 基础数据类型
PlayerId = str
SessionId = str
ActionId = str
EventId = str
ResourceAmount = int
Timestamp = float
Duration = float

# 位置相关类型
Coordinate = int
BoardSize = int
Distance = float

# 游戏相关类型
TurnNumber = int
Score = int
Level = int

# ==================== 泛型类型变量 ====================

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

PlayerType = TypeVar('PlayerType', bound='IPlayer')
ActionType = TypeVar('ActionType', bound='IGameAction')
StateType = TypeVar('StateType', bound='IGameState')

# ==================== 协议定义 ====================

@runtime_checkable
class Serializable(Protocol):
    """可序列化协议"""
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        ...
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Serializable':
        """从字典创建对象"""
        ...

@runtime_checkable
class Validatable(Protocol):
    """可验证协议"""
    
    def validate(self) -> 'ValidationResult':
        """验证对象"""
        ...

@runtime_checkable
class Configurable(Protocol):
    """可配置协议"""
    
    def configure(self, config: Dict[str, Any]) -> None:
        """配置对象"""
        ...
    
    def get_config(self) -> Dict[str, Any]:
        """获取配置"""
        ...

@runtime_checkable
class Observable(Protocol):
    """可观察协议"""
    
    def add_observer(self, observer: 'Observer') -> None:
        """添加观察者"""
        ...
    
    def remove_observer(self, observer: 'Observer') -> None:
        """移除观察者"""
        ...
    
    def notify_observers(self, event: Any) -> None:
        """通知观察者"""
        ...

@runtime_checkable
class Observer(Protocol):
    """观察者协议"""
    
    def update(self, observable: Observable, event: Any) -> None:
        """更新通知"""
        ...

# ==================== TypedDict 定义 ====================

class PlayerData(TypedDict):
    """玩家数据类型"""
    id: PlayerId
    name: str
    type: str
    avatar: str
    resources: Dict[str, ResourceAmount]
    cultivation_realm: str
    yin: int
    yang: int
    wuxing_mastery: Dict[str, int]
    bagua_affinity: Dict[str, int]
    position: Dict[str, Coordinate]
    is_active: bool
    stats: 'PlayerStatsData'

class PlayerStatsData(TypedDict):
    """玩家统计数据类型"""
    games_played: int
    games_won: int
    total_actions: int
    successful_actions: int
    average_game_duration: Duration
    win_rate: float
    success_rate: float

class ActionData(TypedDict):
    """行动数据类型"""
    action_id: ActionId
    player_id: PlayerId
    action_type: str
    description: str
    timestamp: Timestamp
    cost: 'ActionCostData'
    effect: 'ActionEffectData'
    metadata: Dict[str, Any]

class ActionCostData(TypedDict):
    """行动成本数据类型"""
    resources: Dict[str, ResourceAmount]
    energy: int
    time: Duration

class ActionEffectData(TypedDict):
    """行动效果数据类型"""
    resource_changes: Dict[str, int]
    attribute_changes: Dict[str, Union[int, float]]
    status_effects: List[str]
    duration: Duration

class GameStateData(TypedDict):
    """游戏状态数据类型"""
    session_id: SessionId
    players: Dict[PlayerId, PlayerData]
    board: 'BoardData'
    game_phase: str
    current_turn: NotRequired['TurnData']
    turn_order: List[PlayerId]
    start_time: Timestamp
    end_time: NotRequired[Timestamp]
    winner: NotRequired[PlayerId]
    statistics: 'GameStatisticsData'

class BoardData(TypedDict):
    """棋盘数据类型"""
    size: BoardSize
    cells: Dict[str, 'CellData']

class CellData(TypedDict):
    """格子数据类型"""
    position: Dict[str, Coordinate]
    terrain_type: str
    piece: NotRequired[str]
    owner: NotRequired[PlayerId]
    special_effects: List[str]
    wuxing_element: NotRequired[str]
    bagua_type: NotRequired[str]

class TurnData(TypedDict):
    """回合数据类型"""
    turn_number: TurnNumber
    current_player_id: PlayerId
    phase: str
    start_time: Timestamp
    time_limit: Duration
    remaining_time: Duration
    actions_performed: List[ActionId]

class GameStatisticsData(TypedDict):
    """游戏统计数据类型"""
    game_duration: Duration
    total_turns: TurnNumber
    total_actions: int
    player_stats: Dict[PlayerId, 'PlayerGameStatsData']

class PlayerGameStatsData(TypedDict):
    """玩家游戏统计数据类型"""
    name: str
    total_actions: int
    successful_actions: int
    controlled_cells: int
    cultivation_realm: int
    resources: Dict[str, ResourceAmount]

class ConfigData(TypedDict):
    """配置数据类型"""
    basic: 'BasicConfigData'
    yixue: 'YixueConfigData'
    ai: 'AIConfigData'
    ui: 'UIConfigData'
    balance: 'BalanceConfigData'

class BasicConfigData(TypedDict):
    """基础配置数据类型"""
    max_players: int
    board_size: BoardSize
    turn_time_limit: Duration
    max_turns: TurnNumber
    debug_mode: bool
    initial_resources: Dict[str, ResourceAmount]

class YixueConfigData(TypedDict):
    """易学配置数据类型"""
    initial_yin: int
    initial_yang: int
    max_yin_yang: int
    wuxing_interaction_bonus: float
    bagua_prediction_accuracy: float
    cultivation_difficulty: float

class AIConfigData(TypedDict):
    """AI配置数据类型"""
    enabled: bool
    difficulty: str
    thinking_time: Duration
    strategy_weights: Dict[str, float]

class UIConfigData(TypedDict):
    """UI配置数据类型"""
    theme: str
    language: str
    animation_speed: float
    sound_enabled: bool
    auto_save_interval: Duration

class BalanceConfigData(TypedDict):
    """平衡性配置数据类型"""
    resource_generation_rate: Dict[str, float]
    action_cost_multiplier: float
    cultivation_speed_multiplier: float
    victory_condition_thresholds: Dict[str, Union[int, float]]

class EventData(TypedDict):
    """事件数据类型"""
    event_id: EventId
    event_type: str
    timestamp: Timestamp
    source: str
    target: NotRequired[str]
    data: Dict[str, Any]
    priority: str

class ValidationResultData(TypedDict):
    """验证结果数据类型"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    metadata: Dict[str, Any]

class ActionResultData(TypedDict):
    """行动结果数据类型"""
    success: bool
    message: str
    data: Dict[str, Any]
    effects: List['EffectData']

class EffectData(TypedDict):
    """效果数据类型"""
    effect_type: str
    target: str
    value: Union[int, float, str]
    duration: Duration
    metadata: Dict[str, Any]

# ==================== 回调函数类型 ====================

# 事件处理器类型
EventHandler = Callable[['GameEvent'], Awaitable[None]]
EventFilter = Callable[['GameEvent'], bool]

# 验证器类型
Validator = Callable[[Any], 'ValidationResult']
AsyncValidator = Callable[[Any], Awaitable['ValidationResult']]

# 配置处理器类型
ConfigProcessor = Callable[[Dict[str, Any]], Dict[str, Any]]
ConfigValidator = Callable[[Dict[str, Any]], bool]

# 游戏逻辑处理器类型
ActionProcessor = Callable[['IGameAction', 'IGameState'], 'ActionResult']
StateUpdater = Callable[['IGameState', 'ActionResult'], None]

# AI相关类型
AIStrategy = Callable[['IGameState', PlayerId], 'IGameAction']
AIEvaluator = Callable[['IGameState', PlayerId], float]

# UI回调类型
UIUpdateCallback = Callable[[Dict[str, Any]], None]
UserInputHandler = Callable[[str, Dict[str, Any]], Any]

# ==================== 复合类型 ====================

# 资源类型映射
ResourceMap = Dict[str, ResourceAmount]
ResourceCost = Dict[str, ResourceAmount]
ResourceChange = Dict[str, int]

# 位置相关类型
PositionTuple = Tuple[Coordinate, Coordinate]
PositionList = List['Position']
PositionSet = Set['Position']

# 玩家相关类型
PlayerList = List['Player']
PlayerDict = Dict[PlayerId, 'Player']
PlayerSet = Set['Player']

# 行动相关类型
ActionList = List['IGameAction']
ActionDict = Dict[ActionId, 'IGameAction']
ActionQueue = List['IGameAction']

# 事件相关类型
EventList = List['GameEvent']
EventDict = Dict[EventId, 'GameEvent']
EventQueue = List['GameEvent']

# 配置相关类型
ConfigDict = Dict[str, Any]
ConfigSection = Dict[str, Union[str, int, float, bool, List[Any], Dict[str, Any]]]

# 统计相关类型
StatisticsDict = Dict[str, Union[int, float, str]]
MetricsDict = Dict[str, Union[int, float]]

# ==================== 枚举类型扩展 ====================

class Priority(Enum):
    """优先级枚举"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class LogLevel(Enum):
    """日志级别枚举"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class NetworkStatus(Enum):
    """网络状态枚举"""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    ERROR = "error"

class GameMode(Enum):
    """游戏模式枚举"""
    SINGLE_PLAYER = "single_player"
    MULTI_PLAYER = "multi_player"
    AI_VS_AI = "ai_vs_ai"
    TUTORIAL = "tutorial"
    PRACTICE = "practice"

class Difficulty(Enum):
    """难度枚举"""
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"
    EXPERT = "expert"

# ==================== 命名元组 ====================

class GameMetrics(NamedTuple):
    """游戏指标"""
    total_games: int
    total_players: int
    average_game_duration: Duration
    most_popular_action: str
    highest_score: Score

class PerformanceMetrics(NamedTuple):
    """性能指标"""
    cpu_usage: float
    memory_usage: float
    response_time: Duration
    throughput: float

class NetworkMetrics(NamedTuple):
    """网络指标"""
    latency: Duration
    bandwidth: float
    packet_loss: float
    connection_count: int

# ==================== 泛型类定义 ====================

class Result(Generic[T]):
    """结果类型"""
    
    def __init__(self, success: bool, value: Optional[T] = None, error: Optional[str] = None):
        self.success = success
        self.value = value
        self.error = error
    
    def is_success(self) -> bool:
        return self.success
    
    def is_error(self) -> bool:
        return not self.success
    
    def get_value(self) -> T:
        if not self.success:
            raise ValueError(f"Result is error: {self.error}")
        return self.value
    
    def get_error(self) -> str:
        if self.success:
            raise ValueError("Result is success, no error")
        return self.error

class Cache(Generic[K, V]):
    """缓存类型"""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self._cache: Dict[K, Tuple[V, Timestamp]] = {}
    
    def get(self, key: K) -> Optional[V]:
        if key in self._cache:
            value, timestamp = self._cache[key]
            return value
        return None
    
    def put(self, key: K, value: V) -> None:
        if len(self._cache) >= self.max_size:
            # 简单的LRU实现
            oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k][1])
            del self._cache[oldest_key]
        
        self._cache[key] = (value, time.time())
    
    def clear(self) -> None:
        self._cache.clear()

class EventEmitter(Generic[T]):
    """事件发射器"""
    
    def __init__(self):
        self._listeners: List[Callable[[T], None]] = []
    
    def on(self, listener: Callable[[T], None]) -> None:
        self._listeners.append(listener)
    
    def off(self, listener: Callable[[T], None]) -> None:
        if listener in self._listeners:
            self._listeners.remove(listener)
    
    def emit(self, event: T) -> None:
        for listener in self._listeners:
            try:
                listener(event)
            except Exception as e:
                # 记录错误但不中断其他监听器
                print(f"Error in event listener: {e}")

# ==================== 工厂类型 ====================

class Factory(Generic[T], ABC):
    """抽象工厂"""
    
    @abstractmethod
    def create(self, *args, **kwargs) -> T:
        """创建对象"""
        pass

class Singleton(Generic[T]):
    """单例模式"""
    
    _instances: Dict[type, Any] = {}
    
    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]

# ==================== 装饰器类型 ====================

# 方法装饰器类型
MethodDecorator = Callable[[Callable[..., T]], Callable[..., T]]
AsyncMethodDecorator = Callable[[Callable[..., Awaitable[T]]], Callable[..., Awaitable[T]]]

# 类装饰器类型
ClassDecorator = Callable[[type], type]

# 属性装饰器类型
PropertyDecorator = Callable[[Callable[..., T]], property]

# ==================== 上下文管理器类型 ====================

class GameContext(Protocol):
    """游戏上下文协议"""
    
    def __enter__(self) -> 'GameContext':
        ...
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        ...

class AsyncGameContext(Protocol):
    """异步游戏上下文协议"""
    
    async def __aenter__(self) -> 'AsyncGameContext':
        ...
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        ...

# ==================== 字面量类型 ====================

# 游戏阶段字面量
GamePhaseLiteral = Literal["setup", "playing", "paused", "ended"]

# 回合阶段字面量
TurnPhaseLiteral = Literal["start", "action", "resolution", "end"]

# 行动类型字面量
ActionTypeLiteral = Literal[
    "move", "place_piece", "cultivate", "cast_spell", 
    "trade", "breakthrough", "pass", "surrender"
]

# 资源类型字面量
ResourceTypeLiteral = Literal["culture", "wisdom", "influence", "energy"]

# 五行元素字面量
WuxingElementLiteral = Literal["wood", "fire", "earth", "metal", "water"]

# 八卦类型字面量
BaguaTypeLiteral = Literal[
    "qian", "kun", "zhen", "xun", "kan", "li", "gen", "dui"
]

# 修为境界字面量
CultivationRealmLiteral = Literal[
    "mortal", "qi_refining", "foundation", "core_formation",
    "nascent_soul", "spirit_transformation", "void_refinement", 
    "body_integration", "mahayana", "transcendence"
]

# ==================== 类型守卫函数 ====================

def is_player_data(obj: Any) -> bool:
    """检查是否为玩家数据"""
    if not isinstance(obj, dict):
        return False
    
    required_keys = {"id", "name", "type", "resources", "cultivation_realm"}
    return all(key in obj for key in required_keys)

def is_action_data(obj: Any) -> bool:
    """检查是否为行动数据"""
    if not isinstance(obj, dict):
        return False
    
    required_keys = {"action_id", "player_id", "action_type", "timestamp"}
    return all(key in obj for key in required_keys)

def is_game_state_data(obj: Any) -> bool:
    """检查是否为游戏状态数据"""
    if not isinstance(obj, dict):
        return False
    
    required_keys = {"session_id", "players", "board", "game_phase"}
    return all(key in obj for key in required_keys)

# ==================== 类型转换函数 ====================

def to_player_id(value: Any) -> PlayerId:
    """转换为玩家ID"""
    if isinstance(value, str):
        return value
    raise TypeError(f"Cannot convert {type(value)} to PlayerId")

def to_resource_amount(value: Any) -> ResourceAmount:
    """转换为资源数量"""
    if isinstance(value, int) and value >= 0:
        return value
    raise TypeError(f"Cannot convert {type(value)} to ResourceAmount")

def to_coordinate(value: Any) -> Coordinate:
    """转换为坐标"""
    if isinstance(value, int) and value >= 0:
        return value
    raise TypeError(f"Cannot convert {type(value)} to Coordinate")

# ==================== 类型别名导出 ====================

__all__ = [
    # 基础类型别名
    'PlayerId', 'SessionId', 'ActionId', 'EventId', 'ResourceAmount',
    'Timestamp', 'Duration', 'Coordinate', 'BoardSize', 'Distance',
    'TurnNumber', 'Score', 'Level',
    
    # 泛型类型变量
    'T', 'K', 'V', 'PlayerType', 'ActionType', 'StateType',
    
    # 协议
    'Serializable', 'Validatable', 'Configurable', 'Observable', 'Observer',
    
    # TypedDict
    'PlayerData', 'PlayerStatsData', 'ActionData', 'ActionCostData',
    'ActionEffectData', 'GameStateData', 'BoardData', 'CellData',
    'TurnData', 'GameStatisticsData', 'PlayerGameStatsData',
    'ConfigData', 'BasicConfigData', 'YixueConfigData', 'AIConfigData',
    'UIConfigData', 'BalanceConfigData', 'EventData', 'ValidationResultData',
    'ActionResultData', 'EffectData',
    
    # 回调函数类型
    'EventHandler', 'EventFilter', 'Validator', 'AsyncValidator',
    'ConfigProcessor', 'ConfigValidator', 'ActionProcessor', 'StateUpdater',
    'AIStrategy', 'AIEvaluator', 'UIUpdateCallback', 'UserInputHandler',
    
    # 复合类型
    'ResourceMap', 'ResourceCost', 'ResourceChange', 'PositionTuple',
    'PositionList', 'PositionSet', 'PlayerList', 'PlayerDict', 'PlayerSet',
    'ActionList', 'ActionDict', 'ActionQueue', 'EventList', 'EventDict',
    'EventQueue', 'ConfigDict', 'ConfigSection', 'StatisticsDict', 'MetricsDict',
    
    # 枚举
    'Priority', 'LogLevel', 'NetworkStatus', 'GameMode', 'Difficulty',
    
    # 命名元组
    'GameMetrics', 'PerformanceMetrics', 'NetworkMetrics',
    
    # 泛型类
    'Result', 'Cache', 'EventEmitter', 'Factory', 'Singleton',
    
    # 装饰器类型
    'MethodDecorator', 'AsyncMethodDecorator', 'ClassDecorator', 'PropertyDecorator',
    
    # 上下文管理器
    'GameContext', 'AsyncGameContext',
    
    # 字面量类型
    'GamePhaseLiteral', 'TurnPhaseLiteral', 'ActionTypeLiteral',
    'ResourceTypeLiteral', 'WuxingElementLiteral', 'BaguaTypeLiteral',
    'CultivationRealmLiteral',
    
    # 类型守卫和转换函数
    'is_player_data', 'is_action_data', 'is_game_state_data',
    'to_player_id', 'to_resource_amount', 'to_coordinate'
]