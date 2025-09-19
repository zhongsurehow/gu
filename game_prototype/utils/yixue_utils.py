"""
天机变游戏易学计算工具
提供易学相关的计算函数和工具
"""

from typing import Dict, List, Tuple, Optional
import math
from enum import Enum

from ..core.base_types import WuxingElement, BaguaType, CultivationRealm
from ..core.constants import *

# ==================== 五行相关计算 ====================

class WuxingRelation(Enum):
    """五行关系类型"""
    GENERATION = "generation"  # 相生
    DESTRUCTION = "destruction"  # 相克
    NEUTRAL = "neutral"  # 中性

# 五行相生关系：木生火，火生土，土生金，金生水，水生木
WUXING_GENERATION = {
    WuxingElement.WOOD: WuxingElement.FIRE,
    WuxingElement.FIRE: WuxingElement.EARTH,
    WuxingElement.EARTH: WuxingElement.METAL,
    WuxingElement.METAL: WuxingElement.WATER,
    WuxingElement.WATER: WuxingElement.WOOD
}

# 五行相克关系：木克土，土克水，水克火，火克金，金克木
WUXING_DESTRUCTION = {
    WuxingElement.WOOD: WuxingElement.EARTH,
    WuxingElement.EARTH: WuxingElement.WATER,
    WuxingElement.WATER: WuxingElement.FIRE,
    WuxingElement.FIRE: WuxingElement.METAL,
    WuxingElement.METAL: WuxingElement.WOOD
}

def get_wuxing_relation(element1: WuxingElement, element2: WuxingElement) -> WuxingRelation:
    """
    获取两个五行元素之间的关系
    
    Args:
        element1: 第一个元素
        element2: 第二个元素
        
    Returns:
        五行关系类型
    """
    if element1 == element2:
        return WuxingRelation.NEUTRAL
    
    # 检查相生关系
    if WUXING_GENERATION.get(element1) == element2:
        return WuxingRelation.GENERATION
    
    # 检查相克关系
    if WUXING_DESTRUCTION.get(element1) == element2:
        return WuxingRelation.DESTRUCTION
    
    return WuxingRelation.NEUTRAL

def calculate_wuxing_relationship(
    mastery1: Dict[WuxingElement, int], 
    mastery2: Dict[WuxingElement, int]
) -> Tuple[float, WuxingRelation]:
    """
    计算两个五行掌握度之间的关系强度
    
    Args:
        mastery1: 第一个五行掌握度字典
        mastery2: 第二个五行掌握度字典
        
    Returns:
        (关系强度, 主要关系类型)
    """
    generation_strength = 0.0
    destruction_strength = 0.0
    
    for elem1, value1 in mastery1.items():
        for elem2, value2 in mastery2.items():
            relation = get_wuxing_relation(elem1, elem2)
            strength = (value1 * value2) / (MAX_WUXING_MASTERY * MAX_WUXING_MASTERY)
            
            if relation == WuxingRelation.GENERATION:
                generation_strength += strength
            elif relation == WuxingRelation.DESTRUCTION:
                destruction_strength += strength
    
    # 确定主要关系
    if generation_strength > destruction_strength:
        return generation_strength, WuxingRelation.GENERATION
    elif destruction_strength > generation_strength:
        return destruction_strength, WuxingRelation.DESTRUCTION
    else:
        return 0.0, WuxingRelation.NEUTRAL

def calculate_wuxing_balance(mastery: Dict[WuxingElement, int]) -> float:
    """
    计算五行平衡度
    
    Args:
        mastery: 五行掌握度字典
        
    Returns:
        平衡度 (0.0-1.0)
    """
    values = list(mastery.values())
    if not values or all(v == 0 for v in values):
        return 1.0
    
    mean_value = sum(values) / len(values)
    variance = sum((v - mean_value) ** 2 for v in values) / len(values)
    
    # 标准化方差，转换为平衡度
    max_variance = (MAX_WUXING_MASTERY ** 2) / 4  # 理论最大方差
    balance = 1.0 - (variance / max_variance)
    
    return max(0.0, min(1.0, balance))

def get_dominant_wuxing(mastery: Dict[WuxingElement, int]) -> Optional[WuxingElement]:
    """
    获取主导五行元素
    
    Args:
        mastery: 五行掌握度字典
        
    Returns:
        主导元素，如果没有则返回None
    """
    if not mastery:
        return None
    
    max_element = max(mastery.keys(), key=lambda x: mastery[x])
    return max_element if mastery[max_element] > 0 else None

def calculate_wuxing_cycle_completion(mastery: Dict[WuxingElement, int]) -> float:
    """
    计算五行循环完成度
    
    Args:
        mastery: 五行掌握度字典
        
    Returns:
        完成度 (0.0-1.0)
    """
    min_mastery = min(mastery.values()) if mastery else 0
    return min_mastery / MAX_WUXING_MASTERY

# ==================== 八卦相关计算 ====================

# 八卦属性
BAGUA_ATTRIBUTES = {
    BaguaType.QIAN: {"element": "金", "direction": "西北", "nature": "天", "attribute": "刚健"},
    BaguaType.KUN: {"element": "土", "direction": "西南", "nature": "地", "attribute": "柔顺"},
    BaguaType.ZHEN: {"element": "木", "direction": "东", "nature": "雷", "attribute": "动"},
    BaguaType.XUN: {"element": "木", "direction": "东南", "nature": "风", "attribute": "入"},
    BaguaType.KAN: {"element": "水", "direction": "北", "nature": "水", "attribute": "陷"},
    BaguaType.LI: {"element": "火", "direction": "南", "nature": "火", "attribute": "丽"},
    BaguaType.GEN: {"element": "土", "direction": "东北", "nature": "山", "attribute": "止"},
    BaguaType.DUI: {"element": "金", "direction": "西", "nature": "泽", "attribute": "悦"}
}

# 八卦相配关系（基于先天八卦）
BAGUA_COMPATIBILITY = {
    BaguaType.QIAN: [BaguaType.KUN, BaguaType.DUI],  # 乾配坤、兑
    BaguaType.KUN: [BaguaType.QIAN, BaguaType.GEN],  # 坤配乾、艮
    BaguaType.ZHEN: [BaguaType.XUN, BaguaType.LI],   # 震配巽、离
    BaguaType.XUN: [BaguaType.ZHEN, BaguaType.KAN],  # 巽配震、坎
    BaguaType.KAN: [BaguaType.LI, BaguaType.XUN],    # 坎配离、巽
    BaguaType.LI: [BaguaType.KAN, BaguaType.ZHEN],   # 离配坎、震
    BaguaType.GEN: [BaguaType.DUI, BaguaType.KUN],   # 艮配兑、坤
    BaguaType.DUI: [BaguaType.GEN, BaguaType.QIAN]   # 兑配艮、乾
}

def calculate_bagua_compatibility(
    affinity1: Dict[BaguaType, int], 
    affinity2: Dict[BaguaType, int]
) -> float:
    """
    计算两个八卦亲和度之间的兼容性
    
    Args:
        affinity1: 第一个八卦亲和度字典
        affinity2: 第二个八卦亲和度字典
        
    Returns:
        兼容性分数 (0.0-1.0)
    """
    compatibility_score = 0.0
    total_combinations = 0
    
    for bagua1, value1 in affinity1.items():
        for bagua2, value2 in affinity2.items():
            total_combinations += 1
            
            # 计算基础兼容性
            if bagua1 == bagua2:
                # 相同八卦，完全兼容
                compatibility = 1.0
            elif bagua2 in BAGUA_COMPATIBILITY.get(bagua1, []):
                # 相配八卦，高兼容性
                compatibility = 0.8
            else:
                # 其他情况，基于五行关系
                elem1_str = BAGUA_ATTRIBUTES[bagua1]["element"]
                elem2_str = BAGUA_ATTRIBUTES[bagua2]["element"]
                
                # 简化的五行兼容性
                if elem1_str == elem2_str:
                    compatibility = 0.6
                else:
                    compatibility = 0.3
            
            # 加权计算
            weight = (value1 * value2) / (MAX_BAGUA_AFFINITY * MAX_BAGUA_AFFINITY)
            compatibility_score += compatibility * weight
    
    return compatibility_score / total_combinations if total_combinations > 0 else 0.0

def get_bagua_element_distribution(affinity: Dict[BaguaType, int]) -> Dict[str, int]:
    """
    获取八卦的五行元素分布
    
    Args:
        affinity: 八卦亲和度字典
        
    Returns:
        五行元素分布字典
    """
    element_distribution = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
    
    for bagua, value in affinity.items():
        element = BAGUA_ATTRIBUTES[bagua]["element"]
        element_distribution[element] += value
    
    return element_distribution

# ==================== 阴阳相关计算 ====================

def calculate_yinyang_balance(yin: int, yang: int) -> float:
    """
    计算阴阳平衡度
    
    Args:
        yin: 阴能量
        yang: 阳能量
        
    Returns:
        平衡度 (0.0-1.0)
    """
    total = yin + yang
    if total == 0:
        return 1.0
    
    min_energy = min(yin, yang)
    max_energy = max(yin, yang)
    
    if max_energy == 0:
        return 1.0
    
    return min_energy / max_energy

def calculate_yinyang_harmony(
    yin1: int, yang1: int, 
    yin2: int, yang2: int
) -> float:
    """
    计算两个阴阳状态之间的和谐度
    
    Args:
        yin1, yang1: 第一个阴阳状态
        yin2, yang2: 第二个阴阳状态
        
    Returns:
        和谐度 (0.0-1.0)
    """
    balance1 = calculate_yinyang_balance(yin1, yang1)
    balance2 = calculate_yinyang_balance(yin2, yang2)
    
    # 计算平衡度的相似性
    balance_similarity = 1.0 - abs(balance1 - balance2)
    
    # 计算能量比例的互补性
    total1 = yin1 + yang1
    total2 = yin2 + yang2
    
    if total1 == 0 or total2 == 0:
        return balance_similarity
    
    yin_ratio1 = yin1 / total1
    yang_ratio1 = yang1 / total1
    yin_ratio2 = yin2 / total2
    yang_ratio2 = yang2 / total2
    
    # 互补性：一方阴强时另一方阳强
    complementarity = (yin_ratio1 * yang_ratio2 + yang_ratio1 * yin_ratio2)
    
    return (balance_similarity + complementarity) / 2

def suggest_yinyang_adjustment(yin: int, yang: int, target_balance: float = 0.8) -> Tuple[int, int]:
    """
    建议阴阳调整方案
    
    Args:
        yin: 当前阴能量
        yang: 当前阳能量
        target_balance: 目标平衡度
        
    Returns:
        (建议阴调整量, 建议阳调整量)
    """
    current_balance = calculate_yinyang_balance(yin, yang)
    
    if current_balance >= target_balance:
        return 0, 0
    
    total = yin + yang
    if total == 0:
        # 如果都为0，建议平均增加
        return 5, 5
    
    # 计算目标值
    if yin < yang:
        # 阴不足，增加阴
        target_yin = int(yang * target_balance)
        return max(0, target_yin - yin), 0
    else:
        # 阳不足，增加阳
        target_yang = int(yin * target_balance)
        return 0, max(0, target_yang - yang)

# ==================== 修为相关计算 ====================

def get_cultivation_requirements(current_realm: CultivationRealm) -> Dict[str, int]:
    """
    获取修为提升要求
    
    Args:
        current_realm: 当前修为境界
        
    Returns:
        提升要求字典
    """
    requirements = {
        CultivationRealm.MORTAL: {
            "min_balance": 0.3,
            "min_wuxing_total": 10,
            "min_bagua_total": 8,
            "min_culture": 50
        },
        CultivationRealm.QI_REFINING: {
            "min_balance": 0.4,
            "min_wuxing_total": 25,
            "min_bagua_total": 20,
            "min_culture": 100
        },
        CultivationRealm.FOUNDATION: {
            "min_balance": 0.5,
            "min_wuxing_total": 50,
            "min_bagua_total": 40,
            "min_culture": 200
        },
        CultivationRealm.GOLDEN_CORE: {
            "min_balance": 0.6,
            "min_wuxing_total": 100,
            "min_bagua_total": 80,
            "min_culture": 400
        },
        CultivationRealm.NASCENT_SOUL: {
            "min_balance": 0.7,
            "min_wuxing_total": 200,
            "min_bagua_total": 160,
            "min_culture": 800
        },
        CultivationRealm.SPIRIT_TRANSFORMATION: {
            "min_balance": 0.8,
            "min_wuxing_total": 350,
            "min_bagua_total": 280,
            "min_culture": 1500
        },
        CultivationRealm.VOID_REFINEMENT: {
            "min_balance": 0.85,
            "min_wuxing_total": 500,
            "min_bagua_total": 400,
            "min_culture": 2500
        },
        CultivationRealm.UNITY: {
            "min_balance": 0.9,
            "min_wuxing_total": 700,
            "min_bagua_total": 560,
            "min_culture": 4000
        },
        CultivationRealm.MAHAYANA: {
            "min_balance": 0.95,
            "min_wuxing_total": 900,
            "min_bagua_total": 720,
            "min_culture": 6000
        }
    }
    
    realms = list(CultivationRealm)
    current_index = realms.index(current_realm)
    
    if current_index >= len(realms) - 1:
        return {}  # 已达最高境界
    
    next_realm = realms[current_index + 1]
    return requirements.get(next_realm, {})

def calculate_cultivation_progress(
    current_realm: CultivationRealm,
    yin: int, yang: int,
    wuxing_mastery: Dict[WuxingElement, int],
    bagua_affinity: Dict[BaguaType, int],
    culture: int
) -> float:
    """
    计算修为提升进度
    
    Args:
        current_realm: 当前修为境界
        yin, yang: 阴阳能量
        wuxing_mastery: 五行掌握度
        bagua_affinity: 八卦亲和度
        culture: 文化力
        
    Returns:
        进度百分比 (0.0-1.0)
    """
    requirements = get_cultivation_requirements(current_realm)
    if not requirements:
        return 1.0  # 已达最高境界
    
    # 计算各项指标的完成度
    balance = calculate_yinyang_balance(yin, yang)
    wuxing_total = sum(wuxing_mastery.values())
    bagua_total = sum(bagua_affinity.values())
    
    progress_items = []
    
    if "min_balance" in requirements:
        progress_items.append(min(1.0, balance / requirements["min_balance"]))
    
    if "min_wuxing_total" in requirements:
        progress_items.append(min(1.0, wuxing_total / requirements["min_wuxing_total"]))
    
    if "min_bagua_total" in requirements:
        progress_items.append(min(1.0, bagua_total / requirements["min_bagua_total"]))
    
    if "min_culture" in requirements:
        progress_items.append(min(1.0, culture / requirements["min_culture"]))
    
    return sum(progress_items) / len(progress_items) if progress_items else 0.0

# ==================== 综合计算函数 ====================

def calculate_yixue_harmony(
    yin: int, yang: int,
    wuxing_mastery: Dict[WuxingElement, int],
    bagua_affinity: Dict[BaguaType, int]
) -> float:
    """
    计算易学和谐度（综合指标）
    
    Args:
        yin, yang: 阴阳能量
        wuxing_mastery: 五行掌握度
        bagua_affinity: 八卦亲和度
        
    Returns:
        和谐度 (0.0-1.0)
    """
    # 阴阳平衡度
    yinyang_balance = calculate_yinyang_balance(yin, yang)
    
    # 五行平衡度
    wuxing_balance = calculate_wuxing_balance(wuxing_mastery)
    
    # 八卦与五行的协调度
    bagua_elements = get_bagua_element_distribution(bagua_affinity)
    
    # 计算八卦五行与五行掌握度的协调性
    element_harmony = 0.0
    element_map = {
        "木": WuxingElement.WOOD,
        "火": WuxingElement.FIRE,
        "土": WuxingElement.EARTH,
        "金": WuxingElement.METAL,
        "水": WuxingElement.WATER
    }
    
    for elem_str, bagua_value in bagua_elements.items():
        if elem_str in element_map:
            wuxing_elem = element_map[elem_str]
            wuxing_value = wuxing_mastery.get(wuxing_elem, 0)
            
            # 计算协调性（值越接近越好）
            if bagua_value + wuxing_value > 0:
                harmony = 1.0 - abs(bagua_value - wuxing_value) / (bagua_value + wuxing_value)
                element_harmony += harmony
    
    element_harmony /= len(element_map)
    
    # 综合计算
    total_harmony = (yinyang_balance * 0.3 + wuxing_balance * 0.3 + element_harmony * 0.4)
    
    return max(0.0, min(1.0, total_harmony))

def get_yixue_recommendations(
    yin: int, yang: int,
    wuxing_mastery: Dict[WuxingElement, int],
    bagua_affinity: Dict[BaguaType, int]
) -> List[str]:
    """
    获取易学修炼建议
    
    Args:
        yin, yang: 阴阳能量
        wuxing_mastery: 五行掌握度
        bagua_affinity: 八卦亲和度
        
    Returns:
        建议列表
    """
    recommendations = []
    
    # 阴阳建议
    balance = calculate_yinyang_balance(yin, yang)
    if balance < 0.5:
        if yin < yang:
            recommendations.append("建议增强阴能量修炼，如静坐冥想、水行功法")
        else:
            recommendations.append("建议增强阳能量修炼，如动功练习、火行功法")
    
    # 五行建议
    wuxing_balance = calculate_wuxing_balance(wuxing_mastery)
    if wuxing_balance < 0.6:
        min_element = min(wuxing_mastery.keys(), key=lambda x: wuxing_mastery[x])
        recommendations.append(f"建议加强{min_element.value}行修炼，以平衡五行")
    
    # 八卦建议
    bagua_total = sum(bagua_affinity.values())
    if bagua_total < 100:
        weak_bagua = [bagua for bagua, value in bagua_affinity.items() if value < 10]
        if weak_bagua:
            recommendations.append(f"建议提升{weak_bagua[0].value}卦亲和度")
    
    # 综合建议
    harmony = calculate_yixue_harmony(yin, yang, wuxing_mastery, bagua_affinity)
    if harmony < 0.7:
        recommendations.append("建议注重整体修炼平衡，避免偏重某一方面")
    
    return recommendations