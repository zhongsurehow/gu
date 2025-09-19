"""
工具模块包
提供游戏开发中常用的工具和实用函数
"""

from .helpers import (
    # 数据验证
    validate_position, validate_player_id, validate_action_type,
    validate_config_value, validate_game_state,
    
    # 数据转换
    position_to_string, string_to_position, serialize_game_data,
    deserialize_game_data, convert_coordinates,
    
    # 数学计算
    calculate_distance, calculate_direction, normalize_angle,
    interpolate_value, clamp_value,
    
    # 字符串处理
    format_time, format_number, truncate_string,
    sanitize_input, generate_id,
    
    # 文件操作
    ensure_directory, safe_file_write, safe_file_read,
    backup_file, cleanup_temp_files,
    
    # 调试工具
    debug_print, log_function_call, measure_time,
    create_debug_info, format_debug_output
)

from .performance import (
    # 性能分析
    PerformanceProfiler, PerformanceMetrics, SystemMetrics,
    MemoryTracker, PerformanceOptimizer,
    
    # 装饰器
    performance_monitor, track_memory,
    
    # 上下文管理器
    performance_context,
    
    # 便捷函数
    start_profiling, stop_profiling, get_performance_report,
    get_memory_report, clear_all_metrics, print_performance_summary,
    start_system_monitoring
)

__all__ = [
    # 数据验证
    'validate_position', 'validate_player_id', 'validate_action_type',
    'validate_config_value', 'validate_game_state',
    
    # 数据转换
    'position_to_string', 'string_to_position', 'serialize_game_data',
    'deserialize_game_data', 'convert_coordinates',
    
    # 数学计算
    'calculate_distance', 'calculate_direction', 'normalize_angle',
    'interpolate_value', 'clamp_value',
    
    # 字符串处理
    'format_time', 'format_number', 'truncate_string',
    'sanitize_input', 'generate_id',
    
    # 文件操作
    'ensure_directory', 'safe_file_write', 'safe_file_read',
    'backup_file', 'cleanup_temp_files',
    
    # 调试工具
    'debug_print', 'log_function_call', 'measure_time',
    'create_debug_info', 'format_debug_output',
    
    # 性能分析
    'PerformanceProfiler', 'PerformanceMetrics', 'SystemMetrics',
    'MemoryTracker', 'PerformanceOptimizer',
    
    # 装饰器
    'performance_monitor', 'track_memory',
    
    # 上下文管理器
    'performance_context',
    
    # 便捷函数
    'start_profiling', 'stop_profiling', 'get_performance_report',
    'get_memory_report', 'clear_all_metrics', 'print_performance_summary',
    'start_system_monitoring'
]

# 版本信息
__version__ = "1.0.0"