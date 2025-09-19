"""
欺骗和隐藏信息系统
实现游戏中的信息不对称和心理博弈机制
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set
from enum import Enum
import random

class InformationType(Enum):
    """信息类型"""
    HAND_CARDS = "手牌"
    RESOURCES = "资源"
    INTENTIONS = "意图"
    ALLIANCES = "联盟"
    STRATEGIES = "策略"

class DeceptionLevel(Enum):
    """欺骗等级"""
    HONEST = "诚实"
    MISLEADING = "误导"
    DECEPTIVE = "欺骗"
    MASTER_DECEIVER = "欺骗大师"

@dataclass
class HiddenInformation:
    """隐藏信息"""
    info_type: InformationType
    real_value: Any
    displayed_value: Any
    deception_level: int
    duration: int  # 持续回合数
    target_players: Set[str] = field(default_factory=set)  # 针对特定玩家

@dataclass
class PlayerPerception:
    """玩家认知"""
    player_id: str
    perceived_info: Dict[str, Any] = field(default_factory=dict)
    trust_level: int = 50  # 信任度 0-100
    suspicion_level: int = 0  # 怀疑度 0-100
    last_interaction: Optional[str] = None

class DeceptionSystem:
    """欺骗系统"""
    
    def __init__(self):
        self.hidden_info: Dict[str, List[HiddenInformation]] = {}
        self.player_perceptions: Dict[str, Dict[str, PlayerPerception]] = {}
        self.deception_history: List[Dict[str, Any]] = []
    
    def initialize_player(self, player_id: str, other_players: List[str]):
        """初始化玩家的欺骗状态"""
        self.hidden_info[player_id] = []
        self.player_perceptions[player_id] = {}
        
        for other_player in other_players:
            if other_player != player_id:
                self.player_perceptions[player_id][other_player] = PlayerPerception(
                    player_id=other_player
                )
    
    def create_deception(self, deceiver: str, info_type: InformationType,
                        real_value: Any, fake_value: Any,
                        target_players: Optional[List[str]] = None,
                        duration: int = 3) -> bool:
        """创建欺骗信息"""
        if deceiver not in self.hidden_info:
            return False
        
        target_set = set(target_players) if target_players else set()
        
        hidden_info = HiddenInformation(
            info_type=info_type,
            real_value=real_value,
            displayed_value=fake_value,
            deception_level=self._calculate_deception_difficulty(real_value, fake_value),
            duration=duration,
            target_players=target_set
        )
        
        self.hidden_info[deceiver].append(hidden_info)
        
        # 记录欺骗历史
        self.deception_history.append({
            "deceiver": deceiver,
            "type": info_type.value,
            "targets": list(target_set),
            "turn": self._get_current_turn()
        })
        
        return True
    
    def _calculate_deception_difficulty(self, real_value: Any, fake_value: Any) -> int:
        """计算欺骗难度"""
        # 根据真实值和虚假值的差异计算难度
        if isinstance(real_value, (int, float)) and isinstance(fake_value, (int, float)):
            diff_ratio = abs(real_value - fake_value) / max(real_value, 1)
            if diff_ratio < 0.2:
                return 1  # 轻微欺骗
            elif diff_ratio < 0.5:
                return 2  # 中等欺骗
            else:
                return 3  # 重大欺骗
        return 2  # 默认中等难度
    
    def get_perceived_info(self, observer: str, target: str, 
                          info_type: InformationType) -> Any:
        """获取观察者对目标的认知信息"""
        if target not in self.hidden_info:
            return None
        
        # 查找针对观察者的欺骗信息
        for hidden_info in self.hidden_info[target]:
            if hidden_info.info_type == info_type:
                if not hidden_info.target_players or observer in hidden_info.target_players:
                    # 检查是否被识破
                    if self._is_deception_detected(observer, target, hidden_info):
                        return hidden_info.real_value
                    else:
                        return hidden_info.displayed_value
        
        # 没有欺骗信息，返回真实信息
        return self._get_real_info(target, info_type)
    
    def _is_deception_detected(self, observer: str, target: str,
                              hidden_info: HiddenInformation) -> bool:
        """检查欺骗是否被识破"""
        if observer not in self.player_perceptions:
            return False
        
        if target not in self.player_perceptions[observer]:
            return False
        
        perception = self.player_perceptions[observer][target]
        
        # 基于信任度和怀疑度计算识破概率
        detection_chance = (perception.suspicion_level - perception.trust_level) / 100
        detection_chance += hidden_info.deception_level * 0.1
        detection_chance = max(0, min(1, detection_chance))
        
        return random.random() < detection_chance
    
    def _get_real_info(self, player_id: str, info_type: InformationType) -> Any:
        """获取真实信息（需要与游戏状态集成）"""
        # 这里需要与实际的游戏状态系统集成
        return None
    
    def update_trust(self, observer: str, target: str, change: int):
        """更新信任度"""
        if observer in self.player_perceptions and target in self.player_perceptions[observer]:
            perception = self.player_perceptions[observer][target]
            perception.trust_level = max(0, min(100, perception.trust_level + change))
            
            # 信任度变化影响怀疑度
            if change < 0:
                perception.suspicion_level = min(100, perception.suspicion_level - change)
    
    def update_suspicion(self, observer: str, target: str, change: int):
        """更新怀疑度"""
        if observer in self.player_perceptions and target in self.player_perceptions[observer]:
            perception = self.player_perceptions[observer][target]
            perception.suspicion_level = max(0, min(100, perception.suspicion_level + change))
    
    def reveal_deception(self, deceiver: str, info_type: InformationType,
                        revealer: Optional[str] = None) -> Dict[str, Any]:
        """揭露欺骗"""
        if deceiver not in self.hidden_info:
            return {"success": False, "message": "目标玩家无欺骗信息"}
        
        revealed_info = None
        for i, hidden_info in enumerate(self.hidden_info[deceiver]):
            if hidden_info.info_type == info_type:
                revealed_info = self.hidden_info[deceiver].pop(i)
                break
        
        if not revealed_info:
            return {"success": False, "message": "未找到对应的欺骗信息"}
        
        # 影响声誉和信任度
        reputation_loss = revealed_info.deception_level * 10
        
        # 更新所有玩家对欺骗者的信任度
        for observer_id in self.player_perceptions:
            if deceiver in self.player_perceptions[observer_id]:
                self.update_trust(observer_id, deceiver, -reputation_loss)
        
        return {
            "success": True,
            "message": f"揭露了{deceiver}的{info_type.value}欺骗",
            "real_value": revealed_info.real_value,
            "fake_value": revealed_info.displayed_value,
            "reputation_loss": reputation_loss,
            "revealer": revealer
        }
    
    def process_turn_end(self):
        """处理回合结束时的欺骗信息更新"""
        for player_id in self.hidden_info:
            # 减少欺骗信息的持续时间
            self.hidden_info[player_id] = [
                info for info in self.hidden_info[player_id]
                if self._update_duration(info)
            ]
    
    def _update_duration(self, hidden_info: HiddenInformation) -> bool:
        """更新持续时间，返回是否保留"""
        hidden_info.duration -= 1
        return hidden_info.duration > 0
    
    def _get_current_turn(self) -> int:
        """获取当前回合数（需要与游戏状态集成）"""
        return len(self.deception_history)
    
    def get_deception_summary(self, player_id: str) -> Dict[str, Any]:
        """获取玩家的欺骗状态摘要"""
        if player_id not in self.hidden_info:
            return {}
        
        active_deceptions = len(self.hidden_info[player_id])
        deception_types = [info.info_type.value for info in self.hidden_info[player_id]]
        
        # 计算平均信任度
        avg_trust = 0
        if player_id in self.player_perceptions:
            trust_values = [p.trust_level for p in self.player_perceptions[player_id].values()]
            avg_trust = sum(trust_values) / len(trust_values) if trust_values else 50
        
        return {
            "active_deceptions": active_deceptions,
            "deception_types": deception_types,
            "average_trust": avg_trust,
            "deception_history_count": len([
                h for h in self.deception_history if h["deceiver"] == player_id
            ])
        }

# 全局实例
deception_system = DeceptionSystem()