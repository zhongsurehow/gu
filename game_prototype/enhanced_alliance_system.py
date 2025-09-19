"""
增强联盟系统
实现复杂的联盟机制，包括秘密联盟、背叛、利益分配等
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from enum import Enum
import random
from datetime import datetime

class AllianceType(Enum):
    """联盟类型"""
    PUBLIC = "公开联盟"
    SECRET = "秘密联盟"
    TEMPORARY = "临时联盟"
    TRADE = "贸易联盟"
    MILITARY = "军事联盟"

class AllianceStatus(Enum):
    """联盟状态"""
    PROPOSED = "提议中"
    ACTIVE = "活跃"
    SUSPENDED = "暂停"
    BROKEN = "破裂"
    EXPIRED = "过期"

@dataclass
class AllianceTerm:
    """联盟条款"""
    term_id: str
    description: str
    benefit_type: str  # 资源、行动、信息等
    benefit_value: int
    duration: int  # 持续回合数
    conditions: List[str] = field(default_factory=list)
    penalties: List[str] = field(default_factory=list)

@dataclass
class Alliance:
    """联盟"""
    alliance_id: str
    name: str
    alliance_type: AllianceType
    status: AllianceStatus
    members: Set[str]
    leader: Optional[str]
    terms: List[AllianceTerm]
    created_turn: int
    duration: int  # -1 表示永久
    trust_level: int = 50  # 联盟内部信任度
    secret_level: int = 0  # 保密等级 0-100
    shared_resources: Dict[str, int] = field(default_factory=dict)
    shared_information: List[str] = field(default_factory=list)
    violation_count: int = 0
    last_activity: int = 0

@dataclass
class AllianceProposal:
    """联盟提议"""
    proposal_id: str
    proposer: str
    target_members: Set[str]
    alliance_type: AllianceType
    proposed_terms: List[AllianceTerm]
    message: str
    expiry_turn: int
    responses: Dict[str, bool] = field(default_factory=dict)  # 玩家ID -> 是否同意

class EnhancedAllianceSystem:
    """增强联盟系统"""
    
    def __init__(self):
        self.alliances: Dict[str, Alliance] = {}
        self.proposals: Dict[str, AllianceProposal] = {}
        self.player_alliance_history: Dict[str, List[str]] = {}
        self.betrayal_history: Dict[str, List[Dict]] = {}
        self.current_turn = 0
    
    def propose_alliance(self, proposer: str, target_members: List[str],
                        alliance_type: AllianceType, terms: List[AllianceTerm],
                        message: str = "", duration: int = 5) -> str:
        """提议联盟"""
        proposal_id = f"proposal_{len(self.proposals)}_{self.current_turn}"
        
        proposal = AllianceProposal(
            proposal_id=proposal_id,
            proposer=proposer,
            target_members=set(target_members + [proposer]),
            alliance_type=alliance_type,
            proposed_terms=terms,
            message=message,
            expiry_turn=self.current_turn + duration
        )
        
        self.proposals[proposal_id] = proposal
        return proposal_id
    
    def respond_to_proposal(self, player_id: str, proposal_id: str, 
                           accept: bool) -> Dict[str, Any]:
        """回应联盟提议"""
        if proposal_id not in self.proposals:
            return {"success": False, "message": "提议不存在"}
        
        proposal = self.proposals[proposal_id]
        
        if player_id not in proposal.target_members:
            return {"success": False, "message": "您不在此提议的目标成员中"}
        
        proposal.responses[player_id] = accept
        
        # 检查是否所有成员都已回应
        all_responded = all(
            member in proposal.responses 
            for member in proposal.target_members
        )
        
        if all_responded:
            # 检查是否所有人都同意
            all_agreed = all(proposal.responses.values())
            
            if all_agreed:
                # 创建联盟
                alliance_id = self._create_alliance_from_proposal(proposal)
                del self.proposals[proposal_id]
                return {
                    "success": True, 
                    "message": "联盟成立",
                    "alliance_id": alliance_id
                }
            else:
                # 提议被拒绝
                del self.proposals[proposal_id]
                return {"success": True, "message": "联盟提议被拒绝"}
        
        return {"success": True, "message": "等待其他成员回应"}
    
    def _create_alliance_from_proposal(self, proposal: AllianceProposal) -> str:
        """从提议创建联盟"""
        alliance_id = f"alliance_{len(self.alliances)}_{self.current_turn}"
        
        # 确定联盟领袖（提议者或投票选出）
        leader = proposal.proposer
        
        alliance = Alliance(
            alliance_id=alliance_id,
            name=f"{proposal.alliance_type.value}_{alliance_id}",
            alliance_type=proposal.alliance_type,
            status=AllianceStatus.ACTIVE,
            members=proposal.target_members.copy(),
            leader=leader,
            terms=proposal.proposed_terms.copy(),
            created_turn=self.current_turn,
            duration=-1,  # 默认永久
            secret_level=50 if proposal.alliance_type == AllianceType.SECRET else 0
        )
        
        self.alliances[alliance_id] = alliance
        
        # 更新玩家联盟历史
        for member in alliance.members:
            if member not in self.player_alliance_history:
                self.player_alliance_history[member] = []
            self.player_alliance_history[member].append(alliance_id)
        
        return alliance_id
    
    def break_alliance(self, player_id: str, alliance_id: str, 
                      reason: str = "") -> Dict[str, Any]:
        """破坏联盟（背叛）"""
        if alliance_id not in self.alliances:
            return {"success": False, "message": "联盟不存在"}
        
        alliance = self.alliances[alliance_id]
        
        if player_id not in alliance.members:
            return {"success": False, "message": "您不是此联盟成员"}
        
        # 记录背叛历史
        betrayal_record = {
            "betrayer": player_id,
            "alliance_id": alliance_id,
            "alliance_members": list(alliance.members),
            "turn": self.current_turn,
            "reason": reason,
            "trust_penalty": self._calculate_betrayal_penalty(alliance)
        }
        
        if player_id not in self.betrayal_history:
            self.betrayal_history[player_id] = []
        self.betrayal_history[player_id].append(betrayal_record)
        
        # 移除成员
        alliance.members.remove(player_id)
        alliance.status = AllianceStatus.BROKEN
        alliance.violation_count += 1
        
        # 如果是领袖背叛，选择新领袖
        if alliance.leader == player_id and alliance.members:
            alliance.leader = list(alliance.members)[0]
        
        # 如果成员不足，解散联盟
        if len(alliance.members) < 2:
            alliance.status = AllianceStatus.BROKEN
        
        return {
            "success": True,
            "message": f"{player_id}背叛了联盟",
            "trust_penalty": betrayal_record["trust_penalty"],
            "remaining_members": list(alliance.members)
        }
    
    def _calculate_betrayal_penalty(self, alliance: Alliance) -> int:
        """计算背叛惩罚"""
        base_penalty = 20
        trust_penalty = alliance.trust_level // 10
        duration_penalty = min(10, (self.current_turn - alliance.created_turn) // 2)
        
        return base_penalty + trust_penalty + duration_penalty
    
    def share_resource(self, alliance_id: str, contributor: str,
                      resource_type: str, amount: int) -> Dict[str, Any]:
        """共享资源"""
        if alliance_id not in self.alliances:
            return {"success": False, "message": "联盟不存在"}
        
        alliance = self.alliances[alliance_id]
        
        if contributor not in alliance.members:
            return {"success": False, "message": "您不是此联盟成员"}
        
        if resource_type not in alliance.shared_resources:
            alliance.shared_resources[resource_type] = 0
        
        alliance.shared_resources[resource_type] += amount
        alliance.trust_level = min(100, alliance.trust_level + amount // 10)
        alliance.last_activity = self.current_turn
        
        return {
            "success": True,
            "message": f"向联盟贡献了{amount}{resource_type}",
            "total_shared": alliance.shared_resources[resource_type]
        }
    
    def request_alliance_support(self, alliance_id: str, requester: str,
                               support_type: str, amount: int) -> Dict[str, Any]:
        """请求联盟支援"""
        if alliance_id not in self.alliances:
            return {"success": False, "message": "联盟不存在"}
        
        alliance = self.alliances[alliance_id]
        
        if requester not in alliance.members:
            return {"success": False, "message": "您不是此联盟成员"}
        
        # 检查是否有足够的共享资源
        if support_type not in alliance.shared_resources:
            return {"success": False, "message": f"联盟没有{support_type}资源"}
        
        if alliance.shared_resources[support_type] < amount:
            return {
                "success": False, 
                "message": f"联盟{support_type}不足，当前只有{alliance.shared_resources[support_type]}"
            }
        
        # 扣除资源
        alliance.shared_resources[support_type] -= amount
        alliance.last_activity = self.current_turn
        
        return {
            "success": True,
            "message": f"获得联盟支援{amount}{support_type}",
            "remaining": alliance.shared_resources[support_type]
        }
    
    def get_player_alliances(self, player_id: str) -> List[Dict[str, Any]]:
        """获取玩家的所有联盟"""
        player_alliances = []
        
        for alliance_id, alliance in self.alliances.items():
            if player_id in alliance.members and alliance.status == AllianceStatus.ACTIVE:
                alliance_info = {
                    "alliance_id": alliance_id,
                    "name": alliance.name,
                    "type": alliance.alliance_type.value,
                    "members": list(alliance.members),
                    "leader": alliance.leader,
                    "trust_level": alliance.trust_level,
                    "is_leader": alliance.leader == player_id,
                    "shared_resources": alliance.shared_resources.copy(),
                    "duration": alliance.duration,
                    "created_turn": alliance.created_turn
                }
                player_alliances.append(alliance_info)
        
        return player_alliances
    
    def get_alliance_opportunities(self, player_id: str) -> List[Dict[str, Any]]:
        """获取可能的联盟机会"""
        opportunities = []
        
        # 基于玩家历史和当前状态推荐联盟机会
        for other_player in self.player_alliance_history:
            if other_player != player_id:
                # 检查是否已经在联盟中
                already_allied = self._are_players_allied(player_id, other_player)
                
                if not already_allied:
                    # 计算联盟价值
                    alliance_value = self._calculate_alliance_value(player_id, other_player)
                    
                    if alliance_value > 30:  # 阈值
                        opportunities.append({
                            "potential_ally": other_player,
                            "alliance_value": alliance_value,
                            "recommended_type": self._recommend_alliance_type(player_id, other_player),
                            "trust_level": self._get_trust_between_players(player_id, other_player)
                        })
        
        return sorted(opportunities, key=lambda x: x["alliance_value"], reverse=True)
    
    def _are_players_allied(self, player1: str, player2: str) -> bool:
        """检查两个玩家是否已经结盟"""
        for alliance in self.alliances.values():
            if (alliance.status == AllianceStatus.ACTIVE and 
                player1 in alliance.members and player2 in alliance.members):
                return True
        return False
    
    def _calculate_alliance_value(self, player1: str, player2: str) -> int:
        """计算联盟价值"""
        base_value = 50
        
        # 基于背叛历史调整
        betrayal_penalty = len(self.betrayal_history.get(player2, [])) * 10
        
        # 基于共同敌人调整
        common_enemies_bonus = 0  # 需要与游戏状态集成
        
        return max(0, base_value - betrayal_penalty + common_enemies_bonus)
    
    def _recommend_alliance_type(self, player1: str, player2: str) -> AllianceType:
        """推荐联盟类型"""
        # 基于玩家特征和游戏状态推荐
        trust_level = self._get_trust_between_players(player1, player2)
        
        if trust_level > 70:
            return AllianceType.PUBLIC
        elif trust_level > 40:
            return AllianceType.TRADE
        else:
            return AllianceType.TEMPORARY
    
    def _get_trust_between_players(self, player1: str, player2: str) -> int:
        """获取玩家间信任度"""
        # 需要与欺骗系统集成
        return 50  # 默认值
    
    def process_turn_end(self):
        """处理回合结束"""
        self.current_turn += 1
        
        # 清理过期提议
        expired_proposals = [
            pid for pid, proposal in self.proposals.items()
            if proposal.expiry_turn <= self.current_turn
        ]
        
        for pid in expired_proposals:
            del self.proposals[pid]
        
        # 更新联盟状态
        for alliance in self.alliances.values():
            if alliance.duration > 0:
                alliance.duration -= 1
                if alliance.duration == 0:
                    alliance.status = AllianceStatus.EXPIRED
            
            # 降低不活跃联盟的信任度
            if self.current_turn - alliance.last_activity > 3:
                alliance.trust_level = max(0, alliance.trust_level - 5)
    
    def get_alliance_summary(self) -> Dict[str, Any]:
        """获取联盟系统摘要"""
        active_alliances = len([a for a in self.alliances.values() 
                               if a.status == AllianceStatus.ACTIVE])
        
        total_betrayals = sum(len(betrayals) for betrayals in self.betrayal_history.values())
        
        return {
            "total_alliances": len(self.alliances),
            "active_alliances": active_alliances,
            "pending_proposals": len(self.proposals),
            "total_betrayals": total_betrayals,
            "current_turn": self.current_turn
        }

# 全局实例
enhanced_alliance_system = EnhancedAllianceSystem()