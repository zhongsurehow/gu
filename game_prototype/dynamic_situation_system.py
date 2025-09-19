"""
动态局势系统 - Dynamic Situation System
支持三十六计中需要把握时机、利用局势变化的计谋
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple, Callable
from enum import Enum
import random
from datetime import datetime, timedelta
import math

class SituationType(Enum):
    """局势类型"""
    PEACEFUL = "peaceful"           # 和平局势
    TENSE = "tense"                # 紧张局势
    CHAOTIC = "chaotic"            # 混乱局势
    CRISIS = "crisis"              # 危机局势
    OPPORTUNITY = "opportunity"     # 机遇局势
    STALEMATE = "stalemate"        # 僵持局势

class TimingQuality(Enum):
    """时机质量"""
    TERRIBLE = 1    # 极差时机
    POOR = 2        # 差时机
    AVERAGE = 3     # 一般时机
    GOOD = 4        # 好时机
    EXCELLENT = 5   # 绝佳时机

class SituationTrend(Enum):
    """局势趋势"""
    RAPIDLY_DECLINING = -3   # 急剧恶化
    DECLINING = -2           # 恶化
    SLOWLY_DECLINING = -1    # 缓慢恶化
    STABLE = 0               # 稳定
    SLOWLY_IMPROVING = 1     # 缓慢改善
    IMPROVING = 2            # 改善
    RAPIDLY_IMPROVING = 3    # 急剧改善

@dataclass
class SituationFactor:
    """局势因子"""
    factor_id: str
    name: str
    current_value: float
    trend: float  # 变化趋势
    volatility: float  # 波动性
    influence_weight: float  # 影响权重
    last_updated: datetime = field(default_factory=datetime.now)
    
    def update_value(self, time_delta_hours: float):
        """更新因子值"""
        # 基于趋势更新
        trend_change = self.trend * time_delta_hours * 0.1
        
        # 添加随机波动
        volatility_change = random.gauss(0, self.volatility) * time_delta_hours * 0.05
        
        # 更新值
        self.current_value += trend_change + volatility_change
        self.current_value = max(0, min(100, self.current_value))  # 限制在0-100范围
        
        self.last_updated = datetime.now()

@dataclass
class SituationSnapshot:
    """局势快照"""
    timestamp: datetime
    situation_type: SituationType
    overall_stability: float
    tension_level: float
    opportunity_index: float
    factors: Dict[str, float]
    dominant_players: List[str]
    
    def get_timing_quality_for_strategy(self, strategy_type: str) -> TimingQuality:
        """获取特定策略的时机质量"""
        # 不同策略在不同局势下有不同的时机质量
        strategy_preferences = {
            "攻击类": {
                SituationType.CHAOTIC: TimingQuality.EXCELLENT,
                SituationType.CRISIS: TimingQuality.GOOD,
                SituationType.TENSE: TimingQuality.AVERAGE,
                SituationType.PEACEFUL: TimingQuality.POOR,
                SituationType.STALEMATE: TimingQuality.AVERAGE,
                SituationType.OPPORTUNITY: TimingQuality.GOOD
            },
            "防御类": {
                SituationType.PEACEFUL: TimingQuality.EXCELLENT,
                SituationType.TENSE: TimingQuality.GOOD,
                SituationType.CRISIS: TimingQuality.EXCELLENT,
                SituationType.CHAOTIC: TimingQuality.POOR,
                SituationType.STALEMATE: TimingQuality.GOOD,
                SituationType.OPPORTUNITY: TimingQuality.AVERAGE
            },
            "欺骗类": {
                SituationType.CHAOTIC: TimingQuality.EXCELLENT,
                SituationType.TENSE: TimingQuality.GOOD,
                SituationType.CRISIS: TimingQuality.GOOD,
                SituationType.PEACEFUL: TimingQuality.AVERAGE,
                SituationType.STALEMATE: TimingQuality.POOR,
                SituationType.OPPORTUNITY: TimingQuality.AVERAGE
            },
            "外交类": {
                SituationType.PEACEFUL: TimingQuality.GOOD,
                SituationType.TENSE: TimingQuality.EXCELLENT,
                SituationType.CRISIS: TimingQuality.AVERAGE,
                SituationType.CHAOTIC: TimingQuality.POOR,
                SituationType.STALEMATE: TimingQuality.EXCELLENT,
                SituationType.OPPORTUNITY: TimingQuality.GOOD
            }
        }
        
        preferences = strategy_preferences.get(strategy_type, {})
        return preferences.get(self.situation_type, TimingQuality.AVERAGE)

@dataclass
class TimingWindow:
    """时机窗口"""
    window_id: str
    strategy_type: str
    optimal_conditions: Dict[str, Tuple[float, float]]  # 因子名 -> (最小值, 最大值)
    duration_hours: float
    created_time: datetime = field(default_factory=datetime.now)
    
    def is_active(self) -> bool:
        """检查时机窗口是否仍然活跃"""
        elapsed = (datetime.now() - self.created_time).total_seconds() / 3600
        return elapsed < self.duration_hours
    
    def matches_current_situation(self, current_factors: Dict[str, float]) -> float:
        """检查当前局势是否匹配时机窗口，返回匹配度(0-1)"""
        if not self.is_active():
            return 0.0
        
        match_score = 0.0
        total_conditions = len(self.optimal_conditions)
        
        for factor_name, (min_val, max_val) in self.optimal_conditions.items():
            current_val = current_factors.get(factor_name, 50)  # 默认中等值
            
            if min_val <= current_val <= max_val:
                match_score += 1.0
            else:
                # 计算偏离程度
                if current_val < min_val:
                    deviation = (min_val - current_val) / min_val
                else:
                    deviation = (current_val - max_val) / max_val
                
                # 偏离越小，得分越高
                match_score += max(0, 1 - deviation)
        
        return match_score / total_conditions if total_conditions > 0 else 0.0

class DynamicSituationSystem:
    """动态局势系统"""
    
    def __init__(self):
        self.situation_factors: Dict[str, SituationFactor] = {}
        self.situation_history: List[SituationSnapshot] = []
        self.active_timing_windows: List[TimingWindow] = []
        self.situation_triggers: Dict[str, Callable] = {}
        self.last_update: datetime = datetime.now()
        
        self._initialize_base_factors()
        self._setup_situation_triggers()
    
    def _initialize_base_factors(self):
        """初始化基础局势因子"""
        base_factors = [
            SituationFactor("military_tension", "军事紧张度", 30.0, 0.0, 5.0, 0.3),
            SituationFactor("economic_stability", "经济稳定性", 70.0, 0.0, 3.0, 0.2),
            SituationFactor("diplomatic_relations", "外交关系", 60.0, 0.0, 4.0, 0.2),
            SituationFactor("information_chaos", "信息混乱度", 20.0, 0.0, 6.0, 0.15),
            SituationFactor("spiritual_harmony", "精神和谐度", 80.0, 0.0, 2.0, 0.15),
        ]
        
        for factor in base_factors:
            self.situation_factors[factor.factor_id] = factor
    
    def _setup_situation_triggers(self):
        """设置局势触发器"""
        self.situation_triggers = {
            "player_conflict": self._trigger_military_tension,
            "alliance_formed": self._trigger_diplomatic_change,
            "alliance_broken": self._trigger_diplomatic_chaos,
            "major_attack": self._trigger_crisis,
            "resource_shortage": self._trigger_economic_instability,
            "information_warfare": self._trigger_information_chaos,
            "spiritual_breakthrough": self._trigger_spiritual_harmony,
        }
    
    def update_situation(self):
        """更新局势"""
        current_time = datetime.now()
        time_delta = (current_time - self.last_update).total_seconds() / 3600
        
        # 更新所有因子
        for factor in self.situation_factors.values():
            factor.update_value(time_delta)
        
        # 生成新的局势快照
        snapshot = self._generate_situation_snapshot()
        self.situation_history.append(snapshot)
        
        # 保持历史记录在合理范围内
        if len(self.situation_history) > 100:
            self.situation_history = self.situation_history[-100:]
        
        # 检查并创建新的时机窗口
        self._check_for_timing_windows()
        
        # 清理过期的时机窗口
        self.active_timing_windows = [w for w in self.active_timing_windows if w.is_active()]
        
        self.last_update = current_time
    
    def trigger_situation_event(self, event_type: str, **kwargs):
        """触发局势事件"""
        trigger_func = self.situation_triggers.get(event_type)
        if trigger_func:
            trigger_func(**kwargs)
    
    def get_current_situation(self) -> SituationSnapshot:
        """获取当前局势"""
        if not self.situation_history:
            self.update_situation()
        return self.situation_history[-1]
    
    def get_timing_quality(self, strategy_name: str) -> TimingQuality:
        """获取特定策略的时机质量"""
        current_situation = self.get_current_situation()
        
        # 策略分类映射
        strategy_categories = {
            "瞒天过海": "欺骗类", "围魏救赵": "攻击类", "借刀杀人": "外交类",
            "以逸待劳": "防御类", "趁火打劫": "攻击类", "声东击西": "欺骗类",
            "无中生有": "欺骗类", "暗度陈仓": "欺骗类", "隔岸观火": "防御类",
            "笑里藏刀": "欺骗类", "李代桃僵": "防御类", "顺手牵羊": "攻击类",
            "打草惊蛇": "攻击类", "借尸还魂": "欺骗类", "调虎离山": "欺骗类",
            "欲擒故纵": "欺骗类", "抛砖引玉": "欺骗类", "擒贼擒王": "攻击类",
            "釜底抽薪": "攻击类", "混水摸鱼": "攻击类", "金蝉脱壳": "防御类",
            "关门捉贼": "攻击类", "远交近攻": "外交类", "假道伐虢": "外交类",
            "偷梁换柱": "欺骗类", "指桑骂槐": "外交类", "假痴不癫": "欺骗类",
            "上屋抽梯": "攻击类", "树上开花": "欺骗类", "反客为主": "攻击类",
            "美人计": "欺骗类", "空城计": "欺骗类", "反间计": "欺骗类",
            "苦肉计": "欺骗类", "连环计": "欺骗类", "走为上计": "防御类",
        }
        
        strategy_category = strategy_categories.get(strategy_name, "攻击类")
        base_quality = current_situation.get_timing_quality_for_strategy(strategy_category)
        
        # 检查是否有匹配的时机窗口
        best_window_match = 0.0
        for window in self.active_timing_windows:
            if window.strategy_type == strategy_category:
                current_factors = {f.factor_id: f.current_value for f in self.situation_factors.values()}
                match_score = window.matches_current_situation(current_factors)
                best_window_match = max(best_window_match, match_score)
        
        # 时机窗口可以提升时机质量
        if best_window_match > 0.8:
            quality_value = min(5, base_quality.value + 1)
            return TimingQuality(quality_value)
        elif best_window_match > 0.6:
            return base_quality
        else:
            quality_value = max(1, base_quality.value - 1)
            return TimingQuality(quality_value)
    
    def predict_situation_trend(self, hours_ahead: int = 3) -> SituationTrend:
        """预测局势趋势"""
        if len(self.situation_history) < 2:
            return SituationTrend.STABLE
        
        # 计算当前趋势
        recent_snapshots = self.situation_history[-5:] if len(self.situation_history) >= 5 else self.situation_history
        
        stability_trend = 0
        tension_trend = 0
        
        for i in range(1, len(recent_snapshots)):
            stability_change = recent_snapshots[i].overall_stability - recent_snapshots[i-1].overall_stability
            tension_change = recent_snapshots[i].tension_level - recent_snapshots[i-1].tension_level
            
            stability_trend += stability_change
            tension_trend += tension_change
        
        # 综合评估趋势
        overall_trend = stability_trend - tension_trend  # 稳定性增加、紧张度减少为正向
        
        if overall_trend > 10:
            return SituationTrend.RAPIDLY_IMPROVING
        elif overall_trend > 5:
            return SituationTrend.IMPROVING
        elif overall_trend > 1:
            return SituationTrend.SLOWLY_IMPROVING
        elif overall_trend > -1:
            return SituationTrend.STABLE
        elif overall_trend > -5:
            return SituationTrend.SLOWLY_DECLINING
        elif overall_trend > -10:
            return SituationTrend.DECLINING
        else:
            return SituationTrend.RAPIDLY_DECLINING
    
    def create_timing_window(self, strategy_type: str, optimal_conditions: Dict[str, Tuple[float, float]], 
                           duration_hours: float = 2.0) -> TimingWindow:
        """创建时机窗口"""
        window_id = f"window_{len(self.active_timing_windows)}_{datetime.now().timestamp()}"
        
        window = TimingWindow(
            window_id=window_id,
            strategy_type=strategy_type,
            optimal_conditions=optimal_conditions,
            duration_hours=duration_hours
        )
        
        self.active_timing_windows.append(window)
        return window
    
    def execute_situation_strategy(self, strategy_name: str, executor_id: str, **kwargs) -> Dict:
        """执行局势相关策略"""
        strategies = {
            "隔岸观火": self._execute_watch_fire_from_other_shore,
            "以逸待劳": self._execute_wait_at_ease_for_exhausted_enemy,
            "趁火打劫": self._execute_loot_burning_house,
            "调虎离山": self._execute_lure_tiger_from_mountain,
            "欲擒故纵": self._execute_catch_by_letting_go,
            "金蝉脱壳": self._execute_golden_cicada_sheds_shell,
            "走为上计": self._execute_retreat_as_best_strategy,
        }
        
        strategy_func = strategies.get(strategy_name)
        if strategy_func:
            return strategy_func(executor_id, **kwargs)
        
        return {"success": False, "message": f"未知策略: {strategy_name}"}
    
    def _generate_situation_snapshot(self) -> SituationSnapshot:
        """生成局势快照"""
        current_factors = {f.factor_id: f.current_value for f in self.situation_factors.values()}
        
        # 计算整体稳定性
        stability_factors = ["economic_stability", "diplomatic_relations", "spiritual_harmony"]
        overall_stability = sum(current_factors.get(f, 50) for f in stability_factors) / len(stability_factors)
        
        # 计算紧张度
        tension_factors = ["military_tension", "information_chaos"]
        tension_level = sum(current_factors.get(f, 50) for f in tension_factors) / len(tension_factors)
        
        # 计算机遇指数
        opportunity_index = (overall_stability + (100 - tension_level)) / 2
        
        # 确定局势类型
        situation_type = self._determine_situation_type(overall_stability, tension_level, opportunity_index)
        
        return SituationSnapshot(
            timestamp=datetime.now(),
            situation_type=situation_type,
            overall_stability=overall_stability,
            tension_level=tension_level,
            opportunity_index=opportunity_index,
            factors=current_factors.copy(),
            dominant_players=[]  # 这里应该从游戏状态获取
        )
    
    def _determine_situation_type(self, stability: float, tension: float, opportunity: float) -> SituationType:
        """确定局势类型"""
        if tension > 80:
            return SituationType.CRISIS
        elif tension > 60:
            return SituationType.CHAOTIC
        elif tension > 40:
            return SituationType.TENSE
        elif stability > 70 and tension < 30:
            return SituationType.PEACEFUL
        elif opportunity > 70:
            return SituationType.OPPORTUNITY
        else:
            return SituationType.STALEMATE
    
    def _check_for_timing_windows(self):
        """检查并创建新的时机窗口"""
        current_factors = {f.factor_id: f.current_value for f in self.situation_factors.values()}
        
        # 检查各种时机窗口条件
        
        # 攻击类时机窗口
        if (current_factors.get("military_tension", 50) > 60 and 
            current_factors.get("information_chaos", 50) > 50):
            self.create_timing_window(
                "攻击类",
                {
                    "military_tension": (60, 100),
                    "information_chaos": (50, 100)
                },
                duration_hours=1.5
            )
        
        # 欺骗类时机窗口
        if (current_factors.get("information_chaos", 50) > 70 and 
            current_factors.get("diplomatic_relations", 50) < 40):
            self.create_timing_window(
                "欺骗类",
                {
                    "information_chaos": (70, 100),
                    "diplomatic_relations": (0, 40)
                },
                duration_hours=2.0
            )
        
        # 外交类时机窗口
        if (current_factors.get("diplomatic_relations", 50) > 60 and 
            current_factors.get("economic_stability", 50) > 50):
            self.create_timing_window(
                "外交类",
                {
                    "diplomatic_relations": (60, 100),
                    "economic_stability": (50, 100)
                },
                duration_hours=3.0
            )
    
    def _trigger_military_tension(self, intensity: float = 20.0, **kwargs):
        """触发军事紧张"""
        if "military_tension" in self.situation_factors:
            factor = self.situation_factors["military_tension"]
            factor.current_value = min(100, factor.current_value + intensity)
            factor.trend = max(factor.trend, intensity * 0.1)
    
    def _trigger_diplomatic_change(self, change: float = 15.0, **kwargs):
        """触发外交变化"""
        if "diplomatic_relations" in self.situation_factors:
            factor = self.situation_factors["diplomatic_relations"]
            factor.current_value = max(0, min(100, factor.current_value + change))
            factor.trend = change * 0.1
    
    def _trigger_diplomatic_chaos(self, intensity: float = 25.0, **kwargs):
        """触发外交混乱"""
        if "diplomatic_relations" in self.situation_factors:
            factor = self.situation_factors["diplomatic_relations"]
            factor.current_value = max(0, factor.current_value - intensity)
            factor.trend = -intensity * 0.1
    
    def _trigger_crisis(self, severity: float = 30.0, **kwargs):
        """触发危机"""
        # 同时影响多个因子
        if "military_tension" in self.situation_factors:
            self.situation_factors["military_tension"].current_value = min(100, 
                self.situation_factors["military_tension"].current_value + severity)
        
        if "economic_stability" in self.situation_factors:
            self.situation_factors["economic_stability"].current_value = max(0,
                self.situation_factors["economic_stability"].current_value - severity * 0.7)
    
    def _trigger_economic_instability(self, intensity: float = 20.0, **kwargs):
        """触发经济不稳定"""
        if "economic_stability" in self.situation_factors:
            factor = self.situation_factors["economic_stability"]
            factor.current_value = max(0, factor.current_value - intensity)
            factor.trend = -intensity * 0.1
    
    def _trigger_information_chaos(self, intensity: float = 25.0, **kwargs):
        """触发信息混乱"""
        if "information_chaos" in self.situation_factors:
            factor = self.situation_factors["information_chaos"]
            factor.current_value = min(100, factor.current_value + intensity)
            factor.trend = intensity * 0.1
    
    def _trigger_spiritual_harmony(self, improvement: float = 15.0, **kwargs):
        """触发精神和谐"""
        if "spiritual_harmony" in self.situation_factors:
            factor = self.situation_factors["spiritual_harmony"]
            factor.current_value = min(100, factor.current_value + improvement)
            factor.trend = improvement * 0.1
    
    def _execute_watch_fire_from_other_shore(self, executor_id: str, **kwargs) -> Dict:
        """执行隔岸观火策略"""
        current_situation = self.get_current_situation()
        
        # 隔岸观火需要混乱或危机局势
        if current_situation.situation_type not in [SituationType.CHAOTIC, SituationType.CRISIS]:
            return {"success": False, "message": "当前局势不适合隔岸观火"}
        
        # 等待并观察，获得信息优势
        observation_bonus = {
            "information_advantage": 3,
            "strategic_patience": 2,
            "timing_bonus": 1
        }
        
        return {
            "success": True,
            "message": "隔岸观火成功，获得观察优势",
            "effect": "在混乱中保持冷静，获得信息和时机优势",
            "bonuses": observation_bonus
        }
    
    def _execute_wait_at_ease_for_exhausted_enemy(self, executor_id: str, **kwargs) -> Dict:
        """执行以逸待劳策略"""
        current_situation = self.get_current_situation()
        
        # 以逸待劳适合紧张或僵持局势
        if current_situation.situation_type not in [SituationType.TENSE, SituationType.STALEMATE]:
            return {"success": False, "message": "当前局势不适合以逸待劳"}
        
        # 保存体力，等待敌人疲惫
        patience_bonus = {
            "energy_conservation": 2,
            "defensive_bonus": 3,
            "counter_attack_readiness": 2
        }
        
        return {
            "success": True,
            "message": "以逸待劳成功，保存实力等待时机",
            "effect": "避免消耗，等待敌人疲惫后反击",
            "bonuses": patience_bonus
        }
    
    def _execute_loot_burning_house(self, executor_id: str, **kwargs) -> Dict:
        """执行趁火打劫策略"""
        current_situation = self.get_current_situation()
        
        # 趁火打劫需要混乱或危机局势
        if current_situation.situation_type not in [SituationType.CHAOTIC, SituationType.CRISIS]:
            return {"success": False, "message": "当前局势不适合趁火打劫"}
        
        # 在混乱中获得额外收益
        chaos_bonus = {
            "resource_gain": 4,
            "stealth_bonus": 2,
            "opportunity_exploitation": 3
        }
        
        return {
            "success": True,
            "message": "趁火打劫成功，在混乱中获得收益",
            "effect": "利用混乱局势获得额外资源和优势",
            "bonuses": chaos_bonus
        }
    
    def _execute_lure_tiger_from_mountain(self, executor_id: str, **kwargs) -> Dict:
        """执行调虎离山策略"""
        target_location = kwargs.get("target_location")
        lure_location = kwargs.get("lure_location")
        
        if not target_location or not lure_location:
            return {"success": False, "message": "需要指定目标位置和引诱位置"}
        
        # 创建虚假机遇来引诱敌人
        self.create_timing_window(
            "攻击类",
            {"opportunity_index": (70, 100)},
            duration_hours=1.0
        )
        
        return {
            "success": True,
            "message": "调虎离山成功，创造虚假机遇引诱敌人",
            "effect": f"敌人被引诱到{lure_location}，{target_location}防御空虚",
            "lure_location": lure_location,
            "target_location": target_location
        }
    
    def _execute_catch_by_letting_go(self, executor_id: str, **kwargs) -> Dict:
        """执行欲擒故纵策略"""
        # 故意示弱，引诱敌人深入
        current_situation = self.get_current_situation()
        
        # 降低自己的威胁度，引诱敌人放松警惕
        deception_setup = {
            "apparent_weakness": 3,
            "hidden_strength": 4,
            "trap_preparation": 2
        }
        
        return {
            "success": True,
            "message": "欲擒故纵设置完成，故意示弱引诱敌人",
            "effect": "敌人可能因为你的示弱而放松警惕，深入陷阱",
            "setup": deception_setup
        }
    
    def _execute_golden_cicada_sheds_shell(self, executor_id: str, **kwargs) -> Dict:
        """执行金蝉脱壳策略"""
        current_situation = self.get_current_situation()
        
        # 金蝉脱壳适合危机局势
        if current_situation.situation_type != SituationType.CRISIS:
            return {"success": False, "message": "当前局势不适合金蝉脱壳"}
        
        # 保留表象，转移实质
        escape_bonus = {
            "stealth_escape": 4,
            "misdirection": 3,
            "preservation_of_core": 5
        }
        
        return {
            "success": True,
            "message": "金蝉脱壳成功，保留表象转移实质",
            "effect": "在危机中成功转移核心力量，保存实力",
            "bonuses": escape_bonus
        }
    
    def _execute_retreat_as_best_strategy(self, executor_id: str, **kwargs) -> Dict:
        """执行走为上计策略"""
        current_situation = self.get_current_situation()
        
        # 走为上计适合危机或快速恶化的局势
        situation_trend = self.predict_situation_trend()
        
        if (current_situation.situation_type != SituationType.CRISIS and 
            situation_trend not in [SituationTrend.RAPIDLY_DECLINING, SituationTrend.DECLINING]):
            return {"success": False, "message": "当前局势不需要战略撤退"}
        
        # 战略撤退，保存实力
        retreat_bonus = {
            "strategic_withdrawal": 5,
            "force_preservation": 4,
            "future_opportunity": 3
        }
        
        return {
            "success": True,
            "message": "走为上计成功，战略撤退保存实力",
            "effect": "及时撤退避免更大损失，为未来机会保存实力",
            "bonuses": retreat_bonus
        }
    
    def get_situation_summary(self) -> Dict:
        """获取局势摘要"""
        current_situation = self.get_current_situation()
        trend = self.predict_situation_trend()
        
        return {
            "current_type": current_situation.situation_type.value,
            "stability": current_situation.overall_stability,
            "tension": current_situation.tension_level,
            "opportunity": current_situation.opportunity_index,
            "trend": trend.name,
            "active_windows": len(self.active_timing_windows),
            "factors": current_situation.factors
        }