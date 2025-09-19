#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
易经智慧引导系统
为玩家提供基于易经哲学的人生指导和游戏策略建议
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import random

from complete_64_guas_system import complete_guas_system, GuaPhilosophy, YaoPhilosophy
from yijing_mechanics import YinYang, WuXing

class LifeAspect(Enum):
    """人生方面"""
    CAREER = "事业"
    RELATIONSHIP = "人际关系"
    HEALTH = "健康"
    LEARNING = "学习"
    WEALTH = "财富"
    FAMILY = "家庭"
    SPIRITUAL = "精神修养"
    DECISION = "决策"

@dataclass
class WisdomGuidance:
    """智慧指导"""
    aspect: LifeAspect
    situation: str  # 当前情况
    gua_name: str  # 相关卦象
    wisdom: str  # 智慧指导
    action_advice: str  # 行动建议
    warning: str  # 注意事项
    timing: str  # 时机把握

class YijingWisdomGuide:
    """易经智慧引导系统"""
    
    def __init__(self):
        self.wisdom_database = self._initialize_wisdom_database()
        self.life_situations = self._initialize_life_situations()
        
    def _initialize_wisdom_database(self) -> Dict[str, Dict[LifeAspect, WisdomGuidance]]:
        """初始化智慧数据库"""
        wisdom_db = {}
        
        # 乾卦智慧指导
        wisdom_db["乾为天"] = {
            LifeAspect.CAREER: WisdomGuidance(
                aspect=LifeAspect.CAREER,
                situation="事业发展的关键时期",
                gua_name="乾为天",
                wisdom="天行健，君子以自强不息。事业成功需要持续的努力和坚定的意志。",
                action_advice="主动出击，发挥领导才能，但要循序渐进，不可急于求成。",
                warning="避免过于刚猛，要懂得适时调整策略。",
                timing="适合开创新事业，但要选择合适的时机。"
            ),
            LifeAspect.RELATIONSHIP: WisdomGuidance(
                aspect=LifeAspect.RELATIONSHIP,
                situation="需要展现领导力的人际关系",
                gua_name="乾为天",
                wisdom="真正的领导者以德服人，而非以力压人。",
                action_advice="发挥正面影响力，帮助他人成长，建立威信。",
                warning="不要过于强势，要给他人表现的机会。",
                timing="适合在团队中承担更多责任。"
            ),
            LifeAspect.DECISION: WisdomGuidance(
                aspect=LifeAspect.DECISION,
                situation="面临重大决策",
                gua_name="乾为天",
                wisdom="大人者，正己而物正者也。先正己，再正人。",
                action_advice="基于正确的价值观做决定，考虑长远影响。",
                warning="避免独断专行，要听取他人意见。",
                timing="决策要果断，但要充分准备。"
            )
        }
        
        # 坤卦智慧指导
        wisdom_db["坤为地"] = {
            LifeAspect.CAREER: WisdomGuidance(
                aspect=LifeAspect.CAREER,
                situation="需要配合和支持的工作环境",
                gua_name="坤为地",
                wisdom="地势坤，君子以厚德载物。成功不仅在于个人能力，更在于包容和承载。",
                action_advice="发挥支持作用，善于配合他人，在团队中体现价值。",
                warning="不要过于被动，要在适当时候表达自己的观点。",
                timing="适合在稳定的环境中发展，积累经验。"
            ),
            LifeAspect.RELATIONSHIP: WisdomGuidance(
                aspect=LifeAspect.RELATIONSHIP,
                situation="需要包容和理解的人际关系",
                gua_name="坤为地",
                wisdom="包容是最大的智慧，理解是最深的爱。",
                action_advice="以包容的心态对待他人，善于倾听和理解。",
                warning="包容不等于纵容，要有原则和底线。",
                timing="适合修复关系，化解矛盾。"
            ),
            LifeAspect.FAMILY: WisdomGuidance(
                aspect=LifeAspect.FAMILY,
                situation="家庭和谐与责任",
                gua_name="坤为地",
                wisdom="家和万事兴，家庭是人生的根基。",
                action_advice="承担家庭责任，营造和谐氛围，关爱家人。",
                warning="不要忽视自己的需求，要平衡家庭和个人发展。",
                timing="适合加强家庭联系，处理家庭事务。"
            )
        }
        
        # 屯卦智慧指导
        wisdom_db["水雷屯"] = {
            LifeAspect.CAREER: WisdomGuidance(
                aspect=LifeAspect.CAREER,
                situation="事业初创的艰难时期",
                gua_name="水雷屯",
                wisdom="万事开头难，但困难中蕴含着机遇。坚持就是胜利。",
                action_advice="在困难中坚持，积累经验，寻找突破口。",
                warning="不要被困难吓倒，但也要实事求是，量力而行。",
                timing="适合打基础，积累实力，等待时机。"
            ),
            LifeAspect.LEARNING: WisdomGuidance(
                aspect=LifeAspect.LEARNING,
                situation="学习新知识的困难期",
                gua_name="水雷屯",
                wisdom="学而时习之，不亦说乎。困难是成长的阶梯。",
                action_advice="坚持学习，不怕困难，寻求帮助和指导。",
                warning="不要因为困难而放弃，要相信自己的潜力。",
                timing="适合深入学习，打好基础。"
            )
        }
        
        # 蒙卦智慧指导
        wisdom_db["山水蒙"] = {
            LifeAspect.LEARNING: WisdomGuidance(
                aspect=LifeAspect.LEARNING,
                situation="启蒙教育和知识获取",
                gua_name="山水蒙",
                wisdom="知之为知之，不知为不知，是知也。真正的智慧始于承认无知。",
                action_advice="保持谦逊的学习态度，主动求教，循序渐进。",
                warning="不要不懂装懂，要诚实面对自己的不足。",
                timing="适合开始新的学习，寻找导师。"
            ),
            LifeAspect.SPIRITUAL: WisdomGuidance(
                aspect=LifeAspect.SPIRITUAL,
                situation="精神启蒙和修养提升",
                gua_name="山水蒙",
                wisdom="修身齐家治国平天下，一切从修身开始。",
                action_advice="注重品德修养，培养正确的价值观。",
                warning="不要急于求成，精神修养需要时间积累。",
                timing="适合反思自己，提升品德修养。"
            )
        }
        
        return wisdom_db
    
    def _initialize_life_situations(self) -> Dict[str, List[str]]:
        """初始化人生情境"""
        return {
            "困难挑战": [
                "面临重大挫折，不知如何应对",
                "遇到强大的竞争对手",
                "资源不足，难以推进计划",
                "团队内部出现分歧",
                "外部环境发生不利变化"
            ],
            "机遇选择": [
                "出现多个发展机会，难以选择",
                "有机会承担更大责任",
                "可以学习新的技能或知识",
                "遇到重要的合作伙伴",
                "获得投资或支持的机会"
            ],
            "人际关系": [
                "与重要人物建立联系",
                "需要处理复杂的人际关系",
                "团队合作中的角色定位",
                "领导与被领导的关系",
                "朋友之间的信任问题"
            ],
            "个人成长": [
                "需要提升某项能力",
                "面临价值观的冲突",
                "寻找人生方向和目标",
                "平衡工作与生活",
                "处理内心的焦虑和压力"
            ]
        }
    
    def get_wisdom_guidance(self, gua_name: str, aspect: LifeAspect) -> Optional[WisdomGuidance]:
        """获取智慧指导"""
        gua_wisdom = self.wisdom_database.get(gua_name, {})
        return gua_wisdom.get(aspect)
    
    def get_life_advice(self, current_situation: str, player_state: Dict) -> str:
        """根据当前情况获取人生建议"""
        # 分析玩家状态，选择最适合的卦象
        suitable_gua = self._analyze_suitable_gua(current_situation, player_state)
        
        # 获取卦象哲学
        gua_philosophy = complete_guas_system.get_gua_philosophy(suitable_gua)
        if not gua_philosophy:
            return "变化是永恒的真理，顺应变化，把握当下。"
        
        # 生成综合建议
        advice = f"【{suitable_gua}】指导：\n\n"
        advice += f"卦象智慧：{gua_philosophy.life_wisdom}\n\n"
        advice += f"策略建议：{gua_philosophy.strategic_advice}\n\n"
        advice += f"原文启示：{gua_philosophy.xiang_ci}"
        
        return advice
    
    def _analyze_suitable_gua(self, situation: str, player_state: Dict) -> str:
        """分析适合的卦象"""
        # 根据情况关键词匹配卦象
        situation_keywords = {
            "困难": ["水雷屯", "山水蒙", "水天需"],
            "机遇": ["乾为天", "震为雷", "离为火"],
            "合作": ["坤为地", "水地比", "风地观"],
            "学习": ["山水蒙", "风山渐", "雷风恒"],
            "决策": ["乾为天", "天水讼", "泽天夬"],
            "等待": ["水天需", "山雷颐", "风雷益"],
            "变化": ["泽火革", "火风鼎", "雷水解"]
        }
        
        for keyword, guas in situation_keywords.items():
            if keyword in situation:
                return random.choice(guas)
        
        # 根据玩家状态选择
        qi_level = player_state.get("qi", 0)
        dao_xing = player_state.get("dao_xing", 0)
        
        if qi_level > dao_xing:
            return "乾为天"  # 阳气旺盛
        elif dao_xing > qi_level:
            return "坤为地"  # 道行深厚
        else:
            return "水火既济"  # 平衡状态
    
    def get_daily_wisdom(self) -> str:
        """获取每日智慧"""
        daily_wisdoms = [
            "天行健，君子以自强不息。",
            "地势坤，君子以厚德载物。",
            "云雷屯，君子以经纶。",
            "山下出泉，蒙；君子以果行育德。",
            "云上于天，需；君子以饮食宴乐。",
            "天与水违行，讼；君子以作事谋始。",
            "地中有水，师；君子以容民畜众。",
            "地上有水，比；先王以建万国，亲诸侯。"
        ]
        return random.choice(daily_wisdoms)
    
    def get_strategic_wisdom(self, game_situation: Dict) -> str:
        """获取游戏策略智慧"""
        current_zone = game_situation.get("zone", "地部")
        player_resources = game_situation.get("resources", {})
        opponents = game_situation.get("opponents", [])
        
        if current_zone == "地部":
            return "潜龙勿用。在基础阶段要韬光养晦，积蓄实力。"
        elif current_zone == "人部":
            return "见龙在田，利见大人。要主动建立联系，寻求合作。"
        elif current_zone == "天部":
            return "飞龙在天，利见大人。发挥领导作用，但要避免过度。"
        
        return "时中之道，随机应变。"
    
    def interpret_yao_change(self, gua_name: str, changing_yao: int) -> str:
        """解释爻变的含义"""
        yao_philosophy = complete_guas_system.get_yao_philosophy(gua_name, changing_yao)
        if not yao_philosophy:
            return "变化带来新的机遇，要善于把握。"
        
        interpretation = f"【{yao_philosophy.yao_name}】{yao_philosophy.yao_ci}\n\n"
        interpretation += f"人生情境：{yao_philosophy.life_situation}\n\n"
        interpretation += f"行动指导：{yao_philosophy.action_guidance}"
        
        return interpretation
    
    def get_meditation_guidance(self, player_mood: str) -> str:
        """获取冥想指导"""
        meditation_guides = {
            "焦虑": "深呼吸，观想自己如山般稳定，如水般流动。焦虑如云，终将散去。",
            "愤怒": "愤怒如火，需要水的智慧来平息。想象自己站在宁静的湖边，让心平静下来。",
            "困惑": "困惑如雾，需要风的力量来吹散。相信内心的智慧，答案自然显现。",
            "悲伤": "悲伤如雨，滋润着成长的土壤。允许情感流动，然后重新开始。",
            "兴奋": "兴奋如雷，要学会适度。保持内心的平衡，避免过度消耗。"
        }
        
        return meditation_guides.get(player_mood, "静坐观心，万法归一。在宁静中寻找智慧。")

# 全局智慧引导系统实例
wisdom_guide = YijingWisdomGuide()