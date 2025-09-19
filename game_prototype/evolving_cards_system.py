"""
演进卦象系统 - 记忆牌库系统
实现卡牌的成长、变化和局内记忆机制
"""

import json
import time
from enum import Enum
from typing import Dict, List, Optional, Set, Any, Tuple
from dataclasses import dataclass, field
from advanced_ui_system import advanced_ui, MessageType

class EvolutionTrigger(Enum):
    """进化触发条件"""
    FIRST_COMPLETION = "首次完成"      # 首次完成爻辞任务
    MULTIPLE_USE = "多次使用"          # 多次使用同一张牌
    ZONE_MASTERY = "区域精通"          # 在特定区域达成条件
    RESOURCE_THRESHOLD = "资源阈值"    # 达到资源阈值
    INTERACTION_SUCCESS = "互动成功"   # 成功的玩家互动
    COMBO_ACHIEVEMENT = "连击成就"     # 连续成功行动
    SACRIFICE = "牺牲进化"             # 牺牲其他卡牌进化

class CardRarity(Enum):
    """卡牌稀有度"""
    COMMON = "普通"
    UNCOMMON = "罕见"
    RARE = "稀有"
    EPIC = "史诗"
    LEGENDARY = "传说"
    MYTHIC = "神话"

@dataclass
class EvolutionCondition:
    """进化条件"""
    trigger: EvolutionTrigger
    requirement: Dict[str, Any]  # 具体要求
    description: str

@dataclass
class CardMemory:
    """卡牌记忆"""
    use_count: int = 0
    success_count: int = 0
    zones_used: Set[str] = field(default_factory=set)
    interactions: List[str] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)
    first_use_turn: Optional[int] = None
    last_use_turn: Optional[int] = None
    evolution_history: List[str] = field(default_factory=list)

@dataclass
class EvolvingCard:
    """演进卡牌"""
    base_name: str
    current_name: str
    rarity: CardRarity
    evolution_level: int = 0
    max_evolution: int = 3
    memory: CardMemory = field(default_factory=CardMemory)
    base_effects: Dict[str, Any] = field(default_factory=dict)
    evolved_effects: Dict[str, Any] = field(default_factory=dict)
    evolution_conditions: List[EvolutionCondition] = field(default_factory=list)
    unlocked_abilities: List[str] = field(default_factory=list)
    owner: str = ""
    
    def can_evolve(self) -> Tuple[bool, Optional[EvolutionCondition]]:
        """检查是否可以进化"""
        if self.evolution_level >= self.max_evolution:
            return False, None
        
        for condition in self.evolution_conditions:
            if self._check_evolution_condition(condition):
                return True, condition
        
        return False, None
    
    def _check_evolution_condition(self, condition: EvolutionCondition) -> bool:
        """检查进化条件"""
        trigger = condition.trigger
        requirement = condition.requirement
        
        if trigger == EvolutionTrigger.FIRST_COMPLETION:
            return len(self.memory.achievements) > 0
        
        elif trigger == EvolutionTrigger.MULTIPLE_USE:
            required_uses = requirement.get("use_count", 5)
            return self.memory.use_count >= required_uses
        
        elif trigger == EvolutionTrigger.ZONE_MASTERY:
            required_zones = requirement.get("zones", [])
            return all(zone in self.memory.zones_used for zone in required_zones)
        
        elif trigger == EvolutionTrigger.RESOURCE_THRESHOLD:
            # 这需要外部传入当前资源状态
            return False  # 暂时返回False，需要外部检查
        
        elif trigger == EvolutionTrigger.INTERACTION_SUCCESS:
            required_interactions = requirement.get("interaction_count", 3)
            return len(self.memory.interactions) >= required_interactions
        
        elif trigger == EvolutionTrigger.COMBO_ACHIEVEMENT:
            required_combo = requirement.get("combo_count", 3)
            return self.memory.success_count >= required_combo
        
        return False
    
    def evolve(self, condition: EvolutionCondition) -> bool:
        """执行进化"""
        if not self._check_evolution_condition(condition):
            return False
        
        self.evolution_level += 1
        old_name = self.current_name
        
        # 生成新的卡牌名称
        evolution_suffix = ["·改", "·真", "·极"]
        if self.evolution_level <= len(evolution_suffix):
            self.current_name = f"{self.base_name}{evolution_suffix[self.evolution_level - 1]}"
        
        # 记录进化历史
        self.memory.evolution_history.append(f"第{self.evolution_level}次进化：{condition.description}")
        
        # 解锁新能力
        self._unlock_evolution_abilities()
        
        # 提升稀有度
        self._upgrade_rarity()
        
        advanced_ui.display_mystical_message(
            f"卡牌进化！\n"
            f"{old_name} → {self.current_name}\n"
            f"进化条件：{condition.description}\n"
            f"新稀有度：{self.rarity.value}",
            "卡牌进化",
            MessageType.HIGHLIGHT
        )
        
        return True
    
    def _unlock_evolution_abilities(self):
        """解锁进化能力"""
        evolution_abilities = {
            1: ["基础强化", "效果增强"],
            2: ["高级能力", "特殊效果"],
            3: ["终极形态", "神话能力"]
        }
        
        if self.evolution_level in evolution_abilities:
            new_abilities = evolution_abilities[self.evolution_level]
            self.unlocked_abilities.extend(new_abilities)
    
    def _upgrade_rarity(self):
        """提升稀有度"""
        rarity_progression = [
            CardRarity.COMMON,
            CardRarity.UNCOMMON,
            CardRarity.RARE,
            CardRarity.EPIC,
            CardRarity.LEGENDARY,
            CardRarity.MYTHIC
        ]
        
        current_index = rarity_progression.index(self.rarity)
        if current_index < len(rarity_progression) - 1:
            self.rarity = rarity_progression[current_index + 1]
    
    def record_use(self, turn: int, zone: str, success: bool, interaction_type: str = ""):
        """记录使用"""
        self.memory.use_count += 1
        if success:
            self.memory.success_count += 1
        
        self.memory.zones_used.add(zone)
        
        if interaction_type:
            self.memory.interactions.append(interaction_type)
        
        if self.memory.first_use_turn is None:
            self.memory.first_use_turn = turn
        
        self.memory.last_use_turn = turn
    
    def add_achievement(self, achievement: str):
        """添加成就"""
        if achievement not in self.memory.achievements:
            self.memory.achievements.append(achievement)

class PlayerDeck:
    """玩家牌库"""
    
    def __init__(self, player_name: str):
        self.player_name = player_name
        self.cards: Dict[str, EvolvingCard] = {}
        self.deck_memory: Dict[str, Any] = {
            "total_games": 0,
            "favorite_cards": [],
            "mastered_strategies": [],
            "evolution_count": 0
        }
        self.synergy_bonuses: Dict[str, float] = {}  # 卡牌协同奖励
    
    def add_card(self, card: EvolvingCard):
        """添加卡牌"""
        card.owner = self.player_name
        self.cards[card.current_name] = card
    
    def get_card(self, card_name: str) -> Optional[EvolvingCard]:
        """获取卡牌"""
        return self.cards.get(card_name)
    
    def evolve_card(self, card_name: str) -> bool:
        """进化卡牌"""
        card = self.get_card(card_name)
        if not card:
            return False
        
        can_evolve, condition = card.can_evolve()
        if can_evolve and condition:
            success = card.evolve(condition)
            if success:
                self.deck_memory["evolution_count"] += 1
                self._update_deck_synergies()
            return success
        
        return False
    
    def _update_deck_synergies(self):
        """更新牌库协同效果"""
        # 计算同系列卡牌的协同奖励
        series_count = {}
        for card in self.cards.values():
            series = card.base_name.split("为")[0] if "为" in card.base_name else card.base_name[:2]
            series_count[series] = series_count.get(series, 0) + 1
        
        # 为拥有多张同系列卡牌的玩家提供协同奖励
        for series, count in series_count.items():
            if count >= 2:
                self.synergy_bonuses[series] = min(0.5, count * 0.1)  # 最大50%奖励
    
    def get_deck_statistics(self) -> Dict[str, Any]:
        """获取牌库统计"""
        total_cards = len(self.cards)
        evolved_cards = sum(1 for card in self.cards.values() if card.evolution_level > 0)
        rarity_distribution = {}
        
        for card in self.cards.values():
            rarity = card.rarity.value
            rarity_distribution[rarity] = rarity_distribution.get(rarity, 0) + 1
        
        return {
            "total_cards": total_cards,
            "evolved_cards": evolved_cards,
            "evolution_rate": evolved_cards / total_cards if total_cards > 0 else 0,
            "rarity_distribution": rarity_distribution,
            "synergy_bonuses": self.synergy_bonuses,
            "deck_memory": self.deck_memory
        }

class EvolvingCardsSystem:
    """演进卡牌系统"""
    
    def __init__(self):
        self.player_decks: Dict[str, PlayerDeck] = {}
        self.card_templates: Dict[str, Dict] = {}
        self.global_evolution_events: List[Dict] = []
        self.current_turn = 0
        
    def initialize_player_deck(self, player_name: str, starting_cards: List[str]):
        """初始化玩家牌库"""
        deck = PlayerDeck(player_name)
        
        for card_name in starting_cards:
            card = self._create_evolving_card(card_name, player_name)
            deck.add_card(card)
        
        self.player_decks[player_name] = deck
    
    def _create_evolving_card(self, card_name: str, owner: str) -> EvolvingCard:
        """创建演进卡牌"""
        # 创建基础卡牌
        card = EvolvingCard(
            base_name=card_name,
            current_name=card_name,
            rarity=CardRarity.COMMON,
            owner=owner
        )
        
        # 设置进化条件
        card.evolution_conditions = self._get_evolution_conditions(card_name)
        
        return card
    
    def _get_evolution_conditions(self, card_name: str) -> List[EvolutionCondition]:
        """获取卡牌的进化条件"""
        # 根据卦象设置不同的进化条件
        conditions = []
        
        if "乾" in card_name:
            conditions.extend([
                EvolutionCondition(
                    EvolutionTrigger.MULTIPLE_USE,
                    {"use_count": 5},
                    "使用乾卦5次"
                ),
                EvolutionCondition(
                    EvolutionTrigger.ZONE_MASTERY,
                    {"zones": ["天"]},
                    "在天部使用并成功"
                ),
                EvolutionCondition(
                    EvolutionTrigger.COMBO_ACHIEVEMENT,
                    {"combo_count": 3},
                    "连续成功3次"
                )
            ])
        
        elif "坤" in card_name:
            conditions.extend([
                EvolutionCondition(
                    EvolutionTrigger.MULTIPLE_USE,
                    {"use_count": 4},
                    "使用坤卦4次"
                ),
                EvolutionCondition(
                    EvolutionTrigger.ZONE_MASTERY,
                    {"zones": ["地"]},
                    "在地部使用并成功"
                ),
                EvolutionCondition(
                    EvolutionTrigger.INTERACTION_SUCCESS,
                    {"interaction_count": 3},
                    "成功进行3次互动"
                )
            ])
        
        elif "水" in card_name or "坎" in card_name:
            conditions.extend([
                EvolutionCondition(
                    EvolutionTrigger.MULTIPLE_USE,
                    {"use_count": 6},
                    "使用水系卦象6次"
                ),
                EvolutionCondition(
                    EvolutionTrigger.FIRST_COMPLETION,
                    {},
                    "首次完成水系爻辞任务"
                )
            ])
        
        # 默认进化条件
        if not conditions:
            conditions.append(
                EvolutionCondition(
                    EvolutionTrigger.MULTIPLE_USE,
                    {"use_count": 3},
                    f"使用{card_name}3次"
                )
            )
        
        return conditions
    
    def record_card_use(self, player_name: str, card_name: str, turn: int, 
                       zone: str, success: bool, interaction_type: str = ""):
        """记录卡牌使用"""
        deck = self.player_decks.get(player_name)
        if not deck:
            return
        
        card = deck.get_card(card_name)
        if card:
            card.record_use(turn, zone, success, interaction_type)
            
            # 检查是否可以进化
            can_evolve, condition = card.can_evolve()
            if can_evolve:
                advanced_ui.display_mystical_message(
                    f"卡牌 {card_name} 可以进化了！\n"
                    f"进化条件：{condition.description}",
                    "进化机会",
                    MessageType.HIGHLIGHT
                )
    
    def trigger_evolution(self, player_name: str, card_name: str) -> bool:
        """触发卡牌进化"""
        deck = self.player_decks.get(player_name)
        if not deck:
            return False
        
        return deck.evolve_card(card_name)
    
    def add_card_achievement(self, player_name: str, card_name: str, achievement: str):
        """添加卡牌成就"""
        deck = self.player_decks.get(player_name)
        if not deck:
            return
        
        card = deck.get_card(card_name)
        if card:
            card.add_achievement(achievement)
    
    def get_evolution_opportunities(self, player_name: str) -> List[Tuple[str, str]]:
        """获取进化机会"""
        deck = self.player_decks.get(player_name)
        if not deck:
            return []
        
        opportunities = []
        for card_name, card in deck.cards.items():
            can_evolve, condition = card.can_evolve()
            if can_evolve and condition:
                opportunities.append((card_name, condition.description))
        
        return opportunities
    
    def display_deck_status(self, player_name: str):
        """显示牌库状态"""
        deck = self.player_decks.get(player_name)
        if not deck:
            advanced_ui.print_colored("牌库未初始化", MessageType.ERROR)
            return
        
        stats = deck.get_deck_statistics()
        
        advanced_ui.print_colored(f"牌库状态 - {player_name}", MessageType.HIGHLIGHT)
        advanced_ui.print_colored(f"总卡牌数：{stats['total_cards']}", MessageType.INFO)
        advanced_ui.print_colored(f"已进化卡牌：{stats['evolved_cards']}", MessageType.INFO)
        advanced_ui.print_colored(f"进化率：{stats['evolution_rate']:.1%}", MessageType.INFO)
        
        if stats['rarity_distribution']:
            advanced_ui.print_colored("稀有度分布：", MessageType.MYSTICAL)
            for rarity, count in stats['rarity_distribution'].items():
                advanced_ui.print_colored(f"  {rarity}: {count}张", MessageType.INFO)
        
        if stats['synergy_bonuses']:
            advanced_ui.print_colored("协同奖励：", MessageType.MYSTICAL)
            for series, bonus in stats['synergy_bonuses'].items():
                advanced_ui.print_colored(f"  {series}系列: +{bonus:.1%}", MessageType.INFO)
        
        # 显示可进化的卡牌
        opportunities = self.get_evolution_opportunities(player_name)
        if opportunities:
            advanced_ui.print_colored("可进化卡牌：", MessageType.HIGHLIGHT)
            for card_name, condition in opportunities:
                advanced_ui.print_colored(f"  • {card_name}: {condition}", MessageType.INFO)
    
    def display_card_details(self, player_name: str, card_name: str):
        """显示卡牌详情"""
        deck = self.player_decks.get(player_name)
        if not deck:
            return
        
        card = deck.get_card(card_name)
        if not card:
            advanced_ui.print_colored(f"未找到卡牌：{card_name}", MessageType.ERROR)
            return
        
        advanced_ui.print_colored(f"卡牌详情 - {card.current_name}", MessageType.HIGHLIGHT)
        advanced_ui.print_colored(f"基础名称：{card.base_name}", MessageType.INFO)
        advanced_ui.print_colored(f"稀有度：{card.rarity.value}", MessageType.INFO)
        advanced_ui.print_colored(f"进化等级：{card.evolution_level}/{card.max_evolution}", MessageType.INFO)
        
        memory = card.memory
        advanced_ui.print_colored("使用记录：", MessageType.MYSTICAL)
        advanced_ui.print_colored(f"  使用次数：{memory.use_count}", MessageType.INFO)
        advanced_ui.print_colored(f"  成功次数：{memory.success_count}", MessageType.INFO)
        advanced_ui.print_colored(f"  使用区域：{', '.join(memory.zones_used)}", MessageType.INFO)
        
        if memory.achievements:
            advanced_ui.print_colored("获得成就：", MessageType.MYSTICAL)
            for achievement in memory.achievements:
                advanced_ui.print_colored(f"  • {achievement}", MessageType.INFO)
        
        if memory.evolution_history:
            advanced_ui.print_colored("进化历史：", MessageType.MYSTICAL)
            for evolution in memory.evolution_history:
                advanced_ui.print_colored(f"  • {evolution}", MessageType.INFO)
        
        if card.unlocked_abilities:
            advanced_ui.print_colored("解锁能力：", MessageType.MYSTICAL)
            for ability in card.unlocked_abilities:
                advanced_ui.print_colored(f"  • {ability}", MessageType.INFO)
    
    def trigger_global_evolution_event(self):
        """触发全局进化事件"""
        events = [
            {
                "name": "天地感应",
                "description": "所有卡牌的进化条件降低50%",
                "effect": "evolution_requirement_reduction",
                "value": 0.5,
                "duration": 3
            },
            {
                "name": "万物复苏",
                "description": "所有玩家获得一次免费进化机会",
                "effect": "free_evolution",
                "value": 1,
                "duration": 1
            },
            {
                "name": "阴阳调和",
                "description": "协同奖励效果翻倍",
                "effect": "synergy_boost",
                "value": 2.0,
                "duration": 5
            }
        ]
        
        import random
        event = random.choice(events)
        self.global_evolution_events.append(event)
        
        advanced_ui.display_mystical_message(
            f"全局进化事件：{event['name']}\n"
            f"{event['description']}\n"
            f"持续{event['duration']}回合",
            "天象异变",
            MessageType.HIGHLIGHT
        )
        
        return event

# 全局演进卡牌系统实例
evolving_cards_system = EvolvingCardsSystem()

# 便捷函数
def initialize_player_deck(player_name: str, starting_cards: List[str]):
    """初始化玩家牌库"""
    evolving_cards_system.initialize_player_deck(player_name, starting_cards)

def record_card_use(player_name: str, card_name: str, turn: int, zone: str, 
                   success: bool, interaction_type: str = ""):
    """记录卡牌使用"""
    evolving_cards_system.record_card_use(player_name, card_name, turn, zone, success, interaction_type)

def trigger_evolution(player_name: str, card_name: str) -> bool:
    """触发进化"""
    return evolving_cards_system.trigger_evolution(player_name, card_name)

def display_deck_status(player_name: str):
    """显示牌库状态"""
    evolving_cards_system.display_deck_status(player_name)

def display_card_details(player_name: str, card_name: str):
    """显示卡牌详情"""
    evolving_cards_system.display_card_details(player_name, card_name)

def get_evolution_opportunities(player_name: str) -> List[Tuple[str, str]]:
    """获取进化机会"""
    return evolving_cards_system.get_evolution_opportunities(player_name)

def trigger_global_evolution_event():
    """触发全局进化事件"""
    return evolving_cards_system.trigger_global_evolution_event()