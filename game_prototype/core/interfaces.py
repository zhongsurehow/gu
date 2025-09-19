"""
核心接口定义模块

本模块定义了天机变游戏的核心接口，为游戏的各个组件提供统一的抽象层。
这些接口确保了代码的可扩展性、可测试性和模块间的松耦合。

主要接口包括：
- IPlayer: 玩家接口，定义玩家的基本行为和属性
- IGameAction: 游戏行动接口，定义所有游戏行动的通用结构
- IGameState: 游戏状态接口，管理整个游戏的状态信息
- IGameSystem: 游戏系统接口，定义各种游戏子系统
- IEventBus: 事件总线接口，处理游戏中的事件通信
- IConfigManager: 配置管理接口，管理游戏配置
- IGameFactory: 游戏工厂接口，创建游戏对象

设计原则：
1. 接口隔离：每个接口只包含相关的方法
2. 依赖倒置：高层模块不依赖低层模块，都依赖抽象
3. 开闭原则：对扩展开放，对修改关闭
4. 里氏替换：子类可以替换父类而不影响程序正确性

作者: 天机变开发团队
版本: 1.0.0
创建时间: 2024
"""

from abc import ABC, abstractmethod
from typing import (
    Dict, List, Optional, Any, Union, Tuple, Set, 
    Protocol, runtime_checkable, Callable, Awaitable,
    TypeVar, Generic, Iterator, AsyncIterator
)
from dataclasses import dataclass
from enum import Enum, auto
import time
import asyncio

# 导入基础类型
from .base_types import (
    PlayerId, ActionType, GamePhase, ResourceType, Position,
    GameEvent, ActionResult, ConfigDict, PlayerType, SystemType
)

# 类型变量定义
T = TypeVar('T')
P = TypeVar('P')
R = TypeVar('R')

# ==================== 核心数据结构 ====================

@dataclass
class PlayerInfo:
    """
    玩家信息数据类
    
    包含玩家的基本信息和状态数据。
    
    Attributes:
        player_id: 玩家唯一标识符
        name: 玩家名称
        player_type: 玩家类型（人类/AI）
        level: 玩家等级
        score: 当前得分
        resources: 资源状态
        position: 当前位置
        is_active: 是否活跃
        last_action_time: 最后行动时间
    """
    player_id: PlayerId
    name: str
    player_type: PlayerType
    level: int = 1
    score: int = 0
    resources: Dict[ResourceType, int] = None
    position: Optional[Position] = None
    is_active: bool = True
    last_action_time: Optional[float] = None
    
    def __post_init__(self):
        if self.resources is None:
            self.resources = {}

@dataclass
class SystemInfo:
    """
    系统信息数据类
    
    包含游戏系统的基本信息和状态。
    
    Attributes:
        system_type: 系统类型
        name: 系统名称
        version: 系统版本
        enabled: 是否启用
        priority: 优先级
        dependencies: 依赖的其他系统
        config: 系统配置
    """
    system_type: SystemType
    name: str
    version: str = "1.0.0"
    enabled: bool = True
    priority: int = 0
    dependencies: Set[SystemType] = None
    config: ConfigDict = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = set()
        if self.config is None:
            self.config = {}

# ==================== 核心接口定义 ====================

@runtime_checkable
class IPlayer(Protocol):
    """
    玩家接口
    
    定义所有玩家类型（人类玩家、AI玩家）必须实现的基本方法。
    提供玩家身份识别、行动选择、状态查询等核心功能。
    """
    
    @property
    def player_id(self) -> PlayerId:
        """获取玩家唯一标识符"""
        ...
    
    @property
    def name(self) -> str:
        """获取玩家名称"""
        ...
    
    @property
    def player_type(self) -> PlayerType:
        """获取玩家类型"""
        ...
    
    @property
    def is_active(self) -> bool:
        """检查玩家是否活跃"""
        ...
    
    def get_info(self) -> PlayerInfo:
        """
        获取玩家信息
        
        Returns:
            PlayerInfo: 玩家详细信息
        """
        ...
    
    def choose_action(
        self, 
        game_state: 'IGameState', 
        available_actions: List['IGameAction']
    ) -> Optional['IGameAction']:
        """
        选择要执行的行动
        
        Args:
            game_state: 当前游戏状态
            available_actions: 可用的行动列表
            
        Returns:
            Optional[IGameAction]: 选择的行动，如果没有选择则返回None
        """
        ...
    
    def on_action_result(self, action: 'IGameAction', result: ActionResult) -> None:
        """
        处理行动结果
        
        Args:
            action: 执行的行动
            result: 行动结果
        """
        ...
    
    def on_game_event(self, event: GameEvent) -> None:
        """
        处理游戏事件
        
        Args:
            event: 游戏事件
        """
        ...
    
    def update_state(self, game_state: 'IGameState') -> None:
        """
        更新玩家状态
        
        Args:
            game_state: 当前游戏状态
        """
        ...

@runtime_checkable
class IGameAction(Protocol):
    """
    游戏行动接口
    
    定义所有游戏行动必须实现的基本方法。
    包括行动验证、执行、撤销等核心功能。
    """
    
    @property
    def action_type(self) -> ActionType:
        """获取行动类型"""
        ...
    
    @property
    def player_id(self) -> PlayerId:
        """获取执行行动的玩家ID"""
        ...
    
    @property
    def cost(self) -> Dict[ResourceType, int]:
        """获取行动消耗的资源"""
        ...
    
    @property
    def description(self) -> str:
        """获取行动描述"""
        ...
    
    def can_execute(self, player_id: PlayerId, game_state: 'IGameState') -> bool:
        """
        检查行动是否可以执行
        
        Args:
            player_id: 玩家ID
            game_state: 游戏状态
            
        Returns:
            bool: 是否可以执行
        """
        ...
    
    def execute(self, player_id: PlayerId, game_state: 'IGameState') -> ActionResult:
        """
        执行行动
        
        Args:
            player_id: 玩家ID
            game_state: 游戏状态
            
        Returns:
            ActionResult: 行动执行结果
        """
        ...
    
    def validate(self, player_id: PlayerId, game_state: 'IGameState') -> bool:
        """
        验证行动的合法性
        
        Args:
            player_id: 玩家ID
            game_state: 游戏状态
            
        Returns:
            bool: 是否合法
        """
        ...
    
    def get_preview(self, player_id: PlayerId, game_state: 'IGameState') -> Dict[str, Any]:
        """
        获取行动预览信息
        
        Args:
            player_id: 玩家ID
            game_state: 游戏状态
            
        Returns:
            Dict[str, Any]: 预览信息
        """
        ...

@runtime_checkable
class IGameState(Protocol):
    """
    游戏状态接口
    
    管理整个游戏的状态信息，包括玩家状态、游戏阶段、
    资源分布、胜利条件等。提供状态查询和修改的统一接口。
    """
    
    @property
    def current_phase(self) -> GamePhase:
        """获取当前游戏阶段"""
        ...
    
    @property
    def round_number(self) -> int:
        """获取当前回合数"""
        ...
    
    @property
    def current_player(self) -> Optional[PlayerId]:
        """获取当前行动玩家"""
        ...
    
    @property
    def players(self) -> List[PlayerId]:
        """获取所有玩家ID列表"""
        ...
    
    def initialize_game(self, players: List[IPlayer]) -> None:
        """
        初始化游戏状态
        
        Args:
            players: 参与游戏的玩家列表
        """
        ...
    
    def get_player_info(self, player_id: PlayerId) -> Optional[PlayerInfo]:
        """
        获取玩家信息
        
        Args:
            player_id: 玩家ID
            
        Returns:
            Optional[PlayerInfo]: 玩家信息，如果不存在则返回None
        """
        ...
    
    def update_player_resources(
        self, 
        player_id: PlayerId, 
        resource_changes: Dict[ResourceType, int]
    ) -> bool:
        """
        更新玩家资源
        
        Args:
            player_id: 玩家ID
            resource_changes: 资源变化量（正数为增加，负数为减少）
            
        Returns:
            bool: 是否更新成功
        """
        ...
    
    def get_available_actions(self, player_id: PlayerId) -> List[ActionType]:
        """
        获取玩家可用的行动类型
        
        Args:
            player_id: 玩家ID
            
        Returns:
            List[ActionType]: 可用行动类型列表
        """
        ...
    
    def is_game_over(self) -> bool:
        """检查游戏是否结束"""
        ...
    
    def get_winner(self) -> Optional[PlayerId]:
        """
        获取游戏获胜者
        
        Returns:
            Optional[PlayerId]: 获胜者ID，如果游戏未结束或平局则返回None
        """
        ...
    
    def get_scores(self) -> Dict[PlayerId, int]:
        """
        获取所有玩家的得分
        
        Returns:
            Dict[PlayerId, int]: 玩家得分字典
        """
        ...
    
    def save_state(self) -> Dict[str, Any]:
        """
        保存游戏状态
        
        Returns:
            Dict[str, Any]: 序列化的游戏状态
        """
        ...
    
    def load_state(self, state_data: Dict[str, Any]) -> bool:
        """
        加载游戏状态
        
        Args:
            state_data: 序列化的游戏状态
            
        Returns:
            bool: 是否加载成功
        """
        ...

@runtime_checkable
class IGameSystem(Protocol):
    """
    游戏系统接口
    
    定义游戏中各种子系统（如易学系统、资源系统、AI系统等）
    必须实现的基本方法。提供系统生命周期管理和状态更新功能。
    """
    
    @property
    def system_type(self) -> SystemType:
        """获取系统类型"""
        ...
    
    @property
    def name(self) -> str:
        """获取系统名称"""
        ...
    
    @property
    def enabled(self) -> bool:
        """检查系统是否启用"""
        ...
    
    def get_info(self) -> SystemInfo:
        """
        获取系统信息
        
        Returns:
            SystemInfo: 系统详细信息
        """
        ...
    
    def initialize(self, config: Optional[ConfigDict] = None) -> bool:
        """
        初始化系统
        
        Args:
            config: 系统配置
            
        Returns:
            bool: 是否初始化成功
        """
        ...
    
    def start(self) -> bool:
        """
        启动系统
        
        Returns:
            bool: 是否启动成功
        """
        ...
    
    def stop(self) -> bool:
        """
        停止系统
        
        Returns:
            bool: 是否停止成功
        """
        ...
    
    def update(self, delta_time: float) -> None:
        """
        更新系统状态
        
        Args:
            delta_time: 距离上次更新的时间间隔（秒）
        """
        ...
    
    def handle_event(self, event: GameEvent) -> None:
        """
        处理游戏事件
        
        Args:
            event: 游戏事件
        """
        ...
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取系统状态
        
        Returns:
            Dict[str, Any]: 系统状态信息
        """
        ...

@runtime_checkable
class IEventBus(Protocol):
    """
    事件总线接口
    
    提供游戏中事件的发布、订阅、分发功能。
    支持同步和异步事件处理，确保系统间的松耦合通信。
    """
    
    def subscribe(
        self, 
        event_type: str, 
        handler: Callable[[GameEvent], None],
        priority: int = 0
    ) -> str:
        """
        订阅事件
        
        Args:
            event_type: 事件类型
            handler: 事件处理函数
            priority: 优先级（数字越小优先级越高）
            
        Returns:
            str: 订阅ID，用于取消订阅
        """
        ...
    
    def unsubscribe(self, subscription_id: str) -> bool:
        """
        取消订阅
        
        Args:
            subscription_id: 订阅ID
            
        Returns:
            bool: 是否取消成功
        """
        ...
    
    def publish(self, event: GameEvent) -> None:
        """
        发布事件
        
        Args:
            event: 要发布的事件
        """
        ...
    
    async def publish_async(self, event: GameEvent) -> None:
        """
        异步发布事件
        
        Args:
            event: 要发布的事件
        """
        ...
    
    def get_subscribers(self, event_type: str) -> List[str]:
        """
        获取事件订阅者列表
        
        Args:
            event_type: 事件类型
            
        Returns:
            List[str]: 订阅者ID列表
        """
        ...
    
    def clear_subscribers(self, event_type: Optional[str] = None) -> None:
        """
        清除订阅者
        
        Args:
            event_type: 事件类型，如果为None则清除所有订阅者
        """
        ...

@runtime_checkable
class IConfigManager(Protocol):
    """
    配置管理接口
    
    管理游戏的各种配置参数，支持配置的加载、保存、
    验证、热更新等功能。提供类型安全的配置访问方式。
    """
    
    def load_config(self, config_path: str) -> bool:
        """
        加载配置文件
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            bool: 是否加载成功
        """
        ...
    
    def save_config(self, config_path: str) -> bool:
        """
        保存配置文件
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            bool: 是否保存成功
        """
        ...
    
    def get_config(self, key: str, default: T = None) -> T:
        """
        获取配置值
        
        Args:
            key: 配置键，支持点分隔的嵌套键
            default: 默认值
            
        Returns:
            T: 配置值
        """
        ...
    
    def set_config(self, key: str, value: Any) -> bool:
        """
        设置配置值
        
        Args:
            key: 配置键
            value: 配置值
            
        Returns:
            bool: 是否设置成功
        """
        ...
    
    def validate_config(self) -> List[str]:
        """
        验证配置的有效性
        
        Returns:
            List[str]: 验证错误列表，空列表表示验证通过
        """
        ...
    
    def get_all_configs(self) -> ConfigDict:
        """
        获取所有配置
        
        Returns:
            ConfigDict: 完整的配置字典
        """
        ...
    
    def reset_to_defaults(self) -> None:
        """重置为默认配置"""
        ...
    
    def watch_config(
        self, 
        key: str, 
        callback: Callable[[str, Any, Any], None]
    ) -> str:
        """
        监听配置变化
        
        Args:
            key: 要监听的配置键
            callback: 变化回调函数，参数为(key, old_value, new_value)
            
        Returns:
            str: 监听器ID
        """
        ...
    
    def unwatch_config(self, watcher_id: str) -> bool:
        """
        取消配置监听
        
        Args:
            watcher_id: 监听器ID
            
        Returns:
            bool: 是否取消成功
        """
        ...

@runtime_checkable
class IGameFactory(Protocol):
    """
    游戏工厂接口
    
    负责创建游戏中的各种对象，包括玩家、行动、系统等。
    提供统一的对象创建接口，支持依赖注入和对象池管理。
    """
    
    def create_player(
        self, 
        player_type: PlayerType, 
        **kwargs: Any
    ) -> IPlayer:
        """
        创建玩家对象
        
        Args:
            player_type: 玩家类型
            **kwargs: 额外参数
            
        Returns:
            IPlayer: 玩家对象
        """
        ...
    
    def create_action(
        self, 
        action_type: ActionType, 
        **kwargs: Any
    ) -> IGameAction:
        """
        创建行动对象
        
        Args:
            action_type: 行动类型
            **kwargs: 额外参数
            
        Returns:
            IGameAction: 行动对象
        """
        ...
    
    def create_system(
        self, 
        system_type: SystemType, 
        **kwargs: Any
    ) -> IGameSystem:
        """
        创建系统对象
        
        Args:
            system_type: 系统类型
            **kwargs: 额外参数
            
        Returns:
            IGameSystem: 系统对象
        """
        ...
    
    def create_game_state(self, **kwargs: Any) -> IGameState:
        """
        创建游戏状态对象
        
        Args:
            **kwargs: 额外参数
            
        Returns:
            IGameState: 游戏状态对象
        """
        ...
    
    def create_event_bus(self, **kwargs: Any) -> IEventBus:
        """
        创建事件总线对象
        
        Args:
            **kwargs: 额外参数
            
        Returns:
            IEventBus: 事件总线对象
        """
        ...
    
    def create_config_manager(self, **kwargs: Any) -> IConfigManager:
        """
        创建配置管理器对象
        
        Args:
            **kwargs: 额外参数
            
        Returns:
            IConfigManager: 配置管理器对象
        """
        ...
    
    def register_creator(
        self, 
        object_type: str, 
        creator: Callable[..., Any]
    ) -> None:
        """
        注册对象创建器
        
        Args:
            object_type: 对象类型
            creator: 创建器函数
        """
        ...
    
    def get_available_types(self, category: str) -> List[str]:
        """
        获取可用的对象类型
        
        Args:
            category: 对象类别
            
        Returns:
            List[str]: 可用类型列表
        """
        ...

# ==================== 扩展接口 ====================

@runtime_checkable
class IAsyncGameSystem(IGameSystem, Protocol):
    """
    异步游戏系统接口
    
    扩展基本游戏系统接口，支持异步操作。
    适用于需要网络通信、文件IO等异步操作的系统。
    """
    
    async def async_initialize(self, config: Optional[ConfigDict] = None) -> bool:
        """
        异步初始化系统
        
        Args:
            config: 系统配置
            
        Returns:
            bool: 是否初始化成功
        """
        ...
    
    async def async_update(self, delta_time: float) -> None:
        """
        异步更新系统状态
        
        Args:
            delta_time: 距离上次更新的时间间隔（秒）
        """
        ...
    
    async def async_handle_event(self, event: GameEvent) -> None:
        """
        异步处理游戏事件
        
        Args:
            event: 游戏事件
        """
        ...

@runtime_checkable
class ISerializable(Protocol):
    """
    序列化接口
    
    定义对象序列化和反序列化的标准方法。
    支持JSON、二进制等多种序列化格式。
    """
    
    def serialize(self) -> Dict[str, Any]:
        """
        序列化对象
        
        Returns:
            Dict[str, Any]: 序列化后的数据
        """
        ...
    
    def deserialize(self, data: Dict[str, Any]) -> bool:
        """
        反序列化对象
        
        Args:
            data: 序列化的数据
            
        Returns:
            bool: 是否反序列化成功
        """
        ...
    
    def get_version(self) -> str:
        """
        获取序列化版本
        
        Returns:
            str: 版本号
        """
        ...

@runtime_checkable
class IValidatable(Protocol):
    """
    可验证接口
    
    定义对象验证的标准方法。
    用于确保对象状态的一致性和有效性。
    """
    
    def validate(self) -> List[str]:
        """
        验证对象状态
        
        Returns:
            List[str]: 验证错误列表，空列表表示验证通过
        """
        ...
    
    def is_valid(self) -> bool:
        """
        检查对象是否有效
        
        Returns:
            bool: 是否有效
        """
        ...

@runtime_checkable
class ICacheable(Protocol):
    """
    可缓存接口
    
    定义对象缓存的标准方法。
    支持缓存键生成、缓存失效等功能。
    """
    
    def get_cache_key(self) -> str:
        """
        获取缓存键
        
        Returns:
            str: 缓存键
        """
        ...
    
    def get_cache_ttl(self) -> Optional[int]:
        """
        获取缓存生存时间
        
        Returns:
            Optional[int]: 生存时间（秒），None表示永不过期
        """
        ...
    
    def invalidate_cache(self) -> None:
        """使缓存失效"""
        ...

# ==================== 工具接口 ====================

@runtime_checkable
class ILogger(Protocol):
    """
    日志接口
    
    提供统一的日志记录功能，支持不同级别的日志输出。
    """
    
    def debug(self, message: str, **kwargs: Any) -> None:
        """记录调试日志"""
        ...
    
    def info(self, message: str, **kwargs: Any) -> None:
        """记录信息日志"""
        ...
    
    def warning(self, message: str, **kwargs: Any) -> None:
        """记录警告日志"""
        ...
    
    def error(self, message: str, **kwargs: Any) -> None:
        """记录错误日志"""
        ...
    
    def critical(self, message: str, **kwargs: Any) -> None:
        """记录严重错误日志"""
        ...

@runtime_checkable
class IMetrics(Protocol):
    """
    指标收集接口
    
    提供性能指标和统计数据的收集功能。
    """
    
    def increment_counter(self, name: str, value: int = 1, tags: Optional[Dict[str, str]] = None) -> None:
        """增加计数器"""
        ...
    
    def set_gauge(self, name: str, value: float, tags: Optional[Dict[str, str]] = None) -> None:
        """设置仪表值"""
        ...
    
    def record_histogram(self, name: str, value: float, tags: Optional[Dict[str, str]] = None) -> None:
        """记录直方图数据"""
        ...
    
    def start_timer(self, name: str) -> str:
        """开始计时"""
        ...
    
    def stop_timer(self, timer_id: str) -> float:
        """停止计时并返回耗时"""
        ...

# ==================== 导出列表 ====================

__all__ = [
    # 数据结构
    'PlayerInfo',
    'SystemInfo',
    
    # 核心接口
    'IPlayer',
    'IGameAction',
    'IGameState',
    'IGameSystem',
    'IEventBus',
    'IConfigManager',
    'IGameFactory',
    
    # 扩展接口
    'IAsyncGameSystem',
    'ISerializable',
    'IValidatable',
    'ICacheable',
    
    # 工具接口
    'ILogger',
    'IMetrics',
]