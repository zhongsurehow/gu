"""
教学系统
提供易经知识学习和游戏指导功能
"""

import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from game_state import Player, GameState

class TutorialType(Enum):
    """教程类型"""
    BASIC_RULES = "基础规则"
    YIJING_KNOWLEDGE = "易经知识"
    STRATEGY_GUIDE = "策略指导"
    ADVANCED_TACTICS = "高级战术"

class LearningLevel(Enum):
    """学习等级"""
    BEGINNER = "初学者"
    INTERMEDIATE = "进阶者"
    ADVANCED = "高级者"
    MASTER = "大师"

@dataclass
class TutorialLesson:
    """教程课程数据结构"""
    id: str
    title: str
    type: TutorialType
    level: LearningLevel
    content: str
    practical_example: str
    quiz_question: str
    quiz_options: List[str]
    correct_answer: int
    reward_description: str
    qi_reward: int = 0
    dao_xing_reward: int = 0
    cheng_yi_reward: int = 0

class TutorialDatabase:
    """教程数据库"""
    
    def __init__(self):
        self.lessons = self._initialize_lessons()
        self.categories = {
            TutorialType.BASIC_RULES: "学习游戏的基本规则和操作",
            TutorialType.YIJING_KNOWLEDGE: "深入了解易经的哲学智慧",
            TutorialType.STRATEGY_GUIDE: "掌握游戏策略和技巧",
            TutorialType.ADVANCED_TACTICS: "学习高级战术和组合技"
        }
    
    def _initialize_lessons(self) -> Dict[str, TutorialLesson]:
        """初始化教程数据库"""
        lessons = {}
        
        # 基础规则教程
        lessons["basic_movement"] = TutorialLesson(
            id="basic_movement",
            title="基础移动与位置",
            type=TutorialType.BASIC_RULES,
            level=LearningLevel.BEGINNER,
            content="""
在天机变中，玩家可以在天、人、地三个位置之间移动：

[星] 天位 (TIAN): 代表天界，冥想时获得更多气
[玩家] 人位 (REN): 代表人间，学习时获得额外卡牌
🌍 地位 (DI): 代表地界，提供稳定的资源基础

移动消耗1点行动力和1点气，但不同位置会给予不同的修行加成。
选择合适的位置进行相应的行动，是游戏的基础策略。
            """,
            practical_example="例如：在天位冥想可以获得4点气而不是3点，在人位学习可以额外抽取1张卡牌。",
            quiz_question="在哪个位置冥想能获得最多的气？",
            quiz_options=["天位", "人位", "地位", "位置无关"],
            correct_answer=0,
            reward_description="掌握位置移动的基础知识",
            qi_reward=2,
            dao_xing_reward=1
        )
        
        lessons["resource_management"] = TutorialLesson(
            id="resource_management",
            title="资源管理基础",
            type=TutorialType.BASIC_RULES,
            level=LearningLevel.BEGINNER,
            content="""
游戏中有三种核心资源：

[电] 气 (Qi): 用于移动、使用特殊能力，通过冥想获得
[书] 道行 (Dao Xing): 代表智慧积累，通过学习和修行获得
[钻] 诚意 (Cheng Yi): 代表内心修养，影响高级能力的使用

合理分配和使用这些资源是获胜的关键。不要让任何资源闲置，
但也要为关键时刻保留足够的资源。
            """,
            practical_example="例如：保留3点气用于占卜，或积累5点道行解锁高级智慧。",
            quiz_question="哪种资源主要通过学习获得？",
            quiz_options=["气", "道行", "诚意", "影响力"],
            correct_answer=1,
            reward_description="理解资源管理的重要性",
            dao_xing_reward=2,
            cheng_yi_reward=1
        )
        
        # 易经知识教程
        lessons["yin_yang_balance"] = TutorialLesson(
            id="yin_yang_balance",
            title="阴阳平衡的智慧",
            type=TutorialType.YIJING_KNOWLEDGE,
            level=LearningLevel.INTERMEDIATE,
            content="""
阴阳是易经的核心概念，代表宇宙中相对而统一的两个方面：

[阴阳] 阴 (Yin): 代表柔、静、内敛、接受
[阴阳] 阳 (Yang): 代表刚、动、外放、主动

在游戏中，保持阴阳平衡会获得额外奖励。过度偏向任何一方
都会失去平衡的力量。真正的智慧在于动态的平衡。

"一阴一阳之谓道" - 这是易经的根本智慧。
            """,
            practical_example="当阴阳差值小于2时，每回合获得额外1点气的奖励。",
            quiz_question="易经中，阴阳的关系是？",
            quiz_options=["对立冲突", "相互补充", "等级高低", "独立存在"],
            correct_answer=1,
            reward_description="领悟阴阳平衡的智慧",
            dao_xing_reward=3,
            cheng_yi_reward=2
        )
        
        lessons["wuxing_cycle"] = TutorialLesson(
            id="wuxing_cycle",
            title="五行相生相克",
            type=TutorialType.YIJING_KNOWLEDGE,
            level=LearningLevel.INTERMEDIATE,
            content="""
五行是中国古代哲学的重要概念，包括：

🌳 木 (Mu): 生长、创造、春天
[火] 火 (Huo): 热情、光明、夏天  
🌍 土 (Tu): 稳定、包容、长夏
🔗 金 (Jin): 收敛、坚固、秋天
💧 水 (Shui): 流动、智慧、冬天

相生循环：木→火→土→金→水→木
相克循环：木克土，土克水，水克火，火克金，金克木

理解五行关系有助于选择最佳的行动时机。
            """,
            practical_example="在火属性强的时候使用木属性卡牌，可以获得相生加成。",
            quiz_question="在五行相生中，火生什么？",
            quiz_options=["木", "土", "金", "水"],
            correct_answer=1,
            reward_description="掌握五行相生相克的规律",
            dao_xing_reward=3,
            qi_reward=2
        )
        
        lessons["bagua_wisdom"] = TutorialLesson(
            id="bagua_wisdom",
            title="八卦的深层含义",
            type=TutorialType.YIJING_KNOWLEDGE,
            level=LearningLevel.ADVANCED,
            content="""
八卦是易经的基础符号系统，每个卦都有深刻的象征意义：

☰ 乾 (Qian): 天、创造、领导
☷ 坤 (Kun): 地、包容、跟随
☳ 震 (Zhen): 雷、行动、震动
☴ 巽 (Xun): 风、渗透、顺从
☵ 坎 (Kan): 水、危险、智慧
☲ 离 (Li): 火、光明、美丽
☶ 艮 (Gen): 山、停止、稳定
☱ 兑 (Dui): 泽、喜悦、交流

每个卦象都代表特定的能量和智慧，理解它们的含义
有助于在游戏中做出更明智的选择。
            """,
            practical_example="控制乾卦可以获得领导力加成，控制坤卦可以获得稳定收益。",
            quiz_question="八卦中代表'天'的是哪一卦？",
            quiz_options=["坤", "乾", "震", "巽"],
            correct_answer=1,
            reward_description="深入理解八卦的智慧",
            dao_xing_reward=4,
            cheng_yi_reward=3
        )
        
        # 策略指导教程
        lessons["zone_control"] = TutorialLesson(
            id="zone_control",
            title="区域控制策略",
            type=TutorialType.STRATEGY_GUIDE,
            level=LearningLevel.INTERMEDIATE,
            content="""
控制卦象区域是获胜的主要途径之一：

[目标] 影响力放置: 通过打牌在目标区域放置影响力标记
🏆 区域控制: 当你的影响力超过阈值时，获得该区域控制权
💰 控制奖励: 控制的区域会提供持续的资源或能力加成

策略要点：
1. 优先控制提供你需要的加成的区域
2. 阻止对手控制关键区域
3. 分散控制多个区域以获得多样化收益
4. 在关键时刻集中资源争夺重要区域
            """,
            practical_example="控制乾卦区域可以获得额外行动点，控制坤卦区域可以增加手牌上限。",
            quiz_question="区域控制的主要方式是？",
            quiz_options=["移动到该区域", "放置影响力标记", "消耗资源", "使用特殊卡牌"],
            correct_answer=1,
            reward_description="掌握区域控制的基本策略",
            cheng_yi_reward=2,
            dao_xing_reward=2
        )
        
        lessons["timing_strategy"] = TutorialLesson(
            id="timing_strategy",
            title="时机把握的艺术",
            type=TutorialType.STRATEGY_GUIDE,
            level=LearningLevel.ADVANCED,
            content="""
在天机变中，时机的把握至关重要：

[时间] 资源积累期: 游戏前期专注于积累资源和卡牌
[战斗] 竞争期: 中期开始争夺关键区域的控制权
🏆 决胜期: 后期集中资源实现胜利条件

关键时机：
- 对手资源不足时发起攻势
- 自己资源充足时扩大优势
- 接近胜利条件时的最后冲刺
- 阻止对手即将获胜的关键时刻

"知其雄，守其雌，为天下溪" - 知道何时进攻，何时防守。
            """,
            practical_example="当对手气不足时，是争夺区域控制权的最佳时机。",
            quiz_question="游戏前期最重要的是？",
            quiz_options=["争夺区域", "积累资源", "攻击对手", "使用高级卡牌"],
            correct_answer=1,
            reward_description="学会把握游戏节奏",
            dao_xing_reward=3,
            cheng_yi_reward=2
        )
        
        # 高级战术教程
        lessons["combo_mastery"] = TutorialLesson(
            id="combo_mastery",
            title="组合技巧大师",
            type=TutorialType.ADVANCED_TACTICS,
            level=LearningLevel.MASTER,
            content="""
高级玩家需要掌握各种组合技巧：

🔗 卡牌组合: 某些卡牌一起使用会产生额外效果
[电] 连击系统: 连续使用同类型行动获得递增奖励
[目标] 位置组合: 在特定位置使用特定能力获得加成
[阴阳] 阴阳五行组合: 利用阴阳五行的相互作用

大师级组合：
- 太极调和 + 阴阳平衡 = 额外回合
- 五行循环 + 对应属性卡牌 = 效果翻倍
- 天人合一 + 三才位置 = 终极修行加成

"善战者，求之于势，不责于人" - 创造有利的组合态势。
            """,
            practical_example="在天位使用乾卦卡牌，同时保持阴阳平衡，可以获得三重加成。",
            quiz_question="组合技巧的核心是？",
            quiz_options=["单一强力", "资源堆积", "协同效应", "随机运气"],
            correct_answer=2,
            reward_description="掌握高级组合技巧",
            dao_xing_reward=5,
            cheng_yi_reward=3,
            qi_reward=3
        )
        
        return lessons
    
    def get_lesson(self, lesson_id: str) -> Optional[TutorialLesson]:
        """获取指定教程"""
        return self.lessons.get(lesson_id)
    
    def get_lessons_by_type(self, tutorial_type: TutorialType) -> List[TutorialLesson]:
        """按类型获取教程"""
        return [lesson for lesson in self.lessons.values() if lesson.type == tutorial_type]
    
    def get_lessons_by_level(self, level: LearningLevel) -> List[TutorialLesson]:
        """按等级获取教程"""
        return [lesson for lesson in self.lessons.values() if lesson.level == level]

class TutorialSystem:
    """教学系统管理器"""
    
    def __init__(self):
        self.database = TutorialDatabase()
        self.player_progress: Dict[str, Dict[str, bool]] = {}
        self.player_scores: Dict[str, int] = {}
    
    def get_player_progress(self, player_name: str) -> Dict[str, bool]:
        """获取玩家学习进度"""
        if player_name not in self.player_progress:
            self.player_progress[player_name] = {}
        return self.player_progress[player_name]
    
    def get_player_score(self, player_name: str) -> int:
        """获取玩家学习分数"""
        return self.player_scores.get(player_name, 0)
    
    def start_lesson(self, player: Player, lesson_id: str) -> bool:
        """开始学习课程"""
        lesson = self.database.get_lesson(lesson_id)
        if not lesson:
            print("课程不存在")
            return False
        
        progress = self.get_player_progress(player.name)
        if progress.get(lesson_id, False):
            print("您已经完成了这个课程")
            return False
        
        self.display_lesson(lesson)
        success = self.conduct_quiz(lesson)
        
        if success:
            self.complete_lesson(player, lesson)
            progress[lesson_id] = True
            return True
        else:
            print("课程未完成，您可以稍后再试")
            return False
    
    def display_lesson(self, lesson: TutorialLesson):
        """显示课程内容"""
        print(f"\n[书] {lesson.title} ({lesson.level.value})")
        print("=" * 60)
        print(lesson.content)
        print(f"\n[提示] 实例说明：{lesson.practical_example}")
        print("=" * 60)
    
    def conduct_quiz(self, lesson: TutorialLesson) -> bool:
        """进行课程测验"""
        print(f"\n❓ 测验问题：{lesson.quiz_question}")
        for i, option in enumerate(lesson.quiz_options):
            print(f"{i + 1}. {option}")
        
        try:
            answer = int(input("请选择答案 (输入数字): ")) - 1
            if 0 <= answer < len(lesson.quiz_options):
                if answer == lesson.correct_answer:
                    print("[完成] 回答正确！")
                    return True
                else:
                    correct_option = lesson.quiz_options[lesson.correct_answer]
                    print(f"[错误] 回答错误。正确答案是：{correct_option}")
                    return False
            else:
                print("无效选择")
                return False
        except ValueError:
            print("请输入有效数字")
            return False
    
    def complete_lesson(self, player: Player, lesson: TutorialLesson):
        """完成课程，给予奖励"""
        print(f"\n[成功] 恭喜完成课程：{lesson.title}")
        print(f"[书] {lesson.reward_description}")
        
        # 给予奖励
        rewards = []
        if lesson.qi_reward > 0:
            player.qi = min(25, player.qi + lesson.qi_reward)
            rewards.append(f"+{lesson.qi_reward}气")
        
        if lesson.dao_xing_reward > 0:
            player.dao_xing = min(20, player.dao_xing + lesson.dao_xing_reward)
            rewards.append(f"+{lesson.dao_xing_reward}道行")
        
        if lesson.cheng_yi_reward > 0:
            player.cheng_yi = min(15, player.cheng_yi + lesson.cheng_yi_reward)
            rewards.append(f"+{lesson.cheng_yi_reward}诚意")
        
        if rewards:
            print(f"🎁 获得奖励：{', '.join(rewards)}")
        
        # 更新学习分数
        score_bonus = {
            LearningLevel.BEGINNER: 10,
            LearningLevel.INTERMEDIATE: 20,
            LearningLevel.ADVANCED: 30,
            LearningLevel.MASTER: 50
        }
        
        bonus = score_bonus.get(lesson.level, 10)
        self.player_scores[player.name] = self.player_scores.get(player.name, 0) + bonus
        print(f"[统计] 学习积分 +{bonus} (总计: {self.player_scores[player.name]})")
    
    def show_available_lessons(self, player_name: str, tutorial_type: Optional[TutorialType] = None):
        """显示可用课程"""
        progress = self.get_player_progress(player_name)
        
        if tutorial_type:
            lessons = self.database.get_lessons_by_type(tutorial_type)
            print(f"\n[书] {tutorial_type.value} 课程列表")
        else:
            lessons = list(self.database.lessons.values())
            print("\n[书] 所有可用课程")
        
        print("=" * 60)
        
        for i, lesson in enumerate(lessons, 1):
            status = "[完成] 已完成" if progress.get(lesson.id, False) else "[等待] 未完成"
            print(f"{i}. {lesson.title} ({lesson.level.value}) - {status}")
        
        print("=" * 60)
    
    def get_learning_statistics(self, player_name: str) -> Dict:
        """获取学习统计信息"""
        progress = self.get_player_progress(player_name)
        total_lessons = len(self.database.lessons)
        completed_count = sum(1 for completed in progress.values() if completed)
        
        type_stats = {}
        for tutorial_type in TutorialType:
            type_lessons = self.database.get_lessons_by_type(tutorial_type)
            completed_in_type = sum(1 for lesson in type_lessons if progress.get(lesson.id, False))
            type_stats[tutorial_type.value] = {
                "total": len(type_lessons),
                "completed": completed_in_type,
                "percentage": (completed_in_type / len(type_lessons)) * 100 if type_lessons else 0
            }
        
        return {
            "total_lessons": total_lessons,
            "completed_count": completed_count,
            "completion_percentage": (completed_count / total_lessons) * 100,
            "learning_score": self.get_player_score(player_name),
            "type_stats": type_stats
        }
    
    def display_learning_progress(self, player_name: str):
        """显示学习进度"""
        stats = self.get_learning_statistics(player_name)
        
        print(f"\n[统计] {player_name} 的学习进度")
        print("=" * 60)
        print(f"总体进度: {stats['completed_count']}/{stats['total_lessons']} ({stats['completion_percentage']:.1f}%)")
        print(f"学习积分: {stats['learning_score']}")
        print("\n分类进度:")
        
        for category, data in stats['type_stats'].items():
            print(f"  {category}: {data['completed']}/{data['total']} ({data['percentage']:.1f}%)")
        
        # 根据完成度给予称号
        completion_rate = stats['completion_percentage']
        if completion_rate >= 90:
            title = "易经大师 🎓"
        elif completion_rate >= 70:
            title = "博学者 [书]"
        elif completion_rate >= 50:
            title = "求知者 🔍"
        elif completion_rate >= 25:
            title = "学习者 [书]"
        else:
            title = "初学者 🌱"
        
        print(f"\n🏆 当前称号: {title}")
        print("=" * 60)

# 全局教学系统实例
tutorial_system = TutorialSystem()