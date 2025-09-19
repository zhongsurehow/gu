"""
天机变游戏系统模块
包含配置管理、易学系统等核心系统组件
"""

from .config_system import (
    ConfigManager, GameConfig, ConfigField, ConfigValidator,
    RangeValidator, ChoiceValidator, TypeValidator,
    get_config_manager, get_config, set_config,
    config_required, with_config
)

from .yixue_system import (
    # 枚举
    CultivationLevel, ElementalReaction, BaguaRelation,
    
    # 数据类
    WuxingState, BaguaState, YinyangState, CultivationState,
    
    # 系统类
    WuxingSystem, BaguaSystem, YinyangSystem, CultivationSystem,
    UltimateYixueSystem,
    
    # 工厂函数
    create_default_wuxing_state, create_default_bagua_state,
    create_default_yinyang_state, create_default_cultivation_state,
    create_yixue_system
)

__all__ = [
    # 配置系统
    'ConfigManager', 'GameConfig', 'ConfigField', 'ConfigValidator',
    'RangeValidator', 'ChoiceValidator', 'TypeValidator',
    'get_config_manager', 'get_config', 'set_config',
    'config_required', 'with_config',
    
    # 易学系统 - 枚举
    'CultivationLevel', 'ElementalReaction', 'BaguaRelation',
    
    # 易学系统 - 数据类
    'WuxingState', 'BaguaState', 'YinyangState', 'CultivationState',
    
    # 易学系统 - 系统类
    'WuxingSystem', 'BaguaSystem', 'YinyangSystem', 'CultivationSystem',
    'UltimateYixueSystem',
    
    # 易学系统 - 工厂函数
    'create_default_wuxing_state', 'create_default_bagua_state',
    'create_default_yinyang_state', 'create_default_cultivation_state',
    'create_yixue_system'
]

__version__ = "1.0.0"