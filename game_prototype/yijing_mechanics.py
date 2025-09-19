"""
易经哲学游戏机制设计
体现阴阳平衡、五行相生相克、变化之道等核心理念
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import random
from config_manager import get_config

class YinYang(Enum):
    """阴阳属性"""
    YIN = "阴"    # 柔、静、收敛
    YANG = "阳"   # 刚、动、发散

class WuXing(Enum):
    """五行属性"""
    JIN = "金"    # 金 - 收敛、肃杀
    MU = "木"     # 木 - 生长、条达  
    SHUI = "水"   # 水 - 滋润、向下
    HUO = "火"    # 火 - 炎热、向上
    TU = "土"     # 土 - 承载、化育

@dataclass
class YinYangBalance:
    """阴阳平衡状态"""
    yin_points: int = 0
    yang_points: int = 0
    
    @property
    def balance_ratio(self) -> float:
        """计算阴阳平衡比例，越接近1越平衡"""
        total = self.yin_points + self.yang_points
        if total == 0:
            return 1.0
        smaller = min(self.yin_points, self.yang_points)
        return (smaller * 2) / total
    
    @property
    def dominant_aspect(self) -> Optional[YinYang]:
        """获取主导方面"""
        if self.yin_points > self.yang_points:
            return YinYang.YIN
        elif self.yang_points > self.yin_points:
            return YinYang.YANG
        return None
    
    def get_balance_bonus(self) -> int:
        """根据阴阳平衡程度给予奖励"""
        ratio = self.balance_ratio
        
        high_threshold = get_config("game_balance.yin_yang_balance.high_balance_threshold", 0.8)
        medium_threshold = get_config("game_balance.yin_yang_balance.medium_balance_threshold", 0.6)
        low_threshold = get_config("game_balance.yin_yang_balance.low_balance_threshold", 0.4)
        
        high_bonus = get_config("game_balance.yin_yang_balance.high_balance_bonus", 3)
        medium_bonus = get_config("game_balance.yin_yang_balance.medium_balance_bonus", 2)
        low_bonus = get_config("game_balance.yin_yang_balance.low_balance_bonus", 1)
        
        if ratio >= high_threshold:
            return high_bonus
        elif ratio >= medium_threshold:
            return medium_bonus
        elif ratio >= low_threshold:
            return low_bonus
        else:
            return 0

class WuXingCycle:
    """五行相生相克循环"""
    
    # 五行相生：金生水，水生木，木生火，火生土，土生金
    SHENG_CYCLE = {
        WuXing.JIN: WuXing.SHUI,
        WuXing.SHUI: WuXing.MU,
        WuXing.MU: WuXing.HUO,
        WuXing.HUO: WuXing.TU,
        WuXing.TU: WuXing.JIN
    }
    
    # 五行相克：金克木，木克土，土克水，水克火，火克金
    KE_CYCLE = {
        WuXing.JIN: WuXing.MU,
        WuXing.MU: WuXing.TU,
        WuXing.TU: WuXing.SHUI,
        WuXing.SHUI: WuXing.HUO,
        WuXing.HUO: WuXing.JIN
    }
    
    @classmethod
    def get_sheng_target(cls, element: WuXing) -> WuXing:
        """获取相生目标"""
        return cls.SHENG_CYCLE[element]
    
    @classmethod
    def get_ke_target(cls, element: WuXing) -> WuXing:
        """获取相克目标"""
        return cls.KE_CYCLE[element]
    
    @classmethod
    def is_sheng_relationship(cls, source: WuXing, target: WuXing) -> bool:
        """判断是否为相生关系"""
        return cls.SHENG_CYCLE[source] == target
    
    @classmethod
    def is_ke_relationship(cls, source: WuXing, target: WuXing) -> bool:
        """判断是否为相克关系"""
        return cls.KE_CYCLE[source] == target

@dataclass
class BianguaTransformation:
    """变卦机制 - 体现易经变化之道"""
    original_gua: str
    transformed_gua: str
    trigger_condition: str
    effect_description: str
    cost_qi: int = 0
    cost_dao_xing: int = 0
    reward_multiplier: float = 1.0
    risk_level: str = "low"  # low, medium, high
    
    def can_transform(self, game_context: Dict) -> bool:
        """检查是否满足变卦条件"""
        player = game_context.get('player')
        if not player:
            return False
            
        # 检查资源是否足够
        if player.qi < self.cost_qi or player.dao_xing < self.cost_dao_xing:
            return False
            
        # 检查特定触发条件
        return self._check_trigger_condition(game_context)
    
    def _check_trigger_condition(self, game_context: Dict) -> bool:
        """检查具体的触发条件"""
        player = game_context.get('player')
        game_state = game_context.get('game_state')
        
        condition_checks = {
            "阴阳失衡": lambda: abs(player.yin_yang_balance.yin_points - player.yin_yang_balance.yang_points) >= 5,
            "道行充足": lambda: player.dao_xing >= 10,
            "气充盈": lambda: player.qi >= 15,
            "五行和谐": lambda: self._check_wuxing_harmony(player),
            "危机时刻": lambda: self._check_crisis_situation(player, game_state),
            "机遇时刻": lambda: self._check_opportunity_situation(player, game_state),
            "回合末期": lambda: game_context.get('turn_phase') == 'end',
            "领先优势": lambda: self._check_leading_position(player, game_state),
            "落后追赶": lambda: self._check_behind_position(player, game_state)
        }
        
        return condition_checks.get(self.trigger_condition, lambda: True)()
    
    def _check_wuxing_harmony(self, player) -> bool:
        """检查五行是否和谐"""
        if not hasattr(player, 'wuxing_affinities'):
            return False
        affinities = player.wuxing_affinities
        # 检查是否有至少3个五行元素都有亲和力
        active_elements = sum(1 for value in affinities.values() if value > 0)
        return active_elements >= 3
    
    def _check_crisis_situation(self, player, game_state) -> bool:
        """检查是否处于危机状况"""
        if not game_state or not hasattr(game_state, 'players'):
            return False
        # 如果玩家的道行在所有玩家中排名后50%
        all_dao_xing = [p.dao_xing for p in game_state.players]
        player_rank = sorted(all_dao_xing, reverse=True).index(player.dao_xing)
        return player_rank >= len(all_dao_xing) // 2
    
    def _check_opportunity_situation(self, player, game_state) -> bool:
        """检查是否处于机遇状况"""
        if not game_state or not hasattr(game_state, 'players'):
            return False
        # 如果玩家有足够资源且处于有利位置
        return player.qi >= 10 and player.dao_xing >= 8
    
    def _check_leading_position(self, player, game_state) -> bool:
        """检查是否处于领先位置"""
        if not game_state or not hasattr(game_state, 'players'):
            return False
        all_dao_xing = [p.dao_xing for p in game_state.players]
        return player.dao_xing == max(all_dao_xing)
    
    def _check_behind_position(self, player, game_state) -> bool:
        """检查是否处于落后位置"""
        if not game_state or not hasattr(game_state, 'players'):
            return False
        all_dao_xing = [p.dao_xing for p in game_state.players]
        avg_dao_xing = sum(all_dao_xing) / len(all_dao_xing)
        return player.dao_xing < avg_dao_xing - 3
    
    def calculate_transformation_outcome(self, game_context: Dict) -> Dict[str, any]:
        """计算变卦的结果"""
        player = game_context.get('player')
        success_rate = self._calculate_success_rate(game_context)
        
        if random.random() < success_rate:
            # 成功变卦
            return {
                "success": True,
                "qi_change": int(self.cost_qi * self.reward_multiplier) - self.cost_qi,
                "dao_xing_change": int(self.cost_dao_xing * self.reward_multiplier) - self.cost_dao_xing,
                "special_effect": self._get_transformation_effect(),
                "message": f"成功从{self.original_gua}变为{self.transformed_gua}！{self.effect_description}"
            }
        else:
            # 失败变卦
            return {
                "success": False,
                "qi_change": -self.cost_qi,
                "dao_xing_change": -self.cost_dao_xing,
                "special_effect": None,
                "message": f"变卦失败，消耗了{self.cost_qi}点气和{self.cost_dao_xing}点道行"
            }
    
    def _calculate_success_rate(self, game_context: Dict) -> float:
        """计算变卦成功率"""
        player = game_context.get('player')
        base_rate = 0.7  # 基础成功率70%
        
        # 根据风险等级调整
        risk_modifiers = {
            "low": 0.2,
            "medium": 0.0,
            "high": -0.3
        }
        
        # 根据玩家道行调整
        dao_xing_bonus = min(0.2, player.dao_xing * 0.01) if player else 0
        
        # 根据阴阳平衡调整
        balance_bonus = 0
        if player and hasattr(player, 'yin_yang_balance'):
            balance_ratio = player.yin_yang_balance.balance_ratio
            if 0.4 <= balance_ratio <= 0.6:  # 平衡状态
                balance_bonus = 0.1
        
        final_rate = base_rate + risk_modifiers.get(self.risk_level, 0) + dao_xing_bonus + balance_bonus
        return max(0.1, min(0.95, final_rate))  # 限制在10%-95%之间
    
    def _get_transformation_effect(self) -> str:
        """获取变卦的特殊效果"""
        effects = {
            "乾为天": "获得'天行健'状态，下回合所有行动效果+50%",
            "坤为地": "获得'厚德载物'状态，本回合免疫所有负面效果",
            "震为雷": "获得'雷霆万钧'状态，可以立即执行一次额外行动",
            "巽为风": "获得'风行草偃'状态，可以影响其他玩家的下一个决策",
            "坎为水": "获得'上善若水'状态，获得额外的适应性和流动性",
            "离为火": "获得'光明磊落'状态，所有行动都被视为最优选择",
            "艮为山": "获得'稳如泰山'状态，获得强大的防御和稳定性",
            "兑为泽": "获得'和悦致祥'状态，与其他玩家的合作效果翻倍"
        }
        return effects.get(self.transformed_gua, "获得神秘的易经加护")

class TaijiMechanism:
    """太极机制 - 体现阴阳转化"""
    
    @staticmethod
    def calculate_transformation_probability(yin_yang_balance: YinYangBalance) -> float:
        """计算太极转化概率"""
        extreme_threshold = get_config("game_balance.yin_yang_balance.extreme_transform_threshold", 10)
        extreme_prob = get_config("game_balance.yin_yang_balance.extreme_transform_probability", 0.8)
        normal_prob = get_config("game_balance.yin_yang_balance.normal_transform_probability", 0.1)
        
        # 极端不平衡时更容易发生转化
        if yin_yang_balance.yin_points >= extreme_threshold and yin_yang_balance.yang_points <= 2:
            return extreme_prob  # 极阴转阳概率高
        elif yin_yang_balance.yang_points >= extreme_threshold and yin_yang_balance.yin_points <= 2:
            return extreme_prob  # 极阳转阴概率高
        return normal_prob  # 正常转化概率低
    
    @staticmethod
    def apply_transformation(yin_yang_balance: YinYangBalance) -> YinYangBalance:
        """应用太极转化效果"""
        yin_loss = get_config("game_balance.yin_yang_balance.transform_yin_loss", 3)
        yang_gain = get_config("game_balance.yin_yang_balance.transform_yang_gain", 2)
        
        prob = TaijiMechanism.calculate_transformation_probability(yin_yang_balance)
        if random.random() < prob:
            # 物极必反的转化
            if yin_yang_balance.yin_points > yin_yang_balance.yang_points:
                # 阴极生阳
                yin_yang_balance.yin_points -= yin_loss
                yin_yang_balance.yang_points += yang_gain
            else:
                # 阳极生阴
                yin_yang_balance.yang_points -= yin_loss
                yin_yang_balance.yin_points += yang_gain
        
        return yin_yang_balance

class ZhouYiWisdom:
    """周易智慧格言系统"""
    
    WISDOM_QUOTES = {
        "自强不息": "天行健，君子以自强不息",
        "厚德载物": "地势坤，君子以厚德载物", 
        "学而时习": "学而时习之，不亦说乎",
        "知者不惑": "知者不惑，仁者不忧，勇者不惧",
        "穷则变": "穷则变，变则通，通则久",
        "中庸之道": "君子中庸，小人反中庸",
        "阴阳调和": "一阴一阳之谓道",
        "五行相生": "五行相生，万物化育"
    }
    
    @classmethod
    def get_random_wisdom(cls) -> Tuple[str, str]:
        """获取随机智慧格言"""
        key = random.choice(list(cls.WISDOM_QUOTES.keys()))
        return key, cls.WISDOM_QUOTES[key]
    
    @classmethod
    def trigger_wisdom(cls, condition: str) -> Optional[str]:
        """根据条件触发相应智慧"""
        wisdom_map = {
            "balance_achieved": "阴阳调和",
            "wuxing_harmony": "五行相生", 
            "dao_progress": "自强不息",
            "study_action": "学而时习",
            "transformation": "穷则变"
        }
        
        wisdom_key = wisdom_map.get(condition)
        if wisdom_key:
            return cls.WISDOM_QUOTES[wisdom_key]
        return None

class ZhanBuSystem:
    """占卜系统 - 易经的核心功能"""
    
    @classmethod
    def divine_fortune(cls, player_dao_xing: int) -> Dict[str, any]:
        """占卜运势，道行影响建议的深度和具体性"""
        # 生成卦象
        gua_names = list(GUA_ATTRIBUTES.keys())
        primary_gua = random.choice(gua_names)
        
        # 道行决定建议的层次：基础安全建议 -> 具体指导 -> 深层洞察
        if player_dao_xing <= 3:
            # 低道行：提供基础安全建议，避免负面结果
            advice_level = "基础"
            fortune_types = ["平", "小吉", "中吉"]  # 只给安全的建议
            weights = [3, 2, 1]
        elif player_dao_xing <= 7:
            # 中道行：提供更具体的指导
            advice_level = "具体"
            fortune_types = ["小凶", "平", "小吉", "中吉", "大吉"]
            weights = [1, 2, 3, 3, 1]
        else:
            # 高道行：提供深层洞察，包含风险和机遇
            advice_level = "深层"
            fortune_types = ["大凶", "中凶", "小凶", "平", "小吉", "中吉", "大吉"]
            weights = [1, 1, 2, 3, 3, 2, 1]
        
        fortune = random.choices(fortune_types, weights=weights)[0]
        
        # 根据道行层次提供不同深度的建议
        actions = cls._get_advice_by_level(fortune, advice_level, primary_gua)
        
        return {
            "gua": primary_gua,
            "fortune": fortune,
            "advice": actions,
            "advice_level": advice_level,
            "dao_xing_threshold": player_dao_xing
        }
    
    @classmethod
    def _get_advice_by_level(cls, fortune: str, level: str, gua: str) -> str:
        """根据道行层次提供不同深度的建议"""
        gua_nature = GUA_ATTRIBUTES.get(gua, {}).get("nature", "平衡")
        
        low_threshold = get_config("game_balance.zhanbu_system.low_dao_xing_threshold", 30)
        high_threshold = get_config("game_balance.zhanbu_system.high_dao_xing_threshold", 70)
        
        if level == "基础":
            # 基础安全建议，重在稳妥
            base_actions = {
                "平": f"保持{gua_nature}之心，稳步前行",
                "小吉": f"顺应{gua_nature}之势，小心积累",
                "中吉": f"把握{gua_nature}之机，适度进取"
            }
            return base_actions.get(fortune, "保持平常心，稳中求进")
            
        elif level == "具体":
            # 具体指导，包含策略建议
            specific_actions = {
                "大吉": f"天时地利，{gua_nature}大成，宜大胆进取，把握机遇",
                "中吉": f"{gua_nature}渐显，宜稳步推进，加强修行",
                "小吉": f"{gua_nature}初现，宜谨慎观察，积累实力",
                "平": f"{gua_nature}平衡，宜中庸之道，等待时机",
                "小凶": f"{gua_nature}受阻，宜内省修德，化解困难"
            }
            return specific_actions.get(fortune, f"顺应{gua_nature}之道，随机应变")
            
        else:  # 深层
            # 深层洞察，包含哲学思考
            deep_actions = {
                "大吉": f"{gua_nature}极盛，当思物极必反，宜功成身退",
                "中吉": f"{gua_nature}正旺，宜乘势而为，但需防骄躁",
                "小吉": f"{gua_nature}渐起，宜顺势培养，积小成大",
                "平": f"{gua_nature}中和，宜守中致和，以静制动",
                "小凶": f"{gua_nature}受挫，宜反求诸己，转危为机",
                "中凶": f"{gua_nature}困顿，宜韬光养晦，待时而动",
                "大凶": f"{gua_nature}极衰，否极泰来，宜静待转机"
            }
            return deep_actions.get(fortune, f"深悟{gua_nature}之理，顺应天道")
    
    @classmethod
    def divine_action_outcome(cls, action_type: str, player_dao_xing: int) -> bool:
        """占卜特定行动的成功率"""
        base_success = 0.5
        dao_bonus = player_dao_xing * 0.03
        
        # 不同行动的基础成功率调整
        action_modifiers = {
            "meditate": 0.1,    # 冥想较容易成功
            "study": 0.05,      # 学习中等难度
            "transform": -0.1,  # 变卦较困难
            "wuxing": 0.0       # 五行中性
        }
        
        modifier = action_modifiers.get(action_type, 0)
        success_rate = min(base_success + dao_bonus + modifier, 0.9)
        
        return random.random() < success_rate

# 卦象属性映射
GUA_ATTRIBUTES = {
    "乾": {"yin_yang": YinYang.YANG, "wuxing": WuXing.JIN, "nature": "刚健"},
    "坤": {"yin_yang": YinYang.YIN, "wuxing": WuXing.TU, "nature": "柔顺"},
    "震": {"yin_yang": YinYang.YANG, "wuxing": WuXing.MU, "nature": "动"},
    "巽": {"yin_yang": YinYang.YIN, "wuxing": WuXing.MU, "nature": "入"},
    "坎": {"yin_yang": YinYang.YANG, "wuxing": WuXing.SHUI, "nature": "陷"},
    "离": {"yin_yang": YinYang.YIN, "wuxing": WuXing.HUO, "nature": "丽"},
    "艮": {"yin_yang": YinYang.YANG, "wuxing": WuXing.TU, "nature": "止"},
    "兑": {"yin_yang": YinYang.YIN, "wuxing": WuXing.JIN, "nature": "悦"}
}

def get_gua_synergy_bonus(gua1: str, gua2: str) -> int:
    """计算卦象协同奖励"""
    if gua1 not in GUA_ATTRIBUTES or gua2 not in GUA_ATTRIBUTES:
        return 0
    
    attr1 = GUA_ATTRIBUTES[gua1]
    attr2 = GUA_ATTRIBUTES[gua2]
    
    bonus = 0
    
    # 阴阳互补奖励
    if attr1["yin_yang"] != attr2["yin_yang"]:
        bonus += 2
    
    # 五行相生奖励
    if WuXingCycle.is_sheng_relationship(attr1["wuxing"], attr2["wuxing"]):
        bonus += 3
    
    # 五行相克惩罚
    if WuXingCycle.is_ke_relationship(attr1["wuxing"], attr2["wuxing"]):
        bonus -= 1
    
    return max(0, bonus)