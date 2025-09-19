"""
动态AI占卜系统 - 活的甲骨
基于数据分析的智能占卜和神谕系统
"""

import random
import math
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from advanced_ui_system import advanced_ui, MessageType

class DivinationType(Enum):
    """占卜类型"""
    FORTUNE = "运势占卜"          # 一般运势
    ACTION = "行动占卜"           # 特定行动
    STRATEGY = "策略占卜"         # 策略建议
    TIMING = "时机占卜"           # 时机选择
    RELATIONSHIP = "关系占卜"     # 玩家关系
    RESOURCE = "资源占卜"         # 资源预测
    DANGER = "危险占卜"           # 风险警告
    OPPORTUNITY = "机遇占卜"      # 机会发现

class OracleLevel(Enum):
    """神谕等级"""
    WHISPER = "低语"      # 模糊提示
    VISION = "异象"       # 清晰预见
    PROPHECY = "预言"     # 详细预测
    REVELATION = "天启"   # 绝对真理

@dataclass
class GameState:
    """游戏状态快照"""
    current_turn: int
    players: Dict[str, Dict[str, Any]]  # 玩家状态
    board_state: Dict[str, Any]         # 棋盘状态
    remaining_cards: List[str]          # 剩余卡牌
    recent_actions: List[Dict]          # 最近行动
    global_events: List[Dict]           # 全局事件

@dataclass
class DivinationResult:
    """占卜结果"""
    divination_type: DivinationType
    oracle_level: OracleLevel
    accuracy: float                     # 准确度 (0-1)
    confidence: float                   # 置信度 (0-1)
    message: str                        # 神谕信息
    specific_advice: str                # 具体建议
    risk_assessment: Dict[str, float]   # 风险评估
    opportunity_score: float            # 机会分数
    mystical_elements: List[str]        # 神秘元素
    numerical_prediction: Optional[Dict[str, float]] = None  # 数值预测

@dataclass
class DivinationHistory:
    """占卜历史"""
    player_name: str
    results: List[DivinationResult] = field(default_factory=list)
    accuracy_record: List[float] = field(default_factory=list)
    total_divinations: int = 0
    successful_predictions: int = 0
    
    def add_result(self, result: DivinationResult):
        """添加占卜结果"""
        self.results.append(result)
        self.total_divinations += 1
    
    def record_accuracy(self, actual_outcome: float, predicted_outcome: float):
        """记录准确度"""
        accuracy = 1.0 - abs(actual_outcome - predicted_outcome)
        self.accuracy_record.append(max(0.0, accuracy))
        if accuracy > 0.7:  # 70%以上算成功预测
            self.successful_predictions += 1
    
    def get_average_accuracy(self) -> float:
        """获取平均准确度"""
        if not self.accuracy_record:
            return 0.5
        return sum(self.accuracy_record) / len(self.accuracy_record)

class AIDivinationSystem:
    """AI占卜系统"""
    
    def __init__(self):
        self.divination_history: Dict[str, DivinationHistory] = {}
        self.oracle_wisdom: Dict[str, List[str]] = self._initialize_oracle_wisdom()
        self.mystical_symbols: List[str] = [
            "龙", "凤", "麒麟", "玄武", "朱雀", "白虎", "青龙",
            "太极", "八卦", "五行", "天干", "地支", "星宿", "神兽"
        ]
        self.prediction_algorithms: Dict[str, callable] = {
            "resource_trend": self._analyze_resource_trend,
            "player_behavior": self._analyze_resource_trend,  # 临时使用相同方法
            "board_control": self._analyze_board_control,
            "victory_probability": self._calculate_opportunity_index  # 临时使用相同方法
        }
    
    def _initialize_oracle_wisdom(self) -> Dict[str, List[str]]:
        """初始化神谕智慧库"""
        return {
            "fortune_positive": [
                "天时地利人和，万事皆可成",
                "紫气东来，福星高照",
                "龙腾虎跃，势不可挡",
                "凤鸣九天，吉祥如意",
                "金玉满堂，富贵临门"
            ],
            "fortune_negative": [
                "乌云蔽日，需谨慎行事",
                "逆水行舟，困难重重",
                "风雨飘摇，宜守不宜攻",
                "阴霾笼罩，暂避锋芒",
                "波涛汹涌，需待时机"
            ],
            "action_advice": [
                "顺势而为，事半功倍",
                "逆流而上，虽难必成",
                "静观其变，伺机而动",
                "果断出击，一击制胜",
                "稳扎稳打，步步为营"
            ],
            "timing_wisdom": [
                "时机未到，再等片刻",
                "机不可失，时不再来",
                "天时已至，正是良机",
                "时过境迁，另寻他法",
                "时来运转，把握当下"
            ],
            "relationship_insight": [
                "盟友可靠，值得信赖",
                "敌友难辨，需多观察",
                "暗流涌动，小心背叛",
                "众望所归，人心所向",
                "孤军奋战，自强不息"
            ]
        }
    
    def perform_divination(self, player_name: str, divination_type: DivinationType,
                          game_state: GameState, specific_query: str = "") -> DivinationResult:
        """执行占卜"""
        # 获取玩家历史
        if player_name not in self.divination_history:
            self.divination_history[player_name] = DivinationHistory(player_name)
        
        history = self.divination_history[player_name]
        
        # 分析游戏状态
        analysis = self._analyze_game_state(game_state, player_name)
        
        # 生成占卜结果
        result = self._generate_divination_result(
            divination_type, analysis, history, specific_query
        )
        
        # 记录历史
        history.add_result(result)
        
        return result
    
    def _analyze_game_state(self, game_state: GameState, player_name: str) -> Dict[str, Any]:
        """分析游戏状态"""
        player_state = game_state.players.get(player_name, {})
        other_players = {k: v for k, v in game_state.players.items() if k != player_name}
        
        analysis = {
            "player_strength": self._calculate_player_strength(player_state),
            "relative_position": self._calculate_relative_position(player_state, other_players),
            "resource_trend": self._analyze_resource_trend(game_state.recent_actions, player_name),
            "board_control": self._analyze_board_control(game_state.board_state, player_name),
            "threat_level": self._assess_threat_level(other_players, player_state),
            "opportunity_index": self._calculate_opportunity_index(game_state, player_name),
            "momentum": self._calculate_momentum(game_state.recent_actions, player_name)
        }
        
        return analysis
    
    def _calculate_player_strength(self, player_state: Dict[str, Any]) -> float:
        """计算玩家实力"""
        resources = player_state.get("resources", {})
        ap = resources.get("ap", 0)
        qi = resources.get("qi", 0)
        dao_xing = resources.get("dao_xing", 0)
        cheng_yi = resources.get("cheng_yi", 0)
        
        # 综合实力计算
        strength = (ap * 0.2 + qi * 0.3 + dao_xing * 0.4 + cheng_yi * 0.1) / 100
        return min(1.0, strength)
    
    def _calculate_relative_position(self, player_state: Dict[str, Any], 
                                   other_players: Dict[str, Dict[str, Any]]) -> float:
        """计算相对位置"""
        if not other_players:
            return 0.5
        
        player_score = self._calculate_player_strength(player_state)
        other_scores = [self._calculate_player_strength(state) for state in other_players.values()]
        
        if not other_scores:
            return 0.5
        
        avg_other_score = sum(other_scores) / len(other_scores)
        
        if avg_other_score == 0:
            return 1.0
        
        relative_position = player_score / (player_score + avg_other_score)
        return relative_position
    
    def _analyze_resource_trend(self, recent_actions: List[Dict], player_name: str) -> float:
        """分析资源趋势"""
        player_actions = [action for action in recent_actions 
                         if action.get("player") == player_name]
        
        if len(player_actions) < 2:
            return 0.5
        
        # 计算资源变化趋势
        resource_changes = []
        for action in player_actions[-5:]:  # 最近5个行动
            change = action.get("resource_change", 0)
            resource_changes.append(change)
        
        if not resource_changes:
            return 0.5
        
        # 计算趋势斜率
        trend = sum(resource_changes) / len(resource_changes)
        return max(0.0, min(1.0, 0.5 + trend / 10))
    
    def _analyze_board_control(self, board_state: Dict[str, Any], player_name: str) -> float:
        """分析棋盘控制力"""
        zones = board_state.get("zones", {})
        total_zones = len(zones)
        
        if total_zones == 0:
            return 0.5
        
        controlled_zones = 0
        for zone_name, zone_data in zones.items():
            controller = zone_data.get("controller")
            if controller == player_name:
                controlled_zones += 1
        
        return controlled_zones / total_zones
    
    def _assess_threat_level(self, other_players: Dict[str, Dict[str, Any]], 
                           player_state: Dict[str, Any]) -> float:
        """评估威胁等级"""
        if not other_players:
            return 0.0
        
        player_strength = self._calculate_player_strength(player_state)
        max_threat = 0.0
        
        for other_state in other_players.values():
            other_strength = self._calculate_player_strength(other_state)
            threat = max(0.0, other_strength - player_strength)
            max_threat = max(max_threat, threat)
        
        return max_threat
    
    def _calculate_opportunity_index(self, game_state: GameState, player_name: str) -> float:
        """计算机会指数"""
        # 基于剩余卡牌、全局事件等计算机会
        remaining_cards = len(game_state.remaining_cards)
        total_cards = remaining_cards + sum(
            len(player.get("hand", [])) for player in game_state.players.values()
        )
        
        if total_cards == 0:
            return 0.5
        
        card_opportunity = remaining_cards / total_cards
        
        # 全局事件带来的机会
        event_opportunity = len(game_state.global_events) * 0.1
        
        return min(1.0, card_opportunity + event_opportunity)
    
    def _calculate_momentum(self, recent_actions: List[Dict], player_name: str) -> float:
        """计算动量"""
        player_actions = [action for action in recent_actions[-10:] 
                         if action.get("player") == player_name]
        
        if not player_actions:
            return 0.5
        
        success_count = sum(1 for action in player_actions if action.get("success", False))
        momentum = success_count / len(player_actions)
        
        return momentum
    
    def _generate_divination_result(self, divination_type: DivinationType,
                                  analysis: Dict[str, Any], history: DivinationHistory,
                                  specific_query: str) -> DivinationResult:
        """生成占卜结果"""
        # 确定神谕等级
        oracle_level = self._determine_oracle_level(analysis, history)
        
        # 计算准确度和置信度
        accuracy = self._calculate_accuracy(analysis, oracle_level)
        confidence = self._calculate_confidence(analysis, history)
        
        # 生成神谕信息
        message = self._generate_oracle_message(divination_type, analysis, oracle_level)
        
        # 生成具体建议
        advice = self._generate_specific_advice(divination_type, analysis)
        
        # 风险评估
        risk_assessment = self._generate_risk_assessment(analysis)
        
        # 机会分数
        opportunity_score = analysis["opportunity_index"]
        
        # 神秘元素
        mystical_elements = self._select_mystical_elements(analysis)
        
        # 数值预测
        numerical_prediction = self._generate_numerical_prediction(divination_type, analysis)
        
        return DivinationResult(
            divination_type=divination_type,
            oracle_level=oracle_level,
            accuracy=accuracy,
            confidence=confidence,
            message=message,
            specific_advice=advice,
            risk_assessment=risk_assessment,
            opportunity_score=opportunity_score,
            mystical_elements=mystical_elements,
            numerical_prediction=numerical_prediction
        )
    
    def _determine_oracle_level(self, analysis: Dict[str, Any], 
                               history: DivinationHistory) -> OracleLevel:
        """确定神谕等级"""
        # 基于玩家历史准确度和当前分析确定等级
        avg_accuracy = history.get_average_accuracy()
        player_strength = analysis["player_strength"]
        
        combined_score = (avg_accuracy + player_strength) / 2
        
        if combined_score >= 0.8:
            return OracleLevel.REVELATION
        elif combined_score >= 0.6:
            return OracleLevel.PROPHECY
        elif combined_score >= 0.4:
            return OracleLevel.VISION
        else:
            return OracleLevel.WHISPER
    
    def _calculate_accuracy(self, analysis: Dict[str, Any], oracle_level: OracleLevel) -> float:
        """计算准确度"""
        base_accuracy = 0.5
        
        # 根据分析质量调整
        analysis_quality = (
            analysis["player_strength"] + 
            analysis["relative_position"] + 
            analysis["momentum"]
        ) / 3
        
        # 根据神谕等级调整
        level_bonus = {
            OracleLevel.WHISPER: 0.0,
            OracleLevel.VISION: 0.1,
            OracleLevel.PROPHECY: 0.2,
            OracleLevel.REVELATION: 0.3
        }
        
        accuracy = base_accuracy + analysis_quality * 0.3 + level_bonus[oracle_level]
        return min(0.95, max(0.1, accuracy))
    
    def _calculate_confidence(self, analysis: Dict[str, Any], 
                            history: DivinationHistory) -> float:
        """计算置信度"""
        # 基于历史准确度和当前分析的一致性
        historical_confidence = history.get_average_accuracy()
        
        # 分析一致性
        analysis_values = [
            analysis["player_strength"],
            analysis["relative_position"],
            analysis["momentum"]
        ]
        
        variance = sum((x - sum(analysis_values)/len(analysis_values))**2 for x in analysis_values)
        consistency = 1.0 - min(1.0, variance)
        
        confidence = (historical_confidence + consistency) / 2
        return confidence
    
    def _generate_oracle_message(self, divination_type: DivinationType,
                                analysis: Dict[str, Any], oracle_level: OracleLevel) -> str:
        """生成神谕信息"""
        # 根据占卜类型和分析结果选择合适的神谕
        if divination_type == DivinationType.FORTUNE:
            if analysis["momentum"] > 0.6:
                wisdom_key = "fortune_positive"
            else:
                wisdom_key = "fortune_negative"
        elif divination_type == DivinationType.ACTION:
            wisdom_key = "action_advice"
        elif divination_type == DivinationType.TIMING:
            wisdom_key = "timing_wisdom"
        elif divination_type == DivinationType.RELATIONSHIP:
            wisdom_key = "relationship_insight"
        else:
            wisdom_key = "fortune_positive"
        
        base_message = random.choice(self.oracle_wisdom[wisdom_key])
        
        # 根据神谕等级添加详细信息
        if oracle_level == OracleLevel.REVELATION:
            detail = f"天机显现：{self._generate_detailed_insight(analysis)}"
            return f"{base_message}\n\n{detail}"
        elif oracle_level == OracleLevel.PROPHECY:
            detail = f"预言所示：{self._generate_prophecy_detail(analysis)}"
            return f"{base_message}\n\n{detail}"
        elif oracle_level == OracleLevel.VISION:
            return f"{base_message}\n\n异象浮现，需细心体悟。"
        else:
            return f"{base_message}"
    
    def _generate_detailed_insight(self, analysis: Dict[str, Any]) -> str:
        """生成详细洞察"""
        insights = []
        
        if analysis["player_strength"] > 0.7:
            insights.append("你的实力已臻上乘")
        elif analysis["player_strength"] < 0.3:
            insights.append("当前实力尚需提升")
        
        if analysis["threat_level"] > 0.5:
            insights.append("强敌环伺，需谨慎应对")
        
        if analysis["opportunity_index"] > 0.6:
            insights.append("良机在前，把握时机")
        
        return "，".join(insights) if insights else "局势复杂，需静心观察"
    
    def _generate_prophecy_detail(self, analysis: Dict[str, Any]) -> str:
        """生成预言详情"""
        if analysis["momentum"] > 0.7:
            return "连胜之势将延续，但需防范乐极生悲"
        elif analysis["momentum"] < 0.3:
            return "低谷即将过去，转机正在酝酿"
        else:
            return "变化即将来临，需做好准备"
    
    def _generate_specific_advice(self, divination_type: DivinationType,
                                 analysis: Dict[str, Any]) -> str:
        """生成具体建议"""
        advice_templates = {
            DivinationType.FORTUNE: [
                "建议专注于{focus_area}，成功概率较高",
                "避免在{risk_area}投入过多资源",
                "当前适合{strategy_type}策略"
            ],
            DivinationType.ACTION: [
                "推荐行动：{recommended_action}",
                "成功概率：{success_rate:.1%}",
                "风险等级：{risk_level}"
            ],
            DivinationType.STRATEGY: [
                "建议采用{strategy_name}策略",
                "重点关注{key_factors}",
                "预期收益：{expected_return}"
            ]
        }
        
        # 根据分析结果填充模板
        if analysis["player_strength"] > 0.6:
            focus_area = "扩张领域"
            strategy_type = "积极进攻"
        else:
            focus_area = "资源积累"
            strategy_type = "稳健发展"
        
        if analysis["threat_level"] > 0.5:
            risk_area = "直接对抗"
            risk_level = "高"
        else:
            risk_area = "过度扩张"
            risk_level = "中"
        
        template = random.choice(advice_templates.get(divination_type, advice_templates[DivinationType.FORTUNE]))
        
        return template.format(
            focus_area=focus_area,
            risk_area=risk_area,
            strategy_type=strategy_type,
            recommended_action="巩固优势" if analysis["momentum"] > 0.5 else "寻求突破",
            success_rate=analysis["momentum"],
            risk_level=risk_level,
            strategy_name="稳扎稳打" if analysis["threat_level"] > 0.5 else "快速扩张",
            key_factors="资源管理" if analysis["player_strength"] < 0.5 else "区域控制",
            expected_return="稳定增长" if analysis["momentum"] > 0.5 else "潜在突破"
        )
    
    def _generate_risk_assessment(self, analysis: Dict[str, Any]) -> Dict[str, float]:
        """生成风险评估"""
        return {
            "整体风险": analysis["threat_level"],
            "资源风险": 1.0 - analysis["resource_trend"],
            "竞争风险": 1.0 - analysis["relative_position"],
            "时机风险": 1.0 - analysis["opportunity_index"],
            "策略风险": 1.0 - analysis["momentum"]
        }
    
    def _select_mystical_elements(self, analysis: Dict[str, Any]) -> List[str]:
        """选择神秘元素"""
        elements = []
        
        # 根据分析结果选择相应的神秘元素
        if analysis["player_strength"] > 0.7:
            elements.extend(["龙", "凤", "麒麟"])
        elif analysis["player_strength"] < 0.3:
            elements.extend(["玄武", "太极"])
        
        if analysis["momentum"] > 0.6:
            elements.extend(["朱雀", "青龙"])
        elif analysis["momentum"] < 0.4:
            elements.extend(["白虎", "八卦"])
        
        if analysis["opportunity_index"] > 0.6:
            elements.extend(["星宿", "神兽"])
        
        # 随机选择2-4个元素
        selected_count = random.randint(2, min(4, len(elements)))
        return random.sample(elements, selected_count) if elements else ["太极", "八卦"]
    
    def _generate_numerical_prediction(self, divination_type: DivinationType,
                                     analysis: Dict[str, Any]) -> Optional[Dict[str, float]]:
        """生成数值预测"""
        if divination_type in [DivinationType.RESOURCE, DivinationType.STRATEGY]:
            return {
                "资源增长率": analysis["resource_trend"] * 100,
                "胜利概率": analysis["player_strength"] * analysis["momentum"] * 100,
                "风险指数": analysis["threat_level"] * 100,
                "机会指数": analysis["opportunity_index"] * 100
            }
        return None
    
    def display_divination_result(self, result: DivinationResult):
        """显示占卜结果"""
        advanced_ui.display_mystical_message(
            f"占卜类型：{result.divination_type.value}\n"
            f"神谕等级：{result.oracle_level.value}\n"
            f"准确度：{result.accuracy:.1%}\n"
            f"置信度：{result.confidence:.1%}",
            "占卜开始",
            MessageType.MYSTICAL
        )
        
        # 显示神秘元素
        if result.mystical_elements:
            elements_text = " ".join(result.mystical_elements)
            advanced_ui.print_colored(f"神秘征象：{elements_text}", MessageType.MYSTICAL)
        
        # 显示神谕信息
        advanced_ui.display_mystical_message(
            result.message,
            "神谕显现",
            MessageType.HIGHLIGHT
        )
        
        # 显示具体建议
        advanced_ui.print_colored(f"具体建议：{result.specific_advice}", MessageType.INFO)
        
        # 显示风险评估
        if result.risk_assessment:
            advanced_ui.print_colored("风险评估：", MessageType.WARNING)
            for risk_type, risk_value in result.risk_assessment.items():
                risk_level = "高" if risk_value > 0.7 else "中" if risk_value > 0.4 else "低"
                advanced_ui.print_colored(f"  {risk_type}: {risk_level} ({risk_value:.1%})", MessageType.INFO)
        
        # 显示数值预测
        if result.numerical_prediction:
            advanced_ui.print_colored("数值预测：", MessageType.MYSTICAL)
            for metric, value in result.numerical_prediction.items():
                advanced_ui.print_colored(f"  {metric}: {value:.1f}%", MessageType.INFO)
        
        # 显示机会分数
        opportunity_level = "极佳" if result.opportunity_score > 0.8 else "良好" if result.opportunity_score > 0.6 else "一般" if result.opportunity_score > 0.4 else "较差"
        advanced_ui.print_colored(f"机会评级：{opportunity_level} ({result.opportunity_score:.1%})", MessageType.HIGHLIGHT)
    
    def get_player_divination_history(self, player_name: str) -> Optional[DivinationHistory]:
        """获取玩家占卜历史"""
        return self.divination_history.get(player_name)
    
    def display_divination_history(self, player_name: str):
        """显示占卜历史"""
        history = self.get_player_divination_history(player_name)
        if not history:
            advanced_ui.print_colored("无占卜历史记录", MessageType.INFO)
            return
        
        advanced_ui.print_colored(f"占卜历史 - {player_name}", MessageType.HIGHLIGHT)
        advanced_ui.print_colored(f"总占卜次数：{history.total_divinations}", MessageType.INFO)
        advanced_ui.print_colored(f"成功预测：{history.successful_predictions}", MessageType.INFO)
        advanced_ui.print_colored(f"平均准确度：{history.get_average_accuracy():.1%}", MessageType.INFO)
        
        if history.results:
            advanced_ui.print_colored("最近占卜：", MessageType.MYSTICAL)
            for i, result in enumerate(history.results[-5:], 1):
                advanced_ui.print_colored(
                    f"  {i}. {result.divination_type.value} - {result.oracle_level.value} "
                    f"(准确度: {result.accuracy:.1%})",
                    MessageType.INFO
                )

# 全局AI占卜系统实例
ai_divination_system = AIDivinationSystem()

# 便捷函数
def perform_divination(player_name: str, divination_type: DivinationType,
                      game_state: GameState, specific_query: str = "") -> DivinationResult:
    """执行占卜"""
    return ai_divination_system.perform_divination(player_name, divination_type, game_state, specific_query)

def display_divination_result(result: DivinationResult):
    """显示占卜结果"""
    ai_divination_system.display_divination_result(result)

def display_divination_history(player_name: str):
    """显示占卜历史"""
    ai_divination_system.display_divination_history(player_name)

def get_divination_history(player_name: str) -> Optional[DivinationHistory]:
    """获取占卜历史"""
    return ai_divination_system.get_player_divination_history(player_name)