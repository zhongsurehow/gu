#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强AI玩家系统 - 具备易经智慧和高级策略的AI对手
实现基于卦象分析、策略评估和适应性学习的智能AI
"""

from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import random
import math
import time

from game_state import GameState, Player
from advanced_strategy_system import (
    advanced_strategy_system, StrategyType, StrategyAction
)
from enhanced_hexagram_system import (
    enhanced_hexagram_system, HexagramRelationType
)
from yijing_mechanics import YinYang, WuXing
from generate_64_guas import GUA_64_INFO
from ui_enhancement import enhanced_print

class AIPersonality(Enum):
    """AI性格类型"""
    AGGRESSIVE = "进取型"      # 积极进攻，快速扩张
    DEFENSIVE = "守成型"       # 稳健防守，步步为营
    BALANCED = "平衡型"        # 攻守兼备，适应性强
    STRATEGIC = "谋略型"       # 深度思考，长远规划
    ADAPTIVE = "适应型"        # 快速学习，灵活应变

class AIDecisionType(Enum):
    """AI决策类型"""
    RESOURCE_MANAGEMENT = "资源管理"
    TERRITORY_EXPANSION = "领土扩张"
    STRATEGY_EXECUTION = "策略执行"
    DEFENSIVE_ACTION = "防御行动"
    OPPORTUNISTIC = "机会主义"

@dataclass
class AIMemory:
    """AI记忆系统"""
    successful_strategies: Dict[str, int] = field(default_factory=dict)
    failed_strategies: Dict[str, int] = field(default_factory=dict)
    opponent_patterns: Dict[str, List[str]] = field(default_factory=dict)
    game_state_evaluations: List[float] = field(default_factory=list)
    hexagram_preferences: Dict[str, float] = field(default_factory=dict)
    
@dataclass
class AIGoal:
    """AI目标"""
    name: str
    priority: float
    conditions: List[str]
    actions: List[str]
    progress: float = 0.0

class EnhancedAIPlayer:
    """增强AI玩家"""
    
    def __init__(self, name: str, personality: AIPersonality = AIPersonality.BALANCED):
        self.name = name
        self.personality = personality
        self.memory = AIMemory()
        self.current_goals: List[AIGoal] = []
        self.decision_weights = self._initialize_decision_weights()
        self.learning_rate = 0.1
        self.exploration_rate = 0.2
        
    def _initialize_decision_weights(self) -> Dict[AIDecisionType, float]:
        """根据性格初始化决策权重"""
        base_weights = {
            AIDecisionType.RESOURCE_MANAGEMENT: 1.0,
            AIDecisionType.TERRITORY_EXPANSION: 1.0,
            AIDecisionType.STRATEGY_EXECUTION: 1.0,
            AIDecisionType.DEFENSIVE_ACTION: 1.0,
            AIDecisionType.OPPORTUNISTIC: 1.0
        }
        
        # 根据性格调整权重
        if self.personality == AIPersonality.AGGRESSIVE:
            base_weights[AIDecisionType.TERRITORY_EXPANSION] = 1.5
            base_weights[AIDecisionType.OPPORTUNISTIC] = 1.3
            base_weights[AIDecisionType.DEFENSIVE_ACTION] = 0.7
            
        elif self.personality == AIPersonality.DEFENSIVE:
            base_weights[AIDecisionType.DEFENSIVE_ACTION] = 1.5
            base_weights[AIDecisionType.RESOURCE_MANAGEMENT] = 1.3
            base_weights[AIDecisionType.TERRITORY_EXPANSION] = 0.7
            
        elif self.personality == AIPersonality.STRATEGIC:
            base_weights[AIDecisionType.STRATEGY_EXECUTION] = 1.5
            base_weights[AIDecisionType.RESOURCE_MANAGEMENT] = 1.2
            
        elif self.personality == AIPersonality.ADAPTIVE:
            base_weights[AIDecisionType.OPPORTUNISTIC] = 1.4
            # 适应型会根据游戏进程动态调整权重
            
        return base_weights
    
    def make_decision(self, player: Player, game_state: GameState) -> str:
        """AI决策主函数"""
        # 分析当前局势
        situation_analysis = self._analyze_game_situation(player, game_state)
        
        # 更新目标
        self._update_goals(player, game_state, situation_analysis)
        
        # 评估可用行动
        available_actions = self._get_available_actions(player, game_state)
        
        # 选择最佳行动
        best_action = self._select_best_action(player, game_state, available_actions, situation_analysis)
        
        # 学习和记忆更新
        self._update_memory(player, game_state, best_action)
        
        return best_action
    
    def _analyze_game_situation(self, player: Player, game_state: GameState) -> Dict:
        """分析游戏局势"""
        analysis = {
            "resource_status": self._evaluate_resources(player),
            "territory_control": self._evaluate_territory(player, game_state),
            "opponent_threat": self._evaluate_threats(player, game_state),
            "strategic_opportunities": self._identify_opportunities(player, game_state),
            "hexagram_synergies": self._analyze_hexagram_synergies(player, game_state),
            "game_phase": self._determine_game_phase(game_state)
        }
        
        return analysis
    
    def _evaluate_resources(self, player: Player) -> Dict:
        """评估资源状况"""
        total_resources = player.qi + player.dao_xing + player.cheng_yi
        
        return {
            "total": total_resources,
            "qi_ratio": player.qi / max(total_resources, 1),
            "dao_xing_ratio": player.dao_xing / max(total_resources, 1),
            "cheng_yi_ratio": player.cheng_yi / max(total_resources, 1),
            "balance_score": 1.0 - abs(player.yin_yang_balance - 0.5) * 2,
            "resource_efficiency": self._calculate_resource_efficiency(player)
        }
    
    def _calculate_resource_efficiency(self, player: Player) -> float:
        """计算资源效率"""
        # 基于资源分布的均衡性计算效率
        resources = [player.qi, player.dao_xing, player.cheng_yi]
        if not resources or max(resources) == 0:
            return 0.0
        
        # 使用标准差衡量资源分布的均衡性
        mean_resource = sum(resources) / len(resources)
        variance = sum((r - mean_resource) ** 2 for r in resources) / len(resources)
        std_dev = math.sqrt(variance)
        
        # 效率与均衡性成反比
        efficiency = 1.0 / (1.0 + std_dev / max(mean_resource, 1))
        return efficiency
    
    def _evaluate_territory(self, player: Player, game_state: GameState) -> Dict:
        """评估领土控制"""
        controlled_zones = []
        total_zones = len(game_state.board.gua_zones)
        
        for zone_name, zone_data in game_state.board.gua_zones.items():
            if zone_data.get("controller") == player.name:
                controlled_zones.append(zone_name)
        
        control_ratio = len(controlled_zones) / max(total_zones, 1)
        
        # 分析控制区域的质量
        zone_quality = self._analyze_zone_quality(controlled_zones)
        
        return {
            "controlled_count": len(controlled_zones),
            "control_ratio": control_ratio,
            "zone_quality": zone_quality,
            "strategic_positions": self._identify_strategic_positions(controlled_zones, game_state)
        }
    
    def _analyze_zone_quality(self, controlled_zones: List[str]) -> Dict:
        """分析控制区域的质量"""
        if not controlled_zones:
            return {"average_power": 0, "element_diversity": 0, "synergy_potential": 0}
        
        total_power = 0
        elements = set()
        
        for zone_name in controlled_zones:
            if zone_name in GUA_64_INFO:
                gua_info = GUA_64_INFO[zone_name]
                # 假设每个卦象都有基础力量值
                total_power += len(gua_info.get("trigrams", []))
                elements.add(gua_info.get("element", ""))
        
        average_power = total_power / len(controlled_zones)
        element_diversity = len(elements)
        
        # 计算协同潜力
        synergy_potential = self._calculate_synergy_potential(controlled_zones)
        
        return {
            "average_power": average_power,
            "element_diversity": element_diversity,
            "synergy_potential": synergy_potential
        }
    
    def _calculate_synergy_potential(self, controlled_zones: List[str]) -> float:
        """计算协同潜力"""
        if len(controlled_zones) < 2:
            return 0.0
        
        synergy_score = 0.0
        
        for i, zone1 in enumerate(controlled_zones):
            for zone2 in controlled_zones[i+1:]:
                # 使用增强卦象系统分析关系
                relations = enhanced_hexagram_system.get_hexagram_relations(zone1)
                for relation in relations:
                    if relation.related == zone2:
                        synergy_score += relation.strength
        
        return synergy_score / max(len(controlled_zones) * (len(controlled_zones) - 1) / 2, 1)
    
    def _identify_strategic_positions(self, controlled_zones: List[str], 
                                    game_state: GameState) -> List[str]:
        """识别战略要地"""
        strategic_positions = []
        
        for zone_name in controlled_zones:
            if zone_name in GUA_64_INFO:
                gua_info = GUA_64_INFO[zone_name]
                
                # 检查是否为关键卦象（如乾、坤等）
                if zone_name in ["乾", "坤", "震", "巽", "坎", "离", "艮", "兑"]:
                    strategic_positions.append(zone_name)
                
                # 检查是否控制重要的五行元素
                if gua_info.get("element") in ["金", "木"]:  # 假设金木为关键元素
                    strategic_positions.append(zone_name)
        
        return strategic_positions
    
    def _evaluate_threats(self, player: Player, game_state: GameState) -> Dict:
        """评估威胁程度"""
        threats = {
            "immediate_threats": [],
            "potential_threats": [],
            "threat_level": 0.0
        }
        
        # 分析对手控制的区域
        for zone_name, zone_data in game_state.board.gua_zones.items():
            controller = zone_data.get("controller")
            if controller and controller != player.name:
                # 检查是否对我方构成威胁
                threat_score = self._calculate_threat_score(zone_name, player, game_state)
                
                if threat_score > 0.7:
                    threats["immediate_threats"].append((zone_name, controller, threat_score))
                elif threat_score > 0.4:
                    threats["potential_threats"].append((zone_name, controller, threat_score))
        
        # 计算总体威胁等级
        total_threat = sum(score for _, _, score in threats["immediate_threats"]) * 1.5
        total_threat += sum(score for _, _, score in threats["potential_threats"])
        
        threats["threat_level"] = min(total_threat, 1.0)
        
        return threats
    
    def _calculate_threat_score(self, zone_name: str, player: Player, 
                              game_state: GameState) -> float:
        """计算特定区域的威胁分数"""
        if zone_name not in GUA_64_INFO:
            return 0.0
        
        threat_score = 0.0
        gua_info = GUA_64_INFO[zone_name]
        
        # 基于卦象力量的威胁
        base_threat = len(gua_info.get("trigrams", [])) * 0.1
        threat_score += base_threat
        
        # 基于位置的威胁（如果靠近我方控制区域）
        my_zones = [z for z, data in game_state.board.gua_zones.items() 
                   if data.get("controller") == player.name]
        
        for my_zone in my_zones:
            relations = enhanced_hexagram_system.get_hexagram_relations(zone_name)
            for relation in relations:
                if relation.related == my_zone:
                    # 如果是相克关系，威胁更大
                    if "克" in relation.description:
                        threat_score += 0.3
                    elif "冲" in relation.description:
                        threat_score += 0.2
        
        return min(threat_score, 1.0)
    
    def _identify_opportunities(self, player: Player, game_state: GameState) -> List[Dict]:
        """识别战略机会"""
        opportunities = []
        
        # 寻找可以控制的中性区域
        for zone_name, zone_data in game_state.board.gua_zones.items():
            if not zone_data.get("controller"):
                opportunity_score = self._calculate_opportunity_score(zone_name, player, game_state)
                if opportunity_score > 0.3:
                    opportunities.append({
                        "zone": zone_name,
                        "type": "expansion",
                        "score": opportunity_score,
                        "description": f"控制{zone_name}可获得战略优势"
                    })
        
        # 寻找策略机会
        available_strategies = advanced_strategy_system.get_available_strategies(player, game_state)
        for strategy in available_strategies:
            strategy_score = self._evaluate_strategy_opportunity(strategy, player, game_state)
            if strategy_score > 0.4:
                opportunities.append({
                    "strategy": strategy,
                    "type": "strategy",
                    "score": strategy_score,
                    "description": f"使用{strategy.name}可获得优势"
                })
        
        # 按分数排序
        opportunities.sort(key=lambda x: x["score"], reverse=True)
        
        return opportunities[:5]  # 返回前5个机会
    
    def _calculate_opportunity_score(self, zone_name: str, player: Player, 
                                   game_state: GameState) -> float:
        """计算机会分数"""
        if zone_name not in GUA_64_INFO:
            return 0.0
        
        score = 0.0
        gua_info = GUA_64_INFO[zone_name]
        
        # 基础价值
        base_value = len(gua_info.get("trigrams", [])) * 0.1
        score += base_value
        
        # 与现有控制区域的协同价值
        my_zones = [z for z, data in game_state.board.gua_zones.items() 
                   if data.get("controller") == player.name]
        
        synergy_bonus = 0.0
        for my_zone in my_zones:
            relations = enhanced_hexagram_system.get_hexagram_relations(zone_name)
            for relation in relations:
                if relation.related == my_zone:
                    synergy_bonus += relation.strength * 0.2
        
        score += synergy_bonus
        
        # 五行平衡价值
        current_elements = set()
        for my_zone in my_zones:
            if my_zone in GUA_64_INFO:
                current_elements.add(GUA_64_INFO[my_zone].get("element", ""))
        
        zone_element = gua_info.get("element", "")
        if zone_element not in current_elements:
            score += 0.3  # 新元素奖励
        
        return min(score, 1.0)
    
    def _evaluate_strategy_opportunity(self, strategy: StrategyAction, 
                                     player: Player, game_state: GameState) -> float:
        """评估策略机会"""
        score = 0.0
        
        # 基于策略类型的基础分数
        type_scores = {
            StrategyType.TRANSFORMATION: 0.6,
            StrategyType.SYNERGY: 0.7,
            StrategyType.BALANCE: 0.5,
            StrategyType.TIMING: 0.8,
            StrategyType.ADAPTATION: 0.6
        }
        
        score += type_scores.get(strategy.strategy_type, 0.5)
        
        # 基于当前局势的适用性
        situation = self._analyze_game_situation(player, game_state)
        
        if strategy.strategy_type == StrategyType.TRANSFORMATION:
            # 如果控制多个卦象，变化策略更有价值
            if situation["territory_control"]["controlled_count"] >= 2:
                score += 0.2
        
        elif strategy.strategy_type == StrategyType.SYNERGY:
            # 如果有协同潜力，协同策略更有价值
            if situation["hexagram_synergies"]["potential"] > 0.5:
                score += 0.3
        
        elif strategy.strategy_type == StrategyType.BALANCE:
            # 如果阴阳失衡，平衡策略更有价值
            if situation["resource_status"]["balance_score"] < 0.6:
                score += 0.3
        
        # 基于历史成功率
        strategy_name = strategy.name
        if strategy_name in self.memory.successful_strategies:
            success_rate = (self.memory.successful_strategies[strategy_name] / 
                          max(self.memory.successful_strategies[strategy_name] + 
                              self.memory.failed_strategies.get(strategy_name, 0), 1))
            score += success_rate * 0.2
        
        return min(score, 1.0)
    
    def _analyze_hexagram_synergies(self, player: Player, game_state: GameState) -> Dict:
        """分析卦象协同效应"""
        my_zones = [z for z, data in game_state.board.gua_zones.items() 
                   if data.get("controller") == player.name]
        
        if len(my_zones) < 2:
            return {"potential": 0.0, "active_synergies": [], "recommendations": []}
        
        active_synergies = []
        total_potential = 0.0
        
        for i, zone1 in enumerate(my_zones):
            for zone2 in my_zones[i+1:]:
                synergy = enhanced_hexagram_system.calculate_synergy(zone1, zone2)
                if synergy["compatibility"] > 0.5:
                    active_synergies.append({
                        "zones": (zone1, zone2),
                        "strength": synergy["compatibility"],
                        "type": synergy["synergy_type"]
                    })
                    total_potential += synergy["compatibility"]
        
        average_potential = total_potential / max(len(my_zones) * (len(my_zones) - 1) / 2, 1)
        
        return {
            "potential": average_potential,
            "active_synergies": active_synergies,
            "recommendations": self._generate_synergy_recommendations(my_zones, game_state)
        }
    
    def _generate_synergy_recommendations(self, my_zones: List[str], 
                                        game_state: GameState) -> List[str]:
        """生成协同建议"""
        recommendations = []
        
        # 分析缺失的元素
        current_elements = set()
        for zone in my_zones:
            if zone in GUA_64_INFO:
                current_elements.add(GUA_64_INFO[zone].get("element", ""))
        
        all_elements = {"金", "木", "水", "火", "土"}
        missing_elements = all_elements - current_elements
        
        if missing_elements:
            recommendations.append(f"建议获取{', '.join(missing_elements)}属性的卦象以完善五行")
        
        # 分析阴阳平衡
        yin_count = yang_count = 0
        for zone in my_zones:
            if zone in GUA_64_INFO:
                trigrams = GUA_64_INFO[zone].get("trigrams", [])
                for trigram in trigrams:
                    # 简化的阴阳判断
                    if trigram in ["坤", "震", "坎", "艮"]:
                        yin_count += 1
                    else:
                        yang_count += 1
        
        if abs(yin_count - yang_count) > 2:
            if yin_count > yang_count:
                recommendations.append("建议获取更多阳性卦象以平衡阴阳")
            else:
                recommendations.append("建议获取更多阴性卦象以平衡阴阳")
        
        return recommendations
    
    def _determine_game_phase(self, game_state: GameState) -> str:
        """判断游戏阶段"""
        total_controlled = sum(1 for data in game_state.board.gua_zones.values() 
                             if data.get("controller"))
        total_zones = len(game_state.board.gua_zones)
        control_ratio = total_controlled / max(total_zones, 1)
        
        if control_ratio < 0.3:
            return "early"  # 早期
        elif control_ratio < 0.7:
            return "middle"  # 中期
        else:
            return "late"  # 后期
    
    def _get_available_actions(self, player: Player, game_state: GameState) -> List[str]:
        """获取可用行动"""
        actions = []
        
        # 基础行动
        actions.extend(["explore", "meditate", "study"])
        
        # 策略行动
        available_strategies = advanced_strategy_system.get_available_strategies(player, game_state)
        for strategy in available_strategies:
            actions.append(f"strategy:{strategy.name}")
        
        # 区域行动
        for zone_name, zone_data in game_state.board.gua_zones.items():
            if not zone_data.get("controller"):
                actions.append(f"claim:{zone_name}")
        
        return actions
    
    def _select_best_action(self, player: Player, game_state: GameState, 
                          available_actions: List[str], situation_analysis: Dict) -> str:
        """选择最佳行动"""
        if not available_actions:
            return "meditate"  # 默认行动
        
        action_scores = {}
        
        for action in available_actions:
            score = self._evaluate_action(action, player, game_state, situation_analysis)
            action_scores[action] = score
        
        # 添加探索因子
        if random.random() < self.exploration_rate:
            # 随机选择一个行动进行探索
            return random.choice(available_actions)
        
        # 选择最高分的行动
        best_action = max(action_scores.items(), key=lambda x: x[1])[0]
        
        return best_action
    
    def _evaluate_action(self, action: str, player: Player, game_state: GameState, 
                        situation_analysis: Dict) -> float:
        """评估行动价值"""
        base_score = 0.5
        
        if action.startswith("strategy:"):
            strategy_name = action.split(":", 1)[1]
            # 基于策略机会评估
            for opportunity in situation_analysis["strategic_opportunities"]:
                if (opportunity.get("type") == "strategy" and 
                    opportunity.get("strategy", {}).get("name") == strategy_name):
                    base_score = opportunity["score"]
                    break
        
        elif action.startswith("claim:"):
            zone_name = action.split(":", 1)[1]
            base_score = self._calculate_opportunity_score(zone_name, player, game_state)
        
        elif action == "explore":
            # 探索在早期更有价值
            if situation_analysis["game_phase"] == "early":
                base_score = 0.7
            else:
                base_score = 0.3
        
        elif action == "meditate":
            # 冥想在资源不足时更有价值
            if situation_analysis["resource_status"]["total"] < 10:
                base_score = 0.6
            else:
                base_score = 0.4
        
        elif action == "study":
            # 学习在中期更有价值
            if situation_analysis["game_phase"] == "middle":
                base_score = 0.6
            else:
                base_score = 0.4
        
        # 根据性格调整分数
        base_score = self._adjust_score_by_personality(action, base_score, situation_analysis)
        
        return base_score
    
    def _adjust_score_by_personality(self, action: str, base_score: float, 
                                   situation_analysis: Dict) -> float:
        """根据性格调整分数"""
        if self.personality == AIPersonality.AGGRESSIVE:
            if action.startswith("claim:") or action.startswith("strategy:"):
                base_score *= 1.2
            elif action == "meditate":
                base_score *= 0.8
        
        elif self.personality == AIPersonality.DEFENSIVE:
            if action == "meditate" or action == "study":
                base_score *= 1.2
            elif action.startswith("claim:"):
                # 只在安全时扩张
                if situation_analysis["opponent_threat"]["threat_level"] < 0.3:
                    base_score *= 1.1
                else:
                    base_score *= 0.7
        
        elif self.personality == AIPersonality.STRATEGIC:
            if action.startswith("strategy:"):
                base_score *= 1.3
            elif action == "study":
                base_score *= 1.1
        
        elif self.personality == AIPersonality.ADAPTIVE:
            # 适应型根据当前局势动态调整
            if situation_analysis["game_phase"] == "early":
                if action == "explore":
                    base_score *= 1.2
            elif situation_analysis["game_phase"] == "late":
                if action.startswith("strategy:"):
                    base_score *= 1.3
        
        return base_score
    
    def _update_goals(self, player: Player, game_state: GameState, situation_analysis: Dict):
        """更新AI目标"""
        # 清除已完成的目标
        self.current_goals = [goal for goal in self.current_goals if goal.progress < 1.0]
        
        # 根据局势添加新目标
        if situation_analysis["game_phase"] == "early":
            if not any(goal.name == "early_expansion" for goal in self.current_goals):
                self.current_goals.append(AIGoal(
                    name="early_expansion",
                    priority=0.8,
                    conditions=["控制至少3个区域"],
                    actions=["explore", "claim"]
                ))
        
        elif situation_analysis["game_phase"] == "middle":
            if not any(goal.name == "synergy_building" for goal in self.current_goals):
                self.current_goals.append(AIGoal(
                    name="synergy_building",
                    priority=0.9,
                    conditions=["建立卦象协同效应"],
                    actions=["strategy:elemental_synergy", "strategy:yin_yang_unity"]
                ))
        
        # 根据威胁等级添加防御目标
        if situation_analysis["opponent_threat"]["threat_level"] > 0.6:
            if not any(goal.name == "defensive_response" for goal in self.current_goals):
                self.current_goals.append(AIGoal(
                    name="defensive_response",
                    priority=1.0,
                    conditions=["降低威胁等级"],
                    actions=["strategy:cosmic_balance", "meditate"]
                ))
    
    def _update_memory(self, player: Player, game_state: GameState, chosen_action: str):
        """更新AI记忆"""
        # 记录当前游戏状态评估
        current_evaluation = self._evaluate_current_position(player, game_state)
        self.memory.game_state_evaluations.append(current_evaluation)
        
        # 保持记忆大小限制
        if len(self.memory.game_state_evaluations) > 100:
            self.memory.game_state_evaluations = self.memory.game_state_evaluations[-50:]
        
        # 更新卦象偏好
        my_zones = [z for z, data in game_state.board.gua_zones.items() 
                   if data.get("controller") == player.name]
        
        for zone in my_zones:
            if zone not in self.memory.hexagram_preferences:
                self.memory.hexagram_preferences[zone] = 0.5
            
            # 基于当前表现调整偏好
            if current_evaluation > 0.6:
                self.memory.hexagram_preferences[zone] += self.learning_rate * 0.1
            elif current_evaluation < 0.4:
                self.memory.hexagram_preferences[zone] -= self.learning_rate * 0.1
            
            # 限制偏好值范围
            self.memory.hexagram_preferences[zone] = max(0.0, min(1.0, 
                self.memory.hexagram_preferences[zone]))
    
    def _evaluate_current_position(self, player: Player, game_state: GameState) -> float:
        """评估当前位置优势"""
        score = 0.0
        
        # 资源评估
        total_resources = player.qi + player.dao_xing + player.cheng_yi
        score += min(total_resources / 30.0, 0.3)  # 最多30%来自资源
        
        # 领土控制评估
        controlled_count = sum(1 for data in game_state.board.gua_zones.values() 
                             if data.get("controller") == player.name)
        total_zones = len(game_state.board.gua_zones)
        control_ratio = controlled_count / max(total_zones, 1)
        score += control_ratio * 0.4  # 最多40%来自领土控制
        
        # 阴阳平衡评估
        balance_score = 1.0 - abs(player.yin_yang_balance - 0.5) * 2
        score += balance_score * 0.2  # 最多20%来自平衡
        
        # 协同效应评估
        synergy_analysis = self._analyze_hexagram_synergies(player, game_state)
        score += synergy_analysis["potential"] * 0.1  # 最多10%来自协同
        
        return min(score, 1.0)
    
    def get_ai_status_report(self, player: Player, game_state: GameState) -> str:
        """获取AI状态报告"""
        situation = self._analyze_game_situation(player, game_state)
        
        report = f"\n=== {self.name} ({self.personality.value}) 状态报告 ===\n"
        report += f"当前评估: {self._evaluate_current_position(player, game_state):.2f}\n"
        report += f"游戏阶段: {situation['game_phase']}\n"
        report += f"威胁等级: {situation['opponent_threat']['threat_level']:.2f}\n"
        report += f"协同潜力: {situation['hexagram_synergies']['potential']:.2f}\n"
        
        if self.current_goals:
            report += "当前目标:\n"
            for goal in self.current_goals[:3]:
                report += f"  - {goal.name} (优先级: {goal.priority:.1f})\n"
        
        return report

# 创建不同性格的AI玩家实例
def create_ai_players() -> Dict[str, EnhancedAIPlayer]:
    """创建不同性格的AI玩家"""
    return {
        "智者": EnhancedAIPlayer("智者", AIPersonality.STRATEGIC),
        "勇者": EnhancedAIPlayer("勇者", AIPersonality.AGGRESSIVE),
        "守护者": EnhancedAIPlayer("守护者", AIPersonality.DEFENSIVE),
        "平衡者": EnhancedAIPlayer("平衡者", AIPersonality.BALANCED),
        "变化者": EnhancedAIPlayer("变化者", AIPersonality.ADAPTIVE)
    }

if __name__ == "__main__":
    # 测试AI玩家系统
    print("=== 增强AI玩家系统测试 ===")
    
    ai_players = create_ai_players()
    for name, ai_player in ai_players.items():
        print(f"{name}: {ai_player.personality.value}")
        print(f"  决策权重: {ai_player.decision_weights}")
        print()