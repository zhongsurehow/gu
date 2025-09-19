#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强卦象系统 - 实现变卦、互卦、错卦等高级易经机制
为游戏添加更深层的策略性和易经智慧
"""

from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum
import random

from yijing_mechanics import YinYang, WuXing
from card_base import GuaCard, YaoCiTask
from generate_64_guas import GUA_64_INFO, ALL_64_GUAS

class HexagramRelationType(Enum):
    """卦象关系类型"""
    ORIGINAL = "本卦"          # 原始卦象
    CHANGED = "变卦"           # 变卦（爻变后的卦）
    MUTUAL = "互卦"            # 互卦（2、3、4爻为下卦，3、4、5爻为上卦）
    INVERSE = "错卦"           # 错卦（阴阳全部颠倒）
    REVERSE = "综卦"           # 综卦（上下颠倒）
    NUCLEAR = "核卦"           # 核卦（内卦）

@dataclass
class HexagramState:
    """卦象状态"""
    name: str
    lines: List[bool]  # True为阳爻，False为阴爻
    changing_lines: Set[int] = None  # 变爻位置（0-5）
    
    def __post_init__(self):
        if self.changing_lines is None:
            self.changing_lines = set()

@dataclass
class HexagramRelation:
    """卦象关系"""
    primary: str
    related: str
    relation_type: HexagramRelationType
    description: str
    strategic_value: int  # 策略价值（1-10）

class EnhancedHexagramSystem:
    """增强卦象系统"""
    
    def __init__(self):
        self.hexagram_lines = self._initialize_hexagram_lines()
        self.relations = self._calculate_all_relations()
        self.strategic_combinations = self._define_strategic_combinations()
        
    def _initialize_hexagram_lines(self) -> Dict[str, List[bool]]:
        """初始化所有卦象的爻线组合"""
        lines_map = {}
        
        # 八卦基础爻线
        basic_trigrams = {
            "乾": [True, True, True],      # ☰
            "坤": [False, False, False],   # ☷
            "震": [False, False, True],    # ☳
            "巽": [True, False, False],    # ☴
            "坎": [False, True, False],    # ☵
            "离": [True, False, True],     # ☲
            "艮": [True, True, False],     # ☶
            "兑": [False, True, True]      # ☱
        }
        
        # 生成64卦的爻线组合
        for gua_name, gua_info in GUA_64_INFO.items():
            upper_trigram, lower_trigram = gua_info["trigrams"]
            upper_lines = basic_trigrams[upper_trigram]
            lower_lines = basic_trigrams[lower_trigram]
            
            # 组合成六爻（下卦在下，上卦在上）
            lines_map[gua_name] = lower_lines + upper_lines
            
        return lines_map
    
    def _calculate_all_relations(self) -> Dict[str, List[HexagramRelation]]:
        """计算所有卦象的关系"""
        relations = {}
        
        for gua_name in GUA_64_INFO.keys():
            relations[gua_name] = []
            
            # 计算错卦（阴阳颠倒）
            inverse_gua = self._get_inverse_hexagram(gua_name)
            if inverse_gua:
                relations[gua_name].append(HexagramRelation(
                    primary=gua_name,
                    related=inverse_gua,
                    relation_type=HexagramRelationType.INVERSE,
                    description=f"{gua_name}的错卦，阴阳相反，互为补充",
                    strategic_value=8
                ))
            
            # 计算综卦（上下颠倒）
            reverse_gua = self._get_reverse_hexagram(gua_name)
            if reverse_gua:
                relations[gua_name].append(HexagramRelation(
                    primary=gua_name,
                    related=reverse_gua,
                    relation_type=HexagramRelationType.REVERSE,
                    description=f"{gua_name}的综卦，上下颠倒，时序相反",
                    strategic_value=7
                ))
            
            # 计算互卦
            mutual_gua = self._get_mutual_hexagram(gua_name)
            if mutual_gua:
                relations[gua_name].append(HexagramRelation(
                    primary=gua_name,
                    related=mutual_gua,
                    relation_type=HexagramRelationType.MUTUAL,
                    description=f"{gua_name}的互卦，内在变化的趋势",
                    strategic_value=9
                ))
            
            # 计算常见变卦（单爻变）
            for line_pos in range(6):
                changed_gua = self._get_changed_hexagram(gua_name, {line_pos})
                if changed_gua:
                    relations[gua_name].append(HexagramRelation(
                        primary=gua_name,
                        related=changed_gua,
                        relation_type=HexagramRelationType.CHANGED,
                        description=f"{gua_name}第{line_pos+1}爻变为{changed_gua}",
                        strategic_value=6
                    ))
        
        return relations
    
    def _get_inverse_hexagram(self, gua_name: str) -> Optional[str]:
        """获取错卦（阴阳颠倒）"""
        if gua_name not in self.hexagram_lines:
            return None
            
        original_lines = self.hexagram_lines[gua_name]
        inverse_lines = [not line for line in original_lines]
        
        # 查找匹配的卦象
        for name, lines in self.hexagram_lines.items():
            if lines == inverse_lines:
                return name
        return None
    
    def _get_reverse_hexagram(self, gua_name: str) -> Optional[str]:
        """获取综卦（上下颠倒）"""
        if gua_name not in self.hexagram_lines:
            return None
            
        original_lines = self.hexagram_lines[gua_name]
        reverse_lines = original_lines[::-1]  # 颠倒顺序
        
        # 查找匹配的卦象
        for name, lines in self.hexagram_lines.items():
            if lines == reverse_lines:
                return name
        return None
    
    def _get_mutual_hexagram(self, gua_name: str) -> Optional[str]:
        """获取互卦（2、3、4爻为下卦，3、4、5爻为上卦）"""
        if gua_name not in self.hexagram_lines:
            return None
            
        original_lines = self.hexagram_lines[gua_name]
        
        # 互卦的构成：2、3、4爻为下卦，3、4、5爻为上卦
        if len(original_lines) >= 6:
            lower_mutual = original_lines[1:4]  # 2、3、4爻
            upper_mutual = original_lines[2:5]  # 3、4、5爻
            mutual_lines = lower_mutual + upper_mutual
            
            # 查找匹配的卦象
            for name, lines in self.hexagram_lines.items():
                if lines == mutual_lines:
                    return name
        return None
    
    def _get_changed_hexagram(self, gua_name: str, changing_lines: Set[int]) -> Optional[str]:
        """获取变卦（指定爻变化后的卦）"""
        if gua_name not in self.hexagram_lines:
            return None
            
        original_lines = self.hexagram_lines[gua_name].copy()
        
        # 变化指定的爻
        for line_pos in changing_lines:
            if 0 <= line_pos < len(original_lines):
                original_lines[line_pos] = not original_lines[line_pos]
        
        # 查找匹配的卦象
        for name, lines in self.hexagram_lines.items():
            if lines == original_lines:
                return name
        return None
    
    def _define_strategic_combinations(self) -> Dict[str, Dict]:
        """定义策略性卦象组合"""
        return {
            "天地定位": {
                "hexagrams": ["乾为天", "坤为地"],
                "description": "乾坤定位，阴阳调和，获得强大的平衡力量",
                "effects": {
                    "yin_yang_balance": 0.5,
                    "qi_bonus": 3,
                    "dao_xing_bonus": 2
                },
                "activation_condition": "同时控制乾卦和坤卦区域"
            },
            "水火既济": {
                "hexagrams": ["坎为水", "离为火"],
                "description": "水火相济，阴阳和合，事业有成",
                "effects": {
                    "wuxing_harmony": True,
                    "action_efficiency": 1.5,
                    "resource_generation": 2
                },
                "activation_condition": "同时拥有水属性和火属性卡牌"
            },
            "雷风相薄": {
                "hexagrams": ["震为雷", "巽为风"],
                "description": "雷风激荡，变化迅速，行动力大增",
                "effects": {
                    "extra_actions": 1,
                    "movement_bonus": 2,
                    "change_resistance": True
                },
                "activation_condition": "连续两回合使用动态行动"
            },
            "山泽通气": {
                "hexagrams": ["艮为山", "兑为泽"],
                "description": "山泽通气，收藏有度，资源管理优化",
                "effects": {
                    "resource_efficiency": 1.3,
                    "storage_bonus": 3,
                    "waste_reduction": True
                },
                "activation_condition": "资源总量达到特定阈值"
            }
        }
    
    def get_hexagram_relations(self, gua_name: str) -> List[HexagramRelation]:
        """获取指定卦象的所有关系"""
        return self.relations.get(gua_name, [])
    
    def get_strategic_combinations(self, player_hexagrams: List[str]) -> List[Dict]:
        """获取玩家可激活的策略组合"""
        activated_combinations = []
        
        for combo_name, combo_data in self.strategic_combinations.items():
            required_hexagrams = set(combo_data["hexagrams"])
            player_hexagram_set = set(player_hexagrams)
            
            if required_hexagrams.issubset(player_hexagram_set):
                activated_combinations.append({
                    "name": combo_name,
                    "data": combo_data
                })
        
        return activated_combinations
    
    def calculate_hexagram_synergy(self, hexagrams: List[str]) -> Dict[str, float]:
        """计算卦象间的协同效应"""
        synergy_scores = {
            "yin_yang_harmony": 0.0,
            "wuxing_balance": 0.0,
            "strategic_depth": 0.0,
            "overall_synergy": 0.0
        }
        
        if len(hexagrams) < 2:
            return synergy_scores
        
        # 计算阴阳和谐度
        yin_count = 0
        yang_count = 0
        for gua_name in hexagrams:
            if gua_name in GUA_64_INFO:
                if GUA_64_INFO[gua_name]["yin_yang"] == YinYang.YIN:
                    yin_count += 1
                else:
                    yang_count += 1
        
        total_guas = yin_count + yang_count
        if total_guas > 0:
            yin_ratio = yin_count / total_guas
            # 最佳平衡点是0.5，偏离越少协同度越高
            synergy_scores["yin_yang_harmony"] = 1.0 - abs(yin_ratio - 0.5) * 2
        
        # 计算五行平衡度
        wuxing_counts = {element: 0 for element in WuXing}
        for gua_name in hexagrams:
            if gua_name in GUA_64_INFO:
                element = GUA_64_INFO[gua_name]["element"]
                wuxing_counts[element] += 1
        
        # 五行分布越均匀，平衡度越高
        max_count = max(wuxing_counts.values()) if wuxing_counts.values() else 0
        min_count = min(wuxing_counts.values()) if wuxing_counts.values() else 0
        if max_count > 0:
            synergy_scores["wuxing_balance"] = 1.0 - (max_count - min_count) / max_count
        
        # 计算策略深度（基于卦象关系）
        relation_count = 0
        for gua1 in hexagrams:
            for gua2 in hexagrams:
                if gua1 != gua2:
                    relations = self.get_hexagram_relations(gua1)
                    for relation in relations:
                        if relation.related == gua2:
                            relation_count += 1
        
        synergy_scores["strategic_depth"] = min(relation_count / 10.0, 1.0)
        
        # 计算总体协同度
        synergy_scores["overall_synergy"] = (
            synergy_scores["yin_yang_harmony"] * 0.4 +
            synergy_scores["wuxing_balance"] * 0.3 +
            synergy_scores["strategic_depth"] * 0.3
        )
        
        return synergy_scores
    
    def suggest_next_hexagram(self, current_hexagrams: List[str], 
                            available_hexagrams: List[str]) -> List[Tuple[str, float]]:
        """建议下一个最佳卦象选择"""
        suggestions = []
        
        for candidate in available_hexagrams:
            if candidate not in current_hexagrams:
                test_combination = current_hexagrams + [candidate]
                synergy = self.calculate_hexagram_synergy(test_combination)
                
                # 计算建议分数
                score = synergy["overall_synergy"]
                
                # 检查是否能激活策略组合
                combinations = self.get_strategic_combinations(test_combination)
                if combinations:
                    score += 0.3  # 能激活组合的额外加分
                
                suggestions.append((candidate, score))
        
        # 按分数排序
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return suggestions[:5]  # 返回前5个建议
    
    def get_hexagram_transformation_path(self, start_gua: str, 
                                       target_gua: str) -> Optional[List[str]]:
        """获取从起始卦到目标卦的变化路径"""
        if start_gua not in self.hexagram_lines or target_gua not in self.hexagram_lines:
            return None
        
        start_lines = self.hexagram_lines[start_gua]
        target_lines = self.hexagram_lines[target_gua]
        
        # 找出需要变化的爻位
        changing_positions = []
        for i, (start_line, target_line) in enumerate(zip(start_lines, target_lines)):
            if start_line != target_line:
                changing_positions.append(i)
        
        if not changing_positions:
            return [start_gua]  # 已经是目标卦
        
        # 生成变化路径（逐步变化）
        path = [start_gua]
        current_lines = start_lines.copy()
        
        for pos in changing_positions:
            current_lines[pos] = not current_lines[pos]
            
            # 查找当前状态对应的卦象
            for name, lines in self.hexagram_lines.items():
                if lines == current_lines:
                    path.append(name)
                    break
        
        return path if path[-1] == target_gua else None
    
    def analyze_hexagram_power(self, gua_name: str) -> Dict[str, any]:
        """分析卦象的力量特征"""
        if gua_name not in GUA_64_INFO:
            return {}
        
        gua_info = GUA_64_INFO[gua_name]
        lines = self.hexagram_lines[gua_name]
        
        # 计算阳爻数量
        yang_count = sum(1 for line in lines if line)
        yin_count = 6 - yang_count
        
        # 分析力量特征
        analysis = {
            "name": gua_name,
            "nature": gua_info["nature"],
            "element": gua_info["element"].value,
            "yin_yang_tendency": gua_info["yin_yang"].value,
            "yang_lines": yang_count,
            "yin_lines": yin_count,
            "power_level": (yang_count * 2 + yin_count) / 6,  # 0-2的力量等级
            "stability": abs(yang_count - yin_count) / 6,  # 0-1的稳定性
            "relations": len(self.get_hexagram_relations(gua_name)),
            "strategic_value": self._calculate_strategic_value(gua_name)
        }
        
        return analysis
    
    def _calculate_strategic_value(self, gua_name: str) -> int:
        """计算卦象的策略价值"""
        base_value = 5
        
        # 根据卦象特性调整价值
        if gua_name in GUA_64_INFO:
            gua_info = GUA_64_INFO[gua_name]
            
            # 纯卦（同卦重叠）价值更高
            if gua_info["trigrams"][0] == gua_info["trigrams"][1]:
                base_value += 2
            
            # 特殊卦象价值调整
            special_values = {
                "乾为天": 10, "坤为地": 10,
                "水火既济": 9, "火水未济": 8,
                "地天泰": 9, "天地否": 7,
                "雷风恒": 8, "风雷益": 8
            }
            
            if gua_name in special_values:
                base_value = special_values[gua_name]
        
        return base_value

# 全局实例
enhanced_hexagram_system = EnhancedHexagramSystem()

def display_hexagram_analysis(gua_name: str):
    """显示卦象分析"""
    analysis = enhanced_hexagram_system.analyze_hexagram_power(gua_name)
    
    if not analysis:
        print(f"未找到卦象: {gua_name}")
        return
    
    print(f"\n=== {analysis['name']} 卦象分析 ===")
    print(f"本性: {analysis['nature']}")
    print(f"五行: {analysis['element']}")
    print(f"阴阳倾向: {analysis['yin_yang_tendency']}")
    print(f"阳爻数: {analysis['yang_lines']}, 阴爻数: {analysis['yin_lines']}")
    print(f"力量等级: {analysis['power_level']:.2f}/2.0")
    print(f"稳定性: {analysis['stability']:.2f}")
    print(f"关系数量: {analysis['relations']}")
    print(f"策略价值: {analysis['strategic_value']}/10")
    
    # 显示相关卦象
    relations = enhanced_hexagram_system.get_hexagram_relations(gua_name)
    if relations:
        print(f"\n相关卦象:")
        for relation in relations[:3]:  # 显示前3个关系
            print(f"  {relation.relation_type.value}: {relation.related}")
            print(f"    {relation.description}")

def display_synergy_analysis(hexagrams: List[str]):
    """显示协同效应分析"""
    synergy = enhanced_hexagram_system.calculate_hexagram_synergy(hexagrams)
    
    print(f"\n=== 卦象协同分析 ===")
    print(f"参与卦象: {', '.join(hexagrams)}")
    print(f"阴阳和谐度: {synergy['yin_yang_harmony']:.2f}")
    print(f"五行平衡度: {synergy['wuxing_balance']:.2f}")
    print(f"策略深度: {synergy['strategic_depth']:.2f}")
    print(f"总体协同度: {synergy['overall_synergy']:.2f}")
    
    # 显示可激活的策略组合
    combinations = enhanced_hexagram_system.get_strategic_combinations(hexagrams)
    if combinations:
        print(f"\n可激活的策略组合:")
        for combo in combinations:
            print(f"  {combo['name']}: {combo['data']['description']}")

if __name__ == "__main__":
    # 测试系统
    print("=== 增强卦象系统测试 ===")
    
    # 测试单个卦象分析
    display_hexagram_analysis("乾为天")
    display_hexagram_analysis("坤为地")
    
    # 测试协同效应
    test_hexagrams = ["乾为天", "坤为地", "坎为水", "离为火"]
    display_synergy_analysis(test_hexagrams)
    
    # 测试建议系统
    current = ["乾为天", "坤为地"]
    available = ["坎为水", "离为火", "震为雷", "巽为风"]
    suggestions = enhanced_hexagram_system.suggest_next_hexagram(current, available)
    
    print(f"\n=== 建议下一个卦象 ===")
    for gua, score in suggestions:
        print(f"{gua}: {score:.3f}")