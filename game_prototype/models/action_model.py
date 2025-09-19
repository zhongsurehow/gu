"""
游戏行动模型
定义各种游戏行动的数据结构和行为
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import time

from core.base_types import *
from core.interfaces import IGameAction
from utils.yixue_utils import *

@dataclass
class ActionCost:
    """行动成本"""
    resources: Dict[ResourceType, int] = field(default_factory=dict)
    energy: int = 0
    time: float = 0.0
    
    def is_affordable(self, available_resources: Dict[ResourceType, int], available_energy: int = 100) -> bool:
        """检查是否能够承担成本"""
        # 检查资源
        for resource_type, cost in self.resources.items():
            if available_resources.get(resource_type, 0) < cost:
                return False
        
        # 检查能量
        if available_energy < self.energy:
            return False
        
        return True

@dataclass
class ActionEffect:
    """行动效果"""
    resource_changes: Dict[ResourceType, int] = field(default_factory=dict)
    attribute_changes: Dict[str, Union[int, float]] = field(default_factory=dict)
    status_effects: List[str] = field(default_factory=list)
    duration: float = 0.0
    
    def apply_to_player(self, player: 'Player') -> None:
        """将效果应用到玩家"""
        # 应用资源变化
        for resource_type, change in self.resource_changes.items():
            current = player.resources.get(resource_type, 0)
            player.resources[resource_type] = max(0, current + change)
        
        # 应用属性变化
        for attr_name, change in self.attribute_changes.items():
            if hasattr(player, attr_name):
                current_value = getattr(player, attr_name)
                if isinstance(current_value, (int, float)):
                    setattr(player, attr_name, current_value + change)

class BaseGameAction(IGameAction):
    """基础游戏行动类"""
    
    def __init__(
        self,
        action_type: ActionType,
        player_id: str,
        cost: Optional[ActionCost] = None,
        effect: Optional[ActionEffect] = None,
        description: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.action_type = action_type
        self.player_id = player_id
        self.cost = cost or ActionCost()
        self.effect = effect or ActionEffect()
        self.description = description
        self.metadata = metadata or {}
        self.timestamp = time.time()
        self.action_id = f"{action_type.value}_{player_id}_{int(self.timestamp)}"
    
    def get_action_id(self) -> str:
        """获取行动ID"""
        return self.action_id
    
    def get_player_id(self) -> str:
        """获取玩家ID"""
        return self.player_id
    
    def get_cost(self) -> ActionCost:
        """获取行动成本"""
        return self.cost
    
    def get_effect(self) -> ActionEffect:
        """获取行动效果"""
        return self.effect
    
    def validate(self, game_state: Any) -> ValidationResult:
        """验证行动是否有效"""
        from utils.validation_utils import create_validation_result
        return create_validation_result()
    
    def execute(self, game_state: Any) -> ActionResult:
        """执行行动"""
        return ActionResult(
            success=True,
            message=f"执行{self.action_type.value}成功",
            data={"action_id": self.action_id}
        )

@dataclass
class MoveAction(BaseGameAction):
    """移动行动"""
    target_position: Position
    
    def __init__(self, player_id: str, target_position: Position):
        cost = ActionCost(energy=5, time=1.0)
        effect = ActionEffect()
        
        super().__init__(
            action_type=ActionType.MOVE,
            player_id=player_id,
            cost=cost,
            effect=effect,
            description=f"移动到位置 ({target_position.x}, {target_position.y})"
        )
        
        self.target_position = target_position
    
    def validate(self, game_state: Any) -> ValidationResult:
        """验证移动行动"""
        from utils.validation_utils import validate_move_action, create_validation_result
        
        result = create_validation_result()
        
        # 获取玩家当前位置
        player = game_state.get_player(self.player_id)
        if not player:
            result.add_error("玩家不存在")
            return result
        
        current_position = player.state.current_position
        board_size = game_state.config.basic.board_size
        
        # 验证移动
        move_result = validate_move_action(current_position, self.target_position, board_size)
        result.merge(move_result)
        
        return result
    
    def execute(self, game_state: Any) -> ActionResult:
        """执行移动"""
        player = game_state.get_player(self.player_id)
        if not player:
            return ActionResult(False, "玩家不存在", {})
        
        # 更新玩家位置
        player.state.current_position = self.target_position
        
        return ActionResult(
            success=True,
            message=f"移动到 ({self.target_position.x}, {self.target_position.y})",
            data={
                "action_id": self.action_id,
                "new_position": {"x": self.target_position.x, "y": self.target_position.y}
            }
        )

@dataclass
class PlacePieceAction(BaseGameAction):
    """放置棋子行动"""
    position: Position
    piece_type: str
    
    def __init__(self, player_id: str, position: Position, piece_type: str):
        cost = ActionCost(
            resources={ResourceType.CULTURE: 10},
            energy=10,
            time=2.0
        )
        effect = ActionEffect(
            resource_changes={ResourceType.INFLUENCE: 5}
        )
        
        super().__init__(
            action_type=ActionType.PLACE_PIECE,
            player_id=player_id,
            cost=cost,
            effect=effect,
            description=f"在 ({position.x}, {position.y}) 放置 {piece_type}"
        )
        
        self.position = position
        self.piece_type = piece_type

@dataclass
class CultivateAction(BaseGameAction):
    """修炼行动"""
    cultivation_type: str
    target_attribute: str
    
    def __init__(self, player_id: str, cultivation_type: str, target_attribute: str):
        cost = ActionCost(
            resources={ResourceType.CULTURE: 20, ResourceType.WISDOM: 5},
            energy=15,
            time=3.0
        )
        
        # 根据修炼类型确定效果
        effect = self._calculate_cultivation_effect(cultivation_type, target_attribute)
        
        super().__init__(
            action_type=ActionType.CULTIVATE,
            player_id=player_id,
            cost=cost,
            effect=effect,
            description=f"修炼 {cultivation_type}，提升 {target_attribute}"
        )
        
        self.cultivation_type = cultivation_type
        self.target_attribute = target_attribute
    
    def _calculate_cultivation_effect(self, cultivation_type: str, target_attribute: str) -> ActionEffect:
        """计算修炼效果"""
        effect = ActionEffect()
        
        if cultivation_type == "阴阳调和":
            if target_attribute == "yin":
                effect.attribute_changes["yin"] = 2
            elif target_attribute == "yang":
                effect.attribute_changes["yang"] = 2
        
        elif cultivation_type == "五行修炼":
            # 五行修炼效果
            effect.attribute_changes[f"wuxing_{target_attribute}"] = 1
        
        elif cultivation_type == "八卦感悟":
            # 八卦修炼效果
            effect.attribute_changes[f"bagua_{target_attribute}"] = 1
        
        return effect

@dataclass
class CastSpellAction(BaseGameAction):
    """施法行动"""
    spell_name: str
    target_player_id: Optional[str]
    spell_parameters: Dict[str, Any]
    
    def __init__(
        self, 
        player_id: str, 
        spell_name: str, 
        target_player_id: Optional[str] = None,
        spell_parameters: Optional[Dict[str, Any]] = None
    ):
        # 根据法术名称确定成本和效果
        cost, effect = self._get_spell_cost_and_effect(spell_name)
        
        super().__init__(
            action_type=ActionType.CAST_SPELL,
            player_id=player_id,
            cost=cost,
            effect=effect,
            description=f"施展法术: {spell_name}"
        )
        
        self.spell_name = spell_name
        self.target_player_id = target_player_id
        self.spell_parameters = spell_parameters or {}
    
    def _get_spell_cost_and_effect(self, spell_name: str) -> tuple[ActionCost, ActionEffect]:
        """获取法术成本和效果"""
        spell_data = {
            "五行相生": {
                "cost": ActionCost(
                    resources={ResourceType.WISDOM: 10, ResourceType.CULTURE: 15},
                    energy=20
                ),
                "effect": ActionEffect(
                    attribute_changes={"wuxing_power": 3},
                    status_effects=["五行增强"]
                )
            },
            "八卦推演": {
                "cost": ActionCost(
                    resources={ResourceType.WISDOM: 15, ResourceType.CULTURE: 10},
                    energy=25
                ),
                "effect": ActionEffect(
                    attribute_changes={"bagua_insight": 2},
                    status_effects=["预知未来"]
                )
            },
            "阴阳转换": {
                "cost": ActionCost(
                    resources={ResourceType.CULTURE: 20},
                    energy=30
                ),
                "effect": ActionEffect(
                    attribute_changes={"yin": -5, "yang": 5},
                    status_effects=["阴阳转换"]
                )
            }
        }
        
        data = spell_data.get(spell_name, {
            "cost": ActionCost(resources={ResourceType.WISDOM: 5}, energy=10),
            "effect": ActionEffect()
        })
        
        return data["cost"], data["effect"]

@dataclass
class TradeAction(BaseGameAction):
    """交易行动"""
    target_player_id: str
    offer_resources: Dict[ResourceType, int]
    request_resources: Dict[ResourceType, int]
    
    def __init__(
        self,
        player_id: str,
        target_player_id: str,
        offer_resources: Dict[ResourceType, int],
        request_resources: Dict[ResourceType, int]
    ):
        cost = ActionCost(
            resources={ResourceType.INFLUENCE: 5},
            energy=5,
            time=1.0
        )
        
        # 交易效果是资源的转移
        effect = ActionEffect(
            resource_changes={**{rt: -amount for rt, amount in offer_resources.items()},
                            **request_resources}
        )
        
        super().__init__(
            action_type=ActionType.TRADE,
            player_id=player_id,
            cost=cost,
            effect=effect,
            description=f"与 {target_player_id} 交易"
        )
        
        self.target_player_id = target_player_id
        self.offer_resources = offer_resources
        self.request_resources = request_resources

@dataclass
class BreakthroughAction(BaseGameAction):
    """突破境界行动"""
    target_realm: CultivationRealm
    
    def __init__(self, player_id: str, target_realm: CultivationRealm):
        # 突破需要大量资源
        cost = ActionCost(
            resources={
                ResourceType.CULTURE: 50,
                ResourceType.WISDOM: 30,
                ResourceType.INFLUENCE: 20
            },
            energy=50,
            time=10.0
        )
        
        effect = ActionEffect(
            attribute_changes={"cultivation_realm": 1},
            status_effects=["境界突破"],
            duration=0.0  # 永久效果
        )
        
        super().__init__(
            action_type=ActionType.BREAKTHROUGH,
            player_id=player_id,
            cost=cost,
            effect=effect,
            description=f"突破到 {target_realm.value}"
        )
        
        self.target_realm = target_realm
    
    def validate(self, game_state: Any) -> ValidationResult:
        """验证突破行动"""
        from utils.validation_utils import create_validation_result
        
        result = create_validation_result()
        
        player = game_state.get_player(self.player_id)
        if not player:
            result.add_error("玩家不存在")
            return result
        
        # 检查是否满足突破条件
        current_realm = player.cultivation_realm
        if self.target_realm.value <= current_realm.value:
            result.add_error("目标境界不能低于或等于当前境界")
        
        # 检查修炼进度
        progress = calculate_cultivation_progress(
            current_realm,
            player.yin, player.yang,
            player.wuxing_mastery,
            player.bagua_affinity,
            player.resources.get(ResourceType.CULTURE, 0)
        )
        
        if progress < 0.8:  # 需要80%的进度才能突破
            result.add_error(f"修炼进度不足，当前进度: {progress:.1%}")
        
        return result

# ==================== 行动工厂 ====================

class ActionFactory:
    """行动工厂类"""
    
    @staticmethod
    def create_move_action(player_id: str, target_x: int, target_y: int) -> MoveAction:
        """创建移动行动"""
        return MoveAction(player_id, Position(target_x, target_y))
    
    @staticmethod
    def create_place_piece_action(
        player_id: str, 
        x: int, y: int, 
        piece_type: str
    ) -> PlacePieceAction:
        """创建放置棋子行动"""
        return PlacePieceAction(player_id, Position(x, y), piece_type)
    
    @staticmethod
    def create_cultivate_action(
        player_id: str, 
        cultivation_type: str, 
        target_attribute: str
    ) -> CultivateAction:
        """创建修炼行动"""
        return CultivateAction(player_id, cultivation_type, target_attribute)
    
    @staticmethod
    def create_cast_spell_action(
        player_id: str,
        spell_name: str,
        target_player_id: Optional[str] = None,
        **spell_parameters
    ) -> CastSpellAction:
        """创建施法行动"""
        return CastSpellAction(player_id, spell_name, target_player_id, spell_parameters)
    
    @staticmethod
    def create_trade_action(
        player_id: str,
        target_player_id: str,
        offer: Dict[str, int],
        request: Dict[str, int]
    ) -> TradeAction:
        """创建交易行动"""
        # 转换字符串键为ResourceType枚举
        offer_resources = {ResourceType(k): v for k, v in offer.items()}
        request_resources = {ResourceType(k): v for k, v in request.items()}
        
        return TradeAction(player_id, target_player_id, offer_resources, request_resources)
    
    @staticmethod
    def create_breakthrough_action(
        player_id: str, 
        target_realm: str
    ) -> BreakthroughAction:
        """创建突破行动"""
        realm = CultivationRealm(target_realm)
        return BreakthroughAction(player_id, realm)
    
    @staticmethod
    def create_action_from_dict(action_data: Dict[str, Any]) -> BaseGameAction:
        """从字典创建行动"""
        action_type = ActionType(action_data["action_type"])
        player_id = action_data["player_id"]
        
        if action_type == ActionType.MOVE:
            return ActionFactory.create_move_action(
                player_id,
                action_data["target_x"],
                action_data["target_y"]
            )
        
        elif action_type == ActionType.PLACE_PIECE:
            return ActionFactory.create_place_piece_action(
                player_id,
                action_data["x"],
                action_data["y"],
                action_data["piece_type"]
            )
        
        elif action_type == ActionType.CULTIVATE:
            return ActionFactory.create_cultivate_action(
                player_id,
                action_data["cultivation_type"],
                action_data["target_attribute"]
            )
        
        elif action_type == ActionType.CAST_SPELL:
            return ActionFactory.create_cast_spell_action(
                player_id,
                action_data["spell_name"],
                action_data.get("target_player_id"),
                **action_data.get("spell_parameters", {})
            )
        
        elif action_type == ActionType.TRADE:
            return ActionFactory.create_trade_action(
                player_id,
                action_data["target_player_id"],
                action_data["offer"],
                action_data["request"]
            )
        
        elif action_type == ActionType.BREAKTHROUGH:
            return ActionFactory.create_breakthrough_action(
                player_id,
                action_data["target_realm"]
            )
        
        else:
            # 创建基础行动
            return BaseGameAction(
                action_type=action_type,
                player_id=player_id,
                description=action_data.get("description", "")
            )

# ==================== 便捷函数 ====================

def get_available_actions(player: 'Player', game_state: Any) -> List[BaseGameAction]:
    """获取玩家可用的行动列表"""
    available_actions = []
    
    # 移动行动（总是可用）
    current_pos = player.state.current_position
    board_size = game_state.config.basic.board_size
    
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            
            new_x = current_pos.x + dx
            new_y = current_pos.y + dy
            
            if 0 <= new_x < board_size and 0 <= new_y < board_size:
                action = ActionFactory.create_move_action(player.player_id, new_x, new_y)
                if action.cost.is_affordable(player.resources):
                    available_actions.append(action)
    
    # 修炼行动
    cultivation_actions = [
        ("阴阳调和", "yin"),
        ("阴阳调和", "yang"),
        ("五行修炼", "wood"),
        ("五行修炼", "fire"),
        ("五行修炼", "earth"),
        ("五行修炼", "metal"),
        ("五行修炼", "water"),
    ]
    
    for cult_type, target_attr in cultivation_actions:
        action = ActionFactory.create_cultivate_action(player.player_id, cult_type, target_attr)
        if action.cost.is_affordable(player.resources):
            available_actions.append(action)
    
    # 施法行动
    spells = ["五行相生", "八卦推演", "阴阳转换"]
    for spell in spells:
        action = ActionFactory.create_cast_spell_action(player.player_id, spell)
        if action.cost.is_affordable(player.resources):
            available_actions.append(action)
    
    # 突破行动
    current_realm = player.cultivation_realm
    next_realm_value = current_realm.value + 1
    
    try:
        next_realm = CultivationRealm(next_realm_value)
        action = ActionFactory.create_breakthrough_action(player.player_id, next_realm.name)
        if action.cost.is_affordable(player.resources):
            # 还需要检查突破条件
            if action.validate(game_state).is_valid:
                available_actions.append(action)
    except ValueError:
        pass  # 已达到最高境界
    
    return available_actions

def get_action_recommendations(player: 'Player', game_state: Any) -> List[str]:
    """获取行动建议"""
    recommendations = []
    
    # 资源建议
    culture = player.resources.get(ResourceType.CULTURE, 0)
    wisdom = player.resources.get(ResourceType.WISDOM, 0)
    influence = player.resources.get(ResourceType.INFLUENCE, 0)
    
    if culture < 30:
        recommendations.append("建议进行修炼行动，增加文化资源")
    
    if wisdom < 20:
        recommendations.append("建议学习新技能，增加智慧资源")
    
    if influence < 15:
        recommendations.append("建议与其他玩家互动，增加影响力")
    
    # 易学建议
    yin_yang_balance = abs(player.yin - player.yang)
    if yin_yang_balance > 10:
        if player.yin > player.yang:
            recommendations.append("阴气过盛，建议修炼阳属性")
        else:
            recommendations.append("阳气过盛，建议修炼阴属性")
    
    # 五行建议
    wuxing_values = list(player.wuxing_mastery.values())
    if max(wuxing_values) - min(wuxing_values) > 5:
        recommendations.append("五行不平衡，建议均衡发展各元素")
    
    # 境界建议
    progress = calculate_cultivation_progress(
        player.cultivation_realm,
        player.yin, player.yang,
        player.wuxing_mastery,
        player.bagua_affinity,
        culture
    )
    
    if progress > 0.8:
        recommendations.append("修炼进度良好，可考虑突破境界")
    elif progress < 0.3:
        recommendations.append("修炼进度较低，建议加强基础修炼")
    
    return recommendations