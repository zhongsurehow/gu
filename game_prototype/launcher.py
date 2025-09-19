#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天机变游戏启动器
提供统一的游戏启动和开发工具入口
"""

import os
import sys
import json
import argparse
import traceback
import logging
from pathlib import Path
from typing import Dict, Any, Optional

class GameLauncher:
    """游戏启动器"""
    
    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('launcher.log', encoding='utf-8')
            ]
        )

def check_dependencies():
    """检查游戏依赖"""
    required_files = [
        'main.py',
        'game_state.py',
        'config_manager.py',
        'game_data.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ 缺少必要文件:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ 核心文件检查通过")
    return True

def check_enhanced_systems():
    """检查增强系统"""
    enhanced_files = [
        'enhanced_game_balance.py',
        'enhanced_ui_system.py', 
        'complete_64_guas_system.py',
        'yijing_wisdom_guide.py',
        'balance_analyzer.py',
        'game_tester.py',
        'performance_optimizer.py',
        'dev_tools.py',
        'core_engine.py'
    ]
    
    available_systems = []
    for file in enhanced_files:
        if os.path.exists(file):
            available_systems.append(file)
    
    if available_systems:
        print("✅ 增强系统可用:")
        for system in available_systems:
            print(f"   - {system}")
    else:
        print("⚠️  增强系统未找到，将使用基础功能")
    
    return len(available_systems) > 0

def display_welcome():
    """显示欢迎信息"""
    print("=" * 60)
    print("🎮 天机变 - 易经主题策略游戏")
    print("=" * 60)
    print("📖 基于《易经》智慧的策略卡牌游戏")
    print("🎯 体验阴阳五行，感悟人生哲理")
    print("🧘 在游戏中修行，在修行中成长")
    print("=" * 60)

def display_system_info():
    """显示系统信息"""
    print(f"🐍 Python版本: {sys.version.split()[0]}")
    print(f"📁 游戏目录: {os.getcwd()}")
    print(f"💻 操作系统: {os.name}")
    
    # 检查编码
    try:
        test_str = "易经天机变"
        print(f"🔤 编码测试: {test_str}")
    except UnicodeError:
        print("⚠️  编码可能存在问题")

def run_ai_demo():
    """运行AI对战演示"""
    print("\n🤖 AI对战演示")
    print("=" * 60)
    print("这将展示两个AI玩家之间的对战")
    
    try:
        # 检查是否有游戏测试器
        if not os.path.exists('game_tester.py'):
            print("❌ 游戏测试器未找到，无法运行AI演示")
            input("按回车键返回...")
            return
        
        from game_tester import GameTester, TestConfiguration, TestStrategy, TestDifficulty
        
        print("🎯 配置AI对战...")
        config = TestConfiguration(
            num_games=1,
            player_strategies=[TestStrategy.BALANCED, TestStrategy.BALANCED],
            difficulty=TestDifficulty.NORMAL,
            parallel_games=1,
            enable_logging=True
        )
        
        print("🚀 开始AI对战...")
        tester = GameTester()
        result = tester.run_test_suite(config)
        
        # 显示结果
        if "analysis" in result:
            analysis = result["analysis"]
            print("\n📊 对战结果:")
            print(f"游戏完成: {analysis.get('games_completed', 0)}")
            
            victory_analysis = analysis.get("victory_analysis", {})
            winner_dist = victory_analysis.get("winner_distribution", {})
            
            for player, wins in winner_dist.items():
                print(f"{player}: {wins} 胜")
            
            game_length = analysis.get("game_length", {})
            print(f"平均游戏时长: {game_length.get('average', 0):.1f} 回合")
        
        print("\n✅ AI演示完成")
        
    except Exception as e:
        print(f"❌ AI演示失败: {e}")
        print("详细错误信息:")
        traceback.print_exc()
    
    input("按回车键返回...")

def show_dev_tools_menu():
    """显示开发工具菜单"""
    while True:
        print("\n" + "="*50)
        print("🛠️  开发工具菜单")
        print("="*50)
        print("1. 🧪 快速平衡性测试")
        print("2. ⚡ 性能测试")
        print("3. 🎯 策略对比测试")
        print("4. 🔧 核心代码优化")
        print("5. 🎨 界面优化")
        print("6. 📈 完整分析")
        print("7. 📋 生成开发报告")
        print("8. 🔍 系统检查")
        print("9. 🔙 返回主菜单")
        print("="*50)
        
        try:
            choice = input("请选择 (1-9): ").strip()
            
            if choice == '1':
                run_balance_test()
            elif choice == '2':
                run_performance_test()
            elif choice == '3':
                run_strategy_test()
            elif choice == '4':
                run_core_optimization()
            elif choice == '5':
                run_ui_optimization()
            elif choice == '6':
                run_full_analysis()
            elif choice == '7':
                generate_dev_report()
            elif choice == '8':
                run_system_check()
            elif choice == '9':
                break
            else:
                print("❌ 无效选择，请输入 1-9")
        except (EOFError, KeyboardInterrupt):
            print("\n返回主菜单")
            break

def run_balance_test():
    """运行平衡性测试"""
    print("\n🧪 快速平衡性测试")
    print("=" * 40)
    
    try:
        if not os.path.exists('dev_tools.py'):
            print("❌ 开发工具未找到")
            input("按回车键返回...")
            return
        
        from dev_tools import DevToolsManager
        
        tools = DevToolsManager()
        print("🚀 运行平衡性测试...")
        result = tools.quick_test("balance", 5)
        
        if "analysis" in result:
            analysis = result["analysis"]
            print("\n📊 测试结果:")
            print(f"游戏完成率: {analysis.get('victory_analysis', {}).get('completion_rate', 0):.1%}")
            print(f"平均游戏时长: {analysis.get('game_length', {}).get('average', 0):.1f} 回合")
        
        print("✅ 平衡性测试完成")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    input("按回车键返回...")

def run_performance_test():
    """运行性能测试"""
    print("\n⚡ 性能测试")
    print("=" * 40)
    
    try:
        if not os.path.exists('dev_tools.py'):
            print("❌ 开发工具未找到")
            input("按回车键返回...")
            return
        
        from dev_tools import DevToolsManager
        
        tools = DevToolsManager()
        print("🚀 运行性能测试...")
        result = tools.quick_test("performance", 3)
        
        print("✅ 性能测试完成")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    input("按回车键返回...")

def run_strategy_test():
    """运行策略测试"""
    print("\n🎯 策略对比测试")
    print("=" * 40)
    
    try:
        if not os.path.exists('dev_tools.py'):
            print("❌ 开发工具未找到")
            input("按回车键返回...")
            return
        
        from dev_tools import DevToolsManager
        
        tools = DevToolsManager()
        print("🚀 运行策略测试...")
        result = tools.quick_test("strategy", 5)
        
        print("✅ 策略测试完成")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    input("按回车键返回...")

def run_full_analysis():
    """运行完整分析"""
    print("\n📈 完整分析")
    print("=" * 40)
    print("⚠️  这可能需要几分钟时间...")
    
    confirm = input("确认运行完整分析? (y/N): ").strip().lower()
    if confirm != 'y':
        return
    
    try:
        if not os.path.exists('dev_tools.py'):
            print("❌ 开发工具未找到")
            input("按回车键返回...")
            return
        
        from dev_tools import DevToolsManager
        
        tools = DevToolsManager()
        print("🚀 运行完整分析...")
        result = tools.run_full_analysis()
        
        print("✅ 完整分析完成")
        print("📁 结果已保存到 analysis_results 目录")
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")
    
    input("按回车键返回...")

def generate_dev_report():
    """生成开发报告"""
    print("\n📋 生成开发报告")
    print("=" * 40)
    
    try:
        if not os.path.exists('dev_tools.py'):
            print("❌ 开发工具未找到")
            input("按回车键返回...")
            return
        
        from dev_tools import DevToolsManager
        
        tools = DevToolsManager()
        print("🚀 生成开发报告...")
        report = tools.generate_development_report()
        
        print(report)
        
        # 保存报告
        os.makedirs("analysis_results", exist_ok=True)
        report_file = "analysis_results/development_report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📁 报告已保存到 {report_file}")
        
    except Exception as e:
        print(f"❌ 报告生成失败: {e}")
    
    input("按回车键返回...")

def run_core_optimization():
    """运行核心代码优化"""
    print("\n🔧 核心代码优化")
    print("=" * 40)
    
    try:
        if not os.path.exists('performance_optimizer.py'):
            print("❌ 性能优化器未找到")
            input("按回车键返回...")
            return
        
        from performance_optimizer import PerformanceOptimizer
        
        optimizer = PerformanceOptimizer()
        print("🚀 运行核心代码优化...")
        result = optimizer.optimize_core_systems()
        
        print("✅ 核心代码优化完成")
        
    except Exception as e:
        print(f"❌ 优化失败: {e}")
    
    input("按回车键返回...")

def run_ui_optimization():
    """运行界面优化"""
    print("\n🎨 界面优化")
    print("=" * 40)
    
    try:
        if not os.path.exists('enhanced_ui_system.py'):
            print("❌ 增强UI系统未找到")
            input("按回车键返回...")
            return
        
        from enhanced_ui_system import EnhancedUISystem
        
        ui_system = EnhancedUISystem()
        print("🚀 运行界面优化...")
        result = ui_system.optimize_display()
        
        print("✅ 界面优化完成")
        
    except Exception as e:
        print(f"❌ 优化失败: {e}")
    
    input("按回车键返回...")

def run_system_check():
    """运行系统检查"""
    print("\n🔍 系统检查")
    print("=" * 40)
    
    # 基础检查
    print("📋 基础文件检查:")
    check_dependencies()
    print()
    
    print("🔧 增强系统检查:")
    check_enhanced_systems()
    print()
    
    # 配置检查
    print("⚙️  配置文件检查:")
    config_files = ["game_config.json"]
    for config_file in config_files:
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    json.load(f)
                print(f"   ✅ {config_file}: 有效")
            except json.JSONDecodeError:
                print(f"   ❌ {config_file}: 格式错误")
        else:
            print(f"   ❌ {config_file}: 缺失")
    
    print("\n✅ 系统检查完成")
    input("按回车键返回...")

def show_documentation_menu():
    """显示文档菜单"""
    docs = {
        '1': ('COMPLETE_GAME_GUIDE.md', '完整游戏指南'),
        '2': ('64_GUAS_DETAILED_GUIDE.md', '64卦详细指南'),
        '3': ('QUICK_REFERENCE.md', '快速参考'),
        '4': ('README.md', '项目说明'),
        '5': ('YIJING_GUIDE.md', '易经知识指南'),
        '6': ('HOW_TO_RUN.md', '运行指南')
    }
    
    print("\n📚 游戏文档:")
    for key, (filename, description) in docs.items():
        status = "✅" if os.path.exists(filename) else "❌"
        print(f"   {key}. {status} {description}")
    
    print("   7. 返回主菜单")
    
    try:
        choice = input("\n请选择要查看的文档 (1-7): ").strip()
        if choice in docs:
            filename, description = docs[choice]
            if os.path.exists(filename):
                print(f"\n📖 {description}")
                print(f"请使用文本编辑器打开: {filename}")
                input("按回车键继续...")
            else:
                print(f"❌ 文件不存在: {filename}")
        elif choice == '7':
            return
        else:
            print("❌ 无效选择")
    except (EOFError, KeyboardInterrupt):
        print("\n返回主菜单")

def main():
    """主启动函数"""
    try:
        # 设置工作目录
        script_dir = Path(__file__).parent
        os.chdir(script_dir)
        
        # 显示欢迎信息
        display_welcome()
        
        # 系统检查
        print("\n🔍 系统检查:")
        display_system_info()
        
        if not check_dependencies():
            print("\n❌ 系统检查失败，无法启动游戏")
            input("按回车键退出...")
            return
        
        has_enhanced = check_enhanced_systems()
        
        print("\n" + "=" * 60)
        print("🎮 启动选项:")
        print("1. 🎯 开始游戏")
        print("2. 🤖 AI对战演示")
        print("3. 📊 开发工具")
        print("4. 📚 查看文档")
        print("5. 🔧 系统信息")
        print("6. 🚪 退出")
        
        while True:
            try:
                choice = input("\n请选择 (1-6): ").strip()
                
                if choice == '1':
                    print("\n🚀 启动游戏...")
                    print("=" * 60)
                    
                    # 导入并启动主游戏
                    try:
                        import main
                        main.main()
                    except ImportError as e:
                        print(f"❌ 导入游戏模块失败: {e}")
                        print("请检查游戏文件是否完整")
                    except Exception as e:
                        print(f"❌ 游戏运行错误: {e}")
                        print("详细错误信息:")
                        traceback.print_exc()
                    
                    print("\n🎮 游戏结束，返回启动器")
                    print("=" * 60)
                    
                elif choice == '2':
                    run_ai_demo()
                    
                elif choice == '3':
                    show_dev_tools_menu()
                    
                elif choice == '4':
                    show_documentation_menu()
                    
                elif choice == '5':
                    print("\n🔧 详细系统信息:")
                    display_system_info()
                    
                elif choice == '6':
                    print("\n👋 感谢使用天机变游戏！")
                    print("🙏 愿易经智慧伴您前行！")
                    break
                    
                else:
                    print("❌ 无效选择，请输入 1-6")
                    
            except (EOFError, KeyboardInterrupt):
                print("\n\n🙏 愿易经智慧伴您前行！")
                print("再见！")
                break
            except Exception as e:
                print(f"❌ 发生错误: {e}")
                print("请重试或退出程序")
                
    except Exception as e:
        print(f"❌ 启动器错误: {e}")
        print("详细错误信息:")
        traceback.print_exc()
        input("按回车键退出...")

if __name__ == "__main__":
    main()