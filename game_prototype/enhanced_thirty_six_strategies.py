"""
增强版三十六计系统 - Enhanced Thirty-Six Strategies System
集成信息战系统、势力根基系统和动态局势系统
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple, Any
from enum import Enum
import random
from datetime import datetime

# 导入新系统
from information_warfare_system import InformationWarfareSystem, InformationType, InformationReliability
from influence_foundation_system import InfluenceFoundationSystem, FoundationType, InfluenceLevel
from dynamic_situation_system import DynamicSituationSystem, SituationType, TimingQuality
from thirty_six_strategies_system import (
    StrategyType, StrategyCategory, ThirtySixStrategy, StrategyState, ThirtySixStrategiesSystem
)

@dataclass
class EnhancedStrategyCondition:
    """增强策略条件"""
    basic_conditions: List[str]
    information_requirements: Optional[Dict[str, Any]] = None
    foundation_requirements: Optional[Dict[str, Any]] = None
    situation_requirements: Optional[Dict[str, Any]] = None
    timing_requirements: Optional[TimingQuality] = None

@dataclass
class EnhancedStrategyEffect:
    """增强策略效果"""
    basic_effects: List[str]
    information_effects: Optional[Dict[str, Any]] = None
    foundation_effects: Optional[Dict[str, Any]] = None
    situation_effects: Optional[Dict[str, Any]] = None
    timing_bonus: float = 1.0

class EnhancedThirtySixStrategiesSystem:
    """增强版三十六计系统"""
    
    def __init__(self):
        # 基础系统
        self.base_system = ThirtySixStrategiesSystem()
        
        # 新增系统
        self.info_warfare = InformationWarfareSystem()
        self.foundation_system = InfluenceFoundationSystem()
        self.situation_system = DynamicSituationSystem()
        
        # 增强策略定义
        self.enhanced_conditions: Dict[StrategyType, EnhancedStrategyCondition] = {}
        self.enhanced_effects: Dict[StrategyType, EnhancedStrategyEffect] = {}
        
        self._initialize_enhanced_strategies()
    
    def _initialize_enhanced_strategies(self):
        """初始化增强策略"""
        
        # 胜战计增强
        self.enhanced_conditions[StrategyType.MAN_TIAN_GUO_HAI] = EnhancedStrategyCondition(
            basic_conditions=["拥有隐蔽能力", "对手注意力分散"],
            information_requirements={"false_info_planted": 1, "target_attention_diverted": True},
            timing_requirements=TimingQuality.GOOD
        )
        
        self.enhanced_effects[StrategyType.MAN_TIAN_GUO_HAI] = EnhancedStrategyEffect(
            basic_effects=["隐藏真实意图3回合", "下次行动成功率+30%"],
            information_effects={"plant_false_info": 2, "hide_true_intentions": 3}
        )
        
        self.enhanced_conditions[StrategyType.WEI_WEI_JIU_ZHAO] = EnhancedStrategyCondition(
            basic_conditions=["存在多个对手", "拥有机动能力"],
            foundation_requirements={"min_influence_level": InfluenceLevel.MODERATE},
            situation_requirements={"min_tension": 40}
        )
        
        self.enhanced_effects[StrategyType.WEI_WEI_JIU_ZHAO] = EnhancedStrategyEffect(
            basic_effects=["迫使对手改变目标", "获得战略主动权"],
            foundation_effects={"redirect_enemy_focus": True, "gain_initiative": 2}
        )
        
        self.enhanced_conditions[StrategyType.JIE_DAO_SHA_REN] = EnhancedStrategyCondition(
            basic_conditions=["存在第三方势力", "能够影响第三方"],
            foundation_requirements={"third_party_influence": InfluenceLevel.WEAK},
            information_requirements={"third_party_intel": InformationReliability.RELIABLE}
        )
        
        self.enhanced_effects[StrategyType.JIE_DAO_SHA_REN] = EnhancedStrategyEffect(
            basic_effects=["让第三方攻击目标", "自身不承担风险"],
            foundation_effects={"manipulate_third_party": True},
            information_effects={"gather_conflict_intel": 2}
        )
        
        self.enhanced_conditions[StrategyType.YI_YI_DAI_LAO] = EnhancedStrategyCondition(
            basic_conditions=["拥有防御优势", "对手处于攻势"],
            situation_requirements={"situation_type": [SituationType.TENSE, SituationType.STALEMATE]},
            timing_requirements=TimingQuality.GOOD
        )
        
        self.enhanced_effects[StrategyType.YI_YI_DAI_LAO] = EnhancedStrategyEffect(
            basic_effects=["恢复资源", "对手消耗增加50%"],
            situation_effects={"patience_bonus": 2, "enemy_exhaustion": 1.5}
        )
        
        self.enhanced_conditions[StrategyType.CHEN_HUO_DA_JIE] = EnhancedStrategyCondition(
            basic_conditions=["对手处于困境", "拥有攻击能力"],
            situation_requirements={"situation_type": [SituationType.CHAOTIC, SituationType.CRISIS]},
            timing_requirements=TimingQuality.EXCELLENT
        )
        
        self.enhanced_effects[StrategyType.CHEN_HUO_DA_JIE] = EnhancedStrategyEffect(
            basic_effects=["攻击效果翻倍", "获得额外资源"],
            situation_effects={"chaos_exploitation": 3, "resource_bonus": 2}
        )
        
        self.enhanced_conditions[StrategyType.SHENG_DONG_JI_XI] = EnhancedStrategyCondition(
            basic_conditions=["拥有多个行动选项", "对手注意力分散"],
            information_requirements={"misdirection_capability": True},
            timing_requirements=TimingQuality.GOOD
        )
        
        self.enhanced_effects[StrategyType.SHENG_DONG_JI_XI] = EnhancedStrategyEffect(
            basic_effects=["真实目标成功率+40%", "对手防御-20%"],
            information_effects={"create_misdirection": 2, "confuse_enemy": 1}
        )
        
        # 敌战计增强
        self.enhanced_conditions[StrategyType.WU_ZHONG_SHENG_YOU] = EnhancedStrategyCondition(
            basic_conditions=["拥有创造能力", "对手信息不足"],
            information_requirements={"false_info_creation": True, "enemy_intel_gap": True}
        )
        
        self.enhanced_effects[StrategyType.WU_ZHONG_SHENG_YOU] = EnhancedStrategyEffect(
            basic_effects=["创造虚假威胁", "获得心理优势"],
            information_effects={"create_false_threat": 3, "psychological_advantage": 2}
        )
        
        self.enhanced_conditions[StrategyType.AN_DU_CHEN_CANG] = EnhancedStrategyCondition(
            basic_conditions=["拥有隐蔽行动能力", "对手被表面行动吸引"],
            information_requirements={"stealth_capability": True, "distraction_active": True}
        )
        
        self.enhanced_effects[StrategyType.AN_DU_CHEN_CANG] = EnhancedStrategyEffect(
            basic_effects=["隐蔽行动成功率+50%", "获得战略突破"],
            information_effects={"stealth_bonus": 2, "strategic_breakthrough": True}
        )
        
        self.enhanced_conditions[StrategyType.GE_AN_GUAN_HUO] = EnhancedStrategyCondition(
            basic_conditions=["存在多方冲突", "自身保持中立"],
            situation_requirements={"situation_type": [SituationType.CHAOTIC, SituationType.CRISIS]},
            information_requirements={"conflict_intelligence": InformationReliability.RELIABLE}
        )
        
        self.enhanced_effects[StrategyType.GE_AN_GUAN_HUO] = EnhancedStrategyEffect(
            basic_effects=["避免损失", "等待最佳时机"],
            situation_effects={"observation_bonus": 3, "timing_advantage": 2},
            information_effects={"gather_conflict_intel": 2}
        )
        
        # 攻战计增强
        self.enhanced_conditions[StrategyType.FU_DI_CHOU_XIN] = EnhancedStrategyCondition(
            basic_conditions=["识别对手根基", "拥有破坏能力"],
            foundation_requirements={"target_foundation_identified": True, "destruction_capability": True}
        )
        
        self.enhanced_effects[StrategyType.FU_DI_CHOU_XIN] = EnhancedStrategyEffect(
            basic_effects=["摧毁对手根基", "从根本上削弱敌人"],
            foundation_effects={"destroy_foundation": True, "weaken_influence": 3}
        )
        
        self.enhanced_conditions[StrategyType.PAO_ZHUAN_YIN_YU] = EnhancedStrategyCondition(
            basic_conditions=["拥有诱饵", "对手有贪欲"],
            foundation_requirements={"bait_foundation": FoundationType.ECONOMIC},
            information_requirements={"enemy_desires_known": True}
        )
        
        self.enhanced_effects[StrategyType.PAO_ZHUAN_YIN_YU] = EnhancedStrategyEffect(
            basic_effects=["引诱对手", "获得更大利益"],
            foundation_effects={"establish_trap_foundation": True},
            information_effects={"gather_enemy_intel": 2}
        )
        
        # 混战计增强
        self.enhanced_conditions[StrategyType.HUN_SHUI_MO_YU] = EnhancedStrategyCondition(
            basic_conditions=["局势混乱", "拥有机动能力"],
            situation_requirements={"situation_type": [SituationType.CHAOTIC]},
            timing_requirements=TimingQuality.EXCELLENT
        )
        
        self.enhanced_effects[StrategyType.HUN_SHUI_MO_YU] = EnhancedStrategyEffect(
            basic_effects=["在混乱中获利", "避免直接冲突"],
            situation_effects={"chaos_exploitation": 4, "stealth_bonus": 2}
        )
        
        self.enhanced_conditions[StrategyType.JIN_CHAN_TUO_QIAO] = EnhancedStrategyCondition(
            basic_conditions=["需要脱身", "拥有替身或掩护"],
            situation_requirements={"situation_type": [SituationType.CRISIS]},
            information_requirements={"deception_capability": True}
        )
        
        self.enhanced_effects[StrategyType.JIN_CHAN_TUO_QIAO] = EnhancedStrategyEffect(
            basic_effects=["安全撤退", "保存实力"],
            situation_effects={"escape_bonus": 4, "preservation": 3},
            information_effects={"create_deception": 2}
        )
        
        self.enhanced_conditions[StrategyType.YUAN_JIAO_JIN_GONG] = EnhancedStrategyCondition(
            basic_conditions=["存在远近不同势力", "拥有外交能力"],
            foundation_requirements={"diplomatic_foundation": FoundationType.DIPLOMATIC},
            information_requirements={"distant_ally_intel": InformationReliability.RELIABLE}
        )
        
        self.enhanced_effects[StrategyType.YUAN_JIAO_JIN_GONG] = EnhancedStrategyEffect(
            basic_effects=["获得远方盟友", "孤立近敌"],
            foundation_effects={"establish_distant_alliance": True, "isolate_near_enemy": True}
        )
        
        # 并战计增强
        self.enhanced_conditions[StrategyType.TOU_LIANG_HUAN_ZHU] = EnhancedStrategyCondition(
            basic_conditions=["能够替换关键要素", "对手依赖某些支撑"],
            foundation_requirements={"target_support_identified": True},
            information_requirements={"replacement_capability": True}
        )
        
        self.enhanced_effects[StrategyType.TOU_LIANG_HUAN_ZHU] = EnhancedStrategyEffect(
            basic_effects=["暗中改变局势", "对手失去支撑"],
            foundation_effects={"replace_key_support": True, "undermine_stability": 3}
        )
        
        self.enhanced_conditions[StrategyType.MEI_REN_JI] = EnhancedStrategyCondition(
            basic_conditions=["拥有魅力或诱惑能力", "对手有弱点"],
            information_requirements={"target_weakness_known": True, "charm_capability": True},
            foundation_requirements={"social_foundation": FoundationType.CULTURAL}
        )
        
        self.enhanced_effects[StrategyType.MEI_REN_JI] = EnhancedStrategyEffect(
            basic_effects=["诱惑对手", "获得内部信息"],
            information_effects={"seduce_target": True, "gain_insider_info": 3},
            foundation_effects={"establish_personal_influence": True}
        )
        
        # 败战计增强
        self.enhanced_conditions[StrategyType.KONG_CHENG_JI] = EnhancedStrategyCondition(
            basic_conditions=["处于劣势", "对手不了解真实情况"],
            information_requirements={"enemy_intel_limited": True, "bluff_capability": True},
            situation_requirements={"desperation_level": "high"}
        )
        
        self.enhanced_effects[StrategyType.KONG_CHENG_JI] = EnhancedStrategyEffect(
            basic_effects=["威慑对手", "争取时间"],
            information_effects={"create_false_strength": 3, "psychological_warfare": 2}
        )
        
        self.enhanced_conditions[StrategyType.ZOU_WEI_SHANG] = EnhancedStrategyCondition(
            basic_conditions=["无法获胜", "拥有撤退能力"],
            situation_requirements={"situation_trend": "declining"},
            timing_requirements=TimingQuality.EXCELLENT
        )
        
        self.enhanced_effects[StrategyType.ZOU_WEI_SHANG] = EnhancedStrategyEffect(
            basic_effects=["安全撤退", "保存实力"],
            situation_effects={"strategic_withdrawal": 5, "force_preservation": 4},
            foundation_effects={"preserve_core_foundations": True}
        )
    
    def register_player(self, player_id: str):
        """注册玩家到所有系统"""
        self.base_system.player_states[player_id] = StrategyState([], {}, [], {})
        self.info_warfare.register_player(player_id)
        self.foundation_system.register_player(player_id)
    
    def get_enhanced_available_strategies(self, player_id: str, game_state: Dict[str, Any]) -> List[StrategyType]:
        """获取增强版可用策略"""
        # 更新局势
        self.situation_system.update_situation()
        
        # 获取基础可用策略
        base_available = self.base_system.get_available_strategies(player_id, game_state)
        
        # 进一步筛选基于增强条件
        enhanced_available = []
        
        for strategy_type in base_available:
            if self._check_enhanced_conditions(strategy_type, player_id, game_state):
                enhanced_available.append(strategy_type)
        
        return enhanced_available
    
    def _check_enhanced_conditions(self, strategy_type: StrategyType, player_id: str, game_state: Dict[str, Any]) -> bool:
        """检查增强条件"""
        if strategy_type not in self.enhanced_conditions:
            return True  # 没有增强条件的策略默认可用
        
        conditions = self.enhanced_conditions[strategy_type]
        
        # 检查信息战条件
        if conditions.information_requirements:
            if not self._check_information_requirements(conditions.information_requirements, player_id):
                return False
        
        # 检查势力根基条件
        if conditions.foundation_requirements:
            if not self._check_foundation_requirements(conditions.foundation_requirements, player_id):
                return False
        
        # 检查局势条件
        if conditions.situation_requirements:
            if not self._check_situation_requirements(conditions.situation_requirements):
                return False
        
        # 检查时机条件
        if conditions.timing_requirements:
            strategy_name = self.base_system.strategies[strategy_type].name
            current_timing = self.situation_system.get_timing_quality(strategy_name)
            if current_timing.value < conditions.timing_requirements.value:
                return False
        
        return True
    
    def _check_information_requirements(self, requirements: Dict[str, Any], player_id: str) -> bool:
        """检查信息战要求"""
        player_intel = self.info_warfare.player_intelligence.get(player_id)
        if not player_intel:
            return False
        
        for req_key, req_value in requirements.items():
            if req_key == "false_info_planted":
                # 获取所有信息片段
                all_info = []
                for target_infos in player_intel.known_information.values():
                    all_info.extend(target_infos)
                
                false_info_count = len([info for info in all_info 
                                      if hasattr(info, 'reliability') and info.reliability == InformationReliability.FALSE])
                if false_info_count < req_value:
                    return False
            elif req_key == "enemy_intel_gap":
                # 检查是否有足够的敌方信息缺口
                total_info_count = sum(len(infos) for infos in player_intel.known_information.values())
                if total_info_count < 3:  # 简化检查
                    return False
            # 可以添加更多信息战条件检查
        
        return True
    
    def _check_foundation_requirements(self, requirements: Dict[str, Any], player_id: str) -> bool:
        """检查势力根基要求"""
        player_network = self.foundation_system.player_networks.get(player_id)
        if not player_network:
            return False
        
        for req_key, req_value in requirements.items():
            if req_key == "min_influence_level":
                max_influence = max([node.influence_level.value for node in player_network.nodes.values()], 
                                  default=0)
                if max_influence < req_value.value:
                    return False
            elif req_key == "diplomatic_foundation":
                if not any(node.foundation_type == req_value for node in player_network.nodes.values()):
                    return False
            # 可以添加更多根基条件检查
        
        return True
    
    def _check_situation_requirements(self, requirements: Dict[str, Any]) -> bool:
        """检查局势要求"""
        current_situation = self.situation_system.get_current_situation()
        
        for req_key, req_value in requirements.items():
            if req_key == "situation_type":
                if current_situation.situation_type not in req_value:
                    return False
            elif req_key == "min_tension":
                if current_situation.tension_level < req_value:
                    return False
            elif req_key == "situation_trend":
                trend = self.situation_system.predict_situation_trend()
                if req_value == "declining" and trend.value >= 0:
                    return False
            # 可以添加更多局势条件检查
        
        return True
    
    def execute_enhanced_strategy(self, player_id: str, strategy_type: StrategyType, 
                                target_player: str = None, **kwargs) -> Dict[str, Any]:
        """执行增强策略"""
        # 检查策略是否可用
        available_strategies = self.get_enhanced_available_strategies(player_id, kwargs.get('game_state', {}))
        if strategy_type not in available_strategies:
            return {"success": False, "message": "策略当前不可用"}
        
        # 获取时机质量加成
        strategy_name = self.base_system.strategies[strategy_type].name
        timing_quality = self.situation_system.get_timing_quality(strategy_name)
        timing_bonus = timing_quality.value / 3.0  # 时机质量转换为加成
        
        # 执行基础策略
        base_result = self.base_system.execute_strategy(player_id, strategy_type, target_player, 
                                                       kwargs.get('game_state', {}))
        
        if not base_result.get("success", False):
            return base_result
        
        # 应用增强效果
        enhanced_effects = self._apply_enhanced_effects(strategy_type, player_id, target_player, timing_bonus, **kwargs)
        
        # 合并结果
        result = base_result.copy()
        result["enhanced_effects"] = enhanced_effects
        result["timing_bonus"] = timing_bonus
        result["timing_quality"] = timing_quality.name
        
        return result
    
    def _apply_enhanced_effects(self, strategy_type: StrategyType, player_id: str, 
                              target_player: str, timing_bonus: float, **kwargs) -> Dict[str, Any]:
        """应用增强效果"""
        if strategy_type not in self.enhanced_effects:
            return {}
        
        effects = self.enhanced_effects[strategy_type]
        applied_effects = {}
        
        # 应用信息战效果
        if effects.information_effects:
            info_effects = self._apply_information_effects(effects.information_effects, player_id, target_player)
            applied_effects["information"] = info_effects
        
        # 应用势力根基效果
        if effects.foundation_effects:
            foundation_effects = self._apply_foundation_effects(effects.foundation_effects, player_id, target_player)
            applied_effects["foundation"] = foundation_effects
        
        # 应用局势效果
        if effects.situation_effects:
            situation_effects = self._apply_situation_effects(effects.situation_effects, player_id, timing_bonus)
            applied_effects["situation"] = situation_effects
        
        return applied_effects
    
    def _apply_information_effects(self, effects: Dict[str, Any], player_id: str, target_player: str) -> Dict[str, Any]:
        """应用信息战效果"""
        results = {}
        
        for effect_type, effect_value in effects.items():
            if effect_type == "plant_false_info":
                for _ in range(effect_value):
                    result = self.info_warfare.plant_false_information(
                        player_id, target_player, InformationType.STRATEGIC, "虚假战略信息"
                    )
                    results[f"false_info_{_}"] = result
            
            elif effect_type == "gather_conflict_intel":
                for _ in range(effect_value):
                    result = self.info_warfare.collect_information(
                        player_id, InformationType.TACTICAL, f"冲突情报_{_}"
                    )
                    results[f"intel_{_}"] = result
            
            elif effect_type == "create_false_threat":
                result = self.info_warfare.plant_false_information(
                    player_id, target_player, InformationType.THREAT, "虚假威胁"
                )
                results["false_threat"] = result
        
        return results
    
    def _apply_foundation_effects(self, effects: Dict[str, Any], player_id: str, target_player: str) -> Dict[str, Any]:
        """应用势力根基效果"""
        results = {}
        
        for effect_type, effect_value in effects.items():
            if effect_type == "destroy_foundation":
                result = self.foundation_system.attack_foundation(player_id, target_player, "economic_base")
                results["foundation_attack"] = result
            
            elif effect_type == "establish_distant_alliance":
                result = self.foundation_system.establish_foundation(
                    player_id, "distant_ally", FoundationType.DIPLOMATIC
                )
                results["distant_alliance"] = result
            
            elif effect_type == "weaken_influence":
                # 削弱目标影响力
                results["influence_weakening"] = {"target": target_player, "amount": effect_value}
        
        return results
    
    def _apply_situation_effects(self, effects: Dict[str, Any], player_id: str, timing_bonus: float) -> Dict[str, Any]:
        """应用局势效果"""
        results = {}
        
        for effect_type, effect_value in effects.items():
            if effect_type == "chaos_exploitation":
                # 在混乱中获得额外收益
                bonus = effect_value * timing_bonus
                results["chaos_bonus"] = bonus
            
            elif effect_type == "strategic_withdrawal":
                # 战略撤退效果
                result = self.situation_system.execute_situation_strategy("走为上计", player_id)
                results["withdrawal"] = result
            
            elif effect_type == "observation_bonus":
                # 观察加成
                result = self.situation_system.execute_situation_strategy("隔岸观火", player_id)
                results["observation"] = result
        
        return results
    
    def get_strategy_analysis(self, player_id: str, strategy_type: StrategyType) -> Dict[str, Any]:
        """获取策略分析"""
        strategy = self.base_system.strategies[strategy_type]
        strategy_name = strategy.name
        
        # 获取时机分析
        timing_quality = self.situation_system.get_timing_quality(strategy_name)
        current_situation = self.situation_system.get_current_situation()
        
        # 获取条件满足情况
        conditions_met = self._check_enhanced_conditions(strategy_type, player_id, {})
        
        # 获取预期效果
        enhanced_effects = self.enhanced_effects.get(strategy_type)
        
        return {
            "strategy_name": strategy_name,
            "category": strategy.category.value,
            "timing_quality": timing_quality.name,
            "timing_score": timing_quality.value,
            "current_situation": current_situation.situation_type.value,
            "conditions_met": conditions_met,
            "base_success_rate": strategy.success_rate,
            "enhanced_success_rate": strategy.success_rate * (timing_quality.value / 3.0),
            "enhanced_effects_available": enhanced_effects is not None,
            "cost": strategy.cost,
            "cooldown": strategy.cooldown,
            "yijing_basis": strategy.yijing_basis
        }
    
    def get_system_status(self, player_id: str) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            "information_warfare": self.info_warfare.get_player_intelligence_summary(player_id),
            "foundation_system": self.foundation_system.get_network_summary(player_id),
            "situation_system": self.situation_system.get_situation_summary(),
            "available_strategies": len(self.get_enhanced_available_strategies(player_id, {})),
            "total_strategies": len(self.base_system.strategies)
        }