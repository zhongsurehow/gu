"""
天机变游戏易学系统
实现五行、八卦、阴阳等易学核心系统的计算和管理
"""

import logging
from typing import Dict, List, Tuple, Optional, Set, Union, Any
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod
import math
import random

from ..core.interfaces import IYixueSystem
from ..core.base_types import WuxingElement, BaguaType, YinyangType, Position
from ..core.constants import *
from ..core.exceptions import YixueException
from ..utils.yixue_utils import *

logger = logging.getLogger(__name__)

# ==================== 枚举定义 ====================

class CultivationLevel(Enum):
    """修为境界枚举"""
    MORTAL = "凡人"
    QI_REFINING = "练气"
    FOUNDATION = "筑基"
    GOLDEN_CORE = "金丹"
    NASCENT_SOUL = "元婴"
    SPIRIT_TRANSFORMATION = "化神"
    VOID_REFINEMENT = "炼虚"
    UNITY = "合体"
    MAHAYANA = "大乘"
    TRIBULATION = "渡劫"

class ElementalReaction(Enum):
    """五行反应类型"""
    GENERATION = "相生"
    DESTRUCTION = "相克"
    NEUTRAL = "中性"

class BaguaRelation(Enum):
    """八卦关系类型"""
    HARMONY = "和谐"
    CONFLICT = "冲突"
    NEUTRAL = "中性"

# ==================== 数据类定义 ====================

@dataclass
class WuxingState:
    """五行状态数据类"""
    wood: float = 0.0
    fire: float = 0.0
    earth: float = 0.0
    metal: float = 0.0
    water: float = 0.0
    
    def get_element_value(self, element: WuxingElement) -> float:
        """获取指定五行元素的值"""
        return getattr(self, element.value.lower())
    
    def set_element_value(self, element: WuxingElement, value: float) -> None:
        """设置指定五行元素的值"""
        setattr(self, element.value.lower(), max(0.0, value))
    
    def get_total_power(self) -> float:
        """获取五行总力量"""
        return self.wood + self.fire + self.earth + self.metal + self.water
    
    def get_balance_score(self) -> float:
        """获取五行平衡度分数（0-1，1为完全平衡）"""
        total = self.get_total_power()
        if total == 0:
            return 1.0
        
        ideal_value = total / 5
        variance = sum((getattr(self, elem.value.lower()) - ideal_value) ** 2 
                      for elem in WuxingElement) / 5
        
        # 转换为0-1分数，方差越小分数越高
        max_variance = (total ** 2) / 5  # 最大可能方差
        return 1.0 - (variance / max_variance) if max_variance > 0 else 1.0

@dataclass
class BaguaState:
    """八卦状态数据类"""
    qian: float = 0.0    # 乾
    kun: float = 0.0     # 坤
    zhen: float = 0.0    # 震
    xun: float = 0.0     # 巽
    kan: float = 0.0     # 坎
    li: float = 0.0      # 离
    gen: float = 0.0     # 艮
    dui: float = 0.0     # 兑
    
    def get_bagua_value(self, bagua: BaguaType) -> float:
        """获取指定八卦的值"""
        bagua_map = {
            BaguaType.QIAN: self.qian,
            BaguaType.KUN: self.kun,
            BaguaType.ZHEN: self.zhen,
            BaguaType.XUN: self.xun,
            BaguaType.KAN: self.kan,
            BaguaType.LI: self.li,
            BaguaType.GEN: self.gen,
            BaguaType.DUI: self.dui
        }
        return bagua_map.get(bagua, 0.0)
    
    def set_bagua_value(self, bagua: BaguaType, value: float) -> None:
        """设置指定八卦的值"""
        bagua_map = {
            BaguaType.QIAN: 'qian',
            BaguaType.KUN: 'kun',
            BaguaType.ZHEN: 'zhen',
            BaguaType.XUN: 'xun',
            BaguaType.KAN: 'kan',
            BaguaType.LI: 'li',
            BaguaType.GEN: 'gen',
            BaguaType.DUI: 'dui'
        }
        attr_name = bagua_map.get(bagua)
        if attr_name:
            setattr(self, attr_name, max(0.0, value))
    
    def get_total_affinity(self) -> float:
        """获取八卦总亲和度"""
        return (self.qian + self.kun + self.zhen + self.xun + 
                self.kan + self.li + self.gen + self.dui)

@dataclass
class YinyangState:
    """阴阳状态数据类"""
    yin: float = 0.0
    yang: float = 0.0
    
    def get_balance_ratio(self) -> float:
        """获取阴阳平衡比例（0-1，0.5为完全平衡）"""
        total = self.yin + self.yang
        if total == 0:
            return 0.5
        return self.yang / total
    
    def get_balance_score(self) -> float:
        """获取阴阳平衡度分数（0-1，1为完全平衡）"""
        ratio = self.get_balance_ratio()
        # 距离0.5越近，平衡度越高
        return 1.0 - abs(ratio - 0.5) * 2
    
    def get_total_power(self) -> float:
        """获取阴阳总力量"""
        return self.yin + self.yang

@dataclass
class CultivationState:
    """修为状态数据类"""
    level: CultivationLevel = CultivationLevel.MORTAL
    experience: float = 0.0
    breakthrough_progress: float = 0.0
    
    def get_level_index(self) -> int:
        """获取修为等级索引"""
        levels = list(CultivationLevel)
        return levels.index(self.level)
    
    def can_breakthrough(self) -> bool:
        """检查是否可以突破"""
        return (self.breakthrough_progress >= 100.0 and 
                self.level != CultivationLevel.TRIBULATION)
    
    def get_power_multiplier(self) -> float:
        """获取修为力量倍数"""
        level_multipliers = {
            CultivationLevel.MORTAL: 1.0,
            CultivationLevel.QI_REFINING: 1.2,
            CultivationLevel.FOUNDATION: 1.5,
            CultivationLevel.GOLDEN_CORE: 2.0,
            CultivationLevel.NASCENT_SOUL: 3.0,
            CultivationLevel.SPIRIT_TRANSFORMATION: 4.5,
            CultivationLevel.VOID_REFINEMENT: 6.5,
            CultivationLevel.UNITY: 9.0,
            CultivationLevel.MAHAYANA: 12.0,
            CultivationLevel.TRIBULATION: 15.0
        }
        return level_multipliers.get(self.level, 1.0)

# ==================== 系统类定义 ====================

class WuxingSystem:
    """五行系统"""
    
    def __init__(self):
        """初始化五行系统"""
        self.generation_cycle = {
            WuxingElement.WOOD: WuxingElement.FIRE,
            WuxingElement.FIRE: WuxingElement.EARTH,
            WuxingElement.EARTH: WuxingElement.METAL,
            WuxingElement.METAL: WuxingElement.WATER,
            WuxingElement.WATER: WuxingElement.WOOD
        }
        
        self.destruction_cycle = {
            WuxingElement.WOOD: WuxingElement.EARTH,
            WuxingElement.FIRE: WuxingElement.METAL,
            WuxingElement.EARTH: WuxingElement.WATER,
            WuxingElement.METAL: WuxingElement.WOOD,
            WuxingElement.WATER: WuxingElement.FIRE
        }
    
    def get_element_relation(self, source: WuxingElement, target: WuxingElement) -> ElementalReaction:
        """获取两个五行元素之间的关系"""
        if self.generation_cycle.get(source) == target:
            return ElementalReaction.GENERATION
        elif self.destruction_cycle.get(source) == target:
            return ElementalReaction.DESTRUCTION
        else:
            return ElementalReaction.NEUTRAL
    
    def calculate_interaction_bonus(self, source: WuxingElement, target: WuxingElement, 
                                  base_value: float) -> float:
        """计算五行相互作用奖励"""
        relation = self.get_element_relation(source, target)
        
        if relation == ElementalReaction.GENERATION:
            return base_value * WUXING_GENERATION_BONUS
        elif relation == ElementalReaction.DESTRUCTION:
            return base_value * WUXING_DESTRUCTION_PENALTY
        else:
            return base_value
    
    def update_wuxing_state(self, state: WuxingState, element: WuxingElement, 
                           change: float) -> WuxingState:
        """更新五行状态"""
        new_state = WuxingState(
            wood=state.wood,
            fire=state.fire,
            earth=state.earth,
            metal=state.metal,
            water=state.water
        )
        
        # 直接影响
        current_value = new_state.get_element_value(element)
        new_state.set_element_value(element, current_value + change)
        
        # 相生影响
        generated_element = self.generation_cycle.get(element)
        if generated_element:
            generated_value = new_state.get_element_value(generated_element)
            bonus = change * 0.3  # 相生奖励为30%
            new_state.set_element_value(generated_element, generated_value + bonus)
        
        # 相克影响
        destroyed_element = self.destruction_cycle.get(element)
        if destroyed_element:
            destroyed_value = new_state.get_element_value(destroyed_element)
            penalty = change * 0.2  # 相克惩罚为20%
            new_state.set_element_value(destroyed_element, destroyed_value - penalty)
        
        return new_state

class BaguaSystem:
    """八卦系统"""
    
    def __init__(self):
        """初始化八卦系统"""
        # 八卦对应关系
        self.bagua_opposites = {
            BaguaType.QIAN: BaguaType.KUN,
            BaguaType.KUN: BaguaType.QIAN,
            BaguaType.ZHEN: BaguaType.DUI,
            BaguaType.DUI: BaguaType.ZHEN,
            BaguaType.KAN: BaguaType.LI,
            BaguaType.LI: BaguaType.KAN,
            BaguaType.GEN: BaguaType.XUN,
            BaguaType.XUN: BaguaType.GEN
        }
        
        # 八卦和谐关系（相邻八卦）
        self.bagua_harmony = {
            BaguaType.QIAN: [BaguaType.XUN, BaguaType.DUI],
            BaguaType.DUI: [BaguaType.QIAN, BaguaType.LI],
            BaguaType.LI: [BaguaType.DUI, BaguaType.ZHEN],
            BaguaType.ZHEN: [BaguaType.LI, BaguaType.XUN],
            BaguaType.XUN: [BaguaType.ZHEN, BaguaType.KAN],
            BaguaType.KAN: [BaguaType.XUN, BaguaType.GEN],
            BaguaType.GEN: [BaguaType.KAN, BaguaType.KUN],
            BaguaType.KUN: [BaguaType.GEN, BaguaType.QIAN]
        }
    
    def get_bagua_relation(self, bagua1: BaguaType, bagua2: BaguaType) -> BaguaRelation:
        """获取两个八卦之间的关系"""
        if self.bagua_opposites.get(bagua1) == bagua2:
            return BaguaRelation.CONFLICT
        elif bagua2 in self.bagua_harmony.get(bagua1, []):
            return BaguaRelation.HARMONY
        else:
            return BaguaRelation.NEUTRAL
    
    def calculate_bagua_bonus(self, state: BaguaState, bagua: BaguaType) -> float:
        """计算八卦奖励"""
        base_value = state.get_bagua_value(bagua)
        total_bonus = base_value
        
        # 计算和谐奖励
        harmony_baguas = self.bagua_harmony.get(bagua, [])
        for harmony_bagua in harmony_baguas:
            harmony_value = state.get_bagua_value(harmony_bagua)
            total_bonus += harmony_value * BAGUA_AFFINITY_BONUS * 0.5
        
        # 计算冲突惩罚
        opposite_bagua = self.bagua_opposites.get(bagua)
        if opposite_bagua:
            opposite_value = state.get_bagua_value(opposite_bagua)
            total_bonus -= opposite_value * BAGUA_CONFLICT_PENALTY * 0.3
        
        return max(0.0, total_bonus)

class YinyangSystem:
    """阴阳系统"""
    
    def calculate_balance_bonus(self, state: YinyangState) -> float:
        """计算阴阳平衡奖励"""
        balance_score = state.get_balance_score()
        total_power = state.get_total_power()
        
        # 平衡度越高，奖励越大
        return total_power * balance_score * YINYANG_BALANCE_BONUS
    
    def calculate_imbalance_penalty(self, state: YinyangState) -> float:
        """计算阴阳失衡惩罚"""
        balance_score = state.get_balance_score()
        total_power = state.get_total_power()
        
        # 失衡度越高，惩罚越大
        imbalance_score = 1.0 - balance_score
        return total_power * imbalance_score * YINYANG_IMBALANCE_PENALTY
    
    def update_yinyang_state(self, state: YinyangState, yin_change: float, 
                           yang_change: float) -> YinyangState:
        """更新阴阳状态"""
        return YinyangState(
            yin=max(0.0, state.yin + yin_change),
            yang=max(0.0, state.yang + yang_change)
        )

class CultivationSystem:
    """修为系统"""
    
    def __init__(self):
        """初始化修为系统"""
        self.level_requirements = {
            CultivationLevel.MORTAL: 0,
            CultivationLevel.QI_REFINING: 100,
            CultivationLevel.FOUNDATION: 300,
            CultivationLevel.GOLDEN_CORE: 600,
            CultivationLevel.NASCENT_SOUL: 1000,
            CultivationLevel.SPIRIT_TRANSFORMATION: 1500,
            CultivationLevel.VOID_REFINEMENT: 2200,
            CultivationLevel.UNITY: 3000,
            CultivationLevel.MAHAYANA: 4000,
            CultivationLevel.TRIBULATION: 5000
        }
    
    def can_advance_level(self, state: CultivationState) -> bool:
        """检查是否可以提升修为等级"""
        current_level_index = state.get_level_index()
        levels = list(CultivationLevel)
        
        if current_level_index >= len(levels) - 1:
            return False
        
        next_level = levels[current_level_index + 1]
        required_exp = self.level_requirements.get(next_level, float('inf'))
        
        return state.experience >= required_exp and state.can_breakthrough()
    
    def advance_level(self, state: CultivationState) -> CultivationState:
        """提升修为等级"""
        if not self.can_advance_level(state):
            raise YixueException("无法提升修为等级：条件不满足")
        
        current_level_index = state.get_level_index()
        levels = list(CultivationLevel)
        next_level = levels[current_level_index + 1]
        
        return CultivationState(
            level=next_level,
            experience=state.experience,
            breakthrough_progress=0.0
        )
    
    def add_experience(self, state: CultivationState, exp: float) -> CultivationState:
        """增加修为经验"""
        return CultivationState(
            level=state.level,
            experience=state.experience + exp,
            breakthrough_progress=state.breakthrough_progress
        )
    
    def add_breakthrough_progress(self, state: CultivationState, progress: float) -> CultivationState:
        """增加突破进度"""
        new_progress = min(100.0, state.breakthrough_progress + progress)
        return CultivationState(
            level=state.level,
            experience=state.experience,
            breakthrough_progress=new_progress
        )

# ==================== 综合易学系统 ====================

class UltimateYixueSystem(IYixueSystem):
    """综合易学系统实现"""
    
    def __init__(self):
        """初始化易学系统"""
        self.wuxing_system = WuxingSystem()
        self.bagua_system = BaguaSystem()
        self.yinyang_system = YinyangSystem()
        self.cultivation_system = CultivationSystem()
        
        logger.info("易学系统初始化完成")
    
    def calculate_culture_power(self, wuxing_state: WuxingState, bagua_state: BaguaState,
                              yinyang_state: YinyangState, cultivation_state: CultivationState) -> float:
        """计算文化力量值"""
        # 基础力量
        wuxing_power = wuxing_state.get_total_power()
        bagua_power = bagua_state.get_total_affinity()
        yinyang_power = yinyang_state.get_total_power()
        
        # 平衡奖励
        wuxing_balance_bonus = wuxing_state.get_balance_score() * wuxing_power * 0.2
        yinyang_balance_bonus = self.yinyang_system.calculate_balance_bonus(yinyang_state)
        
        # 修为倍数
        cultivation_multiplier = cultivation_state.get_power_multiplier()
        
        # 综合计算
        base_power = wuxing_power + bagua_power + yinyang_power
        bonus_power = wuxing_balance_bonus + yinyang_balance_bonus
        
        total_power = (base_power + bonus_power) * cultivation_multiplier
        
        return total_power
    
    def calculate_action_effectiveness(self, action_type: str, wuxing_state: WuxingState,
                                    bagua_state: BaguaState, yinyang_state: YinyangState) -> float:
        """计算行动有效性"""
        # 根据行动类型计算不同的有效性
        effectiveness = 1.0
        
        if action_type == "cultivation":
            # 修炼行动受阴阳平衡影响
            effectiveness *= (1.0 + yinyang_state.get_balance_score() * 0.5)
        
        elif action_type == "spell":
            # 法术行动受五行平衡影响
            effectiveness *= (1.0 + wuxing_state.get_balance_score() * 0.3)
        
        elif action_type == "divination":
            # 占卜行动受八卦亲和度影响
            bagua_total = bagua_state.get_total_affinity()
            effectiveness *= (1.0 + bagua_total * 0.1)
        
        return effectiveness
    
    def process_elemental_interaction(self, source_element: WuxingElement, 
                                    target_element: WuxingElement,
                                    wuxing_state: WuxingState, 
                                    interaction_strength: float) -> WuxingState:
        """处理五行元素相互作用"""
        return self.wuxing_system.update_wuxing_state(
            wuxing_state, source_element, interaction_strength
        )
    
    def get_optimal_bagua_placement(self, position: Position, 
                                  board_size: Tuple[int, int]) -> BaguaType:
        """获取位置的最佳八卦配置"""
        x, y = position.x, position.y
        width, height = board_size
        
        # 根据位置计算八卦
        center_x, center_y = width // 2, height // 2
        
        # 计算相对位置
        rel_x = x - center_x
        rel_y = y - center_y
        
        # 根据八个方位确定八卦
        if rel_x == 0 and rel_y < 0:  # 正北
            return BaguaType.KAN
        elif rel_x > 0 and rel_y < 0:  # 东北
            return BaguaType.GEN
        elif rel_x > 0 and rel_y == 0:  # 正东
            return BaguaType.ZHEN
        elif rel_x > 0 and rel_y > 0:  # 东南
            return BaguaType.XUN
        elif rel_x == 0 and rel_y > 0:  # 正南
            return BaguaType.LI
        elif rel_x < 0 and rel_y > 0:  # 西南
            return BaguaType.KUN
        elif rel_x < 0 and rel_y == 0:  # 正西
            return BaguaType.DUI
        else:  # 西北
            return BaguaType.QIAN
    
    def simulate_cultivation_session(self, cultivation_state: CultivationState,
                                   session_duration: float,
                                   focus_elements: List[WuxingElement]) -> Tuple[CultivationState, WuxingState]:
        """模拟修炼过程"""
        # 基础经验获得
        base_exp = session_duration * 10
        
        # 修为等级影响
        level_multiplier = cultivation_state.get_power_multiplier()
        total_exp = base_exp * level_multiplier
        
        # 更新修为状态
        new_cultivation_state = self.cultivation_system.add_experience(
            cultivation_state, total_exp
        )
        
        # 增加突破进度
        breakthrough_progress = session_duration * 5
        new_cultivation_state = self.cultivation_system.add_breakthrough_progress(
            new_cultivation_state, breakthrough_progress
        )
        
        # 更新五行状态
        new_wuxing_state = WuxingState()
        for element in focus_elements:
            element_gain = session_duration * 2
            current_value = new_wuxing_state.get_element_value(element)
            new_wuxing_state.set_element_value(element, current_value + element_gain)
        
        return new_cultivation_state, new_wuxing_state

# ==================== 工厂函数 ====================

def create_default_wuxing_state() -> WuxingState:
    """创建默认五行状态"""
    return WuxingState(wood=10.0, fire=10.0, earth=10.0, metal=10.0, water=10.0)

def create_default_bagua_state() -> BaguaState:
    """创建默认八卦状态"""
    return BaguaState(qian=5.0, kun=5.0, zhen=5.0, xun=5.0, 
                     kan=5.0, li=5.0, gen=5.0, dui=5.0)

def create_default_yinyang_state() -> YinyangState:
    """创建默认阴阳状态"""
    return YinyangState(yin=25.0, yang=25.0)

def create_default_cultivation_state() -> CultivationState:
    """创建默认修为状态"""
    return CultivationState(
        level=CultivationLevel.MORTAL,
        experience=0.0,
        breakthrough_progress=0.0
    )

def create_yixue_system() -> UltimateYixueSystem:
    """创建易学系统实例"""
    return UltimateYixueSystem()

# ==================== 导出列表 ====================

__all__ = [
    # 枚举
    'CultivationLevel', 'ElementalReaction', 'BaguaRelation',
    
    # 数据类
    'WuxingState', 'BaguaState', 'YinyangState', 'CultivationState',
    
    # 系统类
    'WuxingSystem', 'BaguaSystem', 'YinyangSystem', 'CultivationSystem',
    'UltimateYixueSystem',
    
    # 工厂函数
    'create_default_wuxing_state', 'create_default_bagua_state',
    'create_default_yinyang_state', 'create_default_cultivation_state',
    'create_yixue_system'
]