"""
天机变游戏玩家数据模型
定义玩家相关的数据结构和业务逻辑
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import uuid

from ..core.base_types import (
    PlayerType, WuxingElement, BaguaType, ResourceType,
    Position, ResourceBundle, CultivationRealm
)
from ..core.interfaces import IPlayer
from ..core.constants import *

@dataclass
class PlayerStats:
    """玩家统计信息"""
    
    # 游戏统计
    games_played: int = 0
    games_won: int = 0
    games_lost: int = 0
    total_turns: int = 0
    
    # 行动统计
    successful_actions: int = 0
    failed_actions: int = 0
    special_actions_used: int = 0
    ultimate_actions_used: int = 0
    
    # 资源统计
    max_qi_achieved: int = 0
    max_wisdom_achieved: int = 0
    max_influence_achieved: int = 0
    max_culture_achieved: int = 0
    
    # 易学统计
    highest_cultivation_reached: str = "凡人"
    bagua_masteries_achieved: int = 0
    wuxing_cycles_completed: int = 0
    perfect_balance_achieved: int = 0
    
    # 时间统计
    total_play_time: float = 0.0  # 秒
    average_turn_time: float = 0.0  # 秒
    
    def update_game_result(self, won: bool, turns: int, play_time: float) -> None:
        """更新游戏结果统计"""
        self.games_played += 1
        if won:
            self.games_won += 1
        else:
            self.games_lost += 1
        
        self.total_turns += turns
        self.total_play_time += play_time
        
        if self.total_turns > 0:
            self.average_turn_time = self.total_play_time / self.total_turns
    
    def get_win_rate(self) -> float:
        """获取胜率"""
        if self.games_played == 0:
            return 0.0
        return self.games_won / self.games_played
    
    def get_success_rate(self) -> float:
        """获取行动成功率"""
        total_actions = self.successful_actions + self.failed_actions
        if total_actions == 0:
            return 0.0
        return self.successful_actions / total_actions

@dataclass
class PlayerState:
    """玩家状态信息"""
    
    # 基础状态
    is_active: bool = True
    is_online: bool = True
    is_ready: bool = False
    
    # 游戏状态
    current_position: Optional[Position] = None
    available_actions: List[str] = field(default_factory=list)
    pending_decisions: List[Dict[str, Any]] = field(default_factory=list)
    
    # 临时效果
    active_effects: Dict[str, Any] = field(default_factory=dict)
    status_conditions: List[str] = field(default_factory=list)
    
    # 回合状态
    actions_this_turn: int = 0
    max_actions_per_turn: int = DEFAULT_ACTIONS_PER_TURN
    turn_start_time: Optional[datetime] = None
    
    def can_act(self) -> bool:
        """检查是否可以行动"""
        return (
            self.is_active and 
            self.is_ready and 
            self.actions_this_turn < self.max_actions_per_turn
        )
    
    def start_turn(self) -> None:
        """开始回合"""
        self.actions_this_turn = 0
        self.turn_start_time = datetime.now()
        self.available_actions.clear()
    
    def end_turn(self) -> None:
        """结束回合"""
        self.turn_start_time = None
        self.available_actions.clear()
        self.pending_decisions.clear()
    
    def add_effect(self, effect_name: str, effect_data: Any, duration: int = -1) -> None:
        """添加临时效果"""
        self.active_effects[effect_name] = {
            "data": effect_data,
            "duration": duration,
            "applied_at": datetime.now()
        }
    
    def remove_effect(self, effect_name: str) -> bool:
        """移除临时效果"""
        return self.active_effects.pop(effect_name, None) is not None
    
    def has_effect(self, effect_name: str) -> bool:
        """检查是否有特定效果"""
        return effect_name in self.active_effects

@dataclass
class Player(IPlayer):
    """
    玩家数据模型
    
    包含玩家的所有信息：基础信息、资源、易学状态、统计等
    """
    
    # ==================== 基础信息 ====================
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "未命名玩家"
    player_type: PlayerType = PlayerType.HUMAN
    avatar: str = "default"
    color: str = "#000000"
    
    # ==================== 资源系统 ====================
    
    # 基础资源
    qi: int = INITIAL_QI  # 气
    wisdom: int = INITIAL_WISDOM  # 智慧
    influence: int = INITIAL_INFLUENCE  # 影响力
    culture: int = INITIAL_CULTURE  # 文化力
    
    # 行动点数
    action_points: int = DEFAULT_ACTION_POINTS
    max_action_points: int = DEFAULT_MAX_ACTION_POINTS
    
    # ==================== 易学系统 ====================
    
    # 阴阳系统
    yin_energy: int = INITIAL_YIN_ENERGY
    yang_energy: int = INITIAL_YANG_ENERGY
    
    # 五行掌握度
    wuxing_mastery: Dict[WuxingElement, int] = field(default_factory=lambda: {
        WuxingElement.WOOD: 0,
        WuxingElement.FIRE: 0,
        WuxingElement.EARTH: 0,
        WuxingElement.METAL: 0,
        WuxingElement.WATER: 0
    })
    
    # 八卦亲和度
    bagua_affinity: Dict[BaguaType, int] = field(default_factory=lambda: {
        BaguaType.QIAN: 0,  # 乾
        BaguaType.KUN: 0,   # 坤
        BaguaType.ZHEN: 0,  # 震
        BaguaType.XUN: 0,   # 巽
        BaguaType.KAN: 0,   # 坎
        BaguaType.LI: 0,    # 离
        BaguaType.GEN: 0,   # 艮
        BaguaType.DUI: 0    # 兑
    })
    
    # 修为境界
    cultivation_realm: CultivationRealm = CultivationRealm.MORTAL
    cultivation_progress: int = 0  # 当前境界进度
    
    # ==================== 游戏状态 ====================
    
    state: PlayerState = field(default_factory=PlayerState)
    stats: PlayerStats = field(default_factory=PlayerStats)
    
    # ==================== 时间信息 ====================
    
    created_at: datetime = field(default_factory=datetime.now)
    last_active: datetime = field(default_factory=datetime.now)
    
    # ==================== 资源管理方法 ====================
    
    def get_resource(self, resource_type: ResourceType) -> int:
        """获取指定类型的资源值"""
        resource_map = {
            ResourceType.QI: self.qi,
            ResourceType.WISDOM: self.wisdom,
            ResourceType.INFLUENCE: self.influence,
            ResourceType.CULTURE: self.culture,
            ResourceType.ACTION_POINTS: self.action_points
        }
        return resource_map.get(resource_type, 0)
    
    def set_resource(self, resource_type: ResourceType, value: int) -> None:
        """设置指定类型的资源值"""
        value = max(0, min(value, MAX_RESOURCE_VALUE))
        
        if resource_type == ResourceType.QI:
            self.qi = value
            self.stats.max_qi_achieved = max(self.stats.max_qi_achieved, value)
        elif resource_type == ResourceType.WISDOM:
            self.wisdom = value
            self.stats.max_wisdom_achieved = max(self.stats.max_wisdom_achieved, value)
        elif resource_type == ResourceType.INFLUENCE:
            self.influence = value
            self.stats.max_influence_achieved = max(self.stats.max_influence_achieved, value)
        elif resource_type == ResourceType.CULTURE:
            self.culture = value
            self.stats.max_culture_achieved = max(self.stats.max_culture_achieved, value)
        elif resource_type == ResourceType.ACTION_POINTS:
            self.action_points = min(value, self.max_action_points)
    
    def modify_resource(self, resource_type: ResourceType, amount: int) -> int:
        """修改指定类型的资源值，返回实际修改量"""
        old_value = self.get_resource(resource_type)
        new_value = old_value + amount
        self.set_resource(resource_type, new_value)
        return self.get_resource(resource_type) - old_value
    
    def can_afford(self, cost: ResourceBundle) -> bool:
        """检查是否能承担指定成本"""
        for resource_type, amount in cost.resources.items():
            if self.get_resource(resource_type) < amount:
                return False
        return True
    
    def pay_cost(self, cost: ResourceBundle) -> bool:
        """支付指定成本"""
        if not self.can_afford(cost):
            return False
        
        for resource_type, amount in cost.resources.items():
            self.modify_resource(resource_type, -amount)
        
        return True
    
    def get_resource_bundle(self) -> ResourceBundle:
        """获取当前所有资源的资源包"""
        return ResourceBundle({
            ResourceType.QI: self.qi,
            ResourceType.WISDOM: self.wisdom,
            ResourceType.INFLUENCE: self.influence,
            ResourceType.CULTURE: self.culture,
            ResourceType.ACTION_POINTS: self.action_points
        })
    
    # ==================== 易学系统方法 ====================
    
    def get_yin_yang_balance(self) -> float:
        """
        获取阴阳平衡度
        
        Returns:
            平衡度值 (0.0-1.0)，1.0表示完全平衡
        """
        total = self.yin_energy + self.yang_energy
        if total == 0:
            return 1.0
        
        min_energy = min(self.yin_energy, self.yang_energy)
        max_energy = max(self.yin_energy, self.yang_energy)
        
        if max_energy == 0:
            return 1.0
        
        return min_energy / max_energy
    
    def adjust_yin_yang(self, yin_delta: int, yang_delta: int) -> None:
        """调整阴阳能量"""
        self.yin_energy = max(0, self.yin_energy + yin_delta)
        self.yang_energy = max(0, self.yang_energy + yang_delta)
        
        # 检查是否达到完美平衡
        if abs(self.yin_energy - self.yang_energy) <= 1:
            self.stats.perfect_balance_achieved += 1
    
    def get_wuxing_total(self) -> int:
        """获取五行总掌握度"""
        return sum(self.wuxing_mastery.values())
    
    def get_dominant_wuxing(self) -> Optional[WuxingElement]:
        """获取主导五行元素"""
        if not self.wuxing_mastery:
            return None
        
        return max(self.wuxing_mastery.keys(), key=lambda x: self.wuxing_mastery[x])
    
    def improve_wuxing(self, element: WuxingElement, amount: int) -> None:
        """提升五行掌握度"""
        old_value = self.wuxing_mastery[element]
        self.wuxing_mastery[element] = min(MAX_WUXING_MASTERY, old_value + amount)
        
        # 检查是否完成五行循环
        if all(mastery >= MIN_WUXING_FOR_CYCLE for mastery in self.wuxing_mastery.values()):
            self.stats.wuxing_cycles_completed += 1
    
    def get_bagua_total(self) -> int:
        """获取八卦总亲和度"""
        return sum(self.bagua_affinity.values())
    
    def get_dominant_bagua(self) -> Optional[BaguaType]:
        """获取主导八卦"""
        if not self.bagua_affinity:
            return None
        
        return max(self.bagua_affinity.keys(), key=lambda x: self.bagua_affinity[x])
    
    def improve_bagua(self, bagua: BaguaType, amount: int) -> None:
        """提升八卦亲和度"""
        old_value = self.bagua_affinity[bagua]
        self.bagua_affinity[bagua] = min(MAX_BAGUA_AFFINITY, old_value + amount)
        
        # 检查是否达到精通
        if self.bagua_affinity[bagua] >= BAGUA_MASTERY_THRESHOLD:
            self.stats.bagua_masteries_achieved += 1
    
    def can_advance_cultivation(self) -> bool:
        """检查是否可以提升修为"""
        # 需要满足一定的易学条件
        balance_requirement = self.get_yin_yang_balance() >= CULTIVATION_BALANCE_REQUIREMENT
        wuxing_requirement = self.get_wuxing_total() >= CULTIVATION_WUXING_REQUIREMENT
        bagua_requirement = self.get_bagua_total() >= CULTIVATION_BAGUA_REQUIREMENT
        
        return balance_requirement and wuxing_requirement and bagua_requirement
    
    def advance_cultivation(self) -> bool:
        """提升修为境界"""
        if not self.can_advance_cultivation():
            return False
        
        realms = list(CultivationRealm)
        current_index = realms.index(self.cultivation_realm)
        
        if current_index < len(realms) - 1:
            self.cultivation_realm = realms[current_index + 1]
            self.cultivation_progress = 0
            
            # 更新统计
            self.stats.highest_cultivation_reached = self.cultivation_realm.value
            
            return True
        
        return False
    
    def get_cultivation_bonus(self) -> float:
        """获取修为境界加成"""
        realm_bonuses = {
            CultivationRealm.MORTAL: 1.0,
            CultivationRealm.QI_REFINING: 1.1,
            CultivationRealm.FOUNDATION: 1.2,
            CultivationRealm.GOLDEN_CORE: 1.4,
            CultivationRealm.NASCENT_SOUL: 1.6,
            CultivationRealm.SPIRIT_TRANSFORMATION: 1.8,
            CultivationRealm.VOID_REFINEMENT: 2.0,
            CultivationRealm.UNITY: 2.3,
            CultivationRealm.MAHAYANA: 2.6,
            CultivationRealm.TRIBULATION: 3.0
        }
        
        return realm_bonuses.get(self.cultivation_realm, 1.0)
    
    # ==================== 文化力量计算 ====================
    
    def calculate_cultural_power(self) -> int:
        """
        计算文化力量值
        
        综合考虑阴阳平衡、五行掌握、八卦亲和、修为境界等因素
        """
        # 基础文化力
        base_culture = self.culture
        
        # 阴阳平衡加成
        balance_bonus = int(self.get_yin_yang_balance() * YINYANG_BALANCE_BONUS * 100)
        
        # 五行掌握加成
        wuxing_bonus = int(self.get_wuxing_total() * WUXING_MASTERY_BONUS)
        
        # 八卦亲和加成
        bagua_bonus = int(self.get_bagua_total() * BAGUA_AFFINITY_BONUS)
        
        # 修为境界加成
        cultivation_bonus = int(base_culture * (self.get_cultivation_bonus() - 1.0))
        
        total_power = base_culture + balance_bonus + wuxing_bonus + bagua_bonus + cultivation_bonus
        
        return max(0, total_power)
    
    # ==================== 游戏行为方法 ====================
    
    def start_turn(self) -> None:
        """开始回合"""
        self.state.start_turn()
        self.action_points = min(self.max_action_points, self.action_points + ACTION_POINTS_PER_TURN)
    
    def end_turn(self) -> None:
        """结束回合"""
        self.state.end_turn()
        self.last_active = datetime.now()
    
    def perform_action(self, action_name: str, cost: Optional[ResourceBundle] = None) -> bool:
        """执行行动"""
        if not self.state.can_act():
            return False
        
        if cost and not self.pay_cost(cost):
            self.stats.failed_actions += 1
            return False
        
        self.state.actions_this_turn += 1
        self.stats.successful_actions += 1
        self.last_active = datetime.now()
        
        return True
    
    # ==================== 序列化方法 ====================
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "player_type": self.player_type.value,
            "avatar": self.avatar,
            "color": self.color,
            "resources": {
                "qi": self.qi,
                "wisdom": self.wisdom,
                "influence": self.influence,
                "culture": self.culture,
                "action_points": self.action_points
            },
            "yixue": {
                "yin_energy": self.yin_energy,
                "yang_energy": self.yang_energy,
                "wuxing_mastery": {elem.value: mastery for elem, mastery in self.wuxing_mastery.items()},
                "bagua_affinity": {bagua.value: affinity for bagua, affinity in self.bagua_affinity.items()},
                "cultivation_realm": self.cultivation_realm.value,
                "cultivation_progress": self.cultivation_progress
            },
            "stats": {
                "games_played": self.stats.games_played,
                "games_won": self.stats.games_won,
                "win_rate": self.stats.get_win_rate(),
                "success_rate": self.stats.get_success_rate()
            },
            "cultural_power": self.calculate_cultural_power(),
            "created_at": self.created_at.isoformat(),
            "last_active": self.last_active.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Player':
        """从字典创建玩家实例"""
        player = cls()
        
        # 基础信息
        player.id = data.get("id", player.id)
        player.name = data.get("name", player.name)
        player.player_type = PlayerType(data.get("player_type", PlayerType.HUMAN.value))
        player.avatar = data.get("avatar", player.avatar)
        player.color = data.get("color", player.color)
        
        # 资源
        resources = data.get("resources", {})
        player.qi = resources.get("qi", player.qi)
        player.wisdom = resources.get("wisdom", player.wisdom)
        player.influence = resources.get("influence", player.influence)
        player.culture = resources.get("culture", player.culture)
        player.action_points = resources.get("action_points", player.action_points)
        
        # 易学系统
        yixue = data.get("yixue", {})
        player.yin_energy = yixue.get("yin_energy", player.yin_energy)
        player.yang_energy = yixue.get("yang_energy", player.yang_energy)
        
        # 五行掌握度
        wuxing_data = yixue.get("wuxing_mastery", {})
        for elem_str, mastery in wuxing_data.items():
            try:
                element = WuxingElement(elem_str)
                player.wuxing_mastery[element] = mastery
            except ValueError:
                continue
        
        # 八卦亲和度
        bagua_data = yixue.get("bagua_affinity", {})
        for bagua_str, affinity in bagua_data.items():
            try:
                bagua = BaguaType(bagua_str)
                player.bagua_affinity[bagua] = affinity
            except ValueError:
                continue
        
        # 修为境界
        try:
            player.cultivation_realm = CultivationRealm(yixue.get("cultivation_realm", CultivationRealm.MORTAL.value))
        except ValueError:
            player.cultivation_realm = CultivationRealm.MORTAL
        
        player.cultivation_progress = yixue.get("cultivation_progress", 0)
        
        # 时间信息
        try:
            player.created_at = datetime.fromisoformat(data.get("created_at", datetime.now().isoformat()))
            player.last_active = datetime.fromisoformat(data.get("last_active", datetime.now().isoformat()))
        except ValueError:
            player.created_at = datetime.now()
            player.last_active = datetime.now()
        
        return player
    
    # ==================== 比较和哈希 ====================
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Player):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)
    
    def __str__(self) -> str:
        return f"Player({self.name}, {self.player_type.value}, 文化力:{self.calculate_cultural_power()})"
    
    def __repr__(self) -> str:
        return f"Player(id='{self.id}', name='{self.name}', type={self.player_type})"