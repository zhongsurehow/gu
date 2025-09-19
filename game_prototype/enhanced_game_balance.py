#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强游戏平衡系统
优化游戏机制，提升策略深度和平衡性
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import random

from game_state import GameState, Player, Zone
from yijing_mechanics import YinYang, WuXing
from card_base import GuaCard

@dataclass
class BalanceConfig:
    """游戏平衡配置"""
    # 基础资源配置 - 优化后的配置
    initial_qi: int = 8  # 初始气值（从6提升到8，增加60%）
    initial_dao_xing: int = 1  # 初始道行（从0提升到1，给予起始优势）
    initial_cheng_yi: int = 2  # 初始诚意（从1提升到2，增强初期能力）
    initial_hand_size: int = 3  # 初始手牌数
    
    # 行动点配置
    base_action_points: int = 3  # 基础行动点
    max_action_points: int = 5  # 最大行动点
    
    # 资源上限
    max_qi: int = 25  # 气值上限（从20提升到25）
    max_dao_xing: int = 15  # 道行上限（胜利条件）
    max_cheng_yi: int = 12  # 诚意上限（从10提升到12）
    max_hand_size: int = 7  # 手牌上限
    
    # 动作成本配置 - 新增优化的成本设置
    divination_cost: int = 2  # 占卜运势成本（从3降低到2，降低33%）
    consult_yijing_cost: int = 1  # 咨询易经成本（新增低成本选项）
    meditation_cost: int = 0  # 冥想成本（免费基础行动）
    movement_cost: int = 1  # 移动成本（保持现状）
    
    # 资源获取奖励 - 新增奖励机制
    daily_qi_bonus: int = 1  # 每回合开始获得的气
    balance_qi_bonus: int = 1  # 阴阳平衡时的额外气奖励
    harmony_dao_bonus: int = 1  # 五行和谐时的道行奖励
    wisdom_cheng_bonus: int = 1  # 触发格言时的诚意奖励
    
    # 阴阳平衡配置
    yin_yang_balance_threshold: float = 0.3  # 平衡阈值
    extreme_imbalance_penalty: int = 2  # 极度失衡惩罚
    
    # 五行配置
    wuxing_mastery_threshold: int = 3  # 五行精通阈值
    wuxing_synergy_bonus: int = 1  # 五行协同奖励

class EnhancedGameBalance:
    """增强游戏平衡系统"""
    
    def __init__(self, config: BalanceConfig = None):
        self.config = config or BalanceConfig()
        self.dynamic_difficulty = {}  # 动态难度调整
        
    def apply_balanced_setup(self, game_state: GameState) -> GameState:
        """应用平衡的游戏设置"""
        for player in game_state.players:
            # 重置基础属性
            player.qi = self.config.initial_qi
            player.dao_xing = self.config.initial_dao_xing
            player.cheng_yi = self.config.initial_cheng_yi
            
            # 调整手牌到合适数量
            while len(player.hand) > self.config.initial_hand_size:
                player.hand.pop()
            
            # 初始化动态难度
            self.dynamic_difficulty[player.name] = 1.0
            
        return game_state
    
    def calculate_action_points(self, player: Player, game_state: GameState) -> int:
        """计算玩家的行动点数"""
        base_ap = self.config.base_action_points
        
        # 位置奖励
        position_bonus = {
            Zone.DI: 0,    # 地部：基础
            Zone.REN: 1,   # 人部：+1行动点
            Zone.TIAN: 2,  # 天部：+2行动点
            Zone.TAIJI: 1  # 太极：+1行动点，特殊效果
        }
        
        ap = base_ap + position_bonus.get(player.position, 0)
        
        # 阴阳平衡奖励
        if self.is_yin_yang_balanced(player):
            ap += 1
        
        # 五行协同奖励
        if self.has_wuxing_synergy(player):
            ap += 1
        
        # 诚意奖励（高诚意获得额外行动点）
        if player.cheng_yi >= 5:
            ap += 1
        
        return min(ap, self.config.max_action_points)
    
    def is_yin_yang_balanced(self, player: Player) -> bool:
        """检查玩家的阴阳是否平衡"""
        balance = player.yin_yang_balance
        total = balance.yin + balance.yang
        if total == 0:
            return True
        
        yin_ratio = balance.yin / total
        return abs(yin_ratio - 0.5) <= self.config.yin_yang_balance_threshold
    
    def has_wuxing_synergy(self, player: Player) -> bool:
        """检查玩家是否有五行协同效应"""
        affinities = player.wuxing_affinities
        active_elements = sum(1 for value in affinities.values() if value > 0)
        return active_elements >= 3
    
    def apply_resource_limits(self, player: Player) -> Player:
        """应用资源上限"""
        player.qi = min(player.qi, self.config.max_qi)
        player.dao_xing = min(player.dao_xing, self.config.max_dao_xing)
        player.cheng_yi = min(player.cheng_yi, self.config.max_cheng_yi)
        
        # 手牌上限
        while len(player.hand) > self.config.max_hand_size:
            # 随机弃牌，但优先保留低成本卡牌
            hand_costs = [(i, self.estimate_card_cost(card)) for i, card in enumerate(player.hand)]
            hand_costs.sort(key=lambda x: x[1], reverse=True)  # 按成本降序
            discard_index = hand_costs[0][0]
            player.hand.pop(discard_index)
        
        return player
    
    def estimate_card_cost(self, card: GuaCard) -> int:
        """估算卡牌成本（用于弃牌优先级）"""
        # 基础成本估算
        base_cost = 2
        
        # 根据任务数量调整
        task_cost = len(card.tasks) * 0.5
        
        # 根据卦象复杂度调整
        complexity_cost = len(card.associated_guas) * 0.3
        
        return int(base_cost + task_cost + complexity_cost)
    
    def apply_turn_start_bonuses(self, player: Player) -> Player:
        """应用回合开始时的资源奖励"""
        # 每日修行奖励：每回合开始获得气
        player.qi = min(player.qi + self.config.daily_qi_bonus, self.config.max_qi)
        
        # 阴阳平衡奖励
        if self.is_yin_yang_balanced(player):
            player.qi = min(player.qi + self.config.balance_qi_bonus, self.config.max_qi)
        
        # 五行和谐奖励
        if self.has_wuxing_synergy(player):
            player.dao_xing = min(player.dao_xing + self.config.harmony_dao_bonus, self.config.max_dao_xing)
        
        return player
    
    def apply_wisdom_bonus(self, player: Player) -> Player:
        """应用智慧格言触发时的奖励"""
        player.cheng_yi = min(player.cheng_yi + self.config.wisdom_cheng_bonus, self.config.max_cheng_yi)
        return player
    
    def get_action_cost(self, action_type: str) -> Dict[str, int]:
        """获取动作的资源成本"""
        action_costs = {
            "divine_fortune": {"qi": self.config.divination_cost},
            "consult_yijing": {"qi": self.config.consult_yijing_cost},
            "meditate": {"qi": self.config.meditation_cost},
            "move": {"qi": self.config.movement_cost},
            "study": {"qi": 1},  # 保持原有成本
            "transform": {"cheng_yi": 2},  # 保持原有成本
        }
        return action_costs.get(action_type, {})
    
    def calculate_enhanced_effects(self, player: Player, action_type: str) -> Dict[str, int]:
        """计算增强效果"""
        effects = {}
        
        # 阴阳平衡增强效果
        if self.is_yin_yang_balanced(player):
            if action_type == "meditate":
                effects["qi_bonus"] = 1
            elif action_type == "study":
                effects["dao_xing_bonus"] = 1
        
        # 五行协同增强效果
        if self.has_wuxing_synergy(player):
            if action_type == "divine_fortune":
                effects["accuracy_bonus"] = 0.2
            elif action_type == "consult_yijing":
                effects["wisdom_chance_bonus"] = 0.3
        
        # 高诚意增强效果
        if player.cheng_yi >= 5:
            effects["all_actions_enhanced"] = True
        
        return effects
    
    def apply_yin_yang_effects(self, player: Player) -> Dict[str, int]:
        """应用阴阳效果"""
        effects = {}
        balance = player.yin_yang_balance
        total = balance.yin + balance.yang
        
        if total == 0:
            return effects
        
        yin_ratio = balance.yin / total
        yang_ratio = balance.yang / total
        
        # 极度失衡惩罚
        if abs(yin_ratio - 0.5) > 0.7:
            effects["qi_penalty"] = -self.config.extreme_imbalance_penalty
            effects["message"] = "阴阳极度失衡，气息紊乱！"
        
        # 平衡奖励
        elif abs(yin_ratio - 0.5) <= self.config.yin_yang_balance_threshold:
            effects["qi_bonus"] = 1
            effects["dao_xing_bonus"] = 1
            effects["message"] = "阴阳调和，天人合一！"
        
        # 偏阳效果
        elif yang_ratio > 0.7:
            effects["action_bonus"] = 1
            effects["message"] = "阳气充盛，行动力增强！"
        
        # 偏阴效果
        elif yin_ratio > 0.7:
            effects["wisdom_bonus"] = 1
            effects["message"] = "阴柔内敛，智慧增长！"
        
        return effects
    
    def apply_wuxing_effects(self, player: Player) -> Dict[str, int]:
        """应用五行效果"""
        effects = {}
        affinities = player.wuxing_affinities
        
        # 检查五行精通
        mastered_elements = [element for element, value in affinities.items() 
                           if value >= self.config.wuxing_mastery_threshold]
        
        if len(mastered_elements) >= 3:
            effects["synergy_bonus"] = self.config.wuxing_synergy_bonus
            effects["message"] = f"精通{len(mastered_elements)}种五行，获得协同效应！"
        
        # 单一五行特化效果
        max_element = max(affinities.items(), key=lambda x: x[1])
        if max_element[1] >= 5:
            element_effects = {
                WuXing.JIN: {"qi_bonus": 2, "message": "金行特化：气息凝练！"},
                WuXing.MU: {"hand_bonus": 1, "message": "木行特化：生机勃勃！"},
                WuXing.SHUI: {"wisdom_bonus": 2, "message": "水行特化：智慧如海！"},
                WuXing.HUO: {"action_bonus": 1, "message": "火行特化：行动如火！"},
                WuXing.TU: {"stability_bonus": 1, "message": "土行特化：稳如泰山！"}
            }
            effects.update(element_effects.get(max_element[0], {}))
        
        return effects
    
    def calculate_victory_progress(self, player: Player) -> Dict[str, float]:
        """计算各种胜利条件的进度"""
        progress = {}
        
        # 传统胜利（道行）
        progress["dao_xing"] = player.dao_xing / self.config.max_dao_xing
        
        # 阴阳大师
        balance_score = 1.0 - abs(self.get_yin_yang_ratio(player) - 0.5) * 2
        progress["yin_yang_master"] = min(balance_score * (player.dao_xing / 10), 1.0)
        
        # 五行宗师
        mastered_count = sum(1 for value in player.wuxing_affinities.values() 
                           if value >= self.config.wuxing_mastery_threshold)
        progress["wuxing_master"] = mastered_count / 5
        
        # 变化之道（基于变卦历史）
        change_count = len(player.transformation_history)
        progress["transformation"] = min(change_count / 8, 1.0)
        
        return progress
    
    def get_yin_yang_ratio(self, player: Player) -> float:
        """获取阴阳比例"""
        balance = player.yin_yang_balance
        total = balance.yin + balance.yang
        return balance.yin / total if total > 0 else 0.5
    
    def adjust_dynamic_difficulty(self, player: Player, game_state: GameState):
        """动态难度调整"""
        current_difficulty = self.dynamic_difficulty.get(player.name, 1.0)
        
        # 根据玩家表现调整难度
        progress = self.calculate_victory_progress(player)
        max_progress = max(progress.values())
        
        if max_progress > 0.8:
            # 接近胜利，增加难度
            self.dynamic_difficulty[player.name] = min(current_difficulty * 1.1, 2.0)
        elif max_progress < 0.3:
            # 进度缓慢，降低难度
            self.dynamic_difficulty[player.name] = max(current_difficulty * 0.9, 0.5)
    
    def get_balanced_card_draw_count(self, player: Player, base_count: int) -> int:
        """获取平衡的抽牌数量"""
        difficulty = self.dynamic_difficulty.get(player.name, 1.0)
        
        # 根据难度调整抽牌数
        if difficulty > 1.5:
            return max(base_count - 1, 1)
        elif difficulty < 0.7:
            return base_count + 1
        else:
            return base_count

# 全局平衡配置实例
game_balance = EnhancedGameBalance()