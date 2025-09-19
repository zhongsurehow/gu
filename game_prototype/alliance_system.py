"""
盟约系统 - 盟约与背叛机制
实现玩家间的正式协议、约束和外交博弈
"""

import time
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from advanced_ui_system import advanced_ui, MessageType

class AllianceType(Enum):
    """盟约类型"""
    TRADE = "通商协定"          # 资源交换
    NON_AGGRESSION = "互不侵犯"  # 不能攻击对方区域
    MUTUAL_DEFENSE = "共同防御"  # 互相保护
    INFORMATION = "情报共享"     # 分享信息
    JOINT_VENTURE = "合作开发"   # 共同控制区域
    TRIBUTE = "朝贡关系"        # 单方面资源供给

class AllianceStatus(Enum):
    """盟约状态"""
    PROPOSED = "提议中"
    ACTIVE = "生效中"
    VIOLATED = "已违背"
    EXPIRED = "已过期"
    TERMINATED = "已终止"

class ViolationType(Enum):
    """违约类型"""
    DIRECT_ATTACK = "直接攻击"
    RESOURCE_THEFT = "资源掠夺"
    INFORMATION_LEAK = "情报泄露"
    TERRITORY_INVASION = "领土入侵"
    BETRAYAL = "主动背叛"

@dataclass
class AllianceTerms:
    """盟约条款"""
    resource_exchange: Dict[str, int] = field(default_factory=dict)  # 资源交换
    territory_restrictions: List[str] = field(default_factory=list)  # 领土限制
    information_sharing: bool = False                                # 是否共享信息
    mutual_defense: bool = False                                     # 是否互相防御
    tribute_amount: Dict[str, int] = field(default_factory=dict)     # 朝贡数量
    special_conditions: List[str] = field(default_factory=list)      # 特殊条件

@dataclass
class Alliance:
    """盟约"""
    alliance_id: str
    alliance_type: AllianceType
    participants: List[str]
    terms: AllianceTerms
    duration: int  # 持续回合数
    status: AllianceStatus = AllianceStatus.PROPOSED
    created_turn: int = 0
    expires_turn: int = 0
    violation_count: int = 0
    trust_level: float = 1.0  # 信任度 0.0-1.0
    
    def __post_init__(self):
        self.expires_turn = self.created_turn + self.duration

@dataclass
class Violation:
    """违约记录"""
    violator: str
    victim: str
    violation_type: ViolationType
    alliance_id: str
    turn: int
    severity: float  # 严重程度 0.0-1.0
    description: str
    penalty_applied: bool = False

@dataclass
class Reputation:
    """声誉系统"""
    player_name: str
    trustworthiness: float = 100.0  # 可信度 0-100
    alliance_count: int = 0         # 盟约总数
    violation_count: int = 0        # 违约次数
    betrayal_count: int = 0         # 背叛次数
    honor_points: int = 0           # 荣誉点数
    
    def get_reputation_level(self) -> str:
        """获取声誉等级"""
        if self.trustworthiness >= 90:
            return "圣贤"
        elif self.trustworthiness >= 75:
            return "君子"
        elif self.trustworthiness >= 50:
            return "常人"
        elif self.trustworthiness >= 25:
            return "小人"
        else:
            return "奸佞"

class AllianceSystem:
    """盟约系统"""
    
    def __init__(self):
        self.alliances: Dict[str, Alliance] = {}
        self.violations: List[Violation] = []
        self.reputations: Dict[str, Reputation] = {}
        self.current_turn = 0
        self.alliance_counter = 0
        self.negotiation_history: List[Dict] = []
        
    def initialize_player_reputation(self, player_name: str):
        """初始化玩家声誉"""
        if player_name not in self.reputations:
            self.reputations[player_name] = Reputation(player_name)
    
    def propose_alliance(self, proposer: str, target: str, alliance_type: AllianceType, 
                        terms: AllianceTerms, duration: int) -> str:
        """提议盟约"""
        self.alliance_counter += 1
        alliance_id = f"alliance_{self.alliance_counter}"
        
        alliance = Alliance(
            alliance_id=alliance_id,
            alliance_type=alliance_type,
            participants=[proposer, target],
            terms=terms,
            duration=duration,
            created_turn=self.current_turn,
            status=AllianceStatus.PROPOSED
        )
        
        self.alliances[alliance_id] = alliance
        
        # 记录谈判历史
        self.negotiation_history.append({
            "turn": self.current_turn,
            "action": "propose",
            "proposer": proposer,
            "target": target,
            "type": alliance_type.value,
            "alliance_id": alliance_id
        })
        
        advanced_ui.display_mystical_message(
            f"{proposer} 向 {target} 提议 {alliance_type.value}\n"
            f"持续时间：{duration} 回合\n"
            f"条款：{self._format_terms(terms)}",
            "盟约提议"
        )
        
        return alliance_id
    
    def respond_to_alliance(self, alliance_id: str, responder: str, accept: bool, 
                           counter_terms: Optional[AllianceTerms] = None) -> bool:
        """回应盟约提议"""
        alliance = self.alliances.get(alliance_id)
        if not alliance or alliance.status != AllianceStatus.PROPOSED:
            return False
        
        if responder not in alliance.participants:
            return False
        
        if accept:
            alliance.status = AllianceStatus.ACTIVE
            alliance.expires_turn = self.current_turn + alliance.duration
            
            # 更新声誉
            for participant in alliance.participants:
                self.initialize_player_reputation(participant)
                self.reputations[participant].alliance_count += 1
            
            advanced_ui.display_mystical_message(
                f"{responder} 接受了盟约提议！\n"
                f"{alliance.alliance_type.value} 正式生效",
                "盟约成立"
            )
            
            # 记录谈判历史
            self.negotiation_history.append({
                "turn": self.current_turn,
                "action": "accept",
                "responder": responder,
                "alliance_id": alliance_id
            })
            
            return True
        else:
            if counter_terms:
                # 提出反提议
                alliance.terms = counter_terms
                advanced_ui.display_mystical_message(
                    f"{responder} 提出了修改条款的反提议",
                    "盟约谈判"
                )
            else:
                # 拒绝盟约
                alliance.status = AllianceStatus.TERMINATED
                advanced_ui.display_mystical_message(
                    f"{responder} 拒绝了盟约提议",
                    "盟约拒绝"
                )
            
            return False
    
    def violate_alliance(self, violator: str, victim: str, violation_type: ViolationType, 
                        alliance_id: str, description: str = "") -> bool:
        """违反盟约"""
        alliance = self.alliances.get(alliance_id)
        if not alliance or alliance.status != AllianceStatus.ACTIVE:
            return False
        
        if violator not in alliance.participants or victim not in alliance.participants:
            return False
        
        # 计算违约严重程度
        severity = self._calculate_violation_severity(violation_type, alliance)
        
        violation = Violation(
            violator=violator,
            victim=victim,
            violation_type=violation_type,
            alliance_id=alliance_id,
            turn=self.current_turn,
            severity=severity,
            description=description
        )
        
        self.violations.append(violation)
        alliance.violation_count += 1
        alliance.trust_level *= (1 - severity * 0.3)  # 降低信任度
        
        # 如果违约严重，盟约可能破裂
        if severity > 0.7 or alliance.violation_count >= 3:
            alliance.status = AllianceStatus.VIOLATED
        
        # 更新声誉
        self.initialize_player_reputation(violator)
        self.reputations[violator].violation_count += 1
        self.reputations[violator].trustworthiness -= severity * 20
        
        advanced_ui.display_mystical_message(
            f"{violator} 违反了与 {victim} 的盟约！\n"
            f"违约类型：{violation_type.value}\n"
            f"严重程度：{severity:.1f}\n"
            f"盟约信任度降至：{alliance.trust_level:.2f}",
            "盟约违背",
            MessageType.ERROR
        )
        
        return True
    
    def betray_alliance(self, betrayer: str, alliance_id: str, reason: str = "") -> Dict[str, Any]:
        """主动背叛盟约"""
        alliance = self.alliances.get(alliance_id)
        if not alliance or alliance.status != AllianceStatus.ACTIVE:
            return {"success": False, "message": "盟约不存在或已失效"}
        
        if betrayer not in alliance.participants:
            return {"success": False, "message": "你不是此盟约的参与者"}
        
        # 背叛的代价
        self.initialize_player_reputation(betrayer)
        reputation = self.reputations[betrayer]
        
        # 计算背叛代价
        betrayal_cost = {
            "cheng_yi": min(reputation.honor_points, 10),  # 失去荣誉点数
            "trustworthiness": 30,  # 失去可信度
            "qi": 5  # 失去气
        }
        
        # 应用背叛代价
        reputation.betrayal_count += 1
        reputation.trustworthiness -= betrayal_cost["trustworthiness"]
        reputation.honor_points -= betrayal_cost["cheng_yi"]
        
        # 盟约状态变更
        alliance.status = AllianceStatus.VIOLATED
        
        # 触发背叛事件
        betrayal_event = self._trigger_betrayal_event(betrayer, alliance)
        
        advanced_ui.display_mystical_message(
            f"{betrayer} 主动背叛了盟约！\n"
            f"理由：{reason}\n"
            f"代价：失去 {betrayal_cost['cheng_yi']} 荣誉点数，"
            f"可信度降低 {betrayal_cost['trustworthiness']} 点\n"
            f"触发事件：{betrayal_event['name']}",
            "背叛行为",
            MessageType.ERROR
        )
        
        return {
            "success": True,
            "cost": betrayal_cost,
            "event": betrayal_event,
            "new_reputation": reputation.get_reputation_level()
        }
    
    def _trigger_betrayal_event(self, betrayer: str, alliance: Alliance) -> Dict[str, Any]:
        """触发背叛事件"""
        events = [
            {
                "name": "天谴",
                "description": "背叛者在接下来的3回合内，所有行动消耗额外1点AP",
                "effect": "action_cost_increase",
                "duration": 3
            },
            {
                "name": "众叛亲离",
                "description": "其他玩家对背叛者的怀疑度大幅增加",
                "effect": "suspicion_increase",
                "amount": 50
            },
            {
                "name": "信誉破产",
                "description": "背叛者无法在接下来的5回合内提议新的盟约",
                "effect": "alliance_ban",
                "duration": 5
            }
        ]
        
        import random
        return random.choice(events)
    
    def _calculate_violation_severity(self, violation_type: ViolationType, alliance: Alliance) -> float:
        """计算违约严重程度"""
        base_severity = {
            ViolationType.DIRECT_ATTACK: 0.9,
            ViolationType.RESOURCE_THEFT: 0.6,
            ViolationType.INFORMATION_LEAK: 0.4,
            ViolationType.TERRITORY_INVASION: 0.8,
            ViolationType.BETRAYAL: 1.0
        }
        
        severity = base_severity.get(violation_type, 0.5)
        
        # 根据盟约类型调整严重程度
        if alliance.alliance_type == AllianceType.NON_AGGRESSION and violation_type == ViolationType.DIRECT_ATTACK:
            severity = 1.0
        elif alliance.alliance_type == AllianceType.TRADE and violation_type == ViolationType.RESOURCE_THEFT:
            severity = 0.9
        
        return min(1.0, severity)
    
    def _format_terms(self, terms: AllianceTerms) -> str:
        """格式化盟约条款"""
        formatted = []
        
        if terms.resource_exchange:
            exchange_str = ", ".join([f"{k}:{v}" for k, v in terms.resource_exchange.items()])
            formatted.append(f"资源交换: {exchange_str}")
        
        if terms.territory_restrictions:
            formatted.append(f"领土限制: {', '.join(terms.territory_restrictions)}")
        
        if terms.information_sharing:
            formatted.append("情报共享")
        
        if terms.mutual_defense:
            formatted.append("共同防御")
        
        if terms.tribute_amount:
            tribute_str = ", ".join([f"{k}:{v}" for k, v in terms.tribute_amount.items()])
            formatted.append(f"朝贡: {tribute_str}")
        
        if terms.special_conditions:
            formatted.append(f"特殊条件: {', '.join(terms.special_conditions)}")
        
        return "; ".join(formatted) if formatted else "无特殊条款"
    
    def update_turn(self, turn: int):
        """更新回合"""
        self.current_turn = turn
        
        # 检查盟约到期
        for alliance in self.alliances.values():
            if alliance.status == AllianceStatus.ACTIVE and turn >= alliance.expires_turn:
                alliance.status = AllianceStatus.EXPIRED
                advanced_ui.display_mystical_message(
                    f"{alliance.alliance_type.value} 已到期",
                    "盟约到期"
                )
    
    def get_active_alliances(self, player_name: str) -> List[Alliance]:
        """获取玩家的活跃盟约"""
        return [
            alliance for alliance in self.alliances.values()
            if alliance.status == AllianceStatus.ACTIVE and player_name in alliance.participants
        ]
    
    def get_reputation_summary(self, player_name: str) -> str:
        """获取声誉摘要"""
        self.initialize_player_reputation(player_name)
        reputation = self.reputations[player_name]
        
        summary = f"""
        声誉档案 - {player_name}
        ═══════════════════════
        声誉等级：{reputation.get_reputation_level()}
        可信度：{reputation.trustworthiness:.1f}/100
        荣誉点数：{reputation.honor_points}
        
        历史记录：
        • 盟约总数：{reputation.alliance_count}
        • 违约次数：{reputation.violation_count}
        • 背叛次数：{reputation.betrayal_count}
        """
        
        return summary
    
    def display_alliance_status(self, player_name: str):
        """显示盟约状态"""
        active_alliances = self.get_active_alliances(player_name)
        
        if not active_alliances:
            advanced_ui.print_colored("你目前没有活跃的盟约", MessageType.INFO)
            return
        
        advanced_ui.print_colored("活跃盟约：", MessageType.HIGHLIGHT)
        for alliance in active_alliances:
            other_participants = [p for p in alliance.participants if p != player_name]
            remaining_turns = alliance.expires_turn - self.current_turn
            
            advanced_ui.print_colored(
                f"• {alliance.alliance_type.value} 与 {', '.join(other_participants)}\n"
                f"  剩余回合：{remaining_turns}，信任度：{alliance.trust_level:.2f}\n"
                f"  条款：{self._format_terms(alliance.terms)}",
                MessageType.INFO
            )
    
    def can_propose_alliance(self, player_name: str) -> bool:
        """检查是否可以提议盟约"""
        self.initialize_player_reputation(player_name)
        reputation = self.reputations[player_name]
        
        # 检查是否被禁止提议盟约
        recent_betrayals = [v for v in self.violations 
                          if v.violator == player_name 
                          and v.violation_type == ViolationType.BETRAYAL
                          and self.current_turn - v.turn < 5]
        
        return len(recent_betrayals) == 0 and reputation.trustworthiness > 10

# 全局盟约系统实例
alliance_system = AllianceSystem()

# 便捷函数
def propose_alliance(proposer: str, target: str, alliance_type: AllianceType, 
                    terms: AllianceTerms, duration: int) -> str:
    """提议盟约"""
    return alliance_system.propose_alliance(proposer, target, alliance_type, terms, duration)

def respond_to_alliance(alliance_id: str, responder: str, accept: bool, 
                       counter_terms: Optional[AllianceTerms] = None) -> bool:
    """回应盟约"""
    return alliance_system.respond_to_alliance(alliance_id, responder, accept, counter_terms)

def betray_alliance(betrayer: str, alliance_id: str, reason: str = "") -> Dict[str, Any]:
    """背叛盟约"""
    return alliance_system.betray_alliance(betrayer, alliance_id, reason)

def violate_alliance(violator: str, victim: str, violation_type: ViolationType, 
                    alliance_id: str, description: str = "") -> bool:
    """违反盟约"""
    return alliance_system.violate_alliance(violator, victim, violation_type, alliance_id, description)

def display_alliance_status(player_name: str):
    """显示盟约状态"""
    alliance_system.display_alliance_status(player_name)

def get_reputation_summary(player_name: str) -> str:
    """获取声誉摘要"""
    return alliance_system.get_reputation_summary(player_name)

def update_alliance_turn(turn: int):
    """更新盟约系统回合"""
    alliance_system.update_turn(turn)