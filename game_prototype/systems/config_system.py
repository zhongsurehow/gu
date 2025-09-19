"""
天机变游戏配置管理系统
提供类型安全的配置管理、验证和持久化功能
"""

import json
import os
import logging
from typing import Dict, Any, Optional, Type, TypeVar, Generic, Union, List
from dataclasses import dataclass, field, asdict
from pathlib import Path
from abc import ABC, abstractmethod
import threading

from ..core.interfaces import IConfigManager
from ..core.base_types import GamePhase, PlayerType, WuxingElement, BaguaType
from ..core.exceptions import ConfigException
from ..core.constants import *

logger = logging.getLogger(__name__)

T = TypeVar('T')

class ConfigValidator(ABC):
    """配置验证器基类"""
    
    @abstractmethod
    def validate(self, value: Any) -> bool:
        """验证配置值"""
        pass
    
    @abstractmethod
    def get_error_message(self, value: Any) -> str:
        """获取错误消息"""
        pass

class RangeValidator(ConfigValidator):
    """数值范围验证器"""
    
    def __init__(self, min_value: Union[int, float], max_value: Union[int, float]):
        self.min_value = min_value
        self.max_value = max_value
    
    def validate(self, value: Any) -> bool:
        try:
            num_value = float(value)
            return self.min_value <= num_value <= self.max_value
        except (ValueError, TypeError):
            return False
    
    def get_error_message(self, value: Any) -> str:
        return f"值 {value} 不在范围 [{self.min_value}, {self.max_value}] 内"

class ChoiceValidator(ConfigValidator):
    """选择值验证器"""
    
    def __init__(self, choices: List[Any]):
        self.choices = choices
    
    def validate(self, value: Any) -> bool:
        return value in self.choices
    
    def get_error_message(self, value: Any) -> str:
        return f"值 {value} 不在允许的选择 {self.choices} 中"

class TypeValidator(ConfigValidator):
    """类型验证器"""
    
    def __init__(self, expected_type: Type):
        self.expected_type = expected_type
    
    def validate(self, value: Any) -> bool:
        return isinstance(value, self.expected_type)
    
    def get_error_message(self, value: Any) -> str:
        return f"值 {value} 的类型 {type(value)} 不匹配期望类型 {self.expected_type}"

@dataclass
class ConfigField:
    """配置字段定义"""
    name: str
    default_value: Any
    description: str = ""
    validator: Optional[ConfigValidator] = None
    required: bool = True
    category: str = "general"

@dataclass
class GameConfig:
    """游戏配置数据类"""
    
    # ==================== 基础游戏配置 ====================
    
    # 玩家配置
    max_players: int = DEFAULT_MAX_PLAYERS
    min_players: int = DEFAULT_MIN_PLAYERS
    default_player_type: PlayerType = PlayerType.HUMAN
    
    # 资源配置
    initial_qi: int = INITIAL_QI
    initial_wisdom: int = INITIAL_WISDOM
    initial_influence: int = INITIAL_INFLUENCE
    initial_culture: int = INITIAL_CULTURE
    max_resource_value: int = MAX_RESOURCE_VALUE
    
    # 回合配置
    max_rounds: int = DEFAULT_MAX_ROUNDS
    round_time_limit: int = DEFAULT_ROUND_TIME_LIMIT  # 秒
    
    # ==================== 易学系统配置 ====================
    
    # 八卦系统
    enable_bagua_system: bool = True
    bagua_affinity_bonus: float = BAGUA_AFFINITY_BONUS
    bagua_conflict_penalty: float = BAGUA_CONFLICT_PENALTY
    
    # 五行系统
    enable_wuxing_system: bool = True
    wuxing_generation_bonus: float = WUXING_GENERATION_BONUS
    wuxing_destruction_penalty: float = WUXING_DESTRUCTION_PENALTY
    
    # 阴阳系统
    enable_yinyang_system: bool = True
    yinyang_balance_bonus: float = YINYANG_BALANCE_BONUS
    yinyang_imbalance_penalty: float = YINYANG_IMBALANCE_PENALTY
    
    # 修为系统
    enable_cultivation_system: bool = True
    cultivation_levels: List[str] = field(default_factory=lambda: [
        "凡人", "练气", "筑基", "金丹", "元婴", "化神", "炼虚", "合体", "大乘", "渡劫"
    ])
    
    # ==================== AI配置 ====================
    
    # AI难度
    ai_difficulty: str = "normal"  # easy, normal, hard, expert
    ai_thinking_time: float = 1.0  # 秒
    ai_random_factor: float = 0.1  # 随机性因子
    
    # AI策略权重
    ai_strategy_weights: Dict[str, float] = field(default_factory=lambda: {
        "resource_priority": 0.3,
        "culture_priority": 0.25,
        "influence_priority": 0.25,
        "balance_priority": 0.2
    })
    
    # ==================== UI配置 ====================
    
    # 界面设置
    enable_animations: bool = True
    animation_speed: float = 1.0
    show_tooltips: bool = True
    auto_save_interval: int = 300  # 秒
    
    # 显示设置
    show_debug_info: bool = False
    show_ai_thinking: bool = True
    highlight_valid_moves: bool = True
    
    # ==================== 平衡性配置 ====================
    
    # 行动成本
    action_costs: Dict[str, int] = field(default_factory=lambda: {
        "basic_action": ACTION_COST_BASIC,
        "special_action": ACTION_COST_SPECIAL,
        "ultimate_action": ACTION_COST_ULTIMATE
    })
    
    # 奖励倍数
    reward_multipliers: Dict[str, float] = field(default_factory=lambda: {
        "culture_bonus": 1.0,
        "wisdom_bonus": 1.0,
        "influence_bonus": 1.0
    })
    
    # ==================== 系统配置 ====================
    
    # 日志配置
    log_level: str = "INFO"
    enable_game_log: bool = True
    enable_performance_log: bool = False
    
    # 数据配置
    auto_save: bool = True
    save_format: str = "json"  # json, binary
    backup_count: int = 5
    
    # 网络配置（为未来多人游戏准备）
    enable_multiplayer: bool = False
    server_port: int = 8888
    max_connections: int = 4

class ConfigManager(IConfigManager):
    """配置管理器实现"""
    
    def __init__(self, config_file: str = "game_config.json"):
        self.config_file = Path(config_file)
        self.config = GameConfig()
        self.config_fields: Dict[str, ConfigField] = {}
        self.lock = threading.RLock()
        
        # 注册配置字段
        self._register_config_fields()
        
        # 加载配置
        self.load_config()
        
        logger.info(f"配置管理器初始化完成，配置文件: {self.config_file}")
    
    def _register_config_fields(self) -> None:
        """注册配置字段及其验证器"""
        
        # 基础游戏配置
        self.config_fields.update({
            "max_players": ConfigField(
                "max_players", DEFAULT_MAX_PLAYERS,
                "最大玩家数量",
                RangeValidator(2, 8),
                category="game"
            ),
            "min_players": ConfigField(
                "min_players", DEFAULT_MIN_PLAYERS,
                "最小玩家数量", 
                RangeValidator(2, 8),
                category="game"
            ),
            "max_rounds": ConfigField(
                "max_rounds", DEFAULT_MAX_ROUNDS,
                "最大回合数",
                RangeValidator(10, 1000),
                category="game"
            ),
            "round_time_limit": ConfigField(
                "round_time_limit", DEFAULT_ROUND_TIME_LIMIT,
                "回合时间限制（秒）",
                RangeValidator(30, 3600),
                category="game"
            )
        })
        
        # 资源配置
        self.config_fields.update({
            "initial_qi": ConfigField(
                "initial_qi", INITIAL_QI,
                "初始气值",
                RangeValidator(0, 1000),
                category="resources"
            ),
            "initial_wisdom": ConfigField(
                "initial_wisdom", INITIAL_WISDOM,
                "初始智慧值",
                RangeValidator(0, 1000),
                category="resources"
            ),
            "max_resource_value": ConfigField(
                "max_resource_value", MAX_RESOURCE_VALUE,
                "资源最大值",
                RangeValidator(100, 10000),
                category="resources"
            )
        })
        
        # 易学系统配置
        self.config_fields.update({
            "bagua_affinity_bonus": ConfigField(
                "bagua_affinity_bonus", BAGUA_AFFINITY_BONUS,
                "八卦亲和度奖励",
                RangeValidator(0.0, 2.0),
                category="yixue"
            ),
            "wuxing_generation_bonus": ConfigField(
                "wuxing_generation_bonus", WUXING_GENERATION_BONUS,
                "五行相生奖励",
                RangeValidator(0.0, 2.0),
                category="yixue"
            ),
            "yinyang_balance_bonus": ConfigField(
                "yinyang_balance_bonus", YINYANG_BALANCE_BONUS,
                "阴阳平衡奖励",
                RangeValidator(0.0, 2.0),
                category="yixue"
            )
        })
        
        # AI配置
        self.config_fields.update({
            "ai_difficulty": ConfigField(
                "ai_difficulty", "normal",
                "AI难度",
                ChoiceValidator(["easy", "normal", "hard", "expert"]),
                category="ai"
            ),
            "ai_thinking_time": ConfigField(
                "ai_thinking_time", 1.0,
                "AI思考时间（秒）",
                RangeValidator(0.1, 10.0),
                category="ai"
            ),
            "ai_random_factor": ConfigField(
                "ai_random_factor", 0.1,
                "AI随机性因子",
                RangeValidator(0.0, 1.0),
                category="ai"
            )
        })
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        with self.lock:
            try:
                return getattr(self.config, key, default)
            except AttributeError:
                logger.warning(f"配置键 '{key}' 不存在，返回默认值: {default}")
                return default
    
    def set(self, key: str, value: Any) -> None:
        """设置配置值"""
        with self.lock:
            # 验证配置
            if key in self.config_fields:
                field_def = self.config_fields[key]
                if field_def.validator and not field_def.validator.validate(value):
                    error_msg = field_def.validator.get_error_message(value)
                    raise ConfigException(f"配置验证失败 '{key}': {error_msg}")
            
            # 设置值
            if hasattr(self.config, key):
                setattr(self.config, key, value)
                logger.debug(f"配置已更新: {key} = {value}")
            else:
                logger.warning(f"配置键 '{key}' 不存在，无法设置")
                raise ConfigException(f"未知的配置键: {key}")
    
    def update(self, config_dict: Dict[str, Any]) -> None:
        """批量更新配置"""
        with self.lock:
            for key, value in config_dict.items():
                try:
                    self.set(key, value)
                except ConfigException as e:
                    logger.error(f"更新配置失败 '{key}': {e}")
                    raise
    
    def load_config(self, file_path: Optional[str] = None) -> None:
        """从文件加载配置"""
        config_file = Path(file_path) if file_path else self.config_file
        
        with self.lock:
            try:
                if config_file.exists():
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config_data = json.load(f)
                    
                    # 验证并应用配置
                    for key, value in config_data.items():
                        if hasattr(self.config, key):
                            try:
                                self.set(key, value)
                            except ConfigException as e:
                                logger.warning(f"跳过无效配置 '{key}': {e}")
                        else:
                            logger.warning(f"跳过未知配置键: {key}")
                    
                    logger.info(f"配置已从文件加载: {config_file}")
                else:
                    logger.info(f"配置文件不存在，使用默认配置: {config_file}")
                    # 创建默认配置文件
                    self.save_config()
                    
            except Exception as e:
                logger.error(f"加载配置文件失败: {e}")
                raise ConfigException(f"无法加载配置文件 {config_file}: {e}")
    
    def save_config(self, file_path: Optional[str] = None) -> None:
        """保存配置到文件"""
        config_file = Path(file_path) if file_path else self.config_file
        
        with self.lock:
            try:
                # 确保目录存在
                config_file.parent.mkdir(parents=True, exist_ok=True)
                
                # 转换为字典
                config_dict = asdict(self.config)
                
                # 保存到文件
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(config_dict, f, indent=2, ensure_ascii=False)
                
                logger.info(f"配置已保存到文件: {config_file}")
                
            except Exception as e:
                logger.error(f"保存配置文件失败: {e}")
                raise ConfigException(f"无法保存配置文件 {config_file}: {e}")
    
    def reset_to_defaults(self) -> None:
        """重置为默认配置"""
        with self.lock:
            self.config = GameConfig()
            logger.info("配置已重置为默认值")
    
    def get_config_by_category(self, category: str) -> Dict[str, Any]:
        """按类别获取配置"""
        result = {}
        
        for key, field_def in self.config_fields.items():
            if field_def.category == category:
                result[key] = self.get(key)
        
        return result
    
    def get_all_categories(self) -> List[str]:
        """获取所有配置类别"""
        categories = set()
        for field_def in self.config_fields.values():
            categories.add(field_def.category)
        
        return sorted(list(categories))
    
    def validate_all_config(self) -> Dict[str, str]:
        """验证所有配置，返回错误信息"""
        errors = {}
        
        for key, field_def in self.config_fields.items():
            if field_def.validator:
                value = self.get(key)
                if not field_def.validator.validate(value):
                    errors[key] = field_def.validator.get_error_message(value)
        
        return errors
    
    def get_config_info(self, key: str) -> Optional[ConfigField]:
        """获取配置字段信息"""
        return self.config_fields.get(key)
    
    def export_config(self, file_path: str, format_type: str = "json") -> None:
        """导出配置到指定格式"""
        config_dict = asdict(self.config)
        
        if format_type.lower() == "json":
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
        else:
            raise ConfigException(f"不支持的导出格式: {format_type}")
        
        logger.info(f"配置已导出到: {file_path}")
    
    def import_config(self, file_path: str, format_type: str = "json") -> None:
        """从指定格式导入配置"""
        if format_type.lower() == "json":
            with open(file_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            self.update(config_data)
        else:
            raise ConfigException(f"不支持的导入格式: {format_type}")
        
        logger.info(f"配置已从文件导入: {file_path}")

# ==================== 全局配置管理器 ====================

_global_config_manager: Optional[ConfigManager] = None

def get_config_manager() -> ConfigManager:
    """获取全局配置管理器实例"""
    global _global_config_manager
    
    if _global_config_manager is None:
        _global_config_manager = ConfigManager()
    
    return _global_config_manager

def get_config(key: str, default: Any = None) -> Any:
    """获取配置值的便捷函数"""
    return get_config_manager().get(key, default)

def set_config(key: str, value: Any) -> None:
    """设置配置值的便捷函数"""
    get_config_manager().set(key, value)

# ==================== 配置装饰器 ====================

def config_required(*config_keys):
    """配置依赖装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            config_manager = get_config_manager()
            
            # 检查必需的配置
            for key in config_keys:
                if config_manager.get(key) is None:
                    raise ConfigException(f"函数 {func.__name__} 需要配置 '{key}'")
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator

def with_config(config_key: str, default_value: Any = None):
    """配置注入装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            config_value = get_config(config_key, default_value)
            kwargs[config_key] = config_value
            return func(*args, **kwargs)
        
        return wrapper
    return decorator

# 导出列表
__all__ = [
    # 验证器
    'ConfigValidator',
    'RangeValidator', 
    'ChoiceValidator',
    'TypeValidator',
    
    # 数据类
    'ValidationResult',
    'ConfigField',
    'GameConfig',
    
    # 管理器
    'ConfigManager',
    
    # 全局实例
    'config_manager',
    
    # 装饰器
    'config_required',
    'with_config',
    
    # 类型
    'ConfigValue',
]