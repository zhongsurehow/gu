"""
游戏性能优化模块
监控游戏性能，提供优化建议和自动优化功能
"""

import time
import psutil
import gc
import sys
import threading
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging
from functools import wraps
import json

class PerformanceLevel(Enum):
    """性能等级"""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    POOR = "poor"
    CRITICAL = "critical"

class OptimizationType(Enum):
    """优化类型"""
    MEMORY = "memory"
    CPU = "cpu"
    IO = "io"
    ALGORITHM = "algorithm"
    CACHING = "caching"

@dataclass
class PerformanceMetrics:
    """性能指标"""
    timestamp: float
    cpu_usage: float
    memory_usage: float
    memory_available: float
    execution_time: float
    function_name: str
    thread_id: int
    
@dataclass
class PerformanceReport:
    """性能报告"""
    overall_score: float
    level: PerformanceLevel
    bottlenecks: List[str]
    recommendations: List[str]
    metrics_summary: Dict[str, Any]
    optimization_opportunities: List[Dict[str, Any]]

@dataclass
class OptimizationRule:
    """优化规则"""
    name: str
    condition: Callable[[PerformanceMetrics], bool]
    action: Callable[[], None]
    priority: int
    description: str

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.metrics_history: List[PerformanceMetrics] = []
        self.is_monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.optimization_rules: List[OptimizationRule] = []
        self.performance_thresholds = {
            "cpu_warning": 70.0,
            "cpu_critical": 90.0,
            "memory_warning": 80.0,
            "memory_critical": 95.0,
            "execution_time_warning": 1.0,
            "execution_time_critical": 5.0
        }
        
        self._setup_optimization_rules()
    
    def start_monitoring(self, interval: float = 1.0):
        """开始性能监控"""
        if self.is_monitoring:
            self.logger.warning("性能监控已在运行")
            return
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()
        self.logger.info("性能监控已启动")
    
    def stop_monitoring(self):
        """停止性能监控"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
        self.logger.info("性能监控已停止")
    
    def _monitoring_loop(self, interval: float):
        """监控循环"""
        while self.is_monitoring:
            try:
                metrics = self._collect_system_metrics()
                self.metrics_history.append(metrics)
                
                # 限制历史记录数量
                if len(self.metrics_history) > 1000:
                    self.metrics_history = self.metrics_history[-500:]
                
                # 检查优化规则
                self._check_optimization_rules(metrics)
                
                time.sleep(interval)
            
            except Exception as e:
                self.logger.error(f"监控循环错误: {e}")
                time.sleep(interval)
    
    def _collect_system_metrics(self) -> PerformanceMetrics:
        """收集系统性能指标"""
        process = psutil.Process()
        
        return PerformanceMetrics(
            timestamp=time.time(),
            cpu_usage=process.cpu_percent(),
            memory_usage=process.memory_percent(),
            memory_available=psutil.virtual_memory().available / (1024 * 1024),  # MB
            execution_time=0.0,  # 将在函数装饰器中设置
            function_name="system",
            thread_id=threading.get_ident()
        )
    
    def _setup_optimization_rules(self):
        """设置优化规则"""
        self.optimization_rules = [
            OptimizationRule(
                name="high_memory_usage",
                condition=lambda m: m.memory_usage > self.performance_thresholds["memory_warning"],
                action=self._optimize_memory,
                priority=1,
                description="内存使用率过高，执行内存优化"
            ),
            OptimizationRule(
                name="high_cpu_usage",
                condition=lambda m: m.cpu_usage > self.performance_thresholds["cpu_warning"],
                action=self._optimize_cpu,
                priority=2,
                description="CPU使用率过高，执行CPU优化"
            ),
            OptimizationRule(
                name="slow_execution",
                condition=lambda m: m.execution_time > self.performance_thresholds["execution_time_warning"],
                action=self._optimize_execution,
                priority=3,
                description="执行时间过长，执行算法优化"
            )
        ]
    
    def _check_optimization_rules(self, metrics: PerformanceMetrics):
        """检查优化规则"""
        for rule in sorted(self.optimization_rules, key=lambda r: r.priority):
            try:
                if rule.condition(metrics):
                    self.logger.info(f"触发优化规则: {rule.description}")
                    rule.action()
            except Exception as e:
                self.logger.error(f"执行优化规则 {rule.name} 失败: {e}")
    
    def _optimize_memory(self):
        """内存优化"""
        # 强制垃圾回收
        collected = gc.collect()
        self.logger.info(f"内存优化：回收了 {collected} 个对象")
        
        # 清理旧的性能指标
        if len(self.metrics_history) > 100:
            self.metrics_history = self.metrics_history[-50:]
            self.logger.info("清理了旧的性能指标记录")
    
    def _optimize_cpu(self):
        """CPU优化"""
        # 降低监控频率
        self.logger.info("CPU优化：建议降低监控频率或优化算法")
    
    def _optimize_execution(self):
        """执行优化"""
        self.logger.info("执行优化：建议检查算法效率和数据结构")
    
    def get_performance_report(self) -> PerformanceReport:
        """获取性能报告"""
        if not self.metrics_history:
            return PerformanceReport(
                overall_score=0.0,
                level=PerformanceLevel.CRITICAL,
                bottlenecks=["没有性能数据"],
                recommendations=["开始性能监控"],
                metrics_summary={},
                optimization_opportunities=[]
            )
        
        # 计算性能指标
        recent_metrics = self.metrics_history[-10:] if len(self.metrics_history) >= 10 else self.metrics_history
        
        avg_cpu = sum(m.cpu_usage for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m.memory_usage for m in recent_metrics) / len(recent_metrics)
        avg_execution_time = sum(m.execution_time for m in recent_metrics if m.execution_time > 0) / max(1, len([m for m in recent_metrics if m.execution_time > 0]))
        
        # 计算总体评分
        overall_score = self._calculate_overall_score(avg_cpu, avg_memory, avg_execution_time)
        
        # 确定性能等级
        level = self._determine_performance_level(overall_score)
        
        # 识别瓶颈
        bottlenecks = self._identify_bottlenecks(avg_cpu, avg_memory, avg_execution_time)
        
        # 生成建议
        recommendations = self._generate_recommendations(bottlenecks, avg_cpu, avg_memory, avg_execution_time)
        
        # 优化机会
        optimization_opportunities = self._identify_optimization_opportunities()
        
        return PerformanceReport(
            overall_score=overall_score,
            level=level,
            bottlenecks=bottlenecks,
            recommendations=recommendations,
            metrics_summary={
                "average_cpu_usage": avg_cpu,
                "average_memory_usage": avg_memory,
                "average_execution_time": avg_execution_time,
                "total_metrics_collected": len(self.metrics_history)
            },
            optimization_opportunities=optimization_opportunities
        )
    
    def _calculate_overall_score(self, cpu: float, memory: float, execution_time: float) -> float:
        """计算总体性能评分"""
        # CPU评分 (0-100)
        cpu_score = max(0, 100 - cpu)
        
        # 内存评分 (0-100)
        memory_score = max(0, 100 - memory)
        
        # 执行时间评分 (0-100)
        execution_score = max(0, 100 - min(execution_time * 20, 100))
        
        # 加权平均
        overall_score = (cpu_score * 0.4 + memory_score * 0.4 + execution_score * 0.2)
        
        return round(overall_score, 2)
    
    def _determine_performance_level(self, score: float) -> PerformanceLevel:
        """确定性能等级"""
        if score >= 85:
            return PerformanceLevel.EXCELLENT
        elif score >= 70:
            return PerformanceLevel.GOOD
        elif score >= 55:
            return PerformanceLevel.ACCEPTABLE
        elif score >= 35:
            return PerformanceLevel.POOR
        else:
            return PerformanceLevel.CRITICAL
    
    def _identify_bottlenecks(self, cpu: float, memory: float, execution_time: float) -> List[str]:
        """识别性能瓶颈"""
        bottlenecks = []
        
        if cpu > self.performance_thresholds["cpu_critical"]:
            bottlenecks.append("CPU使用率严重过高")
        elif cpu > self.performance_thresholds["cpu_warning"]:
            bottlenecks.append("CPU使用率偏高")
        
        if memory > self.performance_thresholds["memory_critical"]:
            bottlenecks.append("内存使用率严重过高")
        elif memory > self.performance_thresholds["memory_warning"]:
            bottlenecks.append("内存使用率偏高")
        
        if execution_time > self.performance_thresholds["execution_time_critical"]:
            bottlenecks.append("函数执行时间过长")
        elif execution_time > self.performance_thresholds["execution_time_warning"]:
            bottlenecks.append("函数执行时间偏长")
        
        return bottlenecks
    
    def _generate_recommendations(self, bottlenecks: List[str], cpu: float, memory: float, execution_time: float) -> List[str]:
        """生成优化建议"""
        recommendations = []
        
        if "CPU使用率" in str(bottlenecks):
            recommendations.extend([
                "优化算法复杂度，减少不必要的计算",
                "使用缓存减少重复计算",
                "考虑异步处理或多线程优化"
            ])
        
        if "内存使用率" in str(bottlenecks):
            recommendations.extend([
                "及时释放不需要的对象引用",
                "优化数据结构，减少内存占用",
                "实现对象池或缓存策略"
            ])
        
        if "执行时间" in str(bottlenecks):
            recommendations.extend([
                "分析热点函数，优化关键路径",
                "减少I/O操作或使用异步I/O",
                "优化数据库查询和数据访问"
            ])
        
        if not bottlenecks:
            recommendations.append("性能表现良好，继续保持")
        
        return recommendations
    
    def _identify_optimization_opportunities(self) -> List[Dict[str, Any]]:
        """识别优化机会"""
        opportunities = []
        
        if len(self.metrics_history) < 10:
            return opportunities
        
        # 分析函数执行时间趋势
        function_times = {}
        for metric in self.metrics_history[-50:]:
            if metric.execution_time > 0:
                func_name = metric.function_name
                if func_name not in function_times:
                    function_times[func_name] = []
                function_times[func_name].append(metric.execution_time)
        
        # 找出执行时间最长的函数
        for func_name, times in function_times.items():
            avg_time = sum(times) / len(times)
            if avg_time > 0.5:  # 超过0.5秒
                opportunities.append({
                    "type": OptimizationType.ALGORITHM.value,
                    "target": func_name,
                    "issue": f"平均执行时间 {avg_time:.2f}s",
                    "priority": "high" if avg_time > 2.0 else "medium",
                    "suggestion": "优化算法或使用缓存"
                })
        
        # 内存使用趋势分析
        recent_memory = [m.memory_usage for m in self.metrics_history[-20:]]
        if len(recent_memory) > 5:
            memory_trend = (recent_memory[-1] - recent_memory[0]) / len(recent_memory)
            if memory_trend > 1.0:  # 内存使用持续增长
                opportunities.append({
                    "type": OptimizationType.MEMORY.value,
                    "target": "system",
                    "issue": f"内存使用持续增长 {memory_trend:.2f}%/次",
                    "priority": "high",
                    "suggestion": "检查内存泄漏，优化对象生命周期"
                })
        
        return opportunities

class PerformanceProfiler:
    """性能分析器"""
    
    def __init__(self):
        self.monitor = PerformanceMonitor()
        self.function_stats: Dict[str, List[float]] = {}
        self.logger = logging.getLogger(__name__)
    
    def profile_function(self, func: Callable) -> Callable:
        """函数性能分析装饰器"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss
            
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.time()
                end_memory = psutil.Process().memory_info().rss
                
                execution_time = end_time - start_time
                memory_delta = end_memory - start_memory
                
                # 记录性能指标
                metrics = PerformanceMetrics(
                    timestamp=end_time,
                    cpu_usage=psutil.Process().cpu_percent(),
                    memory_usage=psutil.Process().memory_percent(),
                    memory_available=psutil.virtual_memory().available / (1024 * 1024),
                    execution_time=execution_time,
                    function_name=func.__name__,
                    thread_id=threading.get_ident()
                )
                
                self.monitor.metrics_history.append(metrics)
                
                # 记录函数统计
                if func.__name__ not in self.function_stats:
                    self.function_stats[func.__name__] = []
                self.function_stats[func.__name__].append(execution_time)
                
                # 如果执行时间过长，记录警告
                if execution_time > 1.0:
                    self.logger.warning(
                        f"函数 {func.__name__} 执行时间过长: {execution_time:.3f}s, "
                        f"内存变化: {memory_delta / 1024:.2f}KB"
                    )
        
        return wrapper
    
    def get_function_stats(self) -> Dict[str, Dict[str, float]]:
        """获取函数统计信息"""
        stats = {}
        
        for func_name, times in self.function_stats.items():
            if times:
                stats[func_name] = {
                    "call_count": len(times),
                    "total_time": sum(times),
                    "average_time": sum(times) / len(times),
                    "min_time": min(times),
                    "max_time": max(times)
                }
        
        return stats
    
    def get_slowest_functions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最慢的函数"""
        function_stats = self.get_function_stats()
        
        # 按平均执行时间排序
        sorted_functions = sorted(
            function_stats.items(),
            key=lambda x: x[1]["average_time"],
            reverse=True
        )
        
        return [
            {
                "function_name": func_name,
                **stats
            }
            for func_name, stats in sorted_functions[:limit]
        ]

class PerformanceOptimizer:
    """性能优化器"""
    
    def __init__(self):
        self.monitor = PerformanceMonitor()
        self.profiler = PerformanceProfiler()
        self.cache = {}
        self.cache_stats = {"hits": 0, "misses": 0}
        self.logger = logging.getLogger(__name__)
    
    def start_optimization(self):
        """开始性能优化"""
        self.monitor.start_monitoring()
        self.logger.info("性能优化器已启动")
    
    def stop_optimization(self):
        """停止性能优化"""
        self.monitor.stop_monitoring()
        self.logger.info("性能优化器已停止")
    
    def cached_function(self, cache_size: int = 128):
        """缓存装饰器"""
        def decorator(func: Callable) -> Callable:
            func_cache = {}
            
            @wraps(func)
            def wrapper(*args, **kwargs):
                # 创建缓存键
                cache_key = str(args) + str(sorted(kwargs.items()))
                
                if cache_key in func_cache:
                    self.cache_stats["hits"] += 1
                    return func_cache[cache_key]
                
                # 缓存未命中
                self.cache_stats["misses"] += 1
                result = func(*args, **kwargs)
                
                # 添加到缓存
                if len(func_cache) >= cache_size:
                    # 简单的LRU：删除第一个元素
                    first_key = next(iter(func_cache))
                    del func_cache[first_key]
                
                func_cache[cache_key] = result
                return result
            
            return wrapper
        return decorator
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        total_requests = self.cache_stats["hits"] + self.cache_stats["misses"]
        hit_rate = self.cache_stats["hits"] / total_requests if total_requests > 0 else 0
        
        return {
            "cache_hits": self.cache_stats["hits"],
            "cache_misses": self.cache_stats["misses"],
            "hit_rate": hit_rate,
            "total_requests": total_requests
        }
    
    def optimize_game_state(self, game_state) -> None:
        """优化游戏状态对象"""
        # 清理不必要的临时数据
        if hasattr(game_state, '_temp_data'):
            game_state._temp_data.clear()
        
        # 压缩历史记录
        if hasattr(game_state, 'history') and len(game_state.history) > 100:
            game_state.history = game_state.history[-50:]
        
        self.logger.debug("游戏状态已优化")
    
    def get_optimization_report(self) -> Dict[str, Any]:
        """获取优化报告"""
        performance_report = self.monitor.get_performance_report()
        function_stats = self.profiler.get_function_stats()
        cache_stats = self.get_cache_stats()
        slowest_functions = self.profiler.get_slowest_functions()
        
        return {
            "performance": performance_report.__dict__,
            "function_statistics": function_stats,
            "cache_performance": cache_stats,
            "slowest_functions": slowest_functions,
            "optimization_suggestions": self._generate_optimization_suggestions(
                performance_report, function_stats, cache_stats
            )
        }
    
    def _generate_optimization_suggestions(self, 
                                         performance_report: PerformanceReport,
                                         function_stats: Dict[str, Dict[str, float]],
                                         cache_stats: Dict[str, Any]) -> List[str]:
        """生成优化建议"""
        suggestions = []
        
        # 基于性能报告的建议
        suggestions.extend(performance_report.recommendations)
        
        # 基于函数统计的建议
        if function_stats:
            slowest_func = max(function_stats.items(), key=lambda x: x[1]["average_time"])
            if slowest_func[1]["average_time"] > 0.5:
                suggestions.append(f"优化函数 {slowest_func[0]}，平均执行时间过长")
        
        # 基于缓存统计的建议
        if cache_stats["hit_rate"] < 0.5 and cache_stats["total_requests"] > 10:
            suggestions.append("缓存命中率较低，考虑优化缓存策略")
        
        return suggestions
    
    def export_performance_data(self, filename: str = "performance_data.json"):
        """导出性能数据"""
        try:
            data = {
                "optimization_report": self.get_optimization_report(),
                "raw_metrics": [
                    {
                        "timestamp": m.timestamp,
                        "cpu_usage": m.cpu_usage,
                        "memory_usage": m.memory_usage,
                        "execution_time": m.execution_time,
                        "function_name": m.function_name
                    }
                    for m in self.monitor.metrics_history
                ]
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"性能数据已导出到 {filename}")
        
        except Exception as e:
            self.logger.error(f"导出性能数据失败: {e}")

# 全局性能优化器实例
global_optimizer = PerformanceOptimizer()

# 便捷装饰器
def profile(func: Callable) -> Callable:
    """性能分析装饰器"""
    return global_optimizer.profiler.profile_function(func)

def cached(cache_size: int = 128):
    """缓存装饰器"""
    return global_optimizer.cached_function(cache_size)

# 便捷函数
def start_performance_monitoring():
    """启动性能监控"""
    global_optimizer.start_optimization()

def stop_performance_monitoring():
    """停止性能监控"""
    global_optimizer.stop_optimization()

def get_performance_summary() -> Dict[str, Any]:
    """获取性能摘要"""
    return global_optimizer.get_optimization_report()