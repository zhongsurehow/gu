"""
天机变游戏日志系统
提供统一的日志记录、格式化和管理功能
"""

import logging
import logging.handlers
import os
import sys
import json
import time
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

from .base_types import LogLevel
from .exceptions import SystemException

class LogFormat(Enum):
    """日志格式枚举"""
    SIMPLE = "simple"
    DETAILED = "detailed"
    JSON = "json"
    GAME = "game"

@dataclass
class LogConfig:
    """日志配置"""
    level: LogLevel = LogLevel.INFO
    format_type: LogFormat = LogFormat.DETAILED
    enable_console: bool = True
    enable_file: bool = True
    log_dir: str = "logs"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    enable_game_events: bool = True
    enable_performance: bool = True

class GameLogFormatter(logging.Formatter):
    """游戏专用日志格式化器"""
    
    def __init__(self, format_type: LogFormat = LogFormat.DETAILED):
        self.format_type = format_type
        super().__init__()
    
    def format(self, record: logging.LogRecord) -> str:
        """格式化日志记录"""
        if self.format_type == LogFormat.SIMPLE:
            return self._format_simple(record)
        elif self.format_type == LogFormat.JSON:
            return self._format_json(record)
        elif self.format_type == LogFormat.GAME:
            return self._format_game(record)
        else:
            return self._format_detailed(record)
    
    def _format_simple(self, record: logging.LogRecord) -> str:
        """简单格式"""
        return f"[{record.levelname}] {record.getMessage()}"
    
    def _format_detailed(self, record: logging.LogRecord) -> str:
        """详细格式"""
        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        # 获取额外信息
        player_id = getattr(record, 'player_id', '')
        game_phase = getattr(record, 'game_phase', '')
        action_type = getattr(record, 'action_type', '')
        
        # 构建格式化字符串
        parts = [
            f"[{timestamp}]",
            f"[{record.levelname:8}]",
            f"[{record.name}]"
        ]
        
        if player_id:
            parts.append(f"[Player:{player_id}]")
        if game_phase:
            parts.append(f"[Phase:{game_phase}]")
        if action_type:
            parts.append(f"[Action:{action_type}]")
        
        parts.append(f"- {record.getMessage()}")
        
        return " ".join(parts)
    
    def _format_json(self, record: logging.LogRecord) -> str:
        """JSON格式"""
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # 添加游戏相关字段
        game_fields = ['player_id', 'game_phase', 'action_type', 'event_type', 'performance_data']
        for field in game_fields:
            if hasattr(record, field):
                log_data[field] = getattr(record, field)
        
        # 添加异常信息
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)
    
    def _format_game(self, record: logging.LogRecord) -> str:
        """游戏专用格式"""
        timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")
        
        # 根据日志级别使用不同的符号
        level_symbols = {
            'DEBUG': '🔍',
            'INFO': '[信息]',
            'WARNING': '[警告]',
            'ERROR': '[错误]',
            'CRITICAL': '🚨'
        }
        
        symbol = level_symbols.get(record.levelname, '[笔]')
        
        # 构建游戏风格的日志
        message = record.getMessage()
        
        # 如果有玩家信息，添加玩家标识
        if hasattr(record, 'player_id'):
            player_id = getattr(record, 'player_id')
            message = f"[玩家{player_id}] {message}"
        
        return f"{timestamp} {symbol} {message}"

class PerformanceLogger:
    """性能日志记录器"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.timers: Dict[str, float] = {}
    
    def start_timer(self, name: str) -> None:
        """开始计时"""
        self.timers[name] = time.time()
    
    def end_timer(self, name: str, log_level: LogLevel = LogLevel.DEBUG) -> float:
        """结束计时并记录"""
        if name not in self.timers:
            self.logger.warning(f"计时器 '{name}' 未找到")
            return 0.0
        
        elapsed = time.time() - self.timers[name]
        del self.timers[name]
        
        # 记录性能日志
        self.logger.log(
            log_level.value,
            f"性能统计: {name} 耗时 {elapsed:.3f}秒",
            extra={"performance_data": {"operation": name, "elapsed_time": elapsed}}
        )
        
        return elapsed
    
    def log_memory_usage(self, context: str = "") -> None:
        """记录内存使用情况"""
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            
            self.logger.debug(
                f"内存使用 {context}: RSS={memory_info.rss / 1024 / 1024:.1f}MB, "
                f"VMS={memory_info.vms / 1024 / 1024:.1f}MB",
                extra={"performance_data": {
                    "context": context,
                    "rss_mb": memory_info.rss / 1024 / 1024,
                    "vms_mb": memory_info.vms / 1024 / 1024
                }}
            )
        except ImportError:
            self.logger.debug("psutil 未安装，无法记录内存使用情况")

class GameLogger:
    """游戏日志管理器"""
    
    def __init__(self, config: LogConfig):
        self.config = config
        self.loggers: Dict[str, logging.Logger] = {}
        self.performance_logger: Optional[PerformanceLogger] = None
        
        # 创建日志目录
        self._ensure_log_directory()
        
        # 配置根日志器
        self._configure_root_logger()
        
        # 创建性能日志器
        if config.enable_performance:
            self.performance_logger = PerformanceLogger(self.get_logger("performance"))
    
    def _ensure_log_directory(self) -> None:
        """确保日志目录存在"""
        log_path = Path(self.config.log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
    
    def _configure_root_logger(self) -> None:
        """配置根日志器"""
        root_logger = logging.getLogger()
        root_logger.setLevel(self.config.level.value)
        
        # 清除现有处理器
        root_logger.handlers.clear()
        
        # 创建格式化器
        formatter = GameLogFormatter(self.config.format_type)
        
        # 控制台处理器
        if self.config.enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.config.level.value)
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)
        
        # 文件处理器
        if self.config.enable_file:
            # 主日志文件
            main_log_file = os.path.join(self.config.log_dir, "tianjibian.log")
            file_handler = logging.handlers.RotatingFileHandler(
                main_log_file,
                maxBytes=self.config.max_file_size,
                backupCount=self.config.backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(self.config.level.value)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
            
            # 错误日志文件
            error_log_file = os.path.join(self.config.log_dir, "errors.log")
            error_handler = logging.handlers.RotatingFileHandler(
                error_log_file,
                maxBytes=self.config.max_file_size,
                backupCount=self.config.backup_count,
                encoding='utf-8'
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(formatter)
            root_logger.addHandler(error_handler)
            
            # 游戏事件日志文件
            if self.config.enable_game_events:
                game_log_file = os.path.join(self.config.log_dir, "game_events.log")
                game_handler = logging.handlers.RotatingFileHandler(
                    game_log_file,
                    maxBytes=self.config.max_file_size,
                    backupCount=self.config.backup_count,
                    encoding='utf-8'
                )
                game_handler.setLevel(logging.INFO)
                game_handler.setFormatter(GameLogFormatter(LogFormat.GAME))
                
                # 只记录游戏事件
                game_handler.addFilter(lambda record: hasattr(record, 'event_type') or 'game' in record.name.lower())
                root_logger.addHandler(game_handler)
    
    def get_logger(self, name: str) -> logging.Logger:
        """
        获取指定名称的日志器
        
        Args:
            name: 日志器名称
            
        Returns:
            日志器实例
        """
        if name not in self.loggers:
            self.loggers[name] = logging.getLogger(name)
        
        return self.loggers[name]
    
    def log_game_event(
        self, 
        message: str, 
        level: LogLevel = LogLevel.INFO,
        player_id: Optional[str] = None,
        game_phase: Optional[str] = None,
        action_type: Optional[str] = None,
        event_type: Optional[str] = None,
        **kwargs
    ) -> None:
        """
        记录游戏事件
        
        Args:
            message: 日志消息
            level: 日志级别
            player_id: 玩家ID
            game_phase: 游戏阶段
            action_type: 行动类型
            event_type: 事件类型
            **kwargs: 其他参数
        """
        logger = self.get_logger("game_events")
        
        # 构建额外信息
        extra = {}
        if player_id:
            extra['player_id'] = player_id
        if game_phase:
            extra['game_phase'] = game_phase
        if action_type:
            extra['action_type'] = action_type
        if event_type:
            extra['event_type'] = event_type
        
        extra.update(kwargs)
        
        logger.log(level.value, message, extra=extra)
    
    def log_player_action(
        self, 
        player_id: str, 
        action: str, 
        details: Optional[Dict[str, Any]] = None,
        success: bool = True
    ) -> None:
        """
        记录玩家行动
        
        Args:
            player_id: 玩家ID
            action: 行动描述
            details: 行动详情
            success: 是否成功
        """
        level = LogLevel.INFO if success else LogLevel.WARNING
        message = f"玩家行动: {action}"
        
        if details:
            message += f" - {details}"
        
        self.log_game_event(
            message,
            level=level,
            player_id=player_id,
            action_type=action,
            event_type="player_action",
            success=success,
            details=details
        )
    
    def log_system_event(
        self, 
        system: str, 
        event: str, 
        details: Optional[Dict[str, Any]] = None,
        level: LogLevel = LogLevel.INFO
    ) -> None:
        """
        记录系统事件
        
        Args:
            system: 系统名称
            event: 事件描述
            details: 事件详情
            level: 日志级别
        """
        message = f"系统事件 [{system}]: {event}"
        
        if details:
            message += f" - {details}"
        
        self.log_game_event(
            message,
            level=level,
            event_type="system_event",
            system=system,
            details=details
        )
    
    def get_performance_logger(self) -> Optional[PerformanceLogger]:
        """获取性能日志器"""
        return self.performance_logger
    
    def set_level(self, level: LogLevel) -> None:
        """设置日志级别"""
        self.config.level = level
        
        # 更新所有处理器的级别
        root_logger = logging.getLogger()
        root_logger.setLevel(level.value)
        
        for handler in root_logger.handlers:
            if not isinstance(handler, logging.handlers.RotatingFileHandler) or "errors.log" not in str(handler.baseFilename):
                handler.setLevel(level.value)
    
    def get_log_files(self) -> List[str]:
        """获取所有日志文件路径"""
        log_files = []
        log_dir = Path(self.config.log_dir)
        
        if log_dir.exists():
            for file_path in log_dir.glob("*.log*"):
                log_files.append(str(file_path))
        
        return sorted(log_files)
    
    def cleanup_old_logs(self, days: int = 7) -> int:
        """
        清理旧日志文件
        
        Args:
            days: 保留天数
            
        Returns:
            删除的文件数量
        """
        deleted_count = 0
        log_dir = Path(self.config.log_dir)
        
        if not log_dir.exists():
            return 0
        
        cutoff_time = time.time() - (days * 24 * 60 * 60)
        
        for file_path in log_dir.glob("*.log*"):
            if file_path.stat().st_mtime < cutoff_time:
                try:
                    file_path.unlink()
                    deleted_count += 1
                except OSError as e:
                    self.get_logger("system").warning(f"删除日志文件失败: {file_path}, 错误: {e}")
        
        return deleted_count

# ==================== 全局日志管理器 ====================

# 默认配置
default_config = LogConfig()

# 全局日志管理器实例
_global_logger: Optional[GameLogger] = None

def initialize_logging(config: Optional[LogConfig] = None) -> GameLogger:
    """
    初始化全局日志系统
    
    Args:
        config: 日志配置
        
    Returns:
        游戏日志管理器
    """
    global _global_logger
    
    if config is None:
        config = default_config
    
    _global_logger = GameLogger(config)
    return _global_logger

def get_logger(name: str = "tianjibian") -> logging.Logger:
    """
    获取日志器
    
    Args:
        name: 日志器名称
        
    Returns:
        日志器实例
    """
    if _global_logger is None:
        initialize_logging()
    
    return _global_logger.get_logger(name)

def get_game_logger() -> GameLogger:
    """获取游戏日志管理器"""
    if _global_logger is None:
        initialize_logging()
    
    return _global_logger

# ==================== 便捷函数 ====================

def log_game_event(message: str, **kwargs) -> None:
    """记录游戏事件的便捷函数"""
    get_game_logger().log_game_event(message, **kwargs)

def log_player_action(player_id: str, action: str, **kwargs) -> None:
    """记录玩家行动的便捷函数"""
    get_game_logger().log_player_action(player_id, action, **kwargs)

def log_system_event(system: str, event: str, **kwargs) -> None:
    """记录系统事件的便捷函数"""
    get_game_logger().log_system_event(system, event, **kwargs)

# ==================== 装饰器 ====================

def log_performance(operation_name: Optional[str] = None):
    """性能日志装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            name = operation_name or f"{func.__module__}.{func.__name__}"
            perf_logger = get_game_logger().get_performance_logger()
            
            if perf_logger:
                perf_logger.start_timer(name)
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    perf_logger.end_timer(name)
            else:
                return func(*args, **kwargs)
        
        return wrapper
    return decorator

def log_exceptions(logger_name: str = "exceptions"):
    """异常日志装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger = get_logger(logger_name)
                logger.exception(f"函数 {func.__name__} 执行异常: {e}")
                raise
        
        return wrapper
    return decorator