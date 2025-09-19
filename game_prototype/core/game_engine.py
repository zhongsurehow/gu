"""
天机变游戏引擎

重构后的核心游戏逻辑，提供清晰的架构和接口。
负责协调所有游戏系统，管理游戏状态和玩家交互。

主要组件：
- GameEngine: 核心游戏引擎类
- GameEngineConfig: 引擎配置类
- GameSession: 游戏会话管理类
- ActionProcessor: 行动处理器类

作者: 游戏开发团队
版本: 1.0.0
"""

import logging
import time
import uuid
from typing import (
    Dict, List, Optional, Any, Type, Set, Callable, 
    Union, Tuple, Protocol, TypeVar, Generic
)
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from contextlib import contextmanager
from enum import Enum, auto

from .interfaces import (
    IGameState, IPlayer, IGameAction, IGameSystem, 
    IEventBus, IConfigManager, IGameFactory
)
from .base_types import (
    GameEvent, ActionResult, PlayerId, SystemType,
    GamePhase, ActionType, ConfigDict, Position,
    ResourceType, PlayerType
)
from .exceptions import (
    GameException, GameStateException, PlayerNotFoundException,
    InvalidActionException, SystemException
)
from .constants import GAME_CONSTANTS, ACTION_CONSTANTS

# 类型变量定义
T = TypeVar('T')
P = TypeVar('P', bound=IPlayer)
S = TypeVar('S', bound=IGameSystem)

logger = logging.getLogger(__name__)

# ==================== 配置和状态类 ====================

@dataclass
class GameEngineConfig:
    """
    游戏引擎配置类
    
    定义游戏引擎的各种配置参数，包括玩家限制、
    回合设置、自动保存、调试模式等。
    
    Attributes:
        max_players: 最大玩家数量
        max_rounds: 最大回合数
        auto_save_enabled: 是否启用自动保存
        debug_mode: 是否启用调试模式
        event_logging: 是否启用事件日志
        performance_monitoring: 是否启用性能监控
        ai_timeout: AI决策超时时间（秒）
        turn_timeout: 回合超时时间（秒）
        save_interval: 自动保存间隔（秒）
    """
    max_players: int = GAME_CONSTANTS.MAX_PLAYERS
    max_rounds: int = GAME_CONSTANTS.MAX_ROUNDS
    auto_save_enabled: bool = True
    debug_mode: bool = False
    event_logging: bool = True
    performance_monitoring: bool = False
    ai_timeout: int = 30
    turn_timeout: int = GAME_CONSTANTS.TURN_TIME_LIMIT
    save_interval: int = 300  # 5分钟

@dataclass
class GameStatistics:
    """
    游戏统计信息类
    
    记录游戏过程中的各种统计数据，用于分析和优化。
    
    Attributes:
        total_rounds: 总回合数
        total_actions: 总行动数
        player_actions: 各玩家行动统计
        system_performance: 系统性能统计
        start_time: 游戏开始时间
        end_time: 游戏结束时间
        winner: 获胜者
    """
    total_rounds: int = 0
    total_actions: int = 0
    player_actions: Dict[PlayerId, int] = field(default_factory=dict)
    system_performance: Dict[str, float] = field(default_factory=dict)
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    winner: Optional[PlayerId] = None
    
    @property
    def game_duration(self) -> Optional[float]:
        """获取游戏持续时间"""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None

class EngineState(Enum):
    """
    引擎状态枚举
    
    定义游戏引擎的各种运行状态。
    """
    UNINITIALIZED = auto()
    INITIALIZING = auto()
    READY = auto()
    RUNNING = auto()
    PAUSED = auto()
    STOPPING = auto()
    STOPPED = auto()
    ERROR = auto()

# ==================== 行动处理器 ====================

class ActionProcessor:
    """
    行动处理器类
    
    负责处理和验证玩家行动，确保行动的合法性和一致性。
    提供行动预处理、执行、后处理的完整流程。
    """
    
    def __init__(self, game_state: IGameState, event_bus: IEventBus):
        """
        初始化行动处理器
        
        Args:
            game_state: 游戏状态接口
            event_bus: 事件总线接口
        """
        self.game_state = game_state
        self.event_bus = event_bus
        self._action_validators: Dict[ActionType, Callable[[IGameAction], bool]] = {}
        self._action_processors: Dict[ActionType, Callable[[IGameAction], ActionResult]] = {}
        self._setup_default_processors()
    
    def _setup_default_processors(self) -> None:
        """设置默认的行动处理器"""
        self._action_validators.update({
            ActionType.MOVE: self._validate_move_action,
            ActionType.ATTACK: self._validate_attack_action,
            ActionType.DEFEND: self._validate_defend_action,
            ActionType.MEDITATE: self._validate_meditate_action,
            ActionType.DIVINATION: self._validate_divination_action,
            ActionType.PLAY_CARD: self._validate_play_card_action,
            ActionType.TRANSFORM: self._validate_transform_action,
            ActionType.SPECIAL: self._validate_special_action,
        })
        
        self._action_processors.update({
            ActionType.MOVE: self._process_move_action,
            ActionType.ATTACK: self._process_attack_action,
            ActionType.DEFEND: self._process_defend_action,
            ActionType.MEDITATE: self._process_meditate_action,
            ActionType.DIVINATION: self._process_divination_action,
            ActionType.PLAY_CARD: self._process_play_card_action,
            ActionType.TRANSFORM: self._process_transform_action,
            ActionType.SPECIAL: self._process_special_action,
        })
    
    def process_action(self, action: IGameAction) -> ActionResult:
        """
        处理游戏行动
        
        Args:
            action: 要处理的游戏行动
            
        Returns:
            ActionResult: 行动执行结果
            
        Raises:
            InvalidActionException: 当行动无效时
        """
        try:
            # 预处理验证
            if not self._validate_action(action):
                return ActionResult(
                    success=False,
                    message="行动验证失败",
                    action_type=action.action_type
                )
            
            # 执行行动
            result = self._execute_action(action)
            
            # 后处理
            self._post_process_action(action, result)
            
            return result
            
        except Exception as e:
            logger.error(f"处理行动时发生错误: {e}")
            return ActionResult(
                success=False,
                message=f"行动处理错误: {str(e)}",
                action_type=action.action_type
            )
    
    def _validate_action(self, action: IGameAction) -> bool:
        """验证行动的合法性"""
        validator = self._action_validators.get(action.action_type)
        if validator:
            return validator(action)
        return True
    
    def _execute_action(self, action: IGameAction) -> ActionResult:
        """执行具体的行动"""
        processor = self._action_processors.get(action.action_type)
        if processor:
            return processor(action)
        
        # 默认处理
        return ActionResult(
            success=True,
            message="行动执行成功",
            action_type=action.action_type
        )
    
    def _post_process_action(self, action: IGameAction, result: ActionResult) -> None:
        """行动后处理"""
        # 发布行动完成事件
        event = GameEvent(
            event_type="action_completed",
            data={
                "action": action,
                "result": result,
                "timestamp": time.time()
            }
        )
        self.event_bus.publish(event)
    
    # 具体行动验证方法
    def _validate_move_action(self, action: IGameAction) -> bool:
        """验证移动行动"""
        # 实现移动验证逻辑
        return True
    
    def _validate_attack_action(self, action: IGameAction) -> bool:
        """验证攻击行动"""
        # 实现攻击验证逻辑
        return True
    
    def _validate_defend_action(self, action: IGameAction) -> bool:
        """验证防御行动"""
        # 实现防御验证逻辑
        return True
    
    def _validate_meditate_action(self, action: IGameAction) -> bool:
        """验证冥想行动"""
        # 实现冥想验证逻辑
        return True
    
    def _validate_divination_action(self, action: IGameAction) -> bool:
        """验证占卜行动"""
        # 实现占卜验证逻辑
        return True
    
    def _validate_play_card_action(self, action: IGameAction) -> bool:
        """验证出牌行动"""
        # 实现出牌验证逻辑
        return True
    
    def _validate_transform_action(self, action: IGameAction) -> bool:
        """验证变换行动"""
        # 实现变换验证逻辑
        return True
    
    def _validate_special_action(self, action: IGameAction) -> bool:
        """验证特殊行动"""
        # 实现特殊行动验证逻辑
        return True
    
    # 具体行动处理方法
    def _process_move_action(self, action: IGameAction) -> ActionResult:
        """处理移动行动"""
        # 实现移动处理逻辑
        return ActionResult(success=True, message="移动成功", action_type=ActionType.MOVE)
    
    def _process_attack_action(self, action: IGameAction) -> ActionResult:
        """处理攻击行动"""
        # 实现攻击处理逻辑
        return ActionResult(success=True, message="攻击成功", action_type=ActionType.ATTACK)
    
    def _process_defend_action(self, action: IGameAction) -> ActionResult:
        """处理防御行动"""
        # 实现防御处理逻辑
        return ActionResult(success=True, message="防御成功", action_type=ActionType.DEFEND)
    
    def _process_meditate_action(self, action: IGameAction) -> ActionResult:
        """处理冥想行动"""
        # 实现冥想处理逻辑
        return ActionResult(success=True, message="冥想成功", action_type=ActionType.MEDITATE)
    
    def _process_divination_action(self, action: IGameAction) -> ActionResult:
        """处理占卜行动"""
        # 实现占卜处理逻辑
        return ActionResult(success=True, message="占卜成功", action_type=ActionType.DIVINATION)
    
    def _process_play_card_action(self, action: IGameAction) -> ActionResult:
        """处理出牌行动"""
        # 实现出牌处理逻辑
        return ActionResult(success=True, message="出牌成功", action_type=ActionType.PLAY_CARD)
    
    def _process_transform_action(self, action: IGameAction) -> ActionResult:
        """处理变换行动"""
        # 实现变换处理逻辑
        return ActionResult(success=True, message="变换成功", action_type=ActionType.TRANSFORM)
    
    def _process_special_action(self, action: IGameAction) -> ActionResult:
        """处理特殊行动"""
        # 实现特殊行动处理逻辑
        return ActionResult(success=True, message="特殊行动成功", action_type=ActionType.SPECIAL)

# ==================== 游戏会话管理 ====================

class GameSession:
    """
    游戏会话管理类
    
    管理单个游戏会话的生命周期，包括会话创建、
    状态管理、玩家管理、保存/加载等功能。
    """
    
    def __init__(self, session_id: str, config: GameEngineConfig):
        """
        初始化游戏会话
        
        Args:
            session_id: 会话唯一标识符
            config: 游戏引擎配置
        """
        self.session_id = session_id
        self.config = config
        self.created_at = time.time()
        self.last_activity = time.time()
        self.players: Dict[PlayerId, IPlayer] = {}
        self.statistics = GameStatistics()
        self._is_active = False
    
    def add_player(self, player: IPlayer) -> bool:
        """
        添加玩家到会话
        
        Args:
            player: 要添加的玩家
            
        Returns:
            bool: 是否成功添加
        """
        if len(self.players) >= self.config.max_players:
            return False
        
        self.players[player.player_id] = player
        self.statistics.player_actions[player.player_id] = 0
        self.last_activity = time.time()
        return True
    
    def remove_player(self, player_id: PlayerId) -> bool:
        """
        从会话中移除玩家
        
        Args:
            player_id: 要移除的玩家ID
            
        Returns:
            bool: 是否成功移除
        """
        if player_id in self.players:
            del self.players[player_id]
            self.last_activity = time.time()
            return True
        return False
    
    def get_player(self, player_id: PlayerId) -> Optional[IPlayer]:
        """
        获取指定玩家
        
        Args:
            player_id: 玩家ID
            
        Returns:
            Optional[IPlayer]: 玩家对象，如果不存在则返回None
        """
        return self.players.get(player_id)
    
    def is_full(self) -> bool:
        """检查会话是否已满"""
        return len(self.players) >= self.config.max_players
    
    def is_empty(self) -> bool:
        """检查会话是否为空"""
        return len(self.players) == 0
    
    def update_activity(self) -> None:
        """更新最后活动时间"""
        self.last_activity = time.time()
    
    @property
    def is_active(self) -> bool:
        """检查会话是否活跃"""
        return self._is_active
    
    def activate(self) -> None:
        """激活会话"""
        self._is_active = True
        self.statistics.start_time = time.time()
    
    def deactivate(self) -> None:
        """停用会话"""
        self._is_active = False
        self.statistics.end_time = time.time()

# ==================== 核心游戏引擎 ====================

class GameEngine:
    """
    天机变游戏引擎
    
    负责协调所有游戏系统，管理游戏状态和玩家交互。
    提供完整的游戏生命周期管理，包括初始化、运行、
    暂停、停止等功能。
    
    主要职责：
    - 游戏系统协调
    - 状态管理
    - 事件处理
    - 玩家交互
    - 性能监控
    """
    
    def __init__(
        self,
        config_manager: IConfigManager,
        event_bus: IEventBus,
        game_factory: IGameFactory,
        engine_config: Optional[GameEngineConfig] = None
    ):
        """
        初始化游戏引擎
        
        Args:
            config_manager: 配置管理器
            event_bus: 事件总线
            game_factory: 游戏工厂
            engine_config: 引擎配置
        """
        self.config_manager = config_manager
        self.event_bus = event_bus
        self.game_factory = game_factory
        self.config = engine_config or GameEngineConfig()
        
        # 核心组件
        self.game_state: Optional[IGameState] = None
        self.action_processor: Optional[ActionProcessor] = None
        self.current_session: Optional[GameSession] = None
        
        # 系统管理
        self.systems: Dict[SystemType, IGameSystem] = {}
        self.system_order: List[SystemType] = []
        
        # 状态管理
        self.engine_state = EngineState.UNINITIALIZED
        self.last_update_time = 0.0
        self.frame_count = 0
        
        # 性能监控
        self.performance_metrics: Dict[str, float] = {}
        
        # 事件处理
        self._setup_event_handlers()
        
        logger.info(f"游戏引擎初始化完成，配置: {self.config}")
    
    def _setup_event_handlers(self) -> None:
        """设置事件处理器"""
        self.event_bus.subscribe("game_start", self._handle_game_start)
        self.event_bus.subscribe("game_end", self._handle_game_end)
        self.event_bus.subscribe("player_action", self._handle_player_action)
        self.event_bus.subscribe("system_error", self._handle_system_error)
    
    def initialize(self) -> bool:
        """
        初始化游戏引擎
        
        Returns:
            bool: 是否成功初始化
        """
        try:
            self.engine_state = EngineState.INITIALIZING
            
            # 创建游戏状态
            self.game_state = self.game_factory.create_game_state()
            
            # 创建行动处理器
            self.action_processor = ActionProcessor(self.game_state, self.event_bus)
            
            # 初始化系统
            self._initialize_systems()
            
            # 创建默认会话
            self.current_session = GameSession(
                session_id=str(uuid.uuid4()),
                config=self.config
            )
            
            self.engine_state = EngineState.READY
            logger.info("游戏引擎初始化成功")
            return True
            
        except Exception as e:
            self.engine_state = EngineState.ERROR
            logger.error(f"游戏引擎初始化失败: {e}")
            return False
    
    def _initialize_systems(self) -> None:
        """初始化游戏系统"""
        # 从工厂创建系统
        system_types = [
            SystemType.CONFIG,
            SystemType.YIXUE,
            SystemType.RESOURCE,
            SystemType.ACTION,
            SystemType.EVENT,
            SystemType.AI,
            SystemType.UI
        ]
        
        for system_type in system_types:
            try:
                system = self.game_factory.create_system(system_type)
                if system:
                    self.systems[system_type] = system
                    self.system_order.append(system_type)
                    system.initialize()
                    logger.debug(f"系统 {system_type} 初始化成功")
            except Exception as e:
                logger.error(f"系统 {system_type} 初始化失败: {e}")
    
    def start_game(self, players: List[IPlayer]) -> bool:
        """
        开始游戏
        
        Args:
            players: 参与游戏的玩家列表
            
        Returns:
            bool: 是否成功开始游戏
        """
        if self.engine_state != EngineState.READY:
            logger.error("引擎未就绪，无法开始游戏")
            return False
        
        try:
            # 添加玩家到会话
            for player in players:
                if not self.current_session.add_player(player):
                    logger.error(f"无法添加玩家 {player.player_id}")
                    return False
            
            # 激活会话
            self.current_session.activate()
            
            # 初始化游戏状态
            self.game_state.initialize_game(players)
            
            # 启动系统
            for system_type in self.system_order:
                system = self.systems.get(system_type)
                if system:
                    system.start()
            
            self.engine_state = EngineState.RUNNING
            self.last_update_time = time.time()
            
            # 发布游戏开始事件
            event = GameEvent(
                event_type="game_start",
                data={"players": [p.player_id for p in players]}
            )
            self.event_bus.publish(event)
            
            logger.info(f"游戏开始，玩家数量: {len(players)}")
            return True
            
        except Exception as e:
            logger.error(f"开始游戏失败: {e}")
            return False
    
    def update(self, delta_time: float) -> None:
        """
        更新游戏引擎
        
        Args:
            delta_time: 距离上次更新的时间间隔
        """
        if self.engine_state != EngineState.RUNNING:
            return
        
        try:
            start_time = time.time()
            
            # 更新系统
            for system_type in self.system_order:
                system = self.systems.get(system_type)
                if system:
                    system.update(delta_time)
            
            # 更新会话活动时间
            if self.current_session:
                self.current_session.update_activity()
            
            # 更新性能指标
            self.frame_count += 1
            update_time = time.time() - start_time
            self.performance_metrics["update_time"] = update_time
            self.performance_metrics["fps"] = 1.0 / delta_time if delta_time > 0 else 0
            
            # 自动保存检查
            if self.config.auto_save_enabled:
                self._check_auto_save()
            
        except Exception as e:
            logger.error(f"更新游戏引擎时发生错误: {e}")
            self.engine_state = EngineState.ERROR
    
    def process_player_action(self, player_id: PlayerId, action: IGameAction) -> ActionResult:
        """
        处理玩家行动
        
        Args:
            player_id: 玩家ID
            action: 玩家行动
            
        Returns:
            ActionResult: 行动处理结果
        """
        if not self.action_processor:
            return ActionResult(
                success=False,
                message="行动处理器未初始化",
                action_type=action.action_type
            )
        
        # 验证玩家
        if not self.current_session or not self.current_session.get_player(player_id):
            return ActionResult(
                success=False,
                message="玩家不存在",
                action_type=action.action_type
            )
        
        # 处理行动
        result = self.action_processor.process_action(action)
        
        # 更新统计
        if self.current_session:
            self.current_session.statistics.total_actions += 1
            self.current_session.statistics.player_actions[player_id] += 1
        
        return result
    
    def pause_game(self) -> bool:
        """
        暂停游戏
        
        Returns:
            bool: 是否成功暂停
        """
        if self.engine_state == EngineState.RUNNING:
            self.engine_state = EngineState.PAUSED
            
            # 暂停所有系统
            for system in self.systems.values():
                if hasattr(system, 'pause'):
                    system.pause()
            
            logger.info("游戏已暂停")
            return True
        return False
    
    def resume_game(self) -> bool:
        """
        恢复游戏
        
        Returns:
            bool: 是否成功恢复
        """
        if self.engine_state == EngineState.PAUSED:
            self.engine_state = EngineState.RUNNING
            
            # 恢复所有系统
            for system in self.systems.values():
                if hasattr(system, 'resume'):
                    system.resume()
            
            logger.info("游戏已恢复")
            return True
        return False
    
    def stop_game(self) -> bool:
        """
        停止游戏
        
        Returns:
            bool: 是否成功停止
        """
        try:
            self.engine_state = EngineState.STOPPING
            
            # 停止所有系统
            for system in self.systems.values():
                system.stop()
            
            # 停用会话
            if self.current_session:
                self.current_session.deactivate()
            
            # 发布游戏结束事件
            event = GameEvent(
                event_type="game_end",
                data={"statistics": self.current_session.statistics if self.current_session else None}
            )
            self.event_bus.publish(event)
            
            self.engine_state = EngineState.STOPPED
            logger.info("游戏已停止")
            return True
            
        except Exception as e:
            logger.error(f"停止游戏失败: {e}")
            return False
    
    def shutdown(self) -> None:
        """关闭游戏引擎"""
        try:
            if self.engine_state == EngineState.RUNNING:
                self.stop_game()
            
            # 清理系统
            for system in self.systems.values():
                if hasattr(system, 'cleanup'):
                    system.cleanup()
            
            self.systems.clear()
            self.engine_state = EngineState.UNINITIALIZED
            logger.info("游戏引擎已关闭")
            
        except Exception as e:
            logger.error(f"关闭游戏引擎失败: {e}")
    
    def get_game_state(self) -> Optional[IGameState]:
        """获取当前游戏状态"""
        return self.game_state
    
    def get_statistics(self) -> Optional[GameStatistics]:
        """获取游戏统计信息"""
        return self.current_session.statistics if self.current_session else None
    
    def get_performance_metrics(self) -> Dict[str, float]:
        """获取性能指标"""
        return self.performance_metrics.copy()
    
    @contextmanager
    def performance_monitor(self, operation_name: str):
        """性能监控上下文管理器"""
        start_time = time.time()
        try:
            yield
        finally:
            duration = time.time() - start_time
            self.performance_metrics[f"{operation_name}_time"] = duration
    
    def _check_auto_save(self) -> None:
        """检查是否需要自动保存"""
        if not self.current_session:
            return
        
        current_time = time.time()
        if current_time - self.current_session.last_activity > self.config.save_interval:
            self._auto_save()
    
    def _auto_save(self) -> None:
        """执行自动保存"""
        try:
            # 实现自动保存逻辑
            logger.debug("执行自动保存")
        except Exception as e:
            logger.error(f"自动保存失败: {e}")
    
    # 事件处理方法
    def _handle_game_start(self, event: GameEvent) -> None:
        """处理游戏开始事件"""
        logger.info("处理游戏开始事件")
    
    def _handle_game_end(self, event: GameEvent) -> None:
        """处理游戏结束事件"""
        logger.info("处理游戏结束事件")
    
    def _handle_player_action(self, event: GameEvent) -> None:
        """处理玩家行动事件"""
        logger.debug("处理玩家行动事件")
    
    def _handle_system_error(self, event: GameEvent) -> None:
        """处理系统错误事件"""
        logger.error(f"系统错误: {event.data}")

# ==================== 导出列表 ====================

__all__ = [
    'GameEngine',
    'GameEngineConfig',
    'GameSession',
    'GameStatistics',
    'ActionProcessor',
    'EngineState',
]