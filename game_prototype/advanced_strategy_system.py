#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级策略系统 - 集成增强卦象系统的高级游戏机制
实现变卦、互卦、错卦等易经智慧在游戏中的应用
"""

from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import random
import time

from game_state import GameState, Player
from enhanced_hexagram_system import (
    enhanced_hexagram_system, HexagramRelationType, 
    display_hexagram_analysis, display_synergy_analysis
)
from yijing_mechanics import YinYang, WuXing
from generate_64_guas import GUA_64_INFO
from ui_enhancement import enhanced_print, enhanced_input, ui_enhancement

class StrategyType(Enum):
    """策略类型"""
    TRANSFORMATION = "变卦策略"    # 变卦相关策略
    SYNERGY = "协同策略"          # 卦象协同策略
    BALANCE = "平衡策略"          # 阴阳五行平衡策略
    TIMING = "时机策略"           # 时机把握策略
    ADAPTATION = "适应策略"       # 适应变化策略

@dataclass
class StrategyAction:
    """策略行动"""
    name: str
    description: str
    strategy_type: StrategyType
    cost: Dict[str, int]  # 消耗资源
    effects: Dict[str, any]  # 效果
    conditions: List[str]  # 激活条件
    cooldown: int = 0  # 冷却回合数
    
@dataclass
class PlayerStrategy:
    """玩家策略状态"""
    active_strategies: List[str] = field(default_factory=list)
    strategy_cooldowns: Dict[str, int] = field(default_factory=dict)
    hexagram_mastery: Dict[str, int] = field(default_factory=dict)  # 卦象掌握度
    transformation_history: List[Tuple[str, str]] = field(default_factory=list)  # 变卦历史
    synergy_bonus: float = 1.0
    
class AdvancedStrategySystem:
    """高级策略系统"""
    
    def __init__(self):
        self.strategy_actions = self._initialize_strategy_actions()
        self.player_strategies: Dict[str, PlayerStrategy] = {}
        
    def _initialize_strategy_actions(self) -> Dict[str, StrategyAction]:
        """初始化策略行动"""
        actions = {}
        
        # 变卦策略
        actions["single_line_change"] = StrategyAction(
            name="一爻变",
            description="改变一个爻位，获得新的卦象力量",
            strategy_type=StrategyType.TRANSFORMATION,
            cost={"qi": 3, "dao_xing": 1},
            effects={"transform_hexagram": True, "power_bonus": 1.2},
            conditions=["拥有至少一个卦象", "气≥3"],
            cooldown=2
        )
        
        actions["double_line_change"] = StrategyAction(
            name="二爻变",
            description="同时改变两个爻位，获得强大的变化力量",
            strategy_type=StrategyType.TRANSFORMATION,
            cost={"qi": 5, "dao_xing": 2},
            effects={"transform_hexagram": True, "power_bonus": 1.5, "extra_action": 1},
            conditions=["拥有至少一个卦象", "气≥5", "道行≥2"],
            cooldown=3
        )
        
        actions["mutual_hexagram"] = StrategyAction(
            name="互卦显现",
            description="显现卦象的互卦，获得内在变化的力量",
            strategy_type=StrategyType.TRANSFORMATION,
            cost={"dao_xing": 3},
            effects={"reveal_mutual": True, "insight_bonus": 2},
            conditions=["拥有至少一个卦象", "道行≥3"],
            cooldown=4
        )
        
        actions["inverse_harmony"] = StrategyAction(
            name="错卦和谐",
            description="与错卦建立联系，获得阴阳平衡的力量",
            strategy_type=StrategyType.BALANCE,
            cost={"cheng_yi": 3},
            effects={"yin_yang_balance": 0.5, "stability_bonus": True},
            conditions=["拥有至少一个卦象", "诚意≥3"],
            cooldown=3
        )
        
        # 协同策略
        actions["elemental_synergy"] = StrategyAction(
            name="五行协同",
            description="激活五行相生相克的协同效应",
            strategy_type=StrategyType.SYNERGY,
            cost={"qi": 4, "dao_xing": 2},
            effects={"wuxing_synergy": True, "resource_efficiency": 1.3},
            conditions=["拥有不同五行属性的卦象≥3"],
            cooldown=2
        )
        
        actions["yin_yang_unity"] = StrategyAction(
            name="阴阳合一",
            description="平衡阴阳，获得和谐统一的力量",
            strategy_type=StrategyType.SYNERGY,
            cost={"qi": 3, "cheng_yi": 2},
            effects={"yin_yang_unity": True, "all_actions_enhanced": True},
            conditions=["阴阳平衡度≥0.4"],
            cooldown=4
        )
        
        actions["trigram_mastery"] = StrategyAction(
            name="八卦精通",
            description="展现对八卦的深度理解，获得全面提升",
            strategy_type=StrategyType.SYNERGY,
            cost={"dao_xing": 5},
            effects={"mastery_bonus": True, "all_costs_reduced": 0.8},
            conditions=["掌握不同八卦≥4"],
            cooldown=5
        )
        
        # 平衡策略
        actions["cosmic_balance"] = StrategyAction(
            name="宇宙平衡",
            description="达到天地人三才的完美平衡",
            strategy_type=StrategyType.BALANCE,
            cost={"qi": 6, "dao_xing": 3, "cheng_yi": 3},
            effects={"cosmic_balance": True, "victory_progress": 2},
            conditions=["拥有天、地、人各属性卦象"],
            cooldown=6
        )
        
        # 时机策略
        actions["perfect_timing"] = StrategyAction(
            name="天时地利",
            description="把握完美时机，所有行动效果翻倍",
            strategy_type=StrategyType.TIMING,
            cost={"cheng_yi": 4},
            effects={"timing_bonus": 2.0, "duration": 1},
            conditions=["连续3回合未使用策略行动"],
            cooldown=3
        )
        
        actions["seasonal_adaptation"] = StrategyAction(
            name="顺应时序",
            description="根据游戏阶段调整策略，获得适应性加成",
            strategy_type=StrategyType.ADAPTATION,
            cost={"dao_xing": 2},
            effects={"adaptation_bonus": True, "flexibility": 1},
            conditions=["游戏进行≥5回合"],
            cooldown=2
        )
        
        return actions
    
    def initialize_player_strategy(self, player_name: str):
        """初始化玩家策略状态"""
        if player_name not in self.player_strategies:
            self.player_strategies[player_name] = PlayerStrategy()
    
    def get_available_strategies(self, player: Player, game_state: GameState) -> List[StrategyAction]:
        """获取玩家可用的策略行动"""
        self.initialize_player_strategy(player.name)
        player_strategy = self.player_strategies[player.name]
        
        available = []
        
        for action_id, action in self.strategy_actions.items():
            # 检查冷却时间
            if action_id in player_strategy.strategy_cooldowns:
                if player_strategy.strategy_cooldowns[action_id] > 0:
                    continue
            
            # 检查资源条件
            if not self._check_resource_conditions(player, action.cost):
                continue
            
            # 检查特殊条件
            if self._check_special_conditions(player, game_state, action.conditions):
                available.append(action)
        
        return available
    
    def _check_resource_conditions(self, player: Player, cost: Dict[str, int]) -> bool:
        """检查资源条件"""
        if cost.get("qi", 0) > player.qi:
            return False
        if cost.get("dao_xing", 0) > player.dao_xing:
            return False
        if cost.get("cheng_yi", 0) > player.cheng_yi:
            return False
        return True
    
    def _check_special_conditions(self, player: Player, game_state: GameState, 
                                conditions: List[str]) -> bool:
        """检查特殊条件"""
        player_strategy = self.player_strategies[player.name]
        
        for condition in conditions:
            if "拥有至少一个卦象" in condition:
                # 检查玩家是否控制任何卦象区域
                controlled_zones = sum(1 for zone_data in game_state.board.gua_zones.values() 
                                     if zone_data.get("controller") == player.name)
                if controlled_zones == 0:
                    return False
            
            elif "拥有不同五行属性的卦象≥3" in condition:
                # 检查五行多样性
                controlled_elements = set()
                for zone_name, zone_data in game_state.board.gua_zones.items():
                    if zone_data.get("controller") == player.name:
                        if zone_name in GUA_64_INFO:
                            controlled_elements.add(GUA_64_INFO[zone_name]["element"])
                if len(controlled_elements) < 3:
                    return False
            
            elif "阴阳平衡度≥0.4" in condition:
                if abs(player.yin_yang_balance - 0.5) > 0.1:
                    return False
            
            elif "掌握不同八卦≥4" in condition:
                # 检查八卦掌握度
                mastered_trigrams = set()
                for zone_name, zone_data in game_state.board.gua_zones.items():
                    if zone_data.get("controller") == player.name:
                        if zone_name in GUA_64_INFO:
                            trigrams = GUA_64_INFO[zone_name]["trigrams"]
                            mastered_trigrams.update(trigrams)
                if len(mastered_trigrams) < 4:
                    return False
            
            elif "连续3回合未使用策略行动" in condition:
                # 检查策略使用历史
                if len(player_strategy.active_strategies) > 0:
                    return False
            
            # 添加更多条件检查...
        
        return True
    
    def execute_strategy_action(self, player: Player, game_state: GameState, 
                              action: StrategyAction) -> GameState:
        """执行策略行动"""
        self.initialize_player_strategy(player.name)
        player_strategy = self.player_strategies[player.name]
        
        # 消耗资源
        player.qi -= action.cost.get("qi", 0)
        player.dao_xing -= action.cost.get("dao_xing", 0)
        player.cheng_yi -= action.cost.get("cheng_yi", 0)
        
        # 应用效果
        self._apply_strategy_effects(player, game_state, action)
        
        # 设置冷却时间
        action_id = self._get_action_id(action)
        if action_id:
            player_strategy.strategy_cooldowns[action_id] = action.cooldown
        
        # 记录策略使用
        player_strategy.active_strategies.append(action.name)
        
        enhanced_print(f"{player.name} 使用了策略: {action.name}", "success")
        enhanced_print(action.description, "info")
        
        return game_state
    
    def _get_action_id(self, action: StrategyAction) -> Optional[str]:
        """获取行动ID"""
        for action_id, stored_action in self.strategy_actions.items():
            if stored_action.name == action.name:
                return action_id
        return None
    
    def _apply_strategy_effects(self, player: Player, game_state: GameState, 
                              action: StrategyAction):
        """应用策略效果"""
        effects = action.effects
        
        if effects.get("transform_hexagram"):
            self._handle_hexagram_transformation(player, game_state, effects)
        
        if effects.get("reveal_mutual"):
            self._handle_mutual_hexagram(player, game_state)
        
        if effects.get("yin_yang_balance"):
            player.yin_yang_balance = effects["yin_yang_balance"]
            enhanced_print("阴阳达到完美平衡", "achievement")
        
        if effects.get("wuxing_synergy"):
            self._handle_wuxing_synergy(player, game_state)
        
        if effects.get("power_bonus"):
            # 临时增强效果
            enhanced_print(f"获得 {effects['power_bonus']:.1f}x 力量加成", "achievement")
        
        if effects.get("extra_action"):
            enhanced_print(f"获得 {effects['extra_action']} 次额外行动", "achievement")
        
        if effects.get("insight_bonus"):
            player.dao_xing += effects["insight_bonus"]
            enhanced_print(f"获得 {effects['insight_bonus']} 点道行洞察", "achievement")
        
        if effects.get("cosmic_balance"):
            enhanced_print("达到宇宙平衡状态！", "achievement")
            # 可以添加特殊的胜利进度
        
        if effects.get("timing_bonus"):
            enhanced_print(f"获得 {effects['timing_bonus']:.1f}x 时机加成", "achievement")
    
    def _handle_hexagram_transformation(self, player: Player, game_state: GameState, 
                                      effects: Dict):
        """处理卦象变化"""
        # 获取玩家控制的卦象
        controlled_hexagrams = []
        for zone_name, zone_data in game_state.board.gua_zones.items():
            if zone_data.get("controller") == player.name:
                controlled_hexagrams.append(zone_name)
        
        if not controlled_hexagrams:
            return
        
        # 让玩家选择要变化的卦象
        enhanced_print("选择要进行变化的卦象:", "info")
        for i, gua_name in enumerate(controlled_hexagrams, 1):
            print(f"{i}. {gua_name}")
        
        try:
            choice = int(enhanced_input("请选择 (输入数字): ")) - 1
            if 0 <= choice < len(controlled_hexagrams):
                selected_gua = controlled_hexagrams[choice]
                
                # 获取可能的变化
                relations = enhanced_hexagram_system.get_hexagram_relations(selected_gua)
                change_relations = [r for r in relations 
                                  if r.relation_type == HexagramRelationType.CHANGED]
                
                if change_relations:
                    # 随机选择一个变化或让玩家选择
                    if len(change_relations) == 1:
                        target_relation = change_relations[0]
                    else:
                        enhanced_print("可能的变化:", "info")
                        for i, relation in enumerate(change_relations[:3], 1):
                            print(f"{i}. {relation.related} - {relation.description}")
                        
                        try:
                            change_choice = int(enhanced_input("选择变化 (输入数字): ")) - 1
                            if 0 <= change_choice < len(change_relations):
                                target_relation = change_relations[change_choice]
                            else:
                                target_relation = random.choice(change_relations)
                        except ValueError:
                            target_relation = random.choice(change_relations)
                    
                    # 执行变化
                    target_gua = target_relation.related
                    enhanced_print(f"{selected_gua} 变化为 {target_gua}!", "success")
                    
                    # 更新游戏状态（这里需要根据具体游戏机制实现）
                    # 例如：改变区域控制、获得新的能力等
                    
                    # 记录变化历史
                    player_strategy = self.player_strategies[player.name]
                    player_strategy.transformation_history.append((selected_gua, target_gua))
                    
        except ValueError:
            enhanced_print("无效选择", "warning")
    
    def _handle_mutual_hexagram(self, player: Player, game_state: GameState):
        """处理互卦显现"""
        controlled_hexagrams = []
        for zone_name, zone_data in game_state.board.gua_zones.items():
            if zone_data.get("controller") == player.name:
                controlled_hexagrams.append(zone_name)
        
        for gua_name in controlled_hexagrams:
            relations = enhanced_hexagram_system.get_hexagram_relations(gua_name)
            mutual_relations = [r for r in relations 
                              if r.relation_type == HexagramRelationType.MUTUAL]
            
            if mutual_relations:
                mutual_gua = mutual_relations[0].related
                enhanced_print(f"{gua_name} 的互卦 {mutual_gua} 显现!", "achievement")
                
                # 可以给予特殊洞察或能力
                player.dao_xing += 2
    
    def _handle_wuxing_synergy(self, player: Player, game_state: GameState):
        """处理五行协同效应"""
        controlled_elements = {}
        for zone_name, zone_data in game_state.board.gua_zones.items():
            if zone_data.get("controller") == player.name:
                if zone_name in GUA_64_INFO:
                    element = GUA_64_INFO[zone_name]["element"]
                    controlled_elements[element] = controlled_elements.get(element, 0) + 1
        
        # 计算五行协同奖励
        synergy_bonus = len(controlled_elements) * 0.1
        player_strategy = self.player_strategies[player.name]
        player_strategy.synergy_bonus += synergy_bonus
        
        enhanced_print(f"五行协同激活! 获得 {synergy_bonus:.1f} 协同加成", "achievement")
    
    def update_cooldowns(self, player_name: str):
        """更新冷却时间"""
        if player_name in self.player_strategies:
            player_strategy = self.player_strategies[player_name]
            for action_id in list(player_strategy.strategy_cooldowns.keys()):
                player_strategy.strategy_cooldowns[action_id] -= 1
                if player_strategy.strategy_cooldowns[action_id] <= 0:
                    del player_strategy.strategy_cooldowns[action_id]
    
    def display_strategy_menu(self, player: Player, game_state: GameState):
        """显示策略菜单"""
        available_strategies = self.get_available_strategies(player, game_state)
        
        if not available_strategies:
            enhanced_print("当前没有可用的策略行动", "info")
            return None
        
        ui_enhancement.clear_screen()
        print(ui_enhancement.create_title("高级策略", f"{player.name} 的策略选择"))
        
        # 创建策略表格
        headers = ["编号", "策略名称", "类型", "消耗", "描述"]
        rows = []
        
        for i, action in enumerate(available_strategies, 1):
            cost_str = ", ".join([f"{k}:{v}" for k, v in action.cost.items()])
            rows.append([
                str(i),
                action.name,
                action.strategy_type.value,
                cost_str,
                action.description[:40] + "..." if len(action.description) > 40 else action.description
            ])
        
        table = ui_enhancement.create_table(headers, rows)
        print(table)
        print()
        
        # 显示玩家当前状态
        self._display_player_strategy_status(player)
        
        try:
            choice = enhanced_input("选择策略 (输入数字，0返回): ")
            if choice == "0":
                return None
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(available_strategies):
                selected_action = available_strategies[choice_num - 1]
                
                # 显示详细信息并确认
                self._display_strategy_details(selected_action)
                confirm = enhanced_input("确认使用此策略? (y/n): ").lower()
                
                if confirm == 'y':
                    return selected_action
            else:
                enhanced_print("无效选择", "warning")
                
        except ValueError:
            enhanced_print("请输入有效数字", "error")
        
        return None
    
    def _display_player_strategy_status(self, player: Player):
        """显示玩家策略状态"""
        player_strategy = self.player_strategies.get(player.name)
        if not player_strategy:
            return
        
        print(ui_enhancement.create_section_header("策略状态"))
        print(f"协同加成: {player_strategy.synergy_bonus:.2f}x")
        print(f"变化历史: {len(player_strategy.transformation_history)} 次")
        
        if player_strategy.strategy_cooldowns:
            print("冷却中的策略:")
            for action_id, cooldown in player_strategy.strategy_cooldowns.items():
                action_name = self.strategy_actions.get(action_id, {}).get("name", action_id)
                print(f"  {action_name}: {cooldown} 回合")
        print()
    
    def _display_strategy_details(self, action: StrategyAction):
        """显示策略详细信息"""
        print(ui_enhancement.create_section_header("策略详情"))
        print(f"名称: {action.name}")
        print(f"类型: {action.strategy_type.value}")
        print(f"描述: {action.description}")
        print(f"消耗: {', '.join([f'{k}:{v}' for k, v in action.cost.items()])}")
        print(f"冷却: {action.cooldown} 回合")
        print(f"条件: {', '.join(action.conditions)}")
        print()

# 全局实例
advanced_strategy_system = AdvancedStrategySystem()

def display_hexagram_strategy_guide():
    """显示卦象策略指南"""
    ui_enhancement.clear_screen()
    print(ui_enhancement.create_title("卦象策略指南", "深度易经智慧"))
    
    print(ui_enhancement.create_section_header("基础概念"))
    print("• 变卦: 通过改变爻位获得新的卦象力量")
    print("• 互卦: 显现卦象内在的变化趋势")
    print("• 错卦: 阴阳相反的卦象，互为补充")
    print("• 综卦: 上下颠倒的卦象，时序相反")
    print()
    
    print(ui_enhancement.create_section_header("策略类型"))
    for strategy_type in StrategyType:
        print(f"• {strategy_type.value}: 基于{strategy_type.name.lower()}的策略方法")
    print()
    
    print(ui_enhancement.create_section_header("高级技巧"))
    print("• 观察卦象关系，寻找协同机会")
    print("• 平衡阴阳五行，获得和谐力量")
    print("• 把握时机，在关键时刻使用强力策略")
    print("• 适应变化，根据局势调整策略方向")
    print()
    
    enhanced_input("按回车键继续...")

if __name__ == "__main__":
    # 测试高级策略系统
    print("=== 高级策略系统测试 ===")
    display_hexagram_strategy_guide()