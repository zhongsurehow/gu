"""
爻辞光环系统 - 即时势光环系统
将爻辞从任务链重构为持续生效的光环效果
"""

import json
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from advanced_ui_system import advanced_ui, MessageType

class AuraType(Enum):
    """光环类型"""
    RESOURCE_MODIFIER = "资源修正"     # 修正资源获得
    ACTION_MODIFIER = "行动修正"      # 修正行动效果
    DEFENSE_MODIFIER = "防御修正"     # 修正防御能力
    MOVEMENT_MODIFIER = "移动修正"    # 修正移动能力
    INTERACTION_MODIFIER = "互动修正" # 修正玩家互动
    SPECIAL_ABILITY = "特殊能力"      # 特殊技能
    PASSIVE_EFFECT = "被动效果"       # 被动持续效果

class ZonePosition(Enum):
    """位置区域"""
    DI = "地"    # 地部
    REN = "人"   # 人部  
    TIAN = "天"  # 天部

@dataclass
class AuraEffect:
    """光环效果"""
    name: str
    description: str
    aura_type: AuraType
    modifier_function: str  # 修正函数名
    parameters: Dict[str, Any] = field(default_factory=dict)
    conditions: List[str] = field(default_factory=list)  # 生效条件
    zone_specific: Optional[ZonePosition] = None  # 特定区域生效
    duration: int = -1  # 持续回合数，-1表示永久
    stack_count: int = 1  # 叠加层数
    
class YaoCiAura:
    """爻辞光环"""
    
    def __init__(self, gua_name: str, yao_position: int, yao_text: str, effect: AuraEffect):
        self.gua_name = gua_name
        self.yao_position = yao_position  # 1-6，对应初、二、三、四、五、上
        self.yao_text = yao_text
        self.effect = effect
        self.is_active = False
        self.remaining_duration = effect.duration
        
    def activate(self, player_zone: ZonePosition) -> bool:
        """激活光环"""
        # 检查区域条件
        if self.effect.zone_specific and self.effect.zone_specific != player_zone:
            return False
        
        # 检查其他条件
        if not self._check_conditions():
            return False
        
        self.is_active = True
        return True
    
    def deactivate(self):
        """停用光环"""
        self.is_active = False
    
    def _check_conditions(self) -> bool:
        """检查生效条件"""
        # 这里可以实现复杂的条件检查逻辑
        return True
    
    def apply_effect(self, action_type: str, base_value: Any, context: Dict[str, Any]) -> Any:
        """应用光环效果"""
        if not self.is_active:
            return base_value
        
        # 根据修正函数名调用相应的修正逻辑
        modifier_func = getattr(self, self.effect.modifier_function, None)
        if modifier_func:
            return modifier_func(action_type, base_value, context)
        
        return base_value
    
    def update_turn(self):
        """更新回合"""
        if self.remaining_duration > 0:
            self.remaining_duration -= 1
            if self.remaining_duration == 0:
                self.deactivate()

class GuaAuraSet:
    """卦象光环集合"""
    
    def __init__(self, gua_name: str):
        self.gua_name = gua_name
        self.yao_auras: Dict[int, YaoCiAura] = {}  # 位置 -> 爻辞光环
        self.current_active_positions: List[int] = []  # 当前激活的爻位
        
    def add_yao_aura(self, position: int, aura: YaoCiAura):
        """添加爻辞光环"""
        self.yao_auras[position] = aura
    
    def activate_by_zone(self, player_zone: ZonePosition) -> List[int]:
        """根据玩家位置激活对应的爻辞"""
        activated_positions = []
        
        # 根据位置激活对应的爻辞
        zone_to_positions = {
            ZonePosition.DI: [1, 2],    # 地部激活初爻、二爻
            ZonePosition.REN: [3, 4],   # 人部激活三爻、四爻
            ZonePosition.TIAN: [5, 6]   # 天部激活五爻、上爻
        }
        
        positions_to_activate = zone_to_positions.get(player_zone, [])
        
        for position in positions_to_activate:
            if position in self.yao_auras:
                if self.yao_auras[position].activate(player_zone):
                    activated_positions.append(position)
        
        self.current_active_positions = activated_positions
        return activated_positions
    
    def get_active_auras(self) -> List[YaoCiAura]:
        """获取当前激活的光环"""
        return [self.yao_auras[pos] for pos in self.current_active_positions 
                if pos in self.yao_auras and self.yao_auras[pos].is_active]

class YaoCiAuraSystem:
    """爻辞光环系统"""
    
    def __init__(self):
        self.gua_aura_sets: Dict[str, GuaAuraSet] = {}
        self.player_current_gua: Dict[str, str] = {}  # 玩家当前的卦象
        self.player_zones: Dict[str, ZonePosition] = {}  # 玩家当前位置
        self.effect_modifiers = self._initialize_effect_modifiers()
        
    def _initialize_effect_modifiers(self) -> Dict[str, Callable]:
        """初始化效果修正器"""
        return {
            "meditation_qi_bonus": self._meditation_qi_bonus,
            "movement_restriction": self._movement_restriction,
            "defense_boost": self._defense_boost,
            "resource_exchange_bonus": self._resource_exchange_bonus,
            "action_cost_reduction": self._action_cost_reduction,
            "territory_control_bonus": self._territory_control_bonus,
            "divination_accuracy_boost": self._divination_accuracy_boost,
            "alliance_trust_bonus": self._alliance_trust_bonus
        }
    
    def load_yaoci_database(self, database_path: str):
        """加载爻辞数据库"""
        try:
            with open(database_path, 'r', encoding='utf-8') as f:
                yaoci_data = json.load(f)
            
            for gua_name, gua_data in yaoci_data.items():
                gua_set = GuaAuraSet(gua_name)
                
                for yao_key, yao_data in gua_data.items():
                    if yao_key.startswith(('初', '二', '三', '四', '五', '上')):
                        position = self._parse_yao_position(yao_key)
                        effect = self._create_aura_effect(yao_data)
                        aura = YaoCiAura(gua_name, position, yao_data['text'], effect)
                        gua_set.add_yao_aura(position, aura)
                
                self.gua_aura_sets[gua_name] = gua_set
                
        except FileNotFoundError:
            # 如果文件不存在，创建默认的爻辞光环
            self._create_default_auras()
    
    def _parse_yao_position(self, yao_key: str) -> int:
        """解析爻位"""
        position_map = {
            '初': 1, '二': 2, '三': 3, '四': 4, '五': 5, '上': 6
        }
        for char, pos in position_map.items():
            if char in yao_key:
                return pos
        return 1
    
    def _create_aura_effect(self, yao_data: Dict) -> AuraEffect:
        """创建光环效果"""
        effect_data = yao_data.get('effect', {})
        
        return AuraEffect(
            name=yao_data.get('name', '未知效果'),
            description=effect_data.get('description', ''),
            aura_type=AuraType(effect_data.get('type', 'PASSIVE_EFFECT')),
            modifier_function=effect_data.get('modifier_function', 'default_modifier'),
            parameters=effect_data.get('parameters', {}),
            conditions=effect_data.get('conditions', []),
            zone_specific=ZonePosition(effect_data['zone']) if 'zone' in effect_data else None,
            duration=effect_data.get('duration', -1)
        )
    
    def _create_default_auras(self):
        """创建默认的爻辞光环"""
        # 乾卦示例
        qian_set = GuaAuraSet("乾为天")
        
        # 初九：潜龙勿用
        qian_set.add_yao_aura(1, YaoCiAura(
            "乾为天", 1, "潜龙勿用",
            AuraEffect(
                "潜龙蓄势",
                "在地部时，冥想获得的气增加50%，但无法移动到其他区域",
                AuraType.RESOURCE_MODIFIER,
                "meditation_qi_bonus",
                {"bonus_rate": 0.5},
                zone_specific=ZonePosition.DI
            )
        ))
        
        # 九二：见龙在田
        qian_set.add_yao_aura(2, YaoCiAura(
            "乾为天", 2, "见龙在田，利见大人",
            AuraEffect(
                "见龙在田",
                "在地部时，与其他玩家的互动获得额外诚意",
                AuraType.INTERACTION_MODIFIER,
                "alliance_trust_bonus",
                {"bonus_amount": 2},
                zone_specific=ZonePosition.DI
            )
        ))
        
        # 九三：君子终日乾乾
        qian_set.add_yao_aura(3, YaoCiAura(
            "乾为天", 3, "君子终日乾乾，夕惕若厉，无咎",
            AuraEffect(
                "终日乾乾",
                "在人部时，所有行动消耗减少1点AP",
                AuraType.ACTION_MODIFIER,
                "action_cost_reduction",
                {"reduction": 1},
                zone_specific=ZonePosition.REN
            )
        ))
        
        # 九四：或跃在渊
        qian_set.add_yao_aura(4, YaoCiAura(
            "乾为天", 4, "或跃在渊，无咎",
            AuraEffect(
                "或跃在渊",
                "在人部时，可以选择移动到任意区域，但有风险",
                AuraType.MOVEMENT_MODIFIER,
                "movement_restriction",
                {"allow_any_zone": True, "risk_factor": 0.3},
                zone_specific=ZonePosition.REN
            )
        ))
        
        # 九五：飞龙在天
        qian_set.add_yao_aura(5, YaoCiAura(
            "乾为天", 5, "飞龙在天，利见大人",
            AuraEffect(
                "飞龙在天",
                "在天部时，获得道行时额外获得50%",
                AuraType.RESOURCE_MODIFIER,
                "resource_exchange_bonus",
                {"resource": "dao_xing", "bonus_rate": 0.5},
                zone_specific=ZonePosition.TIAN
            )
        ))
        
        # 上九：亢龙有悔
        qian_set.add_yao_aura(6, YaoCiAura(
            "乾为天", 6, "亢龙有悔",
            AuraEffect(
                "亢龙有悔",
                "在天部时，获得强大能力但每回合失去1点诚意",
                AuraType.SPECIAL_ABILITY,
                "defense_boost",
                {"defense_bonus": 3, "cost_per_turn": {"cheng_yi": 1}},
                zone_specific=ZonePosition.TIAN
            )
        ))
        
        self.gua_aura_sets["乾为天"] = qian_set
        
        # 可以继续添加其他卦象...
    
    def set_player_gua(self, player_name: str, gua_name: str):
        """设置玩家当前卦象"""
        self.player_current_gua[player_name] = gua_name
        
        # 重新激活光环
        if player_name in self.player_zones:
            self.update_player_zone(player_name, self.player_zones[player_name])
    
    def update_player_zone(self, player_name: str, new_zone: ZonePosition):
        """更新玩家位置并激活对应光环"""
        self.player_zones[player_name] = new_zone
        
        current_gua = self.player_current_gua.get(player_name)
        if current_gua and current_gua in self.gua_aura_sets:
            gua_set = self.gua_aura_sets[current_gua]
            
            # 先停用所有光环
            for aura in gua_set.yao_auras.values():
                aura.deactivate()
            
            # 激活新位置对应的光环
            activated_positions = gua_set.activate_by_zone(new_zone)
            
            if activated_positions:
                active_auras = gua_set.get_active_auras()
                aura_names = [aura.effect.name for aura in active_auras]
                
                advanced_ui.display_mystical_message(
                    f"{player_name} 进入 {new_zone.value} 部\n"
                    f"激活光环：{', '.join(aura_names)}",
                    "时势变化"
                )
    
    def apply_aura_effects(self, player_name: str, action_type: str, base_value: Any, 
                          context: Dict[str, Any] = None) -> Any:
        """应用光环效果"""
        if context is None:
            context = {}
        
        current_gua = self.player_current_gua.get(player_name)
        if not current_gua or current_gua not in self.gua_aura_sets:
            return base_value
        
        gua_set = self.gua_aura_sets[current_gua]
        active_auras = gua_set.get_active_auras()
        
        modified_value = base_value
        
        for aura in active_auras:
            modified_value = aura.apply_effect(action_type, modified_value, context)
        
        return modified_value
    
    def get_active_aura_descriptions(self, player_name: str) -> List[str]:
        """获取当前激活光环的描述"""
        current_gua = self.player_current_gua.get(player_name)
        if not current_gua or current_gua not in self.gua_aura_sets:
            return []
        
        gua_set = self.gua_aura_sets[current_gua]
        active_auras = gua_set.get_active_auras()
        
        descriptions = []
        for aura in active_auras:
            descriptions.append(f"{aura.effect.name}: {aura.effect.description}")
        
        return descriptions
    
    def display_current_auras(self, player_name: str):
        """显示当前光环状态"""
        current_gua = self.player_current_gua.get(player_name)
        current_zone = self.player_zones.get(player_name)
        
        if not current_gua:
            advanced_ui.print_colored("你当前没有激活任何卦象", MessageType.INFO)
            return
        
        advanced_ui.print_colored(f"当前卦象：{current_gua}", MessageType.HIGHLIGHT)
        advanced_ui.print_colored(f"当前位置：{current_zone.value if current_zone else '未知'}", MessageType.INFO)
        
        descriptions = self.get_active_aura_descriptions(player_name)
        if descriptions:
            advanced_ui.print_colored("激活的光环效果：", MessageType.MYSTICAL)
            for desc in descriptions:
                advanced_ui.print_colored(f"  • {desc}", MessageType.INFO)
        else:
            advanced_ui.print_colored("当前位置没有激活的光环效果", MessageType.INFO)
    
    # 效果修正器实现
    def _meditation_qi_bonus(self, action_type: str, base_value: Any, context: Dict) -> Any:
        """冥想气奖励修正器"""
        if action_type == "meditation" and isinstance(base_value, dict) and "qi" in base_value:
            bonus_rate = context.get("bonus_rate", 0.5)
            base_value["qi"] = int(base_value["qi"] * (1 + bonus_rate))
        return base_value
    
    def _movement_restriction(self, action_type: str, base_value: Any, context: Dict) -> Any:
        """移动限制修正器"""
        if action_type == "movement":
            allow_any = context.get("allow_any_zone", False)
            if allow_any:
                # 允许移动到任意区域，但可能有风险
                return {"allowed": True, "risk": context.get("risk_factor", 0)}
            else:
                # 限制移动
                return {"allowed": False}
        return base_value
    
    def _defense_boost(self, action_type: str, base_value: Any, context: Dict) -> Any:
        """防御增强修正器"""
        if action_type == "defense":
            bonus = context.get("defense_bonus", 0)
            if isinstance(base_value, (int, float)):
                return base_value + bonus
        return base_value
    
    def _resource_exchange_bonus(self, action_type: str, base_value: Any, context: Dict) -> Any:
        """资源交换奖励修正器"""
        target_resource = context.get("resource")
        bonus_rate = context.get("bonus_rate", 0)
        
        if isinstance(base_value, dict) and target_resource in base_value:
            base_value[target_resource] = int(base_value[target_resource] * (1 + bonus_rate))
        
        return base_value
    
    def _action_cost_reduction(self, action_type: str, base_value: Any, context: Dict) -> Any:
        """行动消耗减少修正器"""
        if action_type == "action_cost":
            reduction = context.get("reduction", 0)
            if isinstance(base_value, (int, float)):
                return max(0, base_value - reduction)
        return base_value
    
    def _territory_control_bonus(self, action_type: str, base_value: Any, context: Dict) -> Any:
        """领土控制奖励修正器"""
        if action_type == "territory_control":
            bonus = context.get("control_bonus", 0)
            if isinstance(base_value, (int, float)):
                return base_value + bonus
        return base_value
    
    def _divination_accuracy_boost(self, action_type: str, base_value: Any, context: Dict) -> Any:
        """占卜准确度增强修正器"""
        if action_type == "divination":
            accuracy_boost = context.get("accuracy_boost", 0)
            if isinstance(base_value, dict) and "accuracy" in base_value:
                base_value["accuracy"] = min(1.0, base_value["accuracy"] + accuracy_boost)
        return base_value
    
    def _alliance_trust_bonus(self, action_type: str, base_value: Any, context: Dict) -> Any:
        """盟约信任奖励修正器"""
        if action_type == "alliance_interaction":
            bonus = context.get("bonus_amount", 0)
            if isinstance(base_value, dict) and "cheng_yi" in base_value:
                base_value["cheng_yi"] += bonus
        return base_value

# 全局爻辞光环系统实例
yaoci_aura_system = YaoCiAuraSystem()

# 便捷函数
def set_player_gua(player_name: str, gua_name: str):
    """设置玩家卦象"""
    yaoci_aura_system.set_player_gua(player_name, gua_name)

def update_player_zone(player_name: str, new_zone: ZonePosition):
    """更新玩家位置"""
    yaoci_aura_system.update_player_zone(player_name, new_zone)

def apply_aura_effects(player_name: str, action_type: str, base_value: Any, 
                      context: Dict[str, Any] = None) -> Any:
    """应用光环效果"""
    return yaoci_aura_system.apply_aura_effects(player_name, action_type, base_value, context)

def display_current_auras(player_name: str):
    """显示当前光环"""
    yaoci_aura_system.display_current_auras(player_name)

def load_yaoci_database(database_path: str):
    """加载爻辞数据库"""
    yaoci_aura_system.load_yaoci_database(database_path)