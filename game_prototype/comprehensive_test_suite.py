#!/usr/bin/env python3
"""
天机变游戏综合测试套件
包含单元测试、集成测试、性能测试和断言检查
"""

import unittest
import sys
import os
import time
import traceback
from typing import List, Dict, Any, Callable
from dataclasses import dataclass

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入所有需要测试的模块
from game_state import GameState, Player, Zone
from card_base import YaoCiTask, GuaCard
from generate_64_guas import generate_all_64_guas, GUA_64_INFO
from authentic_yao_ci_generator import generate_authentic_yao_ci_tasks, AuthenticYaoCiGenerator
from authentic_yao_ci import AUTHENTIC_YAO_CI_DATA
from yijing_mechanics import YinYangBalance, WuXingCycle, TaijiMechanism
from yijing_actions import enhanced_play_card, enhanced_meditate, biangua_transformation
from wisdom_system import wisdom_system
from achievement_system import achievement_system
from tutorial_system import tutorial_system

@dataclass
class TestResult:
    """测试结果数据类"""
    test_name: str
    passed: bool
    execution_time: float
    error_message: str = ""
    details: Dict[str, Any] = None

class TestReporter:
    """测试报告生成器"""
    
    def __init__(self):
        self.results: List[TestResult] = []
        self.start_time = time.time()
    
    def add_result(self, result: TestResult):
        """添加测试结果"""
        self.results.append(result)
    
    def generate_report(self) -> str:
        """生成测试报告"""
        total_time = time.time() - self.start_time
        passed_count = sum(1 for r in self.results if r.passed)
        failed_count = len(self.results) - passed_count
        
        report = f"""
{'='*60}
天机变游戏测试报告
{'='*60}
总测试数: {len(self.results)}
通过: {passed_count}
失败: {failed_count}
总耗时: {total_time:.2f}秒
成功率: {(passed_count/len(self.results)*100):.1f}%
{'='*60}

详细结果:
"""
        
        for result in self.results:
            status = "✅ PASS" if result.passed else "❌ FAIL"
            report += f"{status} {result.test_name} ({result.execution_time:.3f}s)\n"
            if not result.passed and result.error_message:
                report += f"    错误: {result.error_message}\n"
        
        return report

def test_runner(test_func: Callable, test_name: str, reporter: TestReporter):
    """测试运行器装饰器"""
    start_time = time.time()
    try:
        test_func()
        execution_time = time.time() - start_time
        reporter.add_result(TestResult(test_name, True, execution_time))
        print(f"✅ {test_name}")
    except Exception as e:
        execution_time = time.time() - start_time
        error_msg = f"{type(e).__name__}: {str(e)}"
        reporter.add_result(TestResult(test_name, False, execution_time, error_msg))
        print(f"❌ {test_name} - {error_msg}")

class ComprehensiveTestSuite:
    """综合测试套件"""
    
    def __init__(self):
        self.reporter = TestReporter()
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🧪 开始运行综合测试套件...\n")
        
        # 单元测试
        print("📋 单元测试:")
        self.run_unit_tests()
        
        # 集成测试
        print("\n🔗 集成测试:")
        self.run_integration_tests()
        
        # 性能测试
        print("\n⚡ 性能测试:")
        self.run_performance_tests()
        
        # 数据完整性测试
        print("\n📊 数据完整性测试:")
        self.run_data_integrity_tests()
        
        # 生成报告
        print("\n" + self.reporter.generate_report())
    
    def run_unit_tests(self):
        """运行单元测试"""
        
        def test_yao_ci_task_creation():
            """测试爻辞任务创建"""
            task = YaoCiTask("初九", "测试任务", "测试描述", 1, 2)
            assert task.level == "初九"
            assert task.name == "测试任务"
            assert task.reward_dao_xing == 1
            assert task.reward_cheng_yi == 2
        
        def test_gua_card_creation():
            """测试卦卡创建"""
            tasks = [YaoCiTask(f"爻{i}", f"任务{i}", f"描述{i}", i, i) for i in range(6)]
            card = GuaCard("测试卦", ("上卦", "下卦"), tasks)
            assert card.name == "测试卦"
            assert len(card.tasks) == 6
            assert card.associated_guas == ("上卦", "下卦")
        
        def test_yin_yang_balance():
            """测试阴阳平衡机制"""
            balance = YinYangBalance()
            assert balance.yin_points == 0
            assert balance.yang_points == 0
            
            balance.yin_points = 3
            balance.yang_points = 4
            assert balance.yin_points == 3
            assert balance.yang_points == 4
            assert 0.8 < balance.balance_ratio < 0.9
        
        def test_player_creation():
            """测试玩家创建"""
            from game_state import Avatar, AvatarName
            avatar = Avatar(AvatarName.HERMIT, "隐士", "隐士能力")
            player = Player("测试玩家", avatar)
            assert player.name == "测试玩家"
            assert player.dao_xing == 0
            assert player.qi == 0
            assert player.cheng_yi == 0
        
        def test_authentic_yao_ci_data():
            """测试真实爻辞数据完整性"""
            assert len(AUTHENTIC_YAO_CI_DATA) >= 8  # 至少8个基本卦
            for gua_name, yao_ci_list in AUTHENTIC_YAO_CI_DATA.items():
                assert len(yao_ci_list) == 6, f"{gua_name}的爻辞数量不是6个"
                for yao_ci in yao_ci_list:
                    assert yao_ci.original_text, f"{gua_name}的爻辞缺少原文"
                    assert yao_ci.interpretation, f"{gua_name}的爻辞缺少释义"
        
        # 运行单元测试
        test_runner(test_yao_ci_task_creation, "爻辞任务创建", self.reporter)
        test_runner(test_gua_card_creation, "卦卡创建", self.reporter)
        test_runner(test_yin_yang_balance, "阴阳平衡机制", self.reporter)
        test_runner(test_player_creation, "玩家创建", self.reporter)
        test_runner(test_authentic_yao_ci_data, "真实爻辞数据完整性", self.reporter)
    
    def run_integration_tests(self):
        """运行集成测试"""
        
        def test_64_guas_generation():
            """测试64卦生成"""
            all_guas = generate_all_64_guas()
            assert len(all_guas) == 64, f"应该生成64个卦，实际生成{len(all_guas)}个"
            
            for gua_name, gua_card in all_guas.items():
                assert isinstance(gua_card, GuaCard)
                assert len(gua_card.tasks) == 6
                assert gua_card.name == gua_name
        
        def test_authentic_yao_ci_integration():
            """测试真实爻辞系统集成"""
            # 测试有真实爻辞数据的卦
            for gua_name in AUTHENTIC_YAO_CI_DATA.keys():
                tasks = generate_authentic_yao_ci_tasks(gua_name)
                assert len(tasks) == 6, f"{gua_name}应该生成6个任务"
                
                for task in tasks:
                    assert isinstance(task, YaoCiTask)
                    assert task.name
                    assert task.description
        
        def test_game_state_integration():
            """测试游戏状态集成"""
            from game_state import Avatar, AvatarName
            avatar1 = Avatar(AvatarName.HERMIT, "隐士", "隐士能力")
            avatar2 = Avatar(AvatarName.EMPEROR, "帝王", "帝王能力")
            player1 = Player("玩家1", avatar1)
            player2 = Player("玩家2", avatar2)
            
            game = GameState([player1, player2])
            
            assert len(game.players) == 2
            assert game.current_player_index == 0
        
        def test_wisdom_system_integration():
            """测试智慧系统集成"""
            from game_state import Avatar, AvatarName
            from wisdom_system import WisdomSystem
            avatar = Avatar(AvatarName.HERMIT, "隐士", "隐士能力")
            player = Player("测试玩家", avatar)
            wisdom_system_instance = WisdomSystem()
            assert hasattr(wisdom_system_instance, 'database')
            assert hasattr(wisdom_system_instance, 'player_activated_wisdom')
            assert hasattr(wisdom_system_instance, 'player_wisdom_progress')
        
        def test_achievement_system_integration():
            """测试成就系统集成"""
            from game_state import Avatar, AvatarName
            from achievement_system import AchievementSystem
            avatar = Avatar(AvatarName.HERMIT, "隐士", "隐士能力")
            player = Player("测试玩家", avatar)
            
            # 模拟达成成就的条件
            player.dao_xing = 50
            
            # 验证成就系统存在性
            achievement_system_instance = AchievementSystem()
            assert achievement_system_instance is not None
            assert hasattr(achievement_system_instance, 'database')
            assert hasattr(achievement_system_instance, 'player_achievements')
        
        # 运行集成测试
        test_runner(test_64_guas_generation, "64卦生成集成", self.reporter)
        test_runner(test_authentic_yao_ci_integration, "真实爻辞系统集成", self.reporter)
        test_runner(test_game_state_integration, "游戏状态集成", self.reporter)
        test_runner(test_wisdom_system_integration, "智慧系统集成", self.reporter)
        test_runner(test_achievement_system_integration, "成就系统集成", self.reporter)
    
    def run_performance_tests(self):
        """运行性能测试"""
        
        def test_64_guas_generation_performance():
            """测试64卦生成性能"""
            start_time = time.time()
            all_guas = generate_all_64_guas()
            generation_time = time.time() - start_time
            
            assert generation_time < 5.0, f"64卦生成耗时过长: {generation_time:.2f}秒"
            assert len(all_guas) == 64
        
        def test_authentic_yao_ci_performance():
            """测试真实爻辞生成性能"""
            start_time = time.time()
            
            for gua_name in list(AUTHENTIC_YAO_CI_DATA.keys())[:3]:  # 测试前3个卦
                tasks = generate_authentic_yao_ci_tasks(gua_name)
                assert len(tasks) == 6
            
            generation_time = time.time() - start_time
            assert generation_time < 1.0, f"真实爻辞生成耗时过长: {generation_time:.2f}秒"
        
        def test_game_state_operations_performance():
            """测试游戏状态操作性能"""
            from game_state import Avatar, AvatarName
            
            start_time = time.time()
            players = []
            for i in range(100):
                avatar = Avatar(AvatarName.HERMIT, "隐士", "隐士能力")
                player = Player(f"玩家{i}", avatar)
                players.append(player)
            
            game = GameState(players)
            operation_time = time.time() - start_time
            assert operation_time < 1.0, f"游戏状态操作耗时过长: {operation_time:.2f}秒"
        
        # 运行性能测试
        test_runner(test_64_guas_generation_performance, "64卦生成性能", self.reporter)
        test_runner(test_authentic_yao_ci_performance, "真实爻辞生成性能", self.reporter)
        test_runner(test_game_state_operations_performance, "游戏状态操作性能", self.reporter)
    
    def run_data_integrity_tests(self):
        """运行数据完整性测试"""
        
        def test_gua_64_info_integrity():
            """测试64卦信息完整性"""
            assert len(GUA_64_INFO) == 64, f"GUA_64_INFO应该包含64个卦，实际{len(GUA_64_INFO)}个"
            
            for gua_name, gua_info in GUA_64_INFO.items():
                assert 'trigrams' in gua_info, f"{gua_name}缺少卦象信息"
                assert 'nature' in gua_info, f"{gua_name}缺少性质信息"
                assert 'element' in gua_info, f"{gua_name}缺少五行信息"
                assert 'yin_yang' in gua_info, f"{gua_name}缺少阴阳信息"
        
        def test_authentic_yao_ci_consistency():
            """测试真实爻辞数据一致性"""
            for gua_name, yao_ci_list in AUTHENTIC_YAO_CI_DATA.items():
                assert len(yao_ci_list) == 6, f"{gua_name}爻辞数量错误"
                
                for i, yao_ci in enumerate(yao_ci_list):
                    # 验证爻辞位置字段存在且不为空
                    assert hasattr(yao_ci, 'position'), f"{gua_name}第{i+1}爻缺少位置信息"
                    assert yao_ci.position, f"{gua_name}第{i+1}爻位置为空"
                    assert yao_ci.original_text, f"{gua_name}第{i+1}爻缺少原文"
                    assert yao_ci.interpretation, f"{gua_name}第{i+1}爻缺少释义"
        
        def test_task_reward_balance():
            """测试任务奖励平衡性"""
            all_guas = generate_all_64_guas()
            
            total_dao_xing = 0
            total_cheng_yi = 0
            task_count = 0
            
            for gua_card in all_guas.values():
                for task in gua_card.tasks:
                    total_dao_xing += task.reward_dao_xing
                    total_cheng_yi += task.reward_cheng_yi
                    task_count += 1
            
            avg_dao_xing = total_dao_xing / task_count
            avg_cheng_yi = total_cheng_yi / task_count
            
            # 验证平均奖励在合理范围内
            assert 0.5 <= avg_dao_xing <= 3.0, f"道行奖励平均值异常: {avg_dao_xing}"
            assert 0.5 <= avg_cheng_yi <= 3.0, f"诚意奖励平均值异常: {avg_cheng_yi}"
        
        # 运行数据完整性测试
        test_runner(test_gua_64_info_integrity, "64卦信息完整性", self.reporter)
        test_runner(test_authentic_yao_ci_consistency, "真实爻辞数据一致性", self.reporter)
        test_runner(test_task_reward_balance, "任务奖励平衡性", self.reporter)

def main():
    """主函数"""
    suite = ComprehensiveTestSuite()
    suite.run_all_tests()

if __name__ == "__main__":
    main()