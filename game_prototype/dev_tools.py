"""
天机变游戏开发工具集
整合平衡性分析、性能优化、自动化测试等开发工具
"""

import os
import sys
import json
import time
import argparse
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

# 导入各个模块
from balance_analyzer import BalanceAnalyzer, BalanceMetric
from game_tester import GameTester, TestConfiguration, TestStrategy, TestDifficulty
from performance_optimizer import PerformanceOptimizer, global_optimizer
from config_manager import ConfigManager, get_config

class DevToolsManager:
    """开发工具管理器"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.balance_analyzer = BalanceAnalyzer()
        self.game_tester = GameTester()
        self.performance_optimizer = PerformanceOptimizer()
        self.config_manager = ConfigManager()
        
        self.logger.info("开发工具集已初始化")
    
    def _setup_logging(self) -> logging.Logger:
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('dev_tools.log', encoding='utf-8')
            ]
        )
        return logging.getLogger(__name__)
    
    def run_full_analysis(self, output_dir: str = "analysis_results") -> Dict[str, Any]:
        """运行完整分析"""
        self.logger.info("开始运行完整分析...")
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        results = {
            "timestamp": time.time(),
            "analysis_type": "full",
            "results": {}
        }
        
        try:
            # 1. 游戏平衡性测试
            self.logger.info("1. 执行游戏平衡性测试...")
            balance_results = self._run_balance_tests()
            results["results"]["balance_analysis"] = balance_results
            
            # 2. 性能测试
            self.logger.info("2. 执行性能测试...")
            performance_results = self._run_performance_tests()
            results["results"]["performance_analysis"] = performance_results
            
            # 3. 策略对比测试
            self.logger.info("3. 执行策略对比测试...")
            strategy_results = self._run_strategy_comparison()
            results["results"]["strategy_analysis"] = strategy_results
            
            # 4. 配置验证
            self.logger.info("4. 执行配置验证...")
            config_results = self._validate_configuration()
            results["results"]["config_validation"] = config_results
            
            # 5. 生成综合报告
            self.logger.info("5. 生成综合报告...")
            comprehensive_report = self._generate_comprehensive_report(results["results"])
            results["comprehensive_report"] = comprehensive_report
            
            # 保存结果
            self._save_analysis_results(results, output_dir)
            
            self.logger.info("完整分析已完成")
            return results
        
        except Exception as e:
            self.logger.error(f"完整分析失败: {e}")
            results["error"] = str(e)
            return results
    
    def _run_balance_tests(self) -> Dict[str, Any]:
        """运行平衡性测试"""
        # 配置测试参数
        test_configs = [
            TestConfiguration(
                num_games=50,
                player_strategies=[TestStrategy.BALANCED, TestStrategy.BALANCED],
                difficulty=TestDifficulty.NORMAL,
                parallel_games=4
            ),
            TestConfiguration(
                num_games=30,
                player_strategies=[TestStrategy.AGGRESSIVE, TestStrategy.DEFENSIVE],
                difficulty=TestDifficulty.NORMAL,
                parallel_games=4
            ),
            TestConfiguration(
                num_games=30,
                player_strategies=[TestStrategy.DAO_XING_FOCUSED, TestStrategy.CHENG_YI_FOCUSED],
                difficulty=TestDifficulty.NORMAL,
                parallel_games=4
            )
        ]
        
        all_results = []
        
        for i, config in enumerate(test_configs):
            self.logger.info(f"执行平衡性测试 {i+1}/{len(test_configs)}")
            result = self.game_tester.run_test_suite(config)
            all_results.append(result)
        
        # 生成平衡性报告
        balance_reports = {}
        for metric in BalanceMetric:
            report = self.balance_analyzer.generate_balance_report(metric)
            balance_reports[metric.value] = {
                "score": report.score,
                "issues": report.issues,
                "recommendations": report.recommendations,
                "data": report.data
            }
        
        return {
            "test_results": all_results,
            "balance_reports": balance_reports,
            "optimization_suggestions": self.balance_analyzer.get_optimization_suggestions()
        }
    
    def _run_performance_tests(self) -> Dict[str, Any]:
        """运行性能测试"""
        # 启动性能监控
        self.performance_optimizer.start_optimization()
        
        try:
            # 运行性能测试游戏
            config = TestConfiguration(
                num_games=20,
                player_strategies=[TestStrategy.BALANCED, TestStrategy.BALANCED],
                difficulty=TestDifficulty.NORMAL,
                parallel_games=1,  # 单线程以获得准确的性能数据
                enable_logging=False
            )
            
            test_result = self.game_tester.run_test_suite(config)
            
            # 获取性能报告
            performance_report = self.performance_optimizer.get_optimization_report()
            
            return {
                "test_performance": test_result.get("analysis", {}),
                "system_performance": performance_report,
                "performance_recommendations": performance_report.get("optimization_suggestions", [])
            }
        
        finally:
            # 停止性能监控
            self.performance_optimizer.stop_optimization()
    
    def _run_strategy_comparison(self) -> Dict[str, Any]:
        """运行策略对比测试"""
        strategies_to_test = [
            TestStrategy.RANDOM,
            TestStrategy.AGGRESSIVE,
            TestStrategy.DEFENSIVE,
            TestStrategy.BALANCED,
            TestStrategy.DAO_XING_FOCUSED,
            TestStrategy.CHENG_YI_FOCUSED,
            TestStrategy.INTERACTION_HEAVY
        ]
        
        strategy_results = {}
        
        # 每种策略与平衡策略对战
        for strategy in strategies_to_test:
            self.logger.info(f"测试策略: {strategy.value}")
            
            config = TestConfiguration(
                num_games=25,
                player_strategies=[strategy, TestStrategy.BALANCED],
                difficulty=TestDifficulty.NORMAL,
                parallel_games=4
            )
            
            result = self.game_tester.run_test_suite(config)
            strategy_results[strategy.value] = result
        
        # 分析策略表现
        strategy_analysis = self._analyze_strategy_performance(strategy_results)
        
        return {
            "individual_results": strategy_results,
            "strategy_analysis": strategy_analysis,
            "recommendations": self._generate_strategy_recommendations(strategy_analysis)
        }
    
    def _validate_configuration(self) -> Dict[str, Any]:
        """验证配置"""
        validation_results = {
            "config_file_exists": os.path.exists("game_config.json"),
            "config_loaded": False,
            "validation_errors": [],
            "validation_warnings": [],
            "config_completeness": {}
        }
        
        try:
            # 尝试加载配置
            config = self.config_manager.get_all_config()
            validation_results["config_loaded"] = True
            
            # 验证必要的配置项
            required_sections = [
                "game_balance",
                "ui_settings", 
                "debug_settings",
                "multiplayer",
                "achievements",
                "localization"
            ]
            
            for section in required_sections:
                if section in config:
                    validation_results["config_completeness"][section] = True
                else:
                    validation_results["config_completeness"][section] = False
                    validation_results["validation_errors"].append(f"缺少配置节: {section}")
            
            # 验证数值范围
            self._validate_config_values(config, validation_results)
            
        except Exception as e:
            validation_results["validation_errors"].append(f"配置加载失败: {e}")
        
        return validation_results
    
    def _validate_config_values(self, config: Dict[str, Any], validation_results: Dict[str, Any]):
        """验证配置值"""
        # 验证游戏平衡配置
        if "game_balance" in config:
            balance_config = config["game_balance"]
            
            # 检查初始资源
            if "initial_resources" in balance_config:
                resources = balance_config["initial_resources"]
                if resources.get("dao_xing", 0) < 0:
                    validation_results["validation_errors"].append("初始道行不能为负数")
                if resources.get("cheng_yi", 0) < 0:
                    validation_results["validation_errors"].append("初始诚意不能为负数")
                if resources.get("qi", 0) <= 0:
                    validation_results["validation_errors"].append("初始气必须大于0")
            
            # 检查资源限制
            if "resource_limits" in balance_config:
                limits = balance_config["resource_limits"]
                if limits.get("max_dao_xing", 20) < 10:
                    validation_results["validation_warnings"].append("最大道行值可能过低")
                if limits.get("max_cheng_yi", 15) < 8:
                    validation_results["validation_warnings"].append("最大诚意值可能过低")
    
    def _analyze_strategy_performance(self, strategy_results: Dict[str, Any]) -> Dict[str, Any]:
        """分析策略表现"""
        analysis = {
            "win_rates": {},
            "average_game_length": {},
            "resource_efficiency": {},
            "strategy_rankings": []
        }
        
        for strategy_name, result in strategy_results.items():
            if "analysis" in result:
                analysis_data = result["analysis"]
                
                # 胜率分析
                victory_analysis = analysis_data.get("victory_analysis", {})
                winner_dist = victory_analysis.get("winner_distribution", {})
                total_games = sum(winner_dist.values())
                
                if total_games > 0:
                    strategy_wins = winner_dist.get("Player_1", 0)  # 假设Player_1使用测试策略
                    win_rate = strategy_wins / total_games
                    analysis["win_rates"][strategy_name] = win_rate
                
                # 游戏长度分析
                game_length = analysis_data.get("game_length", {})
                analysis["average_game_length"][strategy_name] = game_length.get("average", 0)
                
                # 策略效率分析
                strategy_performance = analysis_data.get("strategy_performance", {})
                if strategy_name in strategy_performance:
                    perf = strategy_performance[strategy_name]
                    analysis["resource_efficiency"][strategy_name] = {
                        "avg_dao_xing": perf.get("average_dao_xing", 0),
                        "avg_cheng_yi": perf.get("average_cheng_yi", 0),
                        "win_rate": perf.get("win_rate", 0)
                    }
        
        # 策略排名
        strategy_scores = []
        for strategy_name in analysis["win_rates"]:
            win_rate = analysis["win_rates"].get(strategy_name, 0)
            efficiency = analysis["resource_efficiency"].get(strategy_name, {})
            
            # 综合评分 (胜率 * 0.6 + 资源效率 * 0.4)
            resource_score = (efficiency.get("avg_dao_xing", 0) + efficiency.get("avg_cheng_yi", 0)) / 35  # 归一化
            total_score = win_rate * 0.6 + resource_score * 0.4
            
            strategy_scores.append({
                "strategy": strategy_name,
                "win_rate": win_rate,
                "resource_score": resource_score,
                "total_score": total_score
            })
        
        analysis["strategy_rankings"] = sorted(strategy_scores, key=lambda x: x["total_score"], reverse=True)
        
        return analysis
    
    def _generate_strategy_recommendations(self, strategy_analysis: Dict[str, Any]) -> List[str]:
        """生成策略建议"""
        recommendations = []
        
        rankings = strategy_analysis.get("strategy_rankings", [])
        if not rankings:
            return ["无法生成策略建议：缺少分析数据"]
        
        # 最强策略
        best_strategy = rankings[0]
        if best_strategy["total_score"] > 0.7:
            recommendations.append(f"策略 {best_strategy['strategy']} 表现优异，可作为AI默认策略")
        
        # 最弱策略
        worst_strategy = rankings[-1]
        if worst_strategy["total_score"] < 0.3:
            recommendations.append(f"策略 {worst_strategy['strategy']} 表现较差，需要优化或调整")
        
        # 平衡性建议
        win_rates = [s["win_rate"] for s in rankings]
        if max(win_rates) - min(win_rates) > 0.4:
            recommendations.append("策略间胜率差异过大，建议平衡调整游戏机制")
        
        # 多样性建议
        if len([s for s in rankings if s["total_score"] > 0.5]) < 3:
            recommendations.append("可行策略数量不足，建议增加策略多样性")
        
        return recommendations
    
    def _generate_comprehensive_report(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """生成综合报告"""
        report = {
            "executive_summary": {},
            "key_findings": [],
            "critical_issues": [],
            "recommendations": [],
            "next_steps": []
        }
        
        # 执行摘要
        balance_results = results.get("balance_analysis", {})
        performance_results = results.get("performance_analysis", {})
        strategy_results = results.get("strategy_analysis", {})
        
        # 平衡性摘要
        balance_reports = balance_results.get("balance_reports", {})
        avg_balance_score = sum(r.get("score", 0) for r in balance_reports.values()) / max(1, len(balance_reports))
        
        report["executive_summary"]["balance_score"] = avg_balance_score
        report["executive_summary"]["balance_level"] = self._get_balance_level(avg_balance_score)
        
        # 性能摘要
        system_performance = performance_results.get("system_performance", {})
        performance_score = system_performance.get("performance", {}).get("overall_score", 0)
        
        report["executive_summary"]["performance_score"] = performance_score
        report["executive_summary"]["performance_level"] = self._get_performance_level(performance_score)
        
        # 策略摘要
        strategy_analysis = strategy_results.get("strategy_analysis", {})
        rankings = strategy_analysis.get("strategy_rankings", [])
        
        if rankings:
            best_strategy = rankings[0]
            report["executive_summary"]["best_strategy"] = best_strategy["strategy"]
            report["executive_summary"]["strategy_balance"] = max(rankings, key=lambda x: x["total_score"])["total_score"]
        
        # 关键发现
        if avg_balance_score < 60:
            report["key_findings"].append("游戏平衡性需要改进")
        if performance_score < 70:
            report["key_findings"].append("系统性能存在优化空间")
        if len(rankings) > 0 and rankings[0]["total_score"] - rankings[-1]["total_score"] > 0.4:
            report["key_findings"].append("策略间平衡性存在问题")
        
        # 关键问题
        for metric_name, metric_data in balance_reports.items():
            if metric_data.get("score", 0) < 40:
                report["critical_issues"].append(f"{metric_name}评分过低: {metric_data.get('score', 0):.1f}")
        
        # 建议汇总
        all_recommendations = []
        all_recommendations.extend(balance_results.get("optimization_suggestions", {}).get("immediate", []))
        all_recommendations.extend(performance_results.get("performance_recommendations", []))
        all_recommendations.extend(strategy_results.get("recommendations", []))
        
        report["recommendations"] = list(set(all_recommendations))  # 去重
        
        # 下一步行动
        if avg_balance_score < 50:
            report["next_steps"].append("优先解决游戏平衡性问题")
        if performance_score < 60:
            report["next_steps"].append("进行性能优化")
        if not report["next_steps"]:
            report["next_steps"].append("继续监控和微调")
        
        return report
    
    def _get_balance_level(self, score: float) -> str:
        """获取平衡性等级"""
        if score >= 85:
            return "优秀"
        elif score >= 70:
            return "良好"
        elif score >= 55:
            return "可接受"
        elif score >= 40:
            return "较差"
        else:
            return "严重失衡"
    
    def _get_performance_level(self, score: float) -> str:
        """获取性能等级"""
        if score >= 85:
            return "优秀"
        elif score >= 70:
            return "良好"
        elif score >= 55:
            return "可接受"
        elif score >= 35:
            return "较差"
        else:
            return "严重问题"
    
    def _save_analysis_results(self, results: Dict[str, Any], output_dir: str):
        """保存分析结果"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # 保存完整结果
        full_results_file = os.path.join(output_dir, f"full_analysis_{timestamp}.json")
        with open(full_results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2, default=str)
        
        # 保存简化报告
        summary_file = os.path.join(output_dir, f"analysis_summary_{timestamp}.json")
        summary = {
            "timestamp": results["timestamp"],
            "executive_summary": results.get("comprehensive_report", {}).get("executive_summary", {}),
            "key_findings": results.get("comprehensive_report", {}).get("key_findings", []),
            "critical_issues": results.get("comprehensive_report", {}).get("critical_issues", []),
            "recommendations": results.get("comprehensive_report", {}).get("recommendations", [])
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2, default=str)
        
        self.logger.info(f"分析结果已保存到 {output_dir}")
    
    def quick_test(self, test_type: str = "balance", num_games: int = 10) -> Dict[str, Any]:
        """快速测试"""
        self.logger.info(f"执行快速{test_type}测试...")
        
        if test_type == "balance":
            config = TestConfiguration(
                num_games=num_games,
                player_strategies=[TestStrategy.BALANCED, TestStrategy.BALANCED],
                difficulty=TestDifficulty.NORMAL,
                parallel_games=2
            )
            return self.game_tester.run_test_suite(config)
        
        elif test_type == "performance":
            self.performance_optimizer.start_optimization()
            try:
                config = TestConfiguration(
                    num_games=min(num_games, 5),  # 性能测试游戏数量较少
                    player_strategies=[TestStrategy.BALANCED, TestStrategy.BALANCED],
                    difficulty=TestDifficulty.NORMAL,
                    parallel_games=1
                )
                result = self.game_tester.run_test_suite(config)
                performance_report = self.performance_optimizer.get_optimization_report()
                
                return {
                    "test_result": result,
                    "performance_report": performance_report
                }
            finally:
                self.performance_optimizer.stop_optimization()
        
        elif test_type == "strategy":
            strategies = [TestStrategy.AGGRESSIVE, TestStrategy.DEFENSIVE]
            config = TestConfiguration(
                num_games=num_games,
                player_strategies=strategies,
                difficulty=TestDifficulty.NORMAL,
                parallel_games=2
            )
            return self.game_tester.run_test_suite(config)
        
        else:
            return {"error": f"未知的测试类型: {test_type}"}
    
    def generate_development_report(self) -> str:
        """生成开发报告"""
        report_lines = [
            "# 天机变游戏开发状态报告",
            f"生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 系统状态",
        ]
        
        # 配置状态
        config_validation = self._validate_configuration()
        report_lines.extend([
            f"- 配置文件状态: {'正常' if config_validation['config_loaded'] else '异常'}",
            f"- 配置完整性: {sum(config_validation['config_completeness'].values())}/{len(config_validation['config_completeness'])} 项",
            f"- 配置错误: {len(config_validation['validation_errors'])} 个",
            ""
        ])
        
        # 快速测试结果
        quick_balance = self.quick_test("balance", 5)
        if "analysis" in quick_balance:
            analysis = quick_balance["analysis"]
            victory_analysis = analysis.get("victory_analysis", {})
            completion_rate = victory_analysis.get("completion_rate", 0)
            
            report_lines.extend([
                "## 快速平衡性测试",
                f"- 游戏完成率: {completion_rate:.1%}",
                f"- 平均游戏时长: {analysis.get('game_length', {}).get('average', 0):.1f} 回合",
                ""
            ])
        
        # 建议
        report_lines.extend([
            "## 开发建议",
            "- 定期运行完整分析以监控游戏平衡性",
            "- 关注性能优化，特别是在游戏规模扩大时",
            "- 持续测试不同策略的平衡性",
            ""
        ])
        
        return "\n".join(report_lines)

def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="天机变游戏开发工具集")
    parser.add_argument("command", choices=["full", "quick", "balance", "performance", "strategy", "report"],
                       help="要执行的命令")
    parser.add_argument("--games", type=int, default=10, help="测试游戏数量")
    parser.add_argument("--output", default="analysis_results", help="输出目录")
    parser.add_argument("--verbose", action="store_true", help="详细输出")
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 创建工具管理器
    tools = DevToolsManager()
    
    try:
        if args.command == "full":
            print("执行完整分析...")
            result = tools.run_full_analysis(args.output)
            print(f"分析完成，结果保存在 {args.output}")
            
        elif args.command == "quick":
            print("执行快速测试...")
            result = tools.quick_test("balance", args.games)
            print("快速测试完成")
            print(json.dumps(result.get("analysis", {}).get("summary", {}), 
                           ensure_ascii=False, indent=2))
            
        elif args.command in ["balance", "performance", "strategy"]:
            print(f"执行{args.command}测试...")
            result = tools.quick_test(args.command, args.games)
            print(f"{args.command}测试完成")
            
        elif args.command == "report":
            print("生成开发报告...")
            report = tools.generate_development_report()
            print(report)
            
            # 保存报告
            report_file = os.path.join(args.output, "development_report.md")
            os.makedirs(args.output, exist_ok=True)
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"报告已保存到 {report_file}")
    
    except KeyboardInterrupt:
        print("\n操作已取消")
    except Exception as e:
        print(f"执行失败: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()