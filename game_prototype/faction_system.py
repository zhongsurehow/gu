"""
阵营系统 - 秘密身份和阵营对抗
实现类似"狼人杀"的隐藏信息和社交推理元素
"""

import random
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass
from advanced_ui_system import advanced_ui, MessageType

class FactionType(Enum):
    """阵营类型"""
    REVOLUTIONARY = "革新派"    # 目标：改变所有区域控制权
    GUARDIAN = "守护者"        # 目标：保持区域控制权不变
    INDIVIDUALIST = "利己者"   # 目标：个人胜利
    HARMONIST = "调和者"       # 目标：维持平衡
    EXPANSIONIST = "扩张者"    # 目标：控制最多区域

class SecretRole(Enum):
    """秘密角色"""
    PROPHET = "先知"           # 可以窥探他人身份
    SABOTEUR = "破坏者"       # 可以干扰他人行动
    DIPLOMAT = "外交官"       # 盟约相关能力增强
    SPY = "间谍"              # 可以获得额外信息
    LEADER = "领袖"           # 阵营胜利时获得额外奖励

@dataclass
class FactionGoal:
    """阵营目标"""
    name: str
    description: str
    check_condition: callable  # 检查胜利条件的函数
    reward_points: int         # 胜利奖励点数

@dataclass
class SecretMission:
    """秘密任务"""
    name: str
    description: str
    faction: FactionType
    progress: int = 0
    target: int = 1
    completed: bool = False
    reward: Dict[str, int] = None

class FactionIdentity:
    """阵营身份"""
    
    def __init__(self, faction: FactionType, role: SecretRole, player_name: str):
        self.faction = faction
        self.role = role
        self.player_name = player_name
        self.revealed = False
        self.loyalty_points = 0
        self.secret_missions: List[SecretMission] = []
        self.known_identities: Set[str] = set()  # 已知的其他玩家身份
        self.suspicion_levels: Dict[str, int] = {}  # 对其他玩家的怀疑度
        
    def add_suspicion(self, target_player: str, amount: int):
        """增加对某玩家的怀疑度"""
        if target_player not in self.suspicion_levels:
            self.suspicion_levels[target_player] = 0
        self.suspicion_levels[target_player] = min(100, self.suspicion_levels[target_player] + amount)
    
    def reveal_identity(self):
        """揭示身份"""
        self.revealed = True
        advanced_ui.display_mystical_message(
            f"{self.player_name} 的真实身份是：{self.faction.value} - {self.role.value}",
            "身份揭露"
        )

class FactionSystem:
    """阵营系统"""
    
    def __init__(self):
        self.player_identities: Dict[str, FactionIdentity] = {}
        self.faction_goals = self._create_faction_goals()
        self.game_phase = "hidden"  # hidden, revealed, endgame
        self.faction_scores: Dict[FactionType, int] = {}
        self.turn_actions: List[Tuple[str, str, Dict]] = []  # 记录玩家行动用于推理
        
    def _create_faction_goals(self) -> Dict[FactionType, FactionGoal]:
        """创建阵营目标"""
        goals = {}
        
        goals[FactionType.REVOLUTIONARY] = FactionGoal(
            "天下大变",
            "游戏结束时，所有区域的控制者与游戏开始时完全不同",
            self._check_revolutionary_victory,
            50
        )
        
        goals[FactionType.GUARDIAN] = FactionGoal(
            "守护传统",
            "游戏结束时，至少70%的区域控制权没有发生变化",
            self._check_guardian_victory,
            40
        )
        
        goals[FactionType.INDIVIDUALIST] = FactionGoal(
            "独善其身",
            "获得最高的个人分数，不依赖阵营胜利",
            self._check_individualist_victory,
            60
        )
        
        goals[FactionType.HARMONIST] = FactionGoal(
            "天下太平",
            "游戏结束时，所有玩家的资源差距最小",
            self._check_harmonist_victory,
            45
        )
        
        goals[FactionType.EXPANSIONIST] = FactionGoal(
            "开疆拓土",
            "控制最多的区域",
            self._check_expansionist_victory,
            55
        )
        
        return goals
    
    def assign_identities(self, players: List[str]):
        """为玩家分配身份"""
        factions = list(FactionType)
        roles = list(SecretRole)
        
        # 确保每个阵营至少有一个玩家
        assigned_factions = []
        for i, player in enumerate(players):
            if i < len(factions):
                faction = factions[i]
            else:
                faction = random.choice(factions)
            
            role = random.choice(roles)
            identity = FactionIdentity(faction, role, player)
            
            # 分配秘密任务
            identity.secret_missions = self._generate_secret_missions(faction, player)
            
            self.player_identities[player] = identity
            assigned_factions.append(faction)
        
        # 初始化阵营分数
        for faction in set(assigned_factions):
            self.faction_scores[faction] = 0
        
        # 为特定角色提供初始信息
        self._provide_initial_information()
    
    def _generate_secret_missions(self, faction: FactionType, player_name: str) -> List[SecretMission]:
        """生成秘密任务"""
        missions = []
        
        if faction == FactionType.REVOLUTIONARY:
            missions.append(SecretMission(
                "颠覆秩序",
                "成功夺取3个不同区域的控制权",
                faction,
                target=3,
                reward={"dao_xing": 5, "cheng_yi": 3}
            ))
        
        elif faction == FactionType.GUARDIAN:
            missions.append(SecretMission(
                "坚守阵地",
                "保护己方控制的区域不被夺取，持续5回合",
                faction,
                target=5,
                reward={"qi": 10, "cheng_yi": 5}
            ))
        
        elif faction == FactionType.INDIVIDUALIST:
            missions.append(SecretMission(
                "独占鳌头",
                "在某项资源上领先所有其他玩家",
                faction,
                target=1,
                reward={"dao_xing": 8}
            ))
        
        elif faction == FactionType.HARMONIST:
            missions.append(SecretMission(
                "调和阴阳",
                "帮助其他玩家达到阴阳平衡状态3次",
                faction,
                target=3,
                reward={"cheng_yi": 8}
            ))
        
        elif faction == FactionType.EXPANSIONIST:
            missions.append(SecretMission(
                "征服四方",
                "同时控制4个或以上区域",
                faction,
                target=1,
                reward={"dao_xing": 10}
            ))
        
        return missions
    
    def _provide_initial_information(self):
        """为特定角色提供初始信息"""
        for player_name, identity in self.player_identities.items():
            if identity.role == SecretRole.PROPHET:
                # 先知可以知道一个其他玩家的阵营
                other_players = [p for p in self.player_identities.keys() if p != player_name]
                if other_players:
                    target = random.choice(other_players)
                    target_faction = self.player_identities[target].faction
                    identity.known_identities.add(f"{target}:{target_faction.value}")
            
            elif identity.role == SecretRole.SPY:
                # 间谍可以知道所有阵营的分布情况
                faction_counts = {}
                for other_identity in self.player_identities.values():
                    faction = other_identity.faction
                    faction_counts[faction] = faction_counts.get(faction, 0) + 1
                identity.known_identities.add(f"faction_distribution:{faction_counts}")
    
    def record_action(self, player_name: str, action: str, details: Dict):
        """记录玩家行动用于推理"""
        self.turn_actions.append((player_name, action, details))
        
        # 基于行动更新怀疑度
        self._update_suspicion_based_on_action(player_name, action, details)
    
    def _update_suspicion_based_on_action(self, player_name: str, action: str, details: Dict):
        """基于行动更新怀疑度"""
        player_identity = self.player_identities.get(player_name)
        if not player_identity:
            return
        
        # 分析行动模式
        if action == "夺取区域":
            # 夺取区域的行为可能暴露革新派身份
            for other_name, other_identity in self.player_identities.items():
                if other_name != player_name:
                    if other_identity.faction == FactionType.GUARDIAN:
                        other_identity.add_suspicion(player_name, 10)
        
        elif action == "保护区域":
            # 保护区域的行为可能暴露守护者身份
            for other_name, other_identity in self.player_identities.items():
                if other_name != player_name:
                    if other_identity.faction == FactionType.REVOLUTIONARY:
                        other_identity.add_suspicion(player_name, 8)
    
    def use_role_ability(self, player_name: str, target_player: str = None) -> Dict[str, Any]:
        """使用角色能力"""
        identity = self.player_identities.get(player_name)
        if not identity:
            return {"success": False, "message": "身份不明"}
        
        result = {"success": False, "message": ""}
        
        if identity.role == SecretRole.PROPHET and target_player:
            # 先知能力：窥探身份
            target_identity = self.player_identities.get(target_player)
            if target_identity:
                identity.known_identities.add(f"{target_player}:{target_identity.faction.value}")
                result = {
                    "success": True,
                    "message": f"你窥探到 {target_player} 的阵营是：{target_identity.faction.value}",
                    "revealed_info": target_identity.faction.value
                }
        
        elif identity.role == SecretRole.SABOTEUR and target_player:
            # 破坏者能力：干扰行动
            result = {
                "success": True,
                "message": f"你对 {target_player} 的下一个行动造成了干扰",
                "effect": "next_action_cost_increase"
            }
        
        elif identity.role == SecretRole.DIPLOMAT:
            # 外交官能力：盟约增强
            result = {
                "success": True,
                "message": "你的外交能力使盟约效果增强",
                "effect": "alliance_enhancement"
            }
        
        elif identity.role == SecretRole.SPY:
            # 间谍能力：获取信息
            recent_actions = self.turn_actions[-3:]  # 最近3个行动
            result = {
                "success": True,
                "message": "你获得了最近的行动情报",
                "intelligence": recent_actions
            }
        
        elif identity.role == SecretRole.LEADER:
            # 领袖能力：激励同阵营
            same_faction_players = [
                name for name, other_identity in self.player_identities.items()
                if other_identity.faction == identity.faction and name != player_name
            ]
            result = {
                "success": True,
                "message": f"你激励了同阵营的成员",
                "affected_players": same_faction_players,
                "effect": "faction_bonus"
            }
        
        return result
    
    def trigger_identity_crisis(self, game_state) -> Optional[str]:
        """触发身份危机事件"""
        if self.game_phase != "hidden":
            return None
        
        # 随机选择一个玩家面临身份暴露的风险
        player_name = random.choice(list(self.player_identities.keys()))
        identity = self.player_identities[player_name]
        
        crisis_text = f"""
        {player_name} 面临身份危机！
        
        由于最近的行动，你的身份可能被其他玩家怀疑。
        你可以选择：
        
        1. 主动揭示身份，获得阵营奖励
        2. 继续隐藏，但怀疑度增加
        3. 使用角色能力转移注意力
        """
        
        return crisis_text
    
    def check_faction_victories(self, game_state) -> Dict[FactionType, bool]:
        """检查阵营胜利条件"""
        victories = {}
        
        for faction, goal in self.faction_goals.items():
            victories[faction] = goal.check_condition(game_state)
        
        return victories
    
    def _check_revolutionary_victory(self, game_state) -> bool:
        """检查革新派胜利条件"""
        # 这里需要与游戏状态集成，检查区域控制权变化
        # 暂时返回False，需要实际游戏数据
        return False
    
    def _check_guardian_victory(self, game_state) -> bool:
        """检查守护者胜利条件"""
        # 这里需要与游戏状态集成
        return False
    
    def _check_individualist_victory(self, game_state) -> bool:
        """检查利己者胜利条件"""
        # 这里需要与游戏状态集成
        return False
    
    def _check_harmonist_victory(self, game_state) -> bool:
        """检查调和者胜利条件"""
        # 这里需要与游戏状态集成
        return False
    
    def _check_expansionist_victory(self, game_state) -> bool:
        """检查扩张者胜利条件"""
        # 这里需要与游戏状态集成
        return False
    
    def display_secret_info(self, player_name: str):
        """显示玩家的秘密信息"""
        identity = self.player_identities.get(player_name)
        if not identity:
            return
        
        advanced_ui.display_mystical_message(
            f"你的秘密身份：{identity.faction.value} - {identity.role.value}\n\n"
            f"阵营目标：{self.faction_goals[identity.faction].description}\n\n"
            f"忠诚度：{identity.loyalty_points}",
            "秘密档案"
        )
        
        # 显示已知信息
        if identity.known_identities:
            advanced_ui.print_colored("已知情报：", MessageType.MYSTICAL)
            for info in identity.known_identities:
                advanced_ui.print_colored(f"  • {info}", MessageType.INFO)
        
        # 显示怀疑度
        if identity.suspicion_levels:
            advanced_ui.print_colored("怀疑度分析：", MessageType.WARNING)
            for target, level in identity.suspicion_levels.items():
                color = MessageType.ERROR if level > 70 else MessageType.WARNING if level > 40 else MessageType.INFO
                advanced_ui.print_colored(f"  • {target}: {level}%", color)
        
        # 显示秘密任务
        if identity.secret_missions:
            advanced_ui.print_colored("秘密任务：", MessageType.HIGHLIGHT)
            for mission in identity.secret_missions:
                status = "✅ 已完成" if mission.completed else f"📋 进度 {mission.progress}/{mission.target}"
                advanced_ui.print_colored(f"  • {mission.name}: {status}", MessageType.INFO)
                advanced_ui.print_colored(f"    {mission.description}", MessageType.INFO)
    
    def get_faction_summary(self) -> str:
        """获取阵营概况"""
        summary = "阵营分布概况：\n"
        faction_counts = {}
        
        for identity in self.player_identities.values():
            faction = identity.faction
            faction_counts[faction] = faction_counts.get(faction, 0) + 1
        
        for faction, count in faction_counts.items():
            summary += f"  {faction.value}: {count}人\n"
        
        return summary

# 全局阵营系统实例
faction_system = FactionSystem()

# 便捷函数
def assign_faction_identities(players: List[str]):
    """分配阵营身份"""
    faction_system.assign_identities(players)

def record_player_action(player_name: str, action: str, details: Dict):
    """记录玩家行动"""
    faction_system.record_action(player_name, action, details)

def use_role_ability(player_name: str, target_player: str = None) -> Dict[str, Any]:
    """使用角色能力"""
    return faction_system.use_role_ability(player_name, target_player)

def display_secret_info(player_name: str):
    """显示秘密信息"""
    faction_system.display_secret_info(player_name)

def trigger_identity_crisis(game_state) -> Optional[str]:
    """触发身份危机"""
    return faction_system.trigger_identity_crisis(game_state)

def check_faction_victories(game_state) -> Dict[FactionType, bool]:
    """检查阵营胜利"""
    return faction_system.check_faction_victories(game_state)