"""
性能分析和优化工具
提供游戏性能监控、分析和优化功能
"""

import time
import functools
import cProfile
import pstats
import io
import threading
import psutil
import gc
from typing import Dict, List, Any, Callable, Optional, Union
from dataclasses import dataclass, field
from collections import defaultdict, deque
from contextlib import contextmanager
import weakref

@dataclass
class PerformanceMetrics:
    """性能指标数据类"""
    function_name: str
    call_count: int = 0
    total_time: float = 0.0
    average_time: float = 0.0
    min_time: float = float('inf')
    max_time: float = 0.0
    memory_usage: float = 0.0
    
    def update(self, execution_time: float, memory_delta: float = 0.0) -> None:
        """更新性能指标"""
        self.call_count += 1
        self.total_time += execution_time
        self.average_time = self.total_time / self.call_count
        self.min_time = min(self.min_time, execution_time)
        self.max_time = max(self.max_time, execution_time)
        self.memory_usage += memory_delta

@dataclass
class SystemMetrics:
    """系统性能指标"""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_used: float  # MB
    memory_available: float  # MB
    
class PerformanceProfiler:
    """性能分析器"""
    
    def __init__(self, max_history: int = 1000):
        self.metrics: Dict[str, PerformanceMetrics] = {}
        self.system_metrics: deque = deque(maxlen=max_history)
        self.profiler: Optional[cProfile.Profile] = None
        self.monitoring_active: bool = False
        self._lock = threading.Lock()
        
    def start_profiling(self) -> None:
        """开始性能分析"""
        with self._lock:
            if self.profiler is None:
                self.profiler = cProfile.Profile()
                self.profiler.enable()
                self.monitoring_active = True
    
    def stop_profiling(self) -> str:
        """停止性能分析并返回报告"""
        with self._lock:
            if self.profiler is not None:
                self.profiler.disable()
                
                # 生成报告
                s = io.StringIO()
                ps = pstats.Stats(self.profiler, stream=s)
                ps.sort_stats('cumulative')
                ps.print_stats()
                
                self.profiler = None
                self.monitoring_active = False
                
                return s.getvalue()
        return "没有活动的性能分析会话"
    
    def record_function_call(self, func_name: str, execution_time: float, 
                           memory_delta: float = 0.0) -> None:
        """记录函数调用性能"""
        with self._lock:
            if func_name not in self.metrics:
                self.metrics[func_name] = PerformanceMetrics(func_name)
            
            self.metrics[func_name].update(execution_time, memory_delta)
    
    def record_system_metrics(self) -> None:
        """记录系统性能指标"""
        try:
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            
            metrics = SystemMetrics(
                timestamp=time.time(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_used=memory.used / 1024 / 1024,  # 转换为MB
                memory_available=memory.available / 1024 / 1024
            )
            
            self.system_metrics.append(metrics)
            
        except Exception as e:
            print(f"记录系统指标时出错: {e}")
    
    def get_performance_report(self) -> Dict[str, Any]:
        """获取性能报告"""
        with self._lock:
            # 函数性能统计
            function_stats = []
            for metrics in self.metrics.values():
                function_stats.append({
                    'function': metrics.function_name,
                    'calls': metrics.call_count,
                    'total_time': round(metrics.total_time, 4),
                    'avg_time': round(metrics.average_time, 4),
                    'min_time': round(metrics.min_time, 4),
                    'max_time': round(metrics.max_time, 4),
                    'memory_usage': round(metrics.memory_usage, 2)
                })
            
            # 按总时间排序
            function_stats.sort(key=lambda x: x['total_time'], reverse=True)
            
            # 系统性能统计
            system_stats = {}
            if self.system_metrics:
                recent_metrics = list(self.system_metrics)[-10:]  # 最近10个记录
                
                system_stats = {
                    'avg_cpu': sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics),
                    'avg_memory': sum(m.memory_percent for m in recent_metrics) / len(recent_metrics),
                    'current_memory_mb': recent_metrics[-1].memory_used if recent_metrics else 0,
                    'peak_memory_mb': max(m.memory_used for m in recent_metrics) if recent_metrics else 0
                }
            
            return {
                'function_performance': function_stats,
                'system_performance': system_stats,
                'total_functions_monitored': len(self.metrics),
                'monitoring_active': self.monitoring_active
            }
    
    def clear_metrics(self) -> None:
        """清除所有性能指标"""
        with self._lock:
            self.metrics.clear()
            self.system_metrics.clear()

# 全局性能分析器实例
_global_profiler = PerformanceProfiler()

def performance_monitor(include_memory: bool = False):
    """性能监控装饰器"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = f"{func.__module__}.{func.__qualname__}"
            
            # 记录开始时的内存使用
            start_memory = 0
            if include_memory:
                gc.collect()  # 强制垃圾回收以获得准确的内存测量
                start_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            start_time = time.perf_counter()
            
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.perf_counter()
                execution_time = end_time - start_time
                
                # 计算内存变化
                memory_delta = 0
                if include_memory:
                    gc.collect()
                    end_memory = psutil.Process().memory_info().rss / 1024 / 1024
                    memory_delta = end_memory - start_memory
                
                # 记录性能指标
                _global_profiler.record_function_call(func_name, execution_time, memory_delta)
        
        return wrapper
    return decorator

@contextmanager
def performance_context(name: str):
    """性能监控上下文管理器"""
    start_time = time.perf_counter()
    start_memory = psutil.Process().memory_info().rss / 1024 / 1024
    
    try:
        yield
    finally:
        end_time = time.perf_counter()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        execution_time = end_time - start_time
        memory_delta = end_memory - start_memory
        
        _global_profiler.record_function_call(name, execution_time, memory_delta)

class MemoryTracker:
    """内存使用跟踪器"""
    
    def __init__(self):
        self.tracked_objects: Dict[str, weakref.WeakSet] = defaultdict(weakref.WeakSet)
        self.allocation_counts: Dict[str, int] = defaultdict(int)
    
    def track_object(self, obj: Any, category: str = "default") -> None:
        """跟踪对象的内存使用"""
        self.tracked_objects[category].add(obj)
        self.allocation_counts[category] += 1
    
    def get_memory_report(self) -> Dict[str, Any]:
        """获取内存使用报告"""
        report = {}
        
        for category, objects in self.tracked_objects.items():
            alive_count = len(objects)
            total_allocated = self.allocation_counts[category]
            
            report[category] = {
                'alive_objects': alive_count,
                'total_allocated': total_allocated,
                'garbage_collected': total_allocated - alive_count
            }
        
        return report

# 全局内存跟踪器
_global_memory_tracker = MemoryTracker()

def track_memory(category: str = "default"):
    """内存跟踪装饰器"""
    def decorator(cls):
        original_init = cls.__init__
        
        @functools.wraps(original_init)
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            _global_memory_tracker.track_object(self, category)
        
        cls.__init__ = new_init
        return cls
    
    return decorator

class PerformanceOptimizer:
    """性能优化器"""
    
    @staticmethod
    def optimize_function_calls(threshold_ms: float = 10.0) -> List[str]:
        """识别需要优化的慢函数"""
        report = _global_profiler.get_performance_report()
        slow_functions = []
        
        for func_stat in report['function_performance']:
            if func_stat['avg_time'] * 1000 > threshold_ms:  # 转换为毫秒
                slow_functions.append(
                    f"{func_stat['function']}: 平均 {func_stat['avg_time']*1000:.2f}ms"
                )
        
        return slow_functions
    
    @staticmethod
    def suggest_optimizations() -> List[str]:
        """提供优化建议"""
        suggestions = []
        report = _global_profiler.get_performance_report()
        
        # 检查系统性能
        if report['system_performance']:
            sys_perf = report['system_performance']
            
            if sys_perf['avg_cpu'] > 80:
                suggestions.append("CPU使用率过高，考虑优化算法复杂度或使用多线程")
            
            if sys_perf['avg_memory'] > 80:
                suggestions.append("内存使用率过高，检查内存泄漏或优化数据结构")
            
            if sys_perf['peak_memory_mb'] > 1000:  # 1GB
                suggestions.append("峰值内存使用过高，考虑使用生成器或分批处理")
        
        # 检查函数性能
        slow_functions = PerformanceOptimizer.optimize_function_calls()
        if slow_functions:
            suggestions.append("发现慢函数，需要优化:")
            suggestions.extend(f"  - {func}" for func in slow_functions[:5])  # 只显示前5个
        
        return suggestions

# 便捷函数
def start_profiling() -> None:
    """开始性能分析"""
    _global_profiler.start_profiling()

def stop_profiling() -> str:
    """停止性能分析"""
    return _global_profiler.stop_profiling()

def get_performance_report() -> Dict[str, Any]:
    """获取性能报告"""
    return _global_profiler.get_performance_report()

def get_memory_report() -> Dict[str, Any]:
    """获取内存报告"""
    return _global_memory_tracker.get_memory_report()

def clear_all_metrics() -> None:
    """清除所有性能指标"""
    _global_profiler.clear_metrics()

def print_performance_summary() -> None:
    """打印性能摘要"""
    report = get_performance_report()
    
    print("=" * 60)
    print("性能分析报告")
    print("=" * 60)
    
    # 系统性能
    if report['system_performance']:
        sys_perf = report['system_performance']
        print(f"平均CPU使用率: {sys_perf['avg_cpu']:.1f}%")
        print(f"平均内存使用率: {sys_perf['avg_memory']:.1f}%")
        print(f"当前内存使用: {sys_perf['current_memory_mb']:.1f} MB")
        print(f"峰值内存使用: {sys_perf['peak_memory_mb']:.1f} MB")
        print()
    
    # 函数性能 (前10个)
    print("函数性能统计 (前10个最耗时):")
    print("-" * 60)
    for i, func_stat in enumerate(report['function_performance'][:10], 1):
        print(f"{i:2d}. {func_stat['function']}")
        print(f"    调用次数: {func_stat['calls']}")
        print(f"    总时间: {func_stat['total_time']:.4f}s")
        print(f"    平均时间: {func_stat['avg_time']*1000:.2f}ms")
        print()
    
    # 优化建议
    suggestions = PerformanceOptimizer.suggest_optimizations()
    if suggestions:
        print("优化建议:")
        print("-" * 60)
        for suggestion in suggestions:
            print(f"• {suggestion}")
        print()

# 自动系统监控
def start_system_monitoring(interval: float = 1.0) -> threading.Timer:
    """启动系统性能监控"""
    def monitor():
        _global_profiler.record_system_metrics()
        # 递归调用以持续监控
        return start_system_monitoring(interval)
    
    timer = threading.Timer(interval, monitor)
    timer.daemon = True
    timer.start()
    return timer