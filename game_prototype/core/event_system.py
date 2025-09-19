"""
天机变游戏事件系统
实现事件驱动架构，支持系统间的解耦通信
"""

import logging
import threading
from typing import Dict, List, Set, Callable, Any, Optional
from collections import defaultdict, deque
from dataclasses import dataclass, field
import time

from .interfaces import IEventBus, IEventHandler
from .base_types import GameEvent
from .exceptions import SystemException

logger = logging.getLogger(__name__)

@dataclass
class EventSubscription:
    """事件订阅信息"""
    handler: IEventHandler
    priority: int = 0
    once: bool = False  # 是否只执行一次
    filter_func: Optional[Callable[[GameEvent], bool]] = None
    created_at: float = field(default_factory=time.time)

class EventBus(IEventBus):
    """
    事件总线实现
    
    提供事件的发布、订阅和处理机制
    """
    
    def __init__(self, max_queue_size: int = 1000, enable_history: bool = True):
        self.max_queue_size = max_queue_size
        self.enable_history = enable_history
        
        # 订阅管理
        self.subscriptions: Dict[str, List[EventSubscription]] = defaultdict(list)
        self.global_handlers: List[EventSubscription] = []
        
        # 事件队列
        self.event_queue: deque = deque(maxlen=max_queue_size)
        self.processing_queue: deque = deque()
        
        # 事件历史
        self.event_history: deque = deque(maxlen=max_queue_size if enable_history else 0)
        
        # 状态管理
        self.is_processing = False
        self.processing_lock = threading.Lock()
        
        # 统计信息
        self.stats = {
            "events_published": 0,
            "events_processed": 0,
            "events_failed": 0,
            "handlers_executed": 0
        }
        
        logger.info("事件总线初始化完成")
    
    def subscribe(
        self, 
        event_type: str, 
        handler: IEventHandler, 
        priority: int = 0,
        once: bool = False,
        filter_func: Optional[Callable[[GameEvent], bool]] = None
    ) -> None:
        """
        订阅事件
        
        Args:
            event_type: 事件类型，使用 "*" 订阅所有事件
            handler: 事件处理器
            priority: 优先级（数字越小优先级越高）
            once: 是否只执行一次
            filter_func: 事件过滤函数
        """
        subscription = EventSubscription(
            handler=handler,
            priority=priority,
            once=once,
            filter_func=filter_func
        )
        
        if event_type == "*":
            # 全局处理器
            self._insert_subscription(self.global_handlers, subscription)
        else:
            # 特定事件类型处理器
            self._insert_subscription(self.subscriptions[event_type], subscription)
        
        logger.debug(f"订阅事件: {event_type}, 处理器: {handler.__class__.__name__}")
    
    def unsubscribe(self, event_type: str, handler: IEventHandler) -> None:
        """
        取消订阅事件
        
        Args:
            event_type: 事件类型
            handler: 事件处理器
        """
        if event_type == "*":
            self._remove_handler(self.global_handlers, handler)
        else:
            self._remove_handler(self.subscriptions[event_type], handler)
        
        logger.debug(f"取消订阅事件: {event_type}, 处理器: {handler.__class__.__name__}")
    
    def publish(self, event: GameEvent) -> None:
        """
        发布事件
        
        Args:
            event: 游戏事件
        """
        self.stats["events_published"] += 1
        
        # 添加到队列
        self.event_queue.append(event)
        
        # 记录历史
        if self.enable_history:
            self.event_history.append(event)
        
        logger.debug(f"发布事件: {event.event_type}, ID: {event.id}")
        
        # 立即处理（同步模式）
        self._process_events()
    
    def publish_async(self, event: GameEvent) -> None:
        """
        异步发布事件
        
        Args:
            event: 游戏事件
        """
        self.stats["events_published"] += 1
        self.event_queue.append(event)
        
        if self.enable_history:
            self.event_history.append(event)
        
        logger.debug(f"异步发布事件: {event.event_type}, ID: {event.id}")
    
    def process_events(self) -> int:
        """
        处理事件队列
        
        Returns:
            处理的事件数量
        """
        return self._process_events()
    
    def _process_events(self) -> int:
        """内部事件处理方法"""
        if self.is_processing:
            return 0
        
        with self.processing_lock:
            self.is_processing = True
            processed_count = 0
            
            try:
                # 将当前队列移到处理队列
                while self.event_queue:
                    self.processing_queue.append(self.event_queue.popleft())
                
                # 处理事件
                while self.processing_queue:
                    event = self.processing_queue.popleft()
                    try:
                        self._handle_event(event)
                        processed_count += 1
                        self.stats["events_processed"] += 1
                    except Exception as e:
                        logger.error(f"处理事件失败: {event.event_type}, 错误: {e}")
                        self.stats["events_failed"] += 1
                
            finally:
                self.is_processing = False
            
            return processed_count
    
    def _handle_event(self, event: GameEvent) -> None:
        """
        处理单个事件
        
        Args:
            event: 游戏事件
        """
        # 获取所有相关处理器
        handlers = self._get_event_handlers(event)
        
        # 按优先级排序
        handlers.sort(key=lambda x: x.priority)
        
        # 执行处理器
        for subscription in handlers:
            try:
                # 应用过滤器
                if subscription.filter_func and not subscription.filter_func(event):
                    continue
                
                # 执行处理器
                new_events = subscription.handler.handle(event)
                self.stats["handlers_executed"] += 1
                
                # 处理新产生的事件
                if new_events:
                    for new_event in new_events:
                        self.event_queue.append(new_event)
                
                # 如果是一次性处理器，移除订阅
                if subscription.once:
                    self._remove_subscription(subscription, event.event_type)
                
            except Exception as e:
                logger.error(f"事件处理器执行失败: {subscription.handler.__class__.__name__}, 错误: {e}")
    
    def _get_event_handlers(self, event: GameEvent) -> List[EventSubscription]:
        """
        获取事件的所有处理器
        
        Args:
            event: 游戏事件
            
        Returns:
            处理器订阅列表
        """
        handlers = []
        
        # 添加全局处理器
        handlers.extend(self.global_handlers)
        
        # 添加特定类型处理器
        handlers.extend(self.subscriptions.get(event.event_type, []))
        
        return handlers
    
    def _insert_subscription(self, subscription_list: List[EventSubscription], subscription: EventSubscription) -> None:
        """
        按优先级插入订阅
        
        Args:
            subscription_list: 订阅列表
            subscription: 新订阅
        """
        inserted = False
        for i, existing in enumerate(subscription_list):
            if subscription.priority < existing.priority:
                subscription_list.insert(i, subscription)
                inserted = True
                break
        
        if not inserted:
            subscription_list.append(subscription)
    
    def _remove_handler(self, subscription_list: List[EventSubscription], handler: IEventHandler) -> None:
        """
        移除处理器
        
        Args:
            subscription_list: 订阅列表
            handler: 要移除的处理器
        """
        subscription_list[:] = [sub for sub in subscription_list if sub.handler != handler]
    
    def _remove_subscription(self, subscription: EventSubscription, event_type: str) -> None:
        """
        移除特定订阅
        
        Args:
            subscription: 要移除的订阅
            event_type: 事件类型
        """
        if event_type == "*":
            if subscription in self.global_handlers:
                self.global_handlers.remove(subscription)
        else:
            if subscription in self.subscriptions[event_type]:
                self.subscriptions[event_type].remove(subscription)
    
    # ==================== 查询和统计 ====================
    
    def get_subscription_count(self, event_type: Optional[str] = None) -> int:
        """
        获取订阅数量
        
        Args:
            event_type: 事件类型，None表示所有订阅
            
        Returns:
            订阅数量
        """
        if event_type is None:
            total = len(self.global_handlers)
            for handlers in self.subscriptions.values():
                total += len(handlers)
            return total
        elif event_type == "*":
            return len(self.global_handlers)
        else:
            return len(self.subscriptions.get(event_type, []))
    
    def get_event_history(self, event_type: Optional[str] = None, limit: int = 100) -> List[GameEvent]:
        """
        获取事件历史
        
        Args:
            event_type: 事件类型过滤
            limit: 返回数量限制
            
        Returns:
            事件历史列表
        """
        if not self.enable_history:
            return []
        
        events = list(self.event_history)
        
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        
        return events[-limit:] if limit > 0 else events
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取统计信息
        
        Returns:
            统计信息字典
        """
        return {
            **self.stats,
            "queue_size": len(self.event_queue),
            "processing_queue_size": len(self.processing_queue),
            "history_size": len(self.event_history),
            "subscription_count": self.get_subscription_count(),
            "is_processing": self.is_processing
        }
    
    def clear_history(self) -> None:
        """清空事件历史"""
        self.event_history.clear()
        logger.info("事件历史已清空")
    
    def clear_queue(self) -> None:
        """清空事件队列"""
        self.event_queue.clear()
        self.processing_queue.clear()
        logger.info("事件队列已清空")

# ==================== 便捷的事件处理器基类 ====================

class BaseEventHandler:
    """基础事件处理器"""
    
    def __init__(self, name: str):
        self.name = name
        self.handled_count = 0
    
    def handle(self, event: GameEvent) -> List[GameEvent]:
        """
        处理事件
        
        Args:
            event: 游戏事件
            
        Returns:
            新产生的事件列表
        """
        self.handled_count += 1
        return self.on_event(event)
    
    def on_event(self, event: GameEvent) -> List[GameEvent]:
        """
        子类重写此方法来处理事件
        
        Args:
            event: 游戏事件
            
        Returns:
            新产生的事件列表
        """
        return []

class LambdaEventHandler(BaseEventHandler):
    """Lambda事件处理器"""
    
    def __init__(self, name: str, handler_func: Callable[[GameEvent], List[GameEvent]]):
        super().__init__(name)
        self.handler_func = handler_func
    
    def on_event(self, event: GameEvent) -> List[GameEvent]:
        return self.handler_func(event)

# ==================== 事件工厂 ====================

class EventFactory:
    """事件工厂"""
    
    @staticmethod
    def create_game_event(event_type: str, source: Optional[str] = None, target: Optional[str] = None, **data) -> GameEvent:
        """
        创建游戏事件
        
        Args:
            event_type: 事件类型
            source: 事件源
            target: 事件目标
            **data: 事件数据
            
        Returns:
            游戏事件
        """
        return GameEvent(
            event_type=event_type,
            source=source,
            target=target,
            data=data
        )
    
    @staticmethod
    def create_system_event(system_name: str, action: str, **data) -> GameEvent:
        """
        创建系统事件
        
        Args:
            system_name: 系统名称
            action: 动作
            **data: 事件数据
            
        Returns:
            游戏事件
        """
        return GameEvent(
            event_type=f"system_{action}",
            source=system_name,
            data={"system": system_name, "action": action, **data}
        )
    
    @staticmethod
    def create_player_event(player_id: str, action: str, **data) -> GameEvent:
        """
        创建玩家事件
        
        Args:
            player_id: 玩家ID
            action: 动作
            **data: 事件数据
            
        Returns:
            游戏事件
        """
        return GameEvent(
            event_type=f"player_{action}",
            source=player_id,
            data={"player_id": player_id, "action": action, **data}
        )

# ==================== 全局事件总线实例 ====================

# 创建全局事件总线实例
global_event_bus = EventBus()

def get_event_bus() -> EventBus:
    """获取全局事件总线实例"""
    return global_event_bus