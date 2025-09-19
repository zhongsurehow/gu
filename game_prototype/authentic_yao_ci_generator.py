#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真实易经爻辞任务生成器
基于authentic_yao_ci.py中的真实爻辞数据生成游戏任务
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
import random
from card_base import YaoCiTask
from authentic_yao_ci import AUTHENTIC_YAO_CI_DATA, AuthenticYaoCi, get_authentic_yao_ci_tasks
from config_manager import get_config

@dataclass
class GameContext:
    """游戏上下文信息，用于判断爻辞任务的触发条件"""
    player_dao_xing: int
    player_cheng_yi: int
    player_yin: int
    player_yang: int
    other_players_dao_xing: List[int]
    turn_number: int
    recent_actions: List[str]
    negative_states: List[str]
    
class AuthenticYaoCiGenerator:
    """真实爻辞任务生成器"""
    
    def __init__(self):
        self.context: Optional[GameContext] = None
        
    def set_game_context(self, context: GameContext):
        """设置游戏上下文"""
        self.context = context
        
    def generate_contextual_yao_ci_tasks(self, gua_name: str) -> List[YaoCiTask]:
        """根据游戏上下文生成爻辞任务"""
        # 直接从AUTHENTIC_YAO_CI_DATA获取爻辞数据
        if gua_name not in AUTHENTIC_YAO_CI_DATA:
            return self._generate_fallback_tasks(gua_name)
        
        yao_ci_list = AUTHENTIC_YAO_CI_DATA[gua_name]
        
        # 确保有6个爻辞数据
        if len(yao_ci_list) != 6:
            return self._generate_fallback_tasks(gua_name)
        
        # 根据上下文筛选合适的爻辞，但确保返回6个任务
        contextual_tasks = []
        for yao_ci in yao_ci_list:
            task = self._create_enhanced_task(yao_ci, gua_name)
            contextual_tasks.append(task)
            
        return contextual_tasks
    
    def _check_condition(self, yao_ci: AuthenticYaoCi) -> bool:
        """检查爻辞的触发条件是否满足"""
        if not self.context:
            return True  # 没有上下文时默认可用
            
        condition = yao_ci.condition.lower()
        
        # 检查道行相关条件
        if "道行比你高" in condition:
            return any(dao > self.context.player_dao_xing for dao in self.context.other_players_dao_xing)
        elif "道行全场最高" in condition:
            return all(self.context.player_dao_xing >= dao for dao in self.context.other_players_dao_xing)
        elif "道行超过70点" in condition:
            return self.context.player_dao_xing > 70
            
        # 检查行动相关条件
        if "3次或以上行动" in condition:
            return len(self.context.recent_actions) >= 3
        elif "保守行动" in condition:
            return "保守" in str(self.context.recent_actions)
            
        # 检查阴阳平衡条件
        if "阴阳平衡度达到90%" in condition:
            total = self.context.player_yin + self.context.player_yang
            if total > 0:
                balance = min(self.context.player_yin, self.context.player_yang) / total
                return balance >= 0.45  # 90%平衡意味着45%-55%的分布
                
        # 检查负面状态条件
        if "负面状态" in condition or "危险" in condition:
            return len(self.context.negative_states) > 0
            
        # 检查失衡条件
        if "阴阳严重失衡" in condition:
            total = self.context.player_yin + self.context.player_yang
            if total > 0:
                balance = min(self.context.player_yin, self.context.player_yang) / total
                return balance < 0.2  # 严重失衡
                
        # 默认条件
        return True
    
    def _create_enhanced_task(self, yao_ci: AuthenticYaoCi, gua_name: str) -> YaoCiTask:
        """创建增强的爻辞任务"""
        # 根据配置调整奖励
        base_dao_xing = get_config("yao_ci.base_dao_xing_reward", 1)
        base_cheng_yi = get_config("yao_ci.base_cheng_yi_reward", 1)
        
        adjusted_dao_xing = yao_ci.reward_dao_xing * base_dao_xing
        adjusted_cheng_yi = yao_ci.reward_cheng_yi * base_cheng_yi
        
        # 创建详细的任务描述
        full_description = f"""
【原文】{yao_ci.original_text}

【释义】{yao_ci.interpretation}

【游戏效果】{yao_ci.game_effect}

【触发条件】{yao_ci.condition}

【特殊效果】{yao_ci.special_effect}
        """.strip()
        
        task = YaoCiTask(
            level=yao_ci.position,
            name=f"{gua_name}·{yao_ci.position}",
            description=full_description,
            reward_dao_xing=adjusted_dao_xing,
            reward_cheng_yi=adjusted_cheng_yi
        )
        
        return task
    
    def _create_basic_tasks(self, yao_ci_list: List[AuthenticYaoCi], gua_name: str) -> List[YaoCiTask]:
        """创建基础任务（当没有符合条件的任务时）"""
        tasks = []
        for yao_ci in yao_ci_list:
            task = self._create_enhanced_task(yao_ci, gua_name)
            tasks.append(task)
        return tasks
    
    def _generate_fallback_tasks(self, gua_name: str) -> List[YaoCiTask]:
        """为没有具体爻辞数据的卦生成后备任务"""
        # 生成6个标准的爻辞任务
        positions = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]
        levels = ["地", "地", "人", "人", "天", "天"]
        
        tasks = []
        for i, (position, level) in enumerate(zip(positions, levels)):
            task = YaoCiTask(
                level=level,
                name=f"{gua_name}·{position}",
                description=f"该卦({gua_name})的{position}爻辞任务尚未实现真实爻辞，使用通用模板。",
                reward_dao_xing=1 if i < 4 else 2,  # 前四爻1点，后两爻2点
                reward_cheng_yi=1 if i % 2 == 0 else 2  # 奇数爻1点，偶数爻2点
            )
            tasks.append(task)
        
        return tasks

class YaoCiEffectProcessor:
    """爻辞特殊效果处理器"""
    
    def __init__(self):
        self.active_effects: Dict[str, int] = {}  # 效果名称 -> 剩余回合数
        
    def apply_special_effect(self, effect_description: str, player_state: Dict) -> Dict:
        """应用爻辞的特殊效果"""
        effect = effect_description.lower()
        
        # 处理各种特殊效果
        if "获得" in effect and "阴气" in effect and "阳气" in effect:
            # 例如："获得2点阴气和2点阳气"
            import re
            yin_match = re.search(r'(\d+)点阴气', effect)
            yang_match = re.search(r'(\d+)点阳气', effect)
            if yin_match:
                player_state['yin'] = player_state.get('yin', 0) + int(yin_match.group(1))
            if yang_match:
                player_state['yang'] = player_state.get('yang', 0) + int(yang_match.group(1))
                
        elif "下回合行动效果+1" in effect:
            self.active_effects["行动加成"] = 1
            
        elif "免疫所有负面效果" in effect:
            self.active_effects["负面免疫"] = 1
            
        elif "行动精准度+100%" in effect:
            self.active_effects["精准行动"] = 1
            
        elif "效果翻倍" in effect:
            self.active_effects["效果翻倍"] = 1
            
        elif "获得领袖地位" in effect:
            self.active_effects["领袖"] = 3  # 持续3回合
            
        elif "智者" in effect:
            self.active_effects["智者"] = -1  # 永久效果
            
        return player_state
    
    def process_turn_start(self) -> List[str]:
        """处理回合开始时的效果"""
        active_this_turn = []
        expired_effects = []
        
        for effect_name, remaining_turns in self.active_effects.items():
            if remaining_turns > 0:
                active_this_turn.append(effect_name)
                self.active_effects[effect_name] -= 1
                if self.active_effects[effect_name] == 0:
                    expired_effects.append(effect_name)
            elif remaining_turns == -1:  # 永久效果
                active_this_turn.append(effect_name)
                
        # 移除过期效果
        for effect in expired_effects:
            del self.active_effects[effect]
            
        return active_this_turn
    
    def has_effect(self, effect_name: str) -> bool:
        """检查是否有特定效果"""
        return effect_name in self.active_effects and self.active_effects[effect_name] != 0

# 全局实例
authentic_generator = AuthenticYaoCiGenerator()
effect_processor = YaoCiEffectProcessor()

def generate_authentic_yao_ci_tasks(gua_name: str, game_context: Optional[GameContext] = None) -> List[YaoCiTask]:
    """生成真实的爻辞任务（便捷函数）"""
    if game_context:
        authentic_generator.set_game_context(game_context)
    return authentic_generator.generate_contextual_yao_ci_tasks(gua_name)