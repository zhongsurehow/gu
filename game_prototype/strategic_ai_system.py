"""
战略AI系统 - 集成三十六计的智能AI
实现基于三十六计的高级AI决策系统
"""

from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass, field
from enum import Enum
import random
import math

from thirty_six_strategies_system import (
    ThirtySixStrategiesSystem, StrategyCategory, StrategyType,
    ThirtySixStrategy, StrategyState
)
from deception_system import DeceptionSystem, InformationType, DeceptionLevel
from enhanced_alliance_system import EnhancedAllianceSystem, AllianceType

class AIStrategicLevel(Enum):
    """AI战略等级"""
    NOVICE = "新手"      # 基础策略
    INTERMEDIATE = "中级"  # 组合策略
    ADVANCED = "高级"     # 复杂计谋
    MASTER = "大师"       # 三十六计融会贯通

class StrategicContext(Enum):
    """战略环境"""
    ADVANTAGE = "优势"    # 领先状态
    DISADVANTAGE = "劣势"  # 落后状态
    BALANCED = "均势"     # 势均力敌
    CHAOS = "混乱"        # 多方混战
    ENDGAME = "终局"      # 游戏后期

@dataclass
class StrategicPlan:
    """战略计划"""
    plan_id: str
    primary_strategy: StrategyType
    supporting_strategies: List[StrategyType]
    target_players: Set[str]
    expected_outcome: str
    confidence: float
    execution_steps: List[str]
    contingency_plans: List[str] = field(default_factory=list)

@dataclass
class AIStrategicMemory:
    """AI战略记忆"""
    successful_strategies: Dict[StrategyType, int] = field(default_factory=dict)
    failed_strategies: Dict[StrategyType, int] = field(default_factory=dict)
    opponent_vulnerabilities: Dict[str, List[StrategyType]] = field(default_factory=dict)
    strategy_combinations: Dict[Tuple[StrategyType, ...], float] = field(default_factory=dict)
    context_preferences: Dict[StrategicContext, List[StrategyType]] = field(default_factory=dict)

class StrategicAISystem:
    """战略AI系统"""
    
    def __init__(self, ai_name: str, strategic_level: AIStrategicLevel = AIStrategicLevel.INTERMEDIATE):
        self.ai_name = ai_name
        self.strategic_level = strategic_level
        self.memory = AIStrategicMemory()
        self.current_plans: List[StrategicPlan] = []
        self.active_strategies: Set[StrategyType] = set()
        
        # 系统集成
        self.strategy_system = ThirtySixStrategiesSystem()
        self.deception_system = DeceptionSystem()
        self.alliance_system = EnhancedAllianceSystem()
        
        # 初始化战略偏好
        self._initialize_strategic_preferences()
    
    def _initialize_strategic_preferences(self):
        """初始化战略偏好"""
        if self.strategic_level == AIStrategicLevel.NOVICE:
            # 新手偏好简单直接的策略
            preferred_strategies = [
                StrategyType.MING_XIU_ZHAN_DAO,  # 明修栈道
                StrategyType.SHENG_DONG_JI_XI,   # 声东击西
                StrategyType.JIE_DAO_SHA_REN     # 借刀杀人
            ]
        elif self.strategic_level == AIStrategicLevel.INTERMEDIATE:
            # 中级偏好组合策略
            preferred_strategies = [
                StrategyType.AN_DU_CHEN_CANG,    # 暗度陈仓
                StrategyType.DIAO_HU_LI_SHAN,    # 调虎离山
                StrategyType.LI_DAI_TAO_JIANG,   # 李代桃僵
                StrategyType.QIN_ZEI_QIN_WANG    # 擒贼擒王
            ]
        elif self.strategic_level == AIStrategicLevel.ADVANCED:
            # 高级偏好复杂计谋
            preferred_strategies = [
                StrategyType.LIAN_HUAN_JI,       # 连环计
                StrategyType.FAN_JIAN_JI,        # 反间计
                StrategyType.KU_ROU_JI,          # 苦肉计
                StrategyType.KONG_CHENG_JI       # 空城计
            ]
        else:  # MASTER
            # 大师级使用所有策略
            preferred_strategies = list(StrategyType)
        
        # 初始化偏好权重
        for strategy in preferred_strategies:
            self.memory.successful_strategies[strategy] = 1
    
    def analyze_game_situation(self, game_state: Dict[str, Any]) -> StrategicContext:
        """分析游戏局势"""
        player_scores = game_state.get("player_scores", {})
        my_score = player_scores.get(self.ai_name, 0)
        other_scores = [score for player, score in player_scores.items() if player != self.ai_name]
        
        if not other_scores:
            return StrategicContext.BALANCED
        
        avg_other_score = sum(other_scores) / len(other_scores)
        max_other_score = max(other_scores)
        
        # 判断局势
        if my_score > max_other_score * 1.2:
            return StrategicContext.ADVANTAGE
        elif my_score < avg_other_score * 0.8:
            return StrategicContext.DISADVANTAGE
        elif len(player_scores) > 3 and max(other_scores) - min(other_scores) > avg_other_score * 0.5:
            return StrategicContext.CHAOS
        elif game_state.get("turn_number", 0) > game_state.get("max_turns", 100) * 0.8:
            return StrategicContext.ENDGAME
        else:
            return StrategicContext.BALANCED
    
    def select_strategy(self, game_state: Dict[str, Any], 
                       available_strategies: List[StrategyType]) -> Optional[StrategyType]:
        """选择最佳策略"""
        context = self.analyze_game_situation(game_state)
        
        # 评估每个可用策略
        strategy_scores = {}
        for strategy in available_strategies:
            score = self._evaluate_strategy(strategy, context, game_state)
            strategy_scores[strategy] = score
        
        if not strategy_scores:
            return None
        
        # 根据AI等级选择策略
        if self.strategic_level == AIStrategicLevel.MASTER:
            # 大师级：选择最佳策略
            return max(strategy_scores, key=strategy_scores.get)
        elif self.strategic_level == AIStrategicLevel.ADVANCED:
            # 高级：在前3个策略中随机选择
            top_strategies = sorted(strategy_scores.items(), key=lambda x: x[1], reverse=True)[:3]
            return random.choice(top_strategies)[0]
        else:
            # 中级和新手：加入更多随机性
            strategies_list = list(strategy_scores.keys())
            weights = [strategy_scores[s] for s in strategies_list]
            return random.choices(strategies_list, weights=weights)[0]
    
    def _evaluate_strategy(self, strategy: StrategyType, context: StrategicContext,
                          game_state: Dict[str, Any]) -> float:
        """评估策略价值"""
        base_score = 1.0
        
        # 历史成功率
        success_count = self.memory.successful_strategies.get(strategy, 0)
        failure_count = self.memory.failed_strategies.get(strategy, 0)
        total_attempts = success_count + failure_count
        
        if total_attempts > 0:
            success_rate = success_count / total_attempts
            base_score *= (0.5 + success_rate)
        
        # 环境适应性
        context_bonus = self._get_context_bonus(strategy, context)
        base_score *= context_bonus
        
        # 对手分析
        opponent_bonus = self._analyze_opponents(strategy, game_state)
        base_score *= opponent_bonus
        
        # 策略组合奖励
        combination_bonus = self._evaluate_strategy_combination(strategy)
        base_score *= combination_bonus
        
        return base_score
    
    def _get_context_bonus(self, strategy: StrategyType, context: StrategicContext) -> float:
        """获取环境适应奖励"""
        context_bonuses = {
            StrategicContext.ADVANTAGE: {
                StrategyType.QING_ZEI_QIN_WANG: 1.5,  # 擒贼擒王
                StrategyType.CHEN_HUO_DA_JIE: 1.3,    # 趁火打劫
            },
            StrategicContext.DISADVANTAGE: {
                StrategyType.KONG_CHENG_JI: 1.5,      # 空城计
                StrategyType.KU_ROU_JI: 1.3,          # 苦肉计
                StrategyType.ZOU_WEI_SHANG: 1.4,      # 走为上
            },
            StrategicContext.CHAOS: {
                StrategyType.HUN_SHUI_MO_YU: 1.5,     # 浑水摸鱼
                StrategyType.LIAN_HUAN_JI: 1.3,       # 连环计
            },
            StrategicContext.ENDGAME: {
                StrategyType.PO_FU_CHEN_ZHOU: 1.5,    # 破釜沉舟
                StrategyType.JIN_CHAN_TUO_QIAO: 1.3,  # 金蝉脱壳
            }
        }
        
        return context_bonuses.get(context, {}).get(strategy, 1.0)
    
    def _analyze_opponents(self, strategy: StrategyType, game_state: Dict[str, Any]) -> float:
        """分析对手弱点"""
        bonus = 1.0
        
        # 分析每个对手的弱点
        for player_id in game_state.get("players", []):
            if player_id == self.ai_name:
                continue
            
            vulnerabilities = self.memory.opponent_vulnerabilities.get(player_id, [])
            if strategy in vulnerabilities:
                bonus += 0.2
        
        return bonus
    
    def _evaluate_strategy_combination(self, strategy: StrategyType) -> float:
        """评估策略组合"""
        if not self.active_strategies:
            return 1.0
        
        # 检查策略组合的历史效果
        for active_strategy in self.active_strategies:
            combination = tuple(sorted([active_strategy, strategy]))
            if combination in self.memory.strategy_combinations:
                return self.memory.strategy_combinations[combination]
        
        return 1.0
    
    def create_strategic_plan(self, primary_strategy: StrategyType,
                             game_state: Dict[str, Any]) -> StrategicPlan:
        """创建战略计划"""
        plan_id = f"plan_{len(self.current_plans)}_{primary_strategy.value}"
        
        # 选择支援策略
        supporting_strategies = self._select_supporting_strategies(primary_strategy, game_state)
        
        # 确定目标玩家
        target_players = self._identify_targets(primary_strategy, game_state)
        
        # 制定执行步骤
        execution_steps = self._create_execution_steps(primary_strategy, supporting_strategies)
        
        plan = StrategicPlan(
            plan_id=plan_id,
            primary_strategy=primary_strategy,
            supporting_strategies=supporting_strategies,
            target_players=target_players,
            expected_outcome=self._predict_outcome(primary_strategy, game_state),
            confidence=self._calculate_confidence(primary_strategy, game_state),
            execution_steps=execution_steps
        )
        
        self.current_plans.append(plan)
        return plan
    
    def _select_supporting_strategies(self, primary: StrategyType,
                                    game_state: Dict[str, Any]) -> List[StrategyType]:
        """选择支援策略"""
        supporting = []
        
        # 基于主策略选择协同策略
        strategy_synergies = {
            StrategyType.AN_DU_CHEN_CANG: [StrategyType.SHENG_DONG_JI_XI],
            StrategyType.LIAN_HUAN_JI: [StrategyType.FAN_JIAN_JI, StrategyType.LI_DAI_TAO_JIANG],
            StrategyType.DIAO_HU_LI_SHAN: [StrategyType.MING_XIU_ZHAN_DAO],
        }
        
        potential_supports = strategy_synergies.get(primary, [])
        available_strategies = self.strategy_system.get_available_strategies(self.ai_name)
        
        for support in potential_supports:
            if support in available_strategies:
                supporting.append(support)
                if len(supporting) >= 2:  # 限制支援策略数量
                    break
        
        return supporting
    
    def _identify_targets(self, strategy: StrategyType, game_state: Dict[str, Any]) -> Set[str]:
        """识别目标玩家"""
        targets = set()
        players = game_state.get("players", [])
        
        # 根据策略类型选择目标
        if strategy in [StrategyType.QING_ZEI_QIN_WANG, StrategyType.CHEN_HUO_DA_JIE]:
            # 攻击性策略：选择最强对手
            player_scores = game_state.get("player_scores", {})
            strongest_opponent = max(
                [p for p in players if p != self.ai_name],
                key=lambda p: player_scores.get(p, 0),
                default=None
            )
            if strongest_opponent:
                targets.add(strongest_opponent)
        
        elif strategy in [StrategyType.LI_JIAN_JI, StrategyType.LIAN_HUAN_JI]:
            # 分化策略：选择多个目标
            other_players = [p for p in players if p != self.ai_name]
            targets.update(random.sample(other_players, min(2, len(other_players))))
        
        return targets
    
    def _create_execution_steps(self, primary: StrategyType,
                               supporting: List[StrategyType]) -> List[str]:
        """创建执行步骤"""
        steps = []
        
        # 基础执行步骤
        steps.append(f"准备执行{primary.value}")
        
        # 支援策略步骤
        for support in supporting:
            steps.append(f"配合执行{support.value}")
        
        # 具体行动步骤
        if primary == StrategyType.AN_DU_CHEN_CANG:
            steps.extend([
                "制造明显的行动吸引注意",
                "暗中准备真正的目标行动",
                "在对手分心时执行关键行动"
            ])
        elif primary == StrategyType.LIAN_HUAN_JI:
            steps.extend([
                "识别对手间的矛盾",
                "加剧对手间的冲突",
                "在混乱中获取利益"
            ])
        
        steps.append("评估执行效果")
        return steps
    
    def _predict_outcome(self, strategy: StrategyType, game_state: Dict[str, Any]) -> str:
        """预测结果"""
        success_rate = self._calculate_success_probability(strategy, game_state)
        
        if success_rate > 0.7:
            return "预期获得显著优势"
        elif success_rate > 0.5:
            return "预期获得适度优势"
        else:
            return "预期获得轻微优势"
    
    def _calculate_confidence(self, strategy: StrategyType, game_state: Dict[str, Any]) -> float:
        """计算执行信心"""
        base_confidence = 0.5
        
        # 基于历史成功率
        success_count = self.memory.successful_strategies.get(strategy, 0)
        total_count = success_count + self.memory.failed_strategies.get(strategy, 0)
        
        if total_count > 0:
            success_rate = success_count / total_count
            base_confidence = success_rate
        
        # 基于当前条件
        conditions_met = self.strategy_system.check_strategy_conditions(self.ai_name, strategy)
        if conditions_met:
            base_confidence += 0.2
        
        return min(1.0, base_confidence)
    
    def _calculate_success_probability(self, strategy: StrategyType,
                                     game_state: Dict[str, Any]) -> float:
        """计算成功概率"""
        base_prob = 0.5
        
        # 基于AI等级调整
        level_bonus = {
            AIStrategicLevel.NOVICE: 0.0,
            AIStrategicLevel.INTERMEDIATE: 0.1,
            AIStrategicLevel.ADVANCED: 0.2,
            AIStrategicLevel.MASTER: 0.3
        }
        
        base_prob += level_bonus[self.strategic_level]
        
        # 基于策略适应性
        context = self.analyze_game_situation(game_state)
        context_bonus = self._get_context_bonus(strategy, context) - 1.0
        base_prob += context_bonus * 0.2
        
        return min(1.0, max(0.1, base_prob))
    
    def execute_strategy(self, strategy: StrategyType, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """执行策略"""
        # 检查策略条件
        if not self.strategy_system.check_strategy_conditions(self.ai_name, strategy):
            return {"success": False, "message": "策略条件不满足"}
        
        # 执行策略
        result = self.strategy_system.execute_strategy(self.ai_name, strategy)
        
        # 更新记忆
        if result.get("success", False):
            self.memory.successful_strategies[strategy] = \
                self.memory.successful_strategies.get(strategy, 0) + 1
            self.active_strategies.add(strategy)
        else:
            self.memory.failed_strategies[strategy] = \
                self.memory.failed_strategies.get(strategy, 0) + 1
        
        # 学习对手弱点
        if result.get("success", False) and "target" in result:
            target = result["target"]
            if target not in self.memory.opponent_vulnerabilities:
                self.memory.opponent_vulnerabilities[target] = []
            if strategy not in self.memory.opponent_vulnerabilities[target]:
                self.memory.opponent_vulnerabilities[target].append(strategy)
        
        return result
    
    def update_strategy_memory(self, strategy_combination: List[StrategyType],
                              effectiveness: float):
        """更新策略组合记忆"""
        if len(strategy_combination) > 1:
            combination = tuple(sorted(strategy_combination))
            current_value = self.memory.strategy_combinations.get(combination, 1.0)
            # 使用指数移动平均更新
            new_value = current_value * 0.8 + effectiveness * 0.2
            self.memory.strategy_combinations[combination] = new_value
    
    def get_strategic_advice(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """获取战略建议"""
        context = self.analyze_game_situation(game_state)
        available_strategies = self.strategy_system.get_available_strategies(self.ai_name)
        
        if not available_strategies:
            return {"advice": "当前无可用策略", "strategies": []}
        
        # 推荐前3个策略
        strategy_scores = {}
        for strategy in available_strategies:
            score = self._evaluate_strategy(strategy, context, game_state)
            strategy_scores[strategy] = score
        
        top_strategies = sorted(strategy_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        
        advice = {
            "context": context.value,
            "recommended_strategies": [
                {
                    "strategy": strategy.value,
                    "score": score,
                    "description": self._get_strategy_description(strategy),
                    "success_probability": self._calculate_success_probability(strategy, game_state)
                }
                for strategy, score in top_strategies
            ],
            "strategic_level": self.strategic_level.value
        }
        
        return advice
    
    def _get_strategy_description(self, strategy: StrategyType) -> str:
        """获取策略描述"""
        descriptions = {
            StrategyType.AN_DU_CHEN_CANG: "明修栈道，暗度陈仓 - 声东击西的经典策略",
            StrategyType.LIAN_HUAN_JI: "连环计 - 利用对手间矛盾，一石二鸟",
            StrategyType.KONG_CHENG_JI: "空城计 - 以弱示强，化险为夷",
            # 添加更多描述...
        }
        return descriptions.get(strategy, f"{strategy.value} - 高级战略计谋")

# 全局实例
strategic_ai_system = StrategicAISystem("AI_Master", AIStrategicLevel.MASTER)