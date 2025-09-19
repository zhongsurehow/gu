#!/usr/bin/env python3
"""
天机变游戏测试运行器
运行所有单元测试并生成测试报告
"""

import unittest
import sys
import os
import time
from pathlib import Path
from typing import List, Dict, Any
import argparse

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def discover_tests(test_dir: str = "tests") -> unittest.TestSuite:
    """发现并加载所有测试"""
    loader = unittest.TestLoader()
    start_dir = os.path.join(project_root, test_dir)
    
    if not os.path.exists(start_dir):
        print(f"警告: 测试目录 {start_dir} 不存在")
        return unittest.TestSuite()
    
    suite = loader.discover(start_dir, pattern='test_*.py')
    return suite

def run_tests(verbosity: int = 2, failfast: bool = False) -> unittest.TestResult:
    """运行测试套件"""
    suite = discover_tests()
    
    if suite.countTestCases() == 0:
        print("没有找到任何测试用例")
        return None
    
    print(f"发现 {suite.countTestCases()} 个测试用例")
    print("=" * 70)
    
    runner = unittest.TextTestRunner(
        verbosity=verbosity,
        failfast=failfast,
        stream=sys.stdout
    )
    
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    print("=" * 70)
    print(f"测试运行时间: {end_time - start_time:.2f} 秒")
    
    return result

def generate_test_report(result: unittest.TestResult) -> Dict[str, Any]:
    """生成测试报告"""
    if result is None:
        return {"error": "没有测试结果"}
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped) if hasattr(result, 'skipped') else 0
    success = total_tests - failures - errors - skipped
    
    success_rate = (success / total_tests * 100) if total_tests > 0 else 0
    
    report = {
        "total_tests": total_tests,
        "success": success,
        "failures": failures,
        "errors": errors,
        "skipped": skipped,
        "success_rate": success_rate
    }
    
    return report

def print_test_summary(report: Dict[str, Any]) -> None:
    """打印测试摘要"""
    if "error" in report:
        print(f"错误: {report['error']}")
        return
    
    print("\n" + "=" * 70)
    print("测试摘要")
    print("=" * 70)
    print(f"总测试数:   {report['total_tests']}")
    print(f"成功:       {report['success']}")
    print(f"失败:       {report['failures']}")
    print(f"错误:       {report['errors']}")
    print(f"跳过:       {report['skipped']}")
    print(f"成功率:     {report['success_rate']:.1f}%")
    
    if report['success_rate'] == 100.0:
        print("\n🎉 所有测试都通过了！")
    elif report['success_rate'] >= 80.0:
        print(f"\n✅ 大部分测试通过 ({report['success_rate']:.1f}%)")
    else:
        print(f"\n❌ 需要修复失败的测试 ({report['success_rate']:.1f}%)")

def run_specific_test(test_name: str, verbosity: int = 2) -> unittest.TestResult:
    """运行特定的测试"""
    loader = unittest.TestLoader()
    
    try:
        # 尝试加载特定测试
        suite = loader.loadTestsFromName(test_name)
        
        runner = unittest.TextTestRunner(verbosity=verbosity)
        result = runner.run(suite)
        
        return result
        
    except Exception as e:
        print(f"无法加载测试 '{test_name}': {e}")
        return None

def list_available_tests() -> List[str]:
    """列出所有可用的测试"""
    suite = discover_tests()
    test_names = []
    
    def extract_test_names(test_suite):
        for test in test_suite:
            if isinstance(test, unittest.TestSuite):
                extract_test_names(test)
            else:
                test_names.append(f"{test.__class__.__module__}.{test.__class__.__name__}.{test._testMethodName}")
    
    extract_test_names(suite)
    return sorted(test_names)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="天机变游戏测试运行器")
    parser.add_argument(
        "-v", "--verbosity",
        type=int,
        choices=[0, 1, 2],
        default=2,
        help="测试输出详细程度 (0=静默, 1=正常, 2=详细)"
    )
    parser.add_argument(
        "-f", "--failfast",
        action="store_true",
        help="遇到第一个失败时停止"
    )
    parser.add_argument(
        "-t", "--test",
        type=str,
        help="运行特定的测试 (例如: tests.test_core.TestInterfaces.test_position_creation)"
    )
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="列出所有可用的测试"
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="运行代码覆盖率分析 (需要安装 coverage 包)"
    )
    
    args = parser.parse_args()
    
    if args.list:
        print("可用的测试:")
        tests = list_available_tests()
        for test in tests:
            print(f"  {test}")
        return
    
    if args.coverage:
        try:
            import coverage
            cov = coverage.Coverage()
            cov.start()
            
            if args.test:
                result = run_specific_test(args.test, args.verbosity)
            else:
                result = run_tests(args.verbosity, args.failfast)
            
            cov.stop()
            cov.save()
            
            print("\n" + "=" * 70)
            print("代码覆盖率报告")
            print("=" * 70)
            cov.report()
            
        except ImportError:
            print("错误: 需要安装 coverage 包来运行覆盖率分析")
            print("运行: pip install coverage")
            return
    else:
        if args.test:
            result = run_specific_test(args.test, args.verbosity)
        else:
            result = run_tests(args.verbosity, args.failfast)
    
    if result:
        report = generate_test_report(result)
        print_test_summary(report)
        
        # 根据测试结果设置退出码
        if report.get('failures', 0) > 0 or report.get('errors', 0) > 0:
            sys.exit(1)
        else:
            sys.exit(0)

if __name__ == "__main__":
    main()