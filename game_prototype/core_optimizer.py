#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核心引擎优化模块
提供代码重构、性能优化和架构改进功能
"""

import ast
import os
import sys
import time
import json
import logging
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import importlib.util

class OptimizationType(Enum):
    """优化类型"""
    CODE_REFACTOR = "code_refactor"
    PERFORMANCE = "performance"
    ARCHITECTURE = "architecture"
    MEMORY = "memory"
    ALGORITHM = "algorithm"

class CodeQuality(Enum):
    """代码质量等级"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"

@dataclass
class CodeMetrics:
    """代码度量指标"""
    lines_of_code: int = 0
    cyclomatic_complexity: int = 0
    function_count: int = 0
    class_count: int = 0
    import_count: int = 0
    comment_ratio: float = 0.0
    duplication_ratio: float = 0.0
    test_coverage: float = 0.0

@dataclass
class OptimizationSuggestion:
    """优化建议"""
    type: OptimizationType
    priority: str  # high, medium, low
    description: str
    file_path: str
    line_number: Optional[int] = None
    estimated_impact: str = "medium"  # high, medium, low
    implementation_effort: str = "medium"  # high, medium, low

@dataclass
class RefactorReport:
    """重构报告"""
    file_path: str
    original_metrics: CodeMetrics
    optimized_metrics: CodeMetrics
    suggestions: List[OptimizationSuggestion] = field(default_factory=list)
    quality_score: float = 0.0
    quality_grade: CodeQuality = CodeQuality.FAIR

class CodeAnalyzer:
    """代码分析器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def analyze_file(self, file_path: str) -> CodeMetrics:
        """分析单个文件的代码度量"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            metrics = CodeMetrics()
            metrics.lines_of_code = len(content.splitlines())
            metrics.function_count = len([node for node in ast.walk(tree) 
                                        if isinstance(node, ast.FunctionDef)])
            metrics.class_count = len([node for node in ast.walk(tree) 
                                     if isinstance(node, ast.ClassDef)])
            metrics.import_count = len([node for node in ast.walk(tree) 
                                      if isinstance(node, (ast.Import, ast.ImportFrom))])
            
            # 计算注释比例
            comment_lines = len([line for line in content.splitlines() 
                               if line.strip().startswith('#')])
            metrics.comment_ratio = comment_lines / max(metrics.lines_of_code, 1)
            
            # 计算圈复杂度
            metrics.cyclomatic_complexity = self._calculate_complexity(tree)
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"分析文件 {file_path} 时出错: {e}")
            return CodeMetrics()
    
    def _calculate_complexity(self, tree: ast.AST) -> int:
        """计算圈复杂度"""
        complexity = 1  # 基础复杂度
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.With):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
    
    def detect_code_smells(self, file_path: str) -> List[OptimizationSuggestion]:
        """检测代码异味"""
        suggestions = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # 检测长函数
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_lines = node.end_lineno - node.lineno + 1
                    if func_lines > 50:
                        suggestions.append(OptimizationSuggestion(
                            type=OptimizationType.CODE_REFACTOR,
                            priority="medium",
                            description=f"函数 {node.name} 过长 ({func_lines} 行)，建议拆分",
                            file_path=file_path,
                            line_number=node.lineno
                        ))
            
            # 检测深层嵌套
            self._check_nesting_depth(tree, file_path, suggestions)
            
            # 检测重复代码
            self._check_code_duplication(content, file_path, suggestions)
            
        except Exception as e:
            self.logger.error(f"检测代码异味时出错: {e}")
        
        return suggestions
    
    def _check_nesting_depth(self, tree: ast.AST, file_path: str, 
                           suggestions: List[OptimizationSuggestion]):
        """检查嵌套深度"""
        def get_depth(node, current_depth=0):
            max_depth = current_depth
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.If, ast.While, ast.For, ast.With)):
                    child_depth = get_depth(child, current_depth + 1)
                    max_depth = max(max_depth, child_depth)
            return max_depth
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                depth = get_depth(node)
                if depth > 4:
                    suggestions.append(OptimizationSuggestion(
                        type=OptimizationType.CODE_REFACTOR,
                        priority="high",
                        description=f"函数 {node.name} 嵌套过深 (深度: {depth})，建议重构",
                        file_path=file_path,
                        line_number=node.lineno
                    ))
    
    def _check_code_duplication(self, content: str, file_path: str, 
                              suggestions: List[OptimizationSuggestion]):
        """检查代码重复"""
        lines = content.splitlines()
        line_groups = {}
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            if len(stripped) > 10 and not stripped.startswith('#'):
                if stripped in line_groups:
                    line_groups[stripped].append(i + 1)
                else:
                    line_groups[stripped] = [i + 1]
        
        for line, occurrences in line_groups.items():
            if len(occurrences) > 2:
                suggestions.append(OptimizationSuggestion(
                    type=OptimizationType.CODE_REFACTOR,
                    priority="medium",
                    description=f"发现重复代码: '{line[:50]}...' (出现 {len(occurrences)} 次)",
                    file_path=file_path,
                    line_number=occurrences[0]
                ))

class PerformanceOptimizer:
    """性能优化器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def analyze_performance_bottlenecks(self, file_path: str) -> List[OptimizationSuggestion]:
        """分析性能瓶颈"""
        suggestions = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # 检测低效的循环
            self._check_inefficient_loops(tree, file_path, suggestions)
            
            # 检测不必要的计算
            self._check_redundant_computations(tree, file_path, suggestions)
            
            # 检测内存泄漏风险
            self._check_memory_leaks(tree, file_path, suggestions)
            
        except Exception as e:
            self.logger.error(f"分析性能瓶颈时出错: {e}")
        
        return suggestions
    
    def _check_inefficient_loops(self, tree: ast.AST, file_path: str, 
                               suggestions: List[OptimizationSuggestion]):
        """检查低效循环"""
        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                # 检查嵌套循环
                nested_loops = [child for child in ast.walk(node) 
                              if isinstance(child, (ast.For, ast.While)) and child != node]
                if len(nested_loops) >= 2:
                    suggestions.append(OptimizationSuggestion(
                        type=OptimizationType.PERFORMANCE,
                        priority="high",
                        description="发现多重嵌套循环，可能影响性能",
                        file_path=file_path,
                        line_number=node.lineno
                    ))
    
    def _check_redundant_computations(self, tree: ast.AST, file_path: str, 
                                    suggestions: List[OptimizationSuggestion]):
        """检查冗余计算"""
        # 这里可以添加更复杂的分析逻辑
        pass
    
    def _check_memory_leaks(self, tree: ast.AST, file_path: str, 
                          suggestions: List[OptimizationSuggestion]):
        """检查内存泄漏风险"""
        # 检查未关闭的文件句柄
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if (isinstance(node.func, ast.Name) and 
                    node.func.id == 'open'):
                    # 检查是否在with语句中
                    parent = node
                    in_with = False
                    # 这里需要更复杂的AST遍历逻辑
                    if not in_with:
                        suggestions.append(OptimizationSuggestion(
                            type=OptimizationType.MEMORY,
                            priority="medium",
                            description="建议使用 with 语句管理文件资源",
                            file_path=file_path,
                            line_number=node.lineno
                        ))

class ArchitectureOptimizer:
    """架构优化器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def analyze_architecture(self, project_path: str) -> List[OptimizationSuggestion]:
        """分析项目架构"""
        suggestions = []
        
        # 分析模块依赖
        dependencies = self._analyze_dependencies(project_path)
        
        # 检查循环依赖
        circular_deps = self._detect_circular_dependencies(dependencies)
        if circular_deps:
            suggestions.append(OptimizationSuggestion(
                type=OptimizationType.ARCHITECTURE,
                priority="high",
                description=f"发现循环依赖: {circular_deps}",
                file_path=project_path
            ))
        
        # 检查模块耦合度
        coupling_issues = self._analyze_coupling(dependencies)
        suggestions.extend(coupling_issues)
        
        return suggestions
    
    def _analyze_dependencies(self, project_path: str) -> Dict[str, Set[str]]:
        """分析模块依赖关系"""
        dependencies = {}
        
        for py_file in Path(project_path).glob("*.py"):
            if py_file.name.startswith('__'):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                imports = set()
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.add(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.add(node.module)
                
                dependencies[py_file.stem] = imports
                
            except Exception as e:
                self.logger.error(f"分析依赖时出错: {e}")
        
        return dependencies
    
    def _detect_circular_dependencies(self, dependencies: Dict[str, Set[str]]) -> List[str]:
        """检测循环依赖"""
        # 简化的循环依赖检测
        circular = []
        
        for module, deps in dependencies.items():
            for dep in deps:
                if dep in dependencies and module in dependencies[dep]:
                    circular.append(f"{module} <-> {dep}")
        
        return circular
    
    def _analyze_coupling(self, dependencies: Dict[str, Set[str]]) -> List[OptimizationSuggestion]:
        """分析模块耦合度"""
        suggestions = []
        
        for module, deps in dependencies.items():
            if len(deps) > 10:
                suggestions.append(OptimizationSuggestion(
                    type=OptimizationType.ARCHITECTURE,
                    priority="medium",
                    description=f"模块 {module} 依赖过多 ({len(deps)} 个)，建议解耦",
                    file_path=f"{module}.py"
                ))
        
        return suggestions

class CoreOptimizer:
    """核心优化器"""
    
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.code_analyzer = CodeAnalyzer()
        self.performance_optimizer = PerformanceOptimizer()
        self.architecture_optimizer = ArchitectureOptimizer()
        self.logger = logging.getLogger(__name__)
    
    def run_full_optimization_analysis(self) -> Dict[str, Any]:
        """运行完整的优化分析"""
        print("🔍 开始核心代码优化分析...")
        
        results = {
            'files_analyzed': 0,
            'total_suggestions': 0,
            'reports': [],
            'summary': {
                'code_quality': {},
                'performance_issues': 0,
                'architecture_issues': 0,
                'refactor_suggestions': 0
            }
        }
        
        # 分析所有Python文件
        for py_file in Path(self.project_path).glob("*.py"):
            if py_file.name.startswith('__'):
                continue
            
            print(f"📊 分析文件: {py_file.name}")
            report = self._analyze_single_file(str(py_file))
            results['reports'].append(report)
            results['files_analyzed'] += 1
            results['total_suggestions'] += len(report.suggestions)
        
        # 架构分析
        print("🏗️ 分析项目架构...")
        arch_suggestions = self.architecture_optimizer.analyze_architecture(self.project_path)
        results['summary']['architecture_issues'] = len(arch_suggestions)
        
        # 汇总统计
        self._generate_summary(results)
        
        print(f"✅ 分析完成！共分析 {results['files_analyzed']} 个文件")
        print(f"📋 发现 {results['total_suggestions']} 个优化建议")
        
        return results
    
    def _analyze_single_file(self, file_path: str) -> RefactorReport:
        """分析单个文件"""
        report = RefactorReport(
            file_path=file_path,
            original_metrics=self.code_analyzer.analyze_file(file_path),
            optimized_metrics=CodeMetrics()  # 优化后的度量
        )
        
        # 代码异味检测
        code_smells = self.code_analyzer.detect_code_smells(file_path)
        report.suggestions.extend(code_smells)
        
        # 性能分析
        perf_issues = self.performance_optimizer.analyze_performance_bottlenecks(file_path)
        report.suggestions.extend(perf_issues)
        
        # 计算质量分数
        report.quality_score = self._calculate_quality_score(report.original_metrics, report.suggestions)
        report.quality_grade = self._get_quality_grade(report.quality_score)
        
        return report
    
    def _calculate_quality_score(self, metrics: CodeMetrics, 
                               suggestions: List[OptimizationSuggestion]) -> float:
        """计算代码质量分数"""
        base_score = 100.0
        
        # 根据度量指标扣分
        if metrics.cyclomatic_complexity > 10:
            base_score -= (metrics.cyclomatic_complexity - 10) * 2
        
        if metrics.comment_ratio < 0.1:
            base_score -= 10
        
        # 根据建议扣分
        for suggestion in suggestions:
            if suggestion.priority == "high":
                base_score -= 15
            elif suggestion.priority == "medium":
                base_score -= 10
            else:
                base_score -= 5
        
        return max(0, min(100, base_score))
    
    def _get_quality_grade(self, score: float) -> CodeQuality:
        """获取质量等级"""
        if score >= 90:
            return CodeQuality.EXCELLENT
        elif score >= 80:
            return CodeQuality.GOOD
        elif score >= 70:
            return CodeQuality.FAIR
        elif score >= 60:
            return CodeQuality.POOR
        else:
            return CodeQuality.CRITICAL
    
    def _generate_summary(self, results: Dict[str, Any]):
        """生成汇总信息"""
        quality_counts = {}
        perf_count = 0
        refactor_count = 0
        
        for report in results['reports']:
            grade = report.quality_grade.value
            quality_counts[grade] = quality_counts.get(grade, 0) + 1
            
            for suggestion in report.suggestions:
                if suggestion.type == OptimizationType.PERFORMANCE:
                    perf_count += 1
                elif suggestion.type == OptimizationType.CODE_REFACTOR:
                    refactor_count += 1
        
        results['summary']['code_quality'] = quality_counts
        results['summary']['performance_issues'] = perf_count
        results['summary']['refactor_suggestions'] = refactor_count
    
    def generate_optimization_report(self, results: Dict[str, Any]) -> str:
        """生成优化报告"""
        report = []
        report.append("=" * 60)
        report.append("🔧 核心代码优化分析报告")
        report.append("=" * 60)
        report.append("")
        
        # 总体统计
        report.append("📊 总体统计:")
        report.append(f"   分析文件数: {results['files_analyzed']}")
        report.append(f"   优化建议数: {results['total_suggestions']}")
        report.append("")
        
        # 代码质量分布
        report.append("🎯 代码质量分布:")
        for grade, count in results['summary']['code_quality'].items():
            report.append(f"   {grade}: {count} 个文件")
        report.append("")
        
        # 问题分类
        report.append("🔍 问题分类:")
        report.append(f"   性能问题: {results['summary']['performance_issues']}")
        report.append(f"   重构建议: {results['summary']['refactor_suggestions']}")
        report.append(f"   架构问题: {results['summary']['architecture_issues']}")
        report.append("")
        
        # 详细建议
        report.append("📋 详细建议:")
        for file_report in results['reports']:
            if file_report.suggestions:
                report.append(f"\n📁 {Path(file_report.file_path).name}:")
                report.append(f"   质量评级: {file_report.quality_grade.value}")
                report.append(f"   质量分数: {file_report.quality_score:.1f}")
                
                for suggestion in file_report.suggestions[:3]:  # 只显示前3个建议
                    report.append(f"   • {suggestion.description}")
        
        return "\n".join(report)
    
    def export_results(self, results: Dict[str, Any], output_file: str):
        """导出结果到文件"""
        try:
            # 转换为可序列化的格式
            serializable_results = self._make_serializable(results)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(serializable_results, f, ensure_ascii=False, indent=2)
            
            print(f"📄 结果已导出到: {output_file}")
            
        except Exception as e:
            self.logger.error(f"导出结果时出错: {e}")
    
    def _make_serializable(self, obj):
        """将对象转换为可序列化的格式"""
        if isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            return self._make_serializable(obj.__dict__)
        elif isinstance(obj, Enum):
            return obj.value
        else:
            return obj

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="核心代码优化分析工具")
    parser.add_argument("--project", default=".", help="项目路径")
    parser.add_argument("--output", default="optimization_report.json", help="输出文件")
    parser.add_argument("--verbose", action="store_true", help="详细输出")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    
    optimizer = CoreOptimizer(args.project)
    results = optimizer.run_full_optimization_analysis()
    
    # 生成报告
    report = optimizer.generate_optimization_report(results)
    print(report)
    
    # 导出结果
    optimizer.export_results(results, args.output)

if __name__ == "__main__":
    main()