#!/usr/bin/env python3
"""
天机变游戏性能检查脚本
检查游戏的性能瓶颈和优化机会
"""

import time
import psutil
import os
import sys
import tracemalloc
from typing import Dict, List, Any
import importlib

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class PerformanceProfiler:
    """性能分析器"""
    
    def __init__(self):
        self.results = {}
        self.memory_snapshots = []
        
    def start_profiling(self):
        """开始性能分析"""
        tracemalloc.start()
        self.start_time = time.time()
        self.start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
    def stop_profiling(self, test_name: str):
        """停止性能分析并记录结果"""
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        self.results[test_name] = {
            'execution_time': end_time - self.start_time,
            'memory_usage': end_memory - self.start_memory,
            'peak_memory': peak / 1024 / 1024,  # MB
            'current_memory': current / 1024 / 1024  # MB
        }
        
    def profile_module_import(self, module_name: str):
        """分析模块导入性能"""
        print(f"📦 分析模块导入: {module_name}")
        
        self.start_profiling()
        try:
            module = importlib.import_module(module_name)
            self.stop_profiling(f"import_{module_name}")
            print(f"✅ 成功导入 {module_name}")
            return module
        except Exception as e:
            print(f"❌ 导入失败 {module_name}: {e}")
            return None
            
    def profile_game_initialization(self):
        """分析游戏初始化性能"""
        print("🎮 分析游戏初始化性能")
        
        self.start_profiling()
        try:
            # 导入核心模块
            from game_state import GameState, Player, Avatar, AvatarName
            from yijing_mechanics import YinYangBalance
            
            # 创建游戏状态
            avatars = [
                Avatar(AvatarName.EMPEROR, "帝王", "统治者"),
                Avatar(AvatarName.HERMIT, "隐士", "修行者"),
            ]
            players = [
                Player("玩家1", avatars[0]),
                Player("玩家2", avatars[1])
            ]
            game_state = GameState(players)
            
            self.stop_profiling("game_initialization")
            print("✅ 游戏初始化完成")
            return game_state
        except Exception as e:
            print(f"❌ 游戏初始化失败: {e}")
            return None
            
    def profile_single_turn(self, game_state):
        """分析单回合性能"""
        print("⚡ 分析单回合性能")
        
        if not game_state:
            print("❌ 无效的游戏状态")
            return
            
        self.start_profiling()
        try:
            # 模拟一个回合的操作
            current_player = game_state.get_current_player()
            
            # 执行一些典型操作
            current_player.dao_xing += 2
            current_player.qi += 1
            current_player.cheng_yi += 1
            
            # 检查胜利条件
            winner = None
            for player in game_state.players:
                if player.dao_xing >= 25:
                    winner = player
                    break
                    
            self.stop_profiling("single_turn")
            print("✅ 单回合分析完成")
        except Exception as e:
            print(f"❌ 单回合分析失败: {e}")
            
    def profile_batch_operations(self, game_state, iterations=1000):
        """分析批量操作性能"""
        print(f"🔄 分析批量操作性能 ({iterations}次)")
        
        if not game_state:
            print("❌ 无效的游戏状态")
            return
            
        self.start_profiling()
        try:
            for i in range(iterations):
                current_player = game_state.get_current_player()
                current_player.dao_xing += 1
                
                # 切换玩家
                game_state.current_player_index = (game_state.current_player_index + 1) % len(game_state.players)
                
            self.stop_profiling("batch_operations")
            print(f"✅ 批量操作完成 ({iterations}次)")
        except Exception as e:
            print(f"❌ 批量操作失败: {e}")
            
    def analyze_memory_usage(self):
        """分析内存使用情况"""
        print("💾 分析内存使用情况")
        
        process = psutil.Process()
        memory_info = process.memory_info()
        
        print(f"当前内存使用: {memory_info.rss / 1024 / 1024:.2f} MB")
        print(f"虚拟内存使用: {memory_info.vms / 1024 / 1024:.2f} MB")
        
        # 检查系统内存
        system_memory = psutil.virtual_memory()
        print(f"系统总内存: {system_memory.total / 1024 / 1024 / 1024:.2f} GB")
        print(f"系统可用内存: {system_memory.available / 1024 / 1024 / 1024:.2f} GB")
        print(f"内存使用率: {system_memory.percent:.1f}%")
        
    def check_file_sizes(self):
        """检查文件大小"""
        print("📁 检查文件大小")
        
        important_files = [
            'game_state.py',
            'yijing_mechanics.py',
            'main.py',
            'enhanced_ui_system.py',
            'wisdom_system.py'
        ]
        
        total_size = 0
        for filename in important_files:
            if os.path.exists(filename):
                size = os.path.getsize(filename)
                total_size += size
                print(f"{filename}: {size / 1024:.1f} KB")
            else:
                print(f"{filename}: 文件不存在")
                
        print(f"核心文件总大小: {total_size / 1024:.1f} KB")
        
    def generate_report(self):
        """生成性能报告"""
        print("\n" + "=" * 60)
        print("🔍 性能分析报告")
        print("=" * 60)
        
        if not self.results:
            print("❌ 没有性能数据")
            return
            
        print("\n📊 执行时间分析:")
        for test_name, data in self.results.items():
            print(f"{test_name}:")
            print(f"  执行时间: {data['execution_time']*1000:.2f} ms")
            print(f"  内存变化: {data['memory_usage']:.2f} MB")
            print(f"  峰值内存: {data['peak_memory']:.2f} MB")
            print()
            
        # 性能建议
        print("💡 性能优化建议:")
        print("----------------------------------------")
        
        # 检查导入时间
        import_times = {k: v for k, v in self.results.items() if k.startswith('import_')}
        if import_times:
            slowest_import = max(import_times.items(), key=lambda x: x[1]['execution_time'])
            if slowest_import[1]['execution_time'] > 0.1:
                print(f"⚠️  模块导入较慢: {slowest_import[0]} ({slowest_import[1]['execution_time']*1000:.1f}ms)")
                print("   建议: 考虑延迟导入或模块拆分")
                
        # 检查初始化时间
        if 'game_initialization' in self.results:
            init_time = self.results['game_initialization']['execution_time']
            if init_time > 0.05:
                print(f"⚠️  游戏初始化较慢: {init_time*1000:.1f}ms")
                print("   建议: 优化对象创建或减少初始化操作")
                
        # 检查单回合性能
        if 'single_turn' in self.results:
            turn_time = self.results['single_turn']['execution_time']
            if turn_time > 0.01:
                print(f"⚠️  单回合执行较慢: {turn_time*1000:.1f}ms")
                print("   建议: 优化回合逻辑或减少计算复杂度")
            else:
                print(f"✅ 单回合性能良好: {turn_time*1000:.2f}ms")
                
        # 检查批量操作性能
        if 'batch_operations' in self.results:
            batch_time = self.results['batch_operations']['execution_time']
            avg_time = batch_time / 1000 * 1000  # ms per operation
            if avg_time > 0.1:
                print(f"⚠️  批量操作效率较低: {avg_time:.3f}ms/操作")
                print("   建议: 优化数据结构或算法")
            else:
                print(f"✅ 批量操作性能良好: {avg_time:.3f}ms/操作")
                
        print("\n✅ 性能分析完成！")

def main():
    """主函数"""
    print("🚀 开始天机变游戏性能检查")
    print("=" * 60)
    
    profiler = PerformanceProfiler()
    
    # 1. 检查文件大小
    profiler.check_file_sizes()
    print()
    
    # 2. 分析内存使用
    profiler.analyze_memory_usage()
    print()
    
    # 3. 分析模块导入性能
    core_modules = [
        'game_state',
        'yijing_mechanics', 
        'wisdom_system'
    ]
    
    for module in core_modules:
        profiler.profile_module_import(module)
    print()
    
    # 4. 分析游戏初始化性能
    game_state = profiler.profile_game_initialization()
    print()
    
    # 5. 分析单回合性能
    profiler.profile_single_turn(game_state)
    print()
    
    # 6. 分析批量操作性能
    profiler.profile_batch_operations(game_state, 1000)
    print()
    
    # 7. 生成报告
    profiler.generate_report()

if __name__ == "__main__":
    main()