"""
成就系统
提供游戏成就追踪和奖励机制
"""

import random
from typing import Dict, List, Optional, Set, Callable
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from game_state import Player, GameState

class AchievementCategory(Enum):
    """成就类别"""
    BASIC = "基础成就"
    MASTERY = "精通成就"
    EXPLORATION = "探索成就"
    WISDOM = "智慧成就"
    STRATEGY = "策略成就"
    LEGENDARY = "传奇成就"

class AchievementRarity(Enum):
    """成就稀有度"""
    COMMON = "普通"
    RARE = "稀有"
    EPIC = "史诗"
    LEGENDARY = "传奇"

@dataclass
class Achievement:
    """成就数据结构"""
    id: str
    title: str
    description: str
    category: AchievementCategory
    rarity: AchievementRarity
    icon: str
    condition_description: str
    check_function: Callable
    reward_qi: int = 0
    reward_dao_xing: int = 0
    reward_cheng_yi: int = 0
    reward_description: str = ""
    hidden: bool = False  # 隐藏成就
    prerequisite_achievements: List[str] = None

@dataclass
class PlayerAchievement:
    """玩家成就记录"""
    achievement_id: str
    unlocked_at: datetime
    progress_data: Dict = None

class AchievementTracker:
    """成就追踪器"""
    
    def __init__(self):
        self.player_stats: Dict[str, Dict] = {}
        self.player_achievements: Dict[str, List[PlayerAchievement]] = {}
        self.session_stats: Dict[str, Dict] = {}
    
    def init_player_stats(self, player_name: str):
        """初始化玩家统计数据"""
        if player_name not in self.player_stats:
            self.player_stats[player_name] = {
                "games_played": 0,
                "games_won": 0,
                "total_qi_gained": 0,
                "total_dao_xing_gained": 0,
                "total_cheng_yi_gained": 0,
                "cards_played": 0,
                "zones_controlled": 0,
                "meditations_performed": 0,
                "studies_performed": 0,
                "yijing_consultations": 0,
                "wisdom_quotes_unlocked": 0,
                "tutorials_completed": 0,
                "max_qi_in_game": 0,
                "max_dao_xing_in_game": 0,
                "max_cheng_yi_in_game": 0,
                "consecutive_wins": 0,
                "perfect_balance_turns": 0,
                "five_element_combos": 0,
                "legendary_cards_played": 0
            }
        
        if player_name not in self.session_stats:
            self.session_stats[player_name] = {
                "session_qi_gained": 0,
                "session_cards_played": 0,
                "session_zones_controlled": 0,
                "session_start_time": datetime.now()
            }
    
    def update_stat(self, player_name: str, stat_name: str, value: int = 1):
        """更新玩家统计数据"""
        self.init_player_stats(player_name)
        if stat_name in self.player_stats[player_name]:
            self.player_stats[player_name][stat_name] += value
    
    def set_stat(self, player_name: str, stat_name: str, value: int):
        """设置玩家统计数据"""
        self.init_player_stats(player_name)
        if stat_name in self.player_stats[player_name]:
            self.player_stats[player_name][stat_name] = max(
                self.player_stats[player_name][stat_name], value
            )
    
    def get_stat(self, player_name: str, stat_name: str) -> int:
        """获取玩家统计数据"""
        self.init_player_stats(player_name)
        return self.player_stats[player_name].get(stat_name, 0)

class AchievementDatabase:
    """成就数据库"""
    
    def __init__(self):
        self.achievements = self._initialize_achievements()
    
    def _initialize_achievements(self) -> Dict[str, Achievement]:
        """初始化成就数据库"""
        achievements = {}
        
        # 基础成就
        achievements["first_game"] = Achievement(
            id="first_game",
            title="初入天机",
            description="完成你的第一局游戏",
            category=AchievementCategory.BASIC,
            rarity=AchievementRarity.COMMON,
            icon="[游戏]",
            condition_description="完成1局游戏",
            check_function=lambda tracker, player: tracker.get_stat(player, "games_played") >= 1,
            reward_qi=5,
            reward_description="获得初学者的勇气"
        )
        
        achievements["first_victory"] = Achievement(
            id="first_victory",
            title="初尝胜果",
            description="赢得你的第一场胜利",
            category=AchievementCategory.BASIC,
            rarity=AchievementRarity.COMMON,
            icon="🏆",
            condition_description="获得1次胜利",
            check_function=lambda tracker, player: tracker.get_stat(player, "games_won") >= 1,
            reward_dao_xing=2,
            reward_description="智慧的第一步"
        )
        
        achievements["zone_master"] = Achievement(
            id="zone_master",
            title="区域掌控者",
            description="在单局游戏中控制5个或更多区域",
            category=AchievementCategory.BASIC,
            rarity=AchievementRarity.RARE,
            icon="[地图]",
            condition_description="单局控制5个区域",
            check_function=lambda tracker, player: tracker.get_stat(player, "zones_controlled") >= 5,
            reward_cheng_yi=3,
            reward_description="展现卓越的战略眼光"
        )
        
        # 精通成就
        achievements["qi_master"] = Achievement(
            id="qi_master",
            title="气之大师",
            description="在单局游戏中气达到20点或以上",
            category=AchievementCategory.MASTERY,
            rarity=AchievementRarity.RARE,
            icon="[电]",
            condition_description="单局气达到20点",
            check_function=lambda tracker, player: tracker.get_stat(player, "max_qi_in_game") >= 20,
            reward_qi=10,
            reward_description="掌握气的奥秘"
        )
        
        achievements["wisdom_seeker"] = Achievement(
            id="wisdom_seeker",
            title="求道者",
            description="道行达到15点或以上",
            category=AchievementCategory.MASTERY,
            rarity=AchievementRarity.EPIC,
            icon="[书]",
            condition_description="道行达到15点",
            check_function=lambda tracker, player: tracker.get_stat(player, "max_dao_xing_in_game") >= 15,
            reward_dao_xing=5,
            reward_description="智慧的深度探索"
        )
        
        achievements["sincere_heart"] = Achievement(
            id="sincere_heart",
            title="至诚之心",
            description="诚意达到12点或以上",
            category=AchievementCategory.MASTERY,
            rarity=AchievementRarity.EPIC,
            icon="[钻]",
            condition_description="诚意达到12点",
            check_function=lambda tracker, player: tracker.get_stat(player, "max_cheng_yi_in_game") >= 12,
            reward_cheng_yi=5,
            reward_description="内心修养的极致"
        )
        
        # 探索成就
        achievements["card_collector"] = Achievement(
            id="card_collector",
            title="卡牌收藏家",
            description="累计打出100张卡牌",
            category=AchievementCategory.EXPLORATION,
            rarity=AchievementRarity.RARE,
            icon="[卡牌]",
            condition_description="累计打出100张卡牌",
            check_function=lambda tracker, player: tracker.get_stat(player, "cards_played") >= 100,
            reward_qi=8,
            reward_dao_xing=3,
            reward_description="对卡牌的深度理解"
        )
        
        achievements["meditation_master"] = Achievement(
            id="meditation_master",
            title="冥想大师",
            description="累计进行50次冥想",
            category=AchievementCategory.EXPLORATION,
            rarity=AchievementRarity.RARE,
            icon="🧘",
            condition_description="累计冥想50次",
            check_function=lambda tracker, player: tracker.get_stat(player, "meditations_performed") >= 50,
            reward_qi=15,
            reward_description="冥想的深层境界"
        )
        
        achievements["scholar"] = Achievement(
            id="scholar",
            title="博学之士",
            description="累计进行30次学习",
            category=AchievementCategory.EXPLORATION,
            rarity=AchievementRarity.RARE,
            icon="[书]",
            condition_description="累计学习30次",
            check_function=lambda tracker, player: tracker.get_stat(player, "studies_performed") >= 30,
            reward_dao_xing=8,
            reward_description="知识的积累者"
        )
        
        # 智慧成就
        achievements["yijing_consultant"] = Achievement(
            id="yijing_consultant",
            title="易经顾问",
            description="累计咨询易经20次",
            category=AchievementCategory.WISDOM,
            rarity=AchievementRarity.EPIC,
            icon="[卷]",
            condition_description="累计咨询易经20次",
            check_function=lambda tracker, player: tracker.get_stat(player, "yijing_consultations") >= 20,
            reward_dao_xing=6,
            reward_cheng_yi=4,
            reward_description="易经智慧的传承者"
        )
        
        achievements["wisdom_collector"] = Achievement(
            id="wisdom_collector",
            title="智慧收集者",
            description="解锁10条智慧格言",
            category=AchievementCategory.WISDOM,
            rarity=AchievementRarity.EPIC,
            icon="[提示]",
            condition_description="解锁10条智慧格言",
            check_function=lambda tracker, player: tracker.get_stat(player, "wisdom_quotes_unlocked") >= 10,
            reward_dao_xing=7,
            reward_description="智慧的汇聚者"
        )
        
        achievements["perfect_student"] = Achievement(
            id="perfect_student",
            title="完美学生",
            description="完成所有教程课程",
            category=AchievementCategory.WISDOM,
            rarity=AchievementRarity.LEGENDARY,
            icon="🎓",
            condition_description="完成所有教程",
            check_function=lambda tracker, player: tracker.get_stat(player, "tutorials_completed") >= 8,
            reward_qi=20,
            reward_dao_xing=10,
            reward_cheng_yi=8,
            reward_description="知识的完美掌握者"
        )
        
        # 策略成就
        achievements["balance_keeper"] = Achievement(
            id="balance_keeper",
            title="平衡守护者",
            description="连续5回合保持阴阳平衡",
            category=AchievementCategory.STRATEGY,
            rarity=AchievementRarity.EPIC,
            icon="[阴阳]",
            condition_description="连续5回合阴阳平衡",
            check_function=lambda tracker, player: tracker.get_stat(player, "perfect_balance_turns") >= 5,
            reward_qi=12,
            reward_cheng_yi=6,
            reward_description="阴阳平衡的守护者"
        )
        
        achievements["element_master"] = Achievement(
            id="element_master",
            title="五行大师",
            description="成功触发10次五行组合效果",
            category=AchievementCategory.STRATEGY,
            rarity=AchievementRarity.EPIC,
            icon="[星]",
            condition_description="触发10次五行组合",
            check_function=lambda tracker, player: tracker.get_stat(player, "five_element_combos") >= 10,
            reward_dao_xing=8,
            reward_description="五行相生的掌控者"
        )
        
        achievements["winning_streak"] = Achievement(
            id="winning_streak",
            title="连胜王者",
            description="连续获得5场胜利",
            category=AchievementCategory.STRATEGY,
            rarity=AchievementRarity.LEGENDARY,
            icon="👑",
            condition_description="连续5场胜利",
            check_function=lambda tracker, player: tracker.get_stat(player, "consecutive_wins") >= 5,
            reward_qi=25,
            reward_dao_xing=15,
            reward_cheng_yi=10,
            reward_description="无可匹敌的战略家"
        )
        
        # 传奇成就
        achievements["legendary_player"] = Achievement(
            id="legendary_player",
            title="传奇修行者",
            description="使用传奇卡牌10次",
            category=AchievementCategory.LEGENDARY,
            rarity=AchievementRarity.LEGENDARY,
            icon="🌠",
            condition_description="使用10张传奇卡牌",
            check_function=lambda tracker, player: tracker.get_stat(player, "legendary_cards_played") >= 10,
            reward_qi=30,
            reward_dao_xing=20,
            reward_cheng_yi=15,
            reward_description="传奇的力量掌控者",
            hidden=True
        )
        
        achievements["grand_master"] = Achievement(
            id="grand_master",
            title="天机大师",
            description="完成100局游戏并获得50场胜利",
            category=AchievementCategory.LEGENDARY,
            rarity=AchievementRarity.LEGENDARY,
            icon="🏮",
            condition_description="100局游戏，50场胜利",
            check_function=lambda tracker, player: (
                tracker.get_stat(player, "games_played") >= 100 and 
                tracker.get_stat(player, "games_won") >= 50
            ),
            reward_qi=50,
            reward_dao_xing=30,
            reward_cheng_yi=25,
            reward_description="天机变的终极大师",
            hidden=True
        )
        
        # 新增成就 - 修行成就
        achievements["dao_seeker"] = Achievement(
            id="dao_seeker",
            title="求道者",
            description="道行达到15点",
            category=AchievementCategory.MASTERY,
            rarity=AchievementRarity.RARE,
            icon="🌟",
            condition_description="道行达到15点",
            check_function=lambda tracker, player: tracker.get_stat(player, "max_dao_xing_in_game") >= 15,
            reward_dao_xing=3,
            reward_description="道的追求者"
        )
        
        achievements["harmony_master"] = Achievement(
            id="harmony_master",
            title="和谐大师",
            description="在单局游戏中保持完美阴阳平衡10回合",
            category=AchievementCategory.STRATEGY,
            rarity=AchievementRarity.EPIC,
            icon="☯️",
            condition_description="保持完美阴阳平衡10回合",
            check_function=lambda tracker, player: tracker.get_stat(player, "perfect_balance_turns") >= 10,
            reward_qi=12,
            reward_dao_xing=8,
            reward_description="阴阳和谐的掌控者"
        )
        
        achievements["element_sage"] = Achievement(
            id="element_sage",
            title="五行贤者",
            description="成功触发五行相生组合20次",
            category=AchievementCategory.STRATEGY,
            rarity=AchievementRarity.EPIC,
            icon="🌈",
            condition_description="触发五行相生组合20次",
            check_function=lambda tracker, player: tracker.get_stat(player, "five_element_combos") >= 20,
            reward_dao_xing=10,
            reward_cheng_yi=5,
            reward_description="五行奥秘的领悟者"
        )
        
        achievements["transformation_artist"] = Achievement(
            id="transformation_artist",
            title="变化艺术家",
            description="成功进行变卦50次",
            category=AchievementCategory.EXPLORATION,
            rarity=AchievementRarity.RARE,
            icon="🔄",
            condition_description="成功变卦50次",
            check_function=lambda tracker, player: tracker.get_stat(player, "successful_transformations") >= 50,
            reward_qi=10,
            reward_dao_xing=5,
            reward_description="变化之道的艺术家"
        )
        
        achievements["wisdom_seeker"] = Achievement(
            id="wisdom_seeker",
            title="智慧求索者",
            description="解锁25条智慧格言",
            category=AchievementCategory.WISDOM,
            rarity=AchievementRarity.LEGENDARY,
            icon="📚",
            condition_description="解锁25条智慧格言",
            check_function=lambda tracker, player: tracker.get_stat(player, "wisdom_quotes_unlocked") >= 25,
            reward_dao_xing=15,
            reward_cheng_yi=10,
            reward_description="智慧的真正求索者"
        )
        
        achievements["perfect_game"] = Achievement(
            id="perfect_game",
            title="完美游戏",
            description="在单局游戏中同时达到气20、道行15、诚意12",
            category=AchievementCategory.LEGENDARY,
            rarity=AchievementRarity.LEGENDARY,
            icon="💎",
            condition_description="单局达到气20、道行15、诚意12",
            check_function=lambda tracker, player: (
                tracker.get_stat(player, "max_qi_in_game") >= 20 and
                tracker.get_stat(player, "max_dao_xing_in_game") >= 15 and
                tracker.get_stat(player, "max_cheng_yi_in_game") >= 12
            ),
            reward_qi=25,
            reward_dao_xing=15,
            reward_cheng_yi=10,
            reward_description="修行的完美境界",
            hidden=True
        )
        
        achievements["speed_runner"] = Achievement(
            id="speed_runner",
            title="疾风修行者",
            description="在15回合内获得胜利",
            category=AchievementCategory.STRATEGY,
            rarity=AchievementRarity.EPIC,
            icon="⚡",
            condition_description="15回合内获胜",
            check_function=lambda tracker, player: tracker.get_stat(player, "fastest_victory") <= 15 and tracker.get_stat(player, "fastest_victory") > 0,
            reward_qi=15,
            reward_dao_xing=8,
            reward_description="迅速的智慧掌控者"
        )
        
        achievements["persistent_learner"] = Achievement(
            id="persistent_learner",
            title="坚持学习者",
            description="连续7天进行游戏",
            category=AchievementCategory.EXPLORATION,
            rarity=AchievementRarity.RARE,
            icon="📅",
            condition_description="连续7天游戏",
            check_function=lambda tracker, player: tracker.get_stat(player, "consecutive_play_days") >= 7,
            reward_dao_xing=6,
            reward_cheng_yi=4,
            reward_description="持之以恒的修行者"
        )
        
        achievements["card_master"] = Achievement(
            id="card_master",
            title="卡牌大师",
            description="使用过所有基础卦牌",
            category=AchievementCategory.EXPLORATION,
            rarity=AchievementRarity.EPIC,
            icon="🃏",
            condition_description="使用所有基础卦牌",
            check_function=lambda tracker, player: tracker.get_stat(player, "unique_cards_played") >= 64,  # 64卦
            reward_qi=20,
            reward_dao_xing=12,
            reward_description="卦牌的完全掌控者"
        )
        
        achievements["mentor"] = Achievement(
            id="mentor",
            title="智慧导师",
            description="帮助其他玩家完成10次学习",
            category=AchievementCategory.WISDOM,
            rarity=AchievementRarity.LEGENDARY,
            icon="👨‍🏫",
            condition_description="帮助他人学习10次",
            check_function=lambda tracker, player: tracker.get_stat(player, "helped_others_learn") >= 10,
            reward_dao_xing=20,
            reward_cheng_yi=15,
            reward_description="智慧的传播者",
            hidden=True
        )

        return achievements
    
    def get_achievement(self, achievement_id: str) -> Optional[Achievement]:
        """获取指定成就"""
        return self.achievements.get(achievement_id)
    
    def get_achievements_by_category(self, category: AchievementCategory) -> List[Achievement]:
        """按类别获取成就"""
        return [ach for ach in self.achievements.values() if ach.category == category]
    
    def get_achievements_by_rarity(self, rarity: AchievementRarity) -> List[Achievement]:
        """按稀有度获取成就"""
        return [ach for ach in self.achievements.values() if ach.rarity == rarity]

class AchievementSystem:
    """成就系统管理器"""
    
    def __init__(self):
        self.database = AchievementDatabase()
        self.tracker = AchievementTracker()
        self.player_achievements: Dict[str, Set[str]] = {}
    
    def get_player_achievements(self, player_name: str) -> Set[str]:
        """获取玩家已解锁的成就"""
        if player_name not in self.player_achievements:
            self.player_achievements[player_name] = set()
        return self.player_achievements[player_name]
    
    def check_achievements(self, player_name: str) -> List[Achievement]:
        """检查并解锁新成就"""
        unlocked_achievements = []
        player_unlocked = self.get_player_achievements(player_name)
        
        for achievement in self.database.achievements.values():
            if achievement.id not in player_unlocked:
                # 检查前置成就
                if achievement.prerequisite_achievements:
                    if not all(prereq in player_unlocked for prereq in achievement.prerequisite_achievements):
                        continue
                
                # 检查成就条件
                if achievement.check_function(self.tracker, player_name):
                    player_unlocked.add(achievement.id)
                    unlocked_achievements.append(achievement)
        
        return unlocked_achievements
    
    def award_achievement_rewards(self, player: Player, achievement: Achievement):
        """给予成就奖励"""
        if achievement.reward_qi > 0:
            player.qi = min(25, player.qi + achievement.reward_qi)
        
        if achievement.reward_dao_xing > 0:
            player.dao_xing = min(20, player.dao_xing + achievement.reward_dao_xing)
        
        if achievement.reward_cheng_yi > 0:
            player.cheng_yi = min(15, player.cheng_yi + achievement.reward_cheng_yi)
    
    def display_achievement_unlock(self, achievement: Achievement):
        """显示成就解锁信息"""
        rarity_colors = {
            AchievementRarity.COMMON: "⚪",
            AchievementRarity.RARE: "🔵", 
            AchievementRarity.EPIC: "🟣",
            AchievementRarity.LEGENDARY: "🟡"
        }
        
        color = rarity_colors.get(achievement.rarity, "⚪")
        print(f"\n[成功] 成就解锁！ {color}")
        print("=" * 50)
        print(f"{achievement.icon} {achievement.title}")
        print(f"[笔] {achievement.description}")
        print(f"[标签] {achievement.category.value} - {achievement.rarity.value}")
        
        rewards = []
        if achievement.reward_qi > 0:
            rewards.append(f"+{achievement.reward_qi}气")
        if achievement.reward_dao_xing > 0:
            rewards.append(f"+{achievement.reward_dao_xing}道行")
        if achievement.reward_cheng_yi > 0:
            rewards.append(f"+{achievement.reward_cheng_yi}诚意")
        
        if rewards:
            print(f"🎁 奖励：{', '.join(rewards)}")
        
        if achievement.reward_description:
            print(f"[星] {achievement.reward_description}")
        
        print("=" * 50)
    
    def display_achievement_progress(self, player_name: str):
        """显示成就进度"""
        unlocked = self.get_player_achievements(player_name)
        total_achievements = len(self.database.achievements)
        unlocked_count = len(unlocked)
        
        print(f"\n🏆 {player_name} 的成就进度")
        print("=" * 60)
        print(f"总体进度: {unlocked_count}/{total_achievements} ({unlocked_count/total_achievements*100:.1f}%)")
        
        # 按类别统计
        category_stats = {}
        for category in AchievementCategory:
            category_achievements = self.database.get_achievements_by_category(category)
            category_unlocked = sum(1 for ach in category_achievements if ach.id in unlocked)
            category_stats[category] = {
                "unlocked": category_unlocked,
                "total": len(category_achievements),
                "percentage": (category_unlocked / len(category_achievements)) * 100 if category_achievements else 0
            }
        
        print("\n分类进度:")
        for category, stats in category_stats.items():
            print(f"  {category.value}: {stats['unlocked']}/{stats['total']} ({stats['percentage']:.1f}%)")
        
        # 按稀有度统计
        print("\n稀有度统计:")
        for rarity in AchievementRarity:
            rarity_achievements = self.database.get_achievements_by_rarity(rarity)
            rarity_unlocked = sum(1 for ach in rarity_achievements if ach.id in unlocked)
            if rarity_achievements:
                print(f"  {rarity.value}: {rarity_unlocked}/{len(rarity_achievements)}")
        
        print("=" * 60)
    
    def display_available_achievements(self, player_name: str, show_hidden: bool = False):
        """显示可用成就列表"""
        unlocked = self.get_player_achievements(player_name)
        
        print(f"\n[目标] 成就列表")
        print("=" * 60)
        
        for category in AchievementCategory:
            achievements = self.database.get_achievements_by_category(category)
            if not achievements:
                continue
            
            print(f"\n📂 {category.value}")
            print("-" * 40)
            
            for achievement in achievements:
                if achievement.hidden and not show_hidden and achievement.id not in unlocked:
                    continue
                
                status = "[完成]" if achievement.id in unlocked else "[等待]"
                rarity_icon = {
                    AchievementRarity.COMMON: "⚪",
                    AchievementRarity.RARE: "🔵",
                    AchievementRarity.EPIC: "🟣", 
                    AchievementRarity.LEGENDARY: "🟡"
                }.get(achievement.rarity, "⚪")
                
                if achievement.hidden and achievement.id not in unlocked:
                    print(f"  {status} {rarity_icon} ??? - 隐藏成就")
                else:
                    print(f"  {status} {rarity_icon} {achievement.title}")
                    print(f"      {achievement.description}")
                    print(f"      条件: {achievement.condition_description}")
        
        print("=" * 60)
    
    # 统计更新方法
    def on_game_start(self, player_name: str):
        """游戏开始时调用"""
        self.tracker.init_player_stats(player_name)
    
    def on_game_end(self, player_name: str, won: bool):
        """游戏结束时调用"""
        self.tracker.update_stat(player_name, "games_played")
        if won:
            self.tracker.update_stat(player_name, "games_won")
            self.tracker.update_stat(player_name, "consecutive_wins")
        else:
            self.tracker.set_stat(player_name, "consecutive_wins", 0)
    
    def on_card_played(self, player_name: str, card_rarity: str = "common"):
        """打出卡牌时调用"""
        self.tracker.update_stat(player_name, "cards_played")
        if card_rarity == "legendary":
            self.tracker.update_stat(player_name, "legendary_cards_played")
    
    def on_meditation(self, player_name: str):
        """冥想时调用"""
        self.tracker.update_stat(player_name, "meditations_performed")
    
    def on_study(self, player_name: str):
        """学习时调用"""
        self.tracker.update_stat(player_name, "studies_performed")
    
    def on_yijing_consultation(self, player_name: str):
        """咨询易经时调用"""
        self.tracker.update_stat(player_name, "yijing_consultations")
    
    def on_wisdom_unlock(self, player_name: str):
        """解锁智慧格言时调用"""
        self.tracker.update_stat(player_name, "wisdom_quotes_unlocked")
    
    def on_tutorial_complete(self, player_name: str):
        """完成教程时调用"""
        self.tracker.update_stat(player_name, "tutorials_completed")
    
    def on_resource_update(self, player_name: str, qi: int, dao_xing: int, cheng_yi: int):
        """资源更新时调用"""
        self.tracker.set_stat(player_name, "max_qi_in_game", qi)
        self.tracker.set_stat(player_name, "max_dao_xing_in_game", dao_xing)
        self.tracker.set_stat(player_name, "max_cheng_yi_in_game", cheng_yi)
    
    def on_zone_control(self, player_name: str, zone_count: int):
        """区域控制时调用"""
        self.tracker.set_stat(player_name, "zones_controlled", zone_count)
    
    def on_balance_turn(self, player_name: str):
        """保持平衡回合时调用"""
        self.tracker.update_stat(player_name, "perfect_balance_turns")
    
    def on_element_combo(self, player_name: str):
        """五行组合时调用"""
        self.tracker.update_stat(player_name, "five_element_combos")

    def on_successful_transformation(self, player_name: str):
        """成功变卦时调用"""
        self.tracker.update_stat(player_name, "successful_transformations")
    
    def on_unique_card_played(self, player_name: str, card_name: str):
        """使用新卡牌时调用"""
        # 追踪独特卡牌使用
        unique_cards_key = f"{player_name}_unique_cards"
        if unique_cards_key not in self.tracker.player_stats:
            self.tracker.player_stats[unique_cards_key] = set()
        
        self.tracker.player_stats[unique_cards_key].add(card_name)
        self.tracker.set_stat(player_name, "unique_cards_played", len(self.tracker.player_stats[unique_cards_key]))
    
    def on_help_other_learn(self, player_name: str):
        """帮助他人学习时调用"""
        self.tracker.update_stat(player_name, "helped_others_learn")
    
    def on_daily_play(self, player_name: str):
        """每日游戏时调用"""
        from datetime import datetime, timedelta
        today = datetime.now().date()
        
        # 获取上次游戏日期
        last_play_key = f"{player_name}_last_play_date"
        if last_play_key not in self.tracker.player_stats:
            self.tracker.player_stats[last_play_key] = today
            self.tracker.set_stat(player_name, "consecutive_play_days", 1)
        else:
            last_date = self.tracker.player_stats[last_play_key]
            if isinstance(last_date, str):
                last_date = datetime.strptime(last_date, "%Y-%m-%d").date()
            
            if today == last_date + timedelta(days=1):
                # 连续游戏
                self.tracker.update_stat(player_name, "consecutive_play_days")
            elif today == last_date:
                # 同一天，不更新
                pass
            else:
                # 中断了，重新开始
                self.tracker.set_stat(player_name, "consecutive_play_days", 1)
            
            self.tracker.player_stats[last_play_key] = today
    
    def on_victory_with_turns(self, player_name: str, turns: int):
        """记录胜利回合数"""
        current_fastest = self.tracker.get_stat(player_name, "fastest_victory")
        if current_fastest == 0 or turns < current_fastest:
            self.tracker.set_stat(player_name, "fastest_victory", turns)
    
    def display_achievement_categories(self):
        """显示成就分类信息"""
        print("\n🏆 成就系统分类")
        print("=" * 60)
        
        for category in AchievementCategory:
            achievements = self.database.get_achievements_by_category(category)
            print(f"\n📂 {category.value} ({len(achievements)}个成就)")
            
            for achievement in achievements[:3]:  # 显示前3个作为示例
                rarity_icon = {
                    AchievementRarity.COMMON: "⚪",
                    AchievementRarity.RARE: "🔵",
                    AchievementRarity.EPIC: "🟣",
                    AchievementRarity.LEGENDARY: "🟡"
                }.get(achievement.rarity, "⚪")
                
                print(f"  {rarity_icon} {achievement.icon} {achievement.title}")
                print(f"     {achievement.description}")
            
            if len(achievements) > 3:
                print(f"     ... 还有 {len(achievements) - 3} 个成就")
    
    def get_achievement_hints(self, player_name: str) -> List[str]:
        """获取成就提示"""
        hints = []
        unlocked = self.get_player_achievements(player_name)
        
        # 找到接近完成的成就
        for achievement in self.database.achievements.values():
            if achievement.id not in unlocked and not achievement.hidden:
                # 简单的进度估算
                if "games_played" in achievement.condition_description:
                    current = self.tracker.get_stat(player_name, "games_played")
                    if current >= 1:  # 已经开始游戏
                        hints.append(f"💡 继续游戏来解锁 '{achievement.title}'")
                elif "dao_xing" in achievement.condition_description:
                    current = self.tracker.get_stat(player_name, "max_dao_xing_in_game")
                    if current >= 10:  # 道行已有一定基础
                        hints.append(f"💡 提升道行来解锁 '{achievement.title}'")
        
        return hints[:3]  # 最多返回3个提示

# 全局成就系统实例
achievement_system = AchievementSystem()