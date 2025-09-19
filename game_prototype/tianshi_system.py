"""
天时系统 - 全局事件和大衍历机制
实现动态的游戏环境变化，打破单调循环
"""

import random
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from advanced_ui_system import advanced_ui, MessageType

class TianShiType(Enum):
    """天时类型"""
    PROSPERITY = "丰年"      # 资源丰富
    CHAOS = "兵乱"          # 行动困难
    HARMONY = "天人感应"     # 效果增强
    CHANGE = "变革"         # 规则改变
    MYSTERY = "天机"        # 神秘事件
    BALANCE = "阴阳调和"    # 平衡相关
    WISDOM = "智慧启发"     # 学习相关
    CONFLICT = "争斗"       # 竞争激化

@dataclass
class TianShiEffect:
    """天时效果"""
    name: str
    description: str
    duration: int  # 持续回合数，-1表示永久
    effect_type: str  # 效果类型
    parameters: Dict[str, Any]  # 效果参数
    condition: Optional[Callable] = None  # 触发条件

class TianShiCard:
    """天时牌"""
    
    def __init__(self, name: str, tianshi_type: TianShiType, effects: List[TianShiEffect], 
                 flavor_text: str = "", rarity: str = "common"):
        self.name = name
        self.tianshi_type = tianshi_type
        self.effects = effects
        self.flavor_text = flavor_text
        self.rarity = rarity  # common, rare, legendary
        self.active = False
        self.remaining_duration = 0
    
    def activate(self, game_state):
        """激活天时牌"""
        self.active = True
        for effect in self.effects:
            if effect.duration > 0:
                self.remaining_duration = max(self.remaining_duration, effect.duration)
            elif effect.duration == -1:
                self.remaining_duration = -1  # 永久效果
        
        # 显示天时激活
        advanced_ui.display_mystical_message(
            f"{self.name}\n\n{self.flavor_text}\n\n效果: {self._get_effects_description()}",
            "天时降临"
        )
    
    def _get_effects_description(self) -> str:
        """获取效果描述"""
        descriptions = []
        for effect in self.effects:
            descriptions.append(f"• {effect.description}")
        return "\n".join(descriptions)
    
    def apply_effects(self, game_state, context: str = ""):
        """应用效果"""
        if not self.active:
            return
        
        for effect in self.effects:
            if effect.condition is None or effect.condition(game_state, context):
                self._apply_single_effect(effect, game_state, context)
    
    def _apply_single_effect(self, effect: TianShiEffect, game_state, context: str):
        """应用单个效果"""
        effect_type = effect.effect_type
        params = effect.parameters
        
        if effect_type == "resource_bonus":
            # 资源奖励
            for player in game_state.players:
                for resource, amount in params.items():
                    if hasattr(player, resource):
                        old_value = getattr(player, resource)
                        setattr(player, resource, old_value + amount)
                        advanced_ui.display_resource_change(resource, old_value, getattr(player, resource))
        
        elif effect_type == "action_cost_modifier":
            # 行动成本修正
            action_name = params.get("action", "")
            modifier = params.get("modifier", 0)
            # 这里需要与行动系统集成
            
        elif effect_type == "effect_amplifier":
            # 效果放大器
            amplifier = params.get("amplifier", 1.0)
            effect_types = params.get("effect_types", [])
            # 这里需要与效果系统集成
        
        elif effect_type == "zone_modifier":
            # 区域修正
            zone_name = params.get("zone", "")
            modifier_type = params.get("modifier_type", "")
            value = params.get("value", 0)
            # 这里需要与区域系统集成
    
    def tick(self):
        """时间流逝"""
        if self.remaining_duration > 0:
            self.remaining_duration -= 1
            if self.remaining_duration == 0:
                self.active = False
                return True  # 表示效果结束
        return False

class TianShiSystem:
    """天时系统"""
    
    def __init__(self):
        self.tianshi_deck = self._create_tianshi_deck()
        self.active_tianshi: List[TianShiCard] = []
        self.used_tianshi: List[TianShiCard] = []
        self.turn_counter = 0
        self.next_tianshi_turn = random.randint(3, 5)  # 首次天时出现时间
        
    def _create_tianshi_deck(self) -> List[TianShiCard]:
        """创建天时牌库"""
        deck = []
        
        # 丰年系列
        deck.append(TianShiCard(
            "春回大地",
            TianShiType.PROSPERITY,
            [TianShiEffect(
                "春回大地",
                "所有玩家在生息阶段额外获得2点气",
                3,
                "resource_bonus",
                {"qi": 2}
            )],
            "万物复苏，生机盎然。天地之气充盈，修行者得天时之助。",
            "common"
        ))
        
        deck.append(TianShiCard(
            "五谷丰登",
            TianShiType.PROSPERITY,
            [TianShiEffect(
                "五谷丰登",
                "所有玩家每回合开始时获得1点诚意",
                4,
                "resource_bonus",
                {"cheng_yi": 1}
            )],
            "年景丰收，民心安定。诚意之德，自然而生。",
            "common"
        ))
        
        # 兵乱系列
        deck.append(TianShiCard(
            "烽火连天",
            TianShiType.CHAOS,
            [TianShiEffect(
                "烽火连天",
                "所有演卦行动的AP消耗增加1",
                3,
                "action_cost_modifier",
                {"action": "演卦", "modifier": 1}
            )],
            "战火纷飞，人心不安。卦象难明，演算不易。",
            "common"
        ))
        
        deck.append(TianShiCard(
            "群雄割据",
            TianShiType.CHAOS,
            [TianShiEffect(
                "群雄割据",
                "区域争夺时，影响力需求增加1",
                4,
                "zone_modifier",
                {"modifier_type": "influence_requirement", "value": 1}
            )],
            "诸侯争霸，天下大乱。欲控一方，需更强实力。",
            "rare"
        ))
        
        # 天人感应系列
        deck.append(TianShiCard(
            "天人合一",
            TianShiType.HARMONY,
            [TianShiEffect(
                "天人合一",
                "所有阴阳属性变化效果翻倍",
                2,
                "effect_amplifier",
                {"amplifier": 2.0, "effect_types": ["yin_yang"]}
            )],
            "天地人三才合一，阴阳之道显现。修行者得天机之助。",
            "rare"
        ))
        
        deck.append(TianShiCard(
            "星宿照命",
            TianShiType.HARMONY,
            [TianShiEffect(
                "星宿照命",
                "占卜行动必定成功，且获得额外信息",
                3,
                "divination_enhancement",
                {"success_rate": 1.0, "extra_info": True}
            )],
            "星辰指引，命运昭然。占卜之术，无不灵验。",
            "legendary"
        ))
        
        # 变革系列
        deck.append(TianShiCard(
            "改天换地",
            TianShiType.CHANGE,
            [TianShiEffect(
                "改天换地",
                "所有玩家可以重新选择当前位置",
                1,
                "position_reset",
                {}
            )],
            "天地大变，乾坤颠倒。旧有格局，一朝改变。",
            "legendary"
        ))
        
        deck.append(TianShiCard(
            "时来运转",
            TianShiType.CHANGE,
            [TianShiEffect(
                "时来运转",
                "本回合所有玩家行动点数翻倍",
                1,
                "resource_bonus",
                {"action_points": "double"}
            )],
            "时运转换，机会难得。把握当下，大展身手。",
            "rare"
        ))
        
        # 天机系列
        deck.append(TianShiCard(
            "天机莫测",
            TianShiType.MYSTERY,
            [TianShiEffect(
                "天机莫测",
                "随机一名玩家获得神秘奖励",
                1,
                "random_blessing",
                {"blessing_types": ["resource", "card", "position"]}
            )],
            "天机深不可测，福祸难以预料。或有奇遇，或有考验。",
            "rare"
        ))
        
        # 阴阳调和系列
        deck.append(TianShiCard(
            "太极生辉",
            TianShiType.BALANCE,
            [TianShiEffect(
                "太极生辉",
                "阴阳平衡的玩家额外获得3点道行",
                1,
                "balance_reward",
                {"dao_xing": 3}
            )],
            "太极图现，阴阳调和。平衡者得天道之奖。",
            "rare"
        ))
        
        # 智慧启发系列
        deck.append(TianShiCard(
            "智慧之光",
            TianShiType.WISDOM,
            [TianShiEffect(
                "智慧之光",
                "学习行动获得的道行翻倍",
                3,
                "action_enhancement",
                {"action": "学习", "multiplier": 2.0}
            )],
            "智慧之光普照，学者得其利。勤学苦练，事半功倍。",
            "common"
        ))
        
        # 争斗系列
        deck.append(TianShiCard(
            "龙争虎斗",
            TianShiType.CONFLICT,
            [TianShiEffect(
                "龙争虎斗",
                "区域争夺胜利者额外获得2点诚意",
                3,
                "conflict_reward",
                {"cheng_yi": 2}
            )],
            "龙虎相争，胜者为王。争斗之中，见真章。",
            "common"
        ))
        
        return deck
    
    def should_draw_tianshi(self) -> bool:
        """是否应该抽取天时牌"""
        return self.turn_counter >= self.next_tianshi_turn
    
    def draw_tianshi(self) -> Optional[TianShiCard]:
        """抽取天时牌"""
        if not self.tianshi_deck:
            # 重新洗牌
            self.tianshi_deck = self.used_tianshi.copy()
            self.used_tianshi.clear()
            random.shuffle(self.tianshi_deck)
        
        if self.tianshi_deck:
            card = self.tianshi_deck.pop()
            self.used_tianshi.append(card)
            
            # 设置下次天时出现时间
            self.next_tianshi_turn = self.turn_counter + random.randint(2, 4)
            
            return card
        return None
    
    def activate_tianshi(self, game_state):
        """激活天时"""
        if self.should_draw_tianshi():
            tianshi_card = self.draw_tianshi()
            if tianshi_card:
                tianshi_card.activate(game_state)
                self.active_tianshi.append(tianshi_card)
    
    def apply_active_effects(self, game_state, context: str = ""):
        """应用当前激活的天时效果"""
        for tianshi in self.active_tianshi[:]:  # 使用切片避免修改列表时的问题
            tianshi.apply_effects(game_state, context)
    
    def tick_turn(self):
        """回合结束时的处理"""
        self.turn_counter += 1
        
        # 处理天时持续时间
        expired_tianshi = []
        for tianshi in self.active_tianshi[:]:
            if tianshi.tick():  # 如果天时效果结束
                expired_tianshi.append(tianshi)
                self.active_tianshi.remove(tianshi)
        
        # 显示结束的天时
        for tianshi in expired_tianshi:
            advanced_ui.display_notification(
                f"天时「{tianshi.name}」的影响已经消散",
                MessageType.INFO
            )
    
    def get_active_tianshi_info(self) -> List[str]:
        """获取当前激活天时的信息"""
        info = []
        for tianshi in self.active_tianshi:
            duration_text = f"剩余{tianshi.remaining_duration}回合" if tianshi.remaining_duration > 0 else "永久"
            info.append(f"[星] {tianshi.name} ({duration_text})")
        return info
    
    def display_tianshi_status(self):
        """显示天时状态"""
        if self.active_tianshi:
            advanced_ui.print_colored("═══ 当前天时 ═══", MessageType.HIGHLIGHT)
            for info in self.get_active_tianshi_info():
                advanced_ui.print_colored(info, MessageType.MYSTICAL)
            print()
        
        # 显示下次天时预测
        turns_until_next = self.next_tianshi_turn - self.turn_counter
        if turns_until_next > 0:
            advanced_ui.print_colored(
                f"🔮 预测：{turns_until_next}回合后可能有天时变化",
                MessageType.INFO
            )

# 全局天时系统实例
tianshi_system = TianShiSystem()

# 便捷函数
def activate_tianshi(game_state):
    """激活天时"""
    tianshi_system.activate_tianshi(game_state)

def apply_tianshi_effects(game_state, context: str = ""):
    """应用天时效果"""
    tianshi_system.apply_active_effects(game_state, context)

def tick_tianshi():
    """天时系统回合结束处理"""
    tianshi_system.tick_turn()

def display_tianshi_status():
    """显示天时状态"""
    tianshi_system.display_tianshi_status()

def get_active_tianshi() -> List[TianShiCard]:
    """获取当前激活的天时"""
    return tianshi_system.active_tianshi.copy()