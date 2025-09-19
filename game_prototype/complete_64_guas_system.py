#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整64卦系统 - 深度易经内涵
包含每卦的详细解释、爻辞、象辞、彖辞等完整易经内容
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

from yijing_mechanics import YinYang, WuXing
from card_base import GuaCard, YaoCiTask

@dataclass
class GuaPhilosophy:
    """卦象哲学内涵"""
    name: str
    number: int  # 卦序
    trigrams: Tuple[str, str]  # (上卦, 下卦)
    
    # 基础属性
    element: WuXing
    yin_yang: YinYang
    nature: str  # 卦性
    
    # 易经原文
    gua_ci: str  # 卦辞
    tuan_ci: str  # 彖辞
    xiang_ci: str  # 象辞
    
    # 现代解释
    meaning: str  # 卦义
    life_wisdom: str  # 人生智慧
    strategic_advice: str  # 策略建议
    
    # 游戏机制
    special_ability: str  # 特殊能力
    synergy_guas: List[str]  # 协同卦象
    counter_guas: List[str]  # 相克卦象

@dataclass
class YaoPhilosophy:
    """爻辞哲学内涵"""
    position: int  # 爻位 (1-6)
    yao_name: str  # 爻名
    yao_ci: str  # 爻辞
    xiang_ci: str  # 小象
    
    # 现代解释
    meaning: str  # 爻义
    life_situation: str  # 人生情境
    action_guidance: str  # 行动指导
    
    # 游戏效果
    game_effect: Dict[str, int]  # 游戏效果
    trigger_condition: str  # 触发条件

class Complete64GuasSystem:
    """完整64卦系统"""
    
    def __init__(self):
        self.guas_philosophy = self._initialize_guas_philosophy()
        self.yaos_philosophy = self._initialize_yaos_philosophy()
        self.gua_relationships = self._initialize_gua_relationships()
        
    def _initialize_guas_philosophy(self) -> Dict[str, GuaPhilosophy]:
        """初始化64卦哲学内涵"""
        guas = {}
        
        # 乾卦 - 第1卦
        guas["乾为天"] = GuaPhilosophy(
            name="乾为天",
            number=1,
            trigrams=("乾", "乾"),
            element=WuXing.JIN,
            yin_yang=YinYang.YANG,
            nature="刚健",
            gua_ci="乾：元，亨，利，贞。",
            tuan_ci="大哉乾元，万物资始，乃统天。云行雨施，品物流形。大明终始，六位时成，时乘六龙以御天。乾道变化，各正性命，保合大和，乃利贞。首出庶物，万国咸宁。",
            xiang_ci="天行健，君子以自强不息。",
            meaning="乾卦象征天，代表刚健、创造、领导的力量。是纯阳之卦，具有开创万物的能力。",
            life_wisdom="天道刚健，君子应当效法天的品德，自强不息，永不懈怠。在人生中要有创造精神，敢于开拓，勇于承担责任。",
            strategic_advice="适合主动出击，开创新局面。要发挥领导才能，但要注意不可过于刚猛，需要把握时机。",
            special_ability="增强所有阳性行动的效果，提升领导力和创造力",
            synergy_guas=["坤为地", "震为雷", "离为火"],
            counter_guas=["坤为地"]  # 对立统一
        )
        
        # 坤卦 - 第2卦
        guas["坤为地"] = GuaPhilosophy(
            name="坤为地",
            number=2,
            trigrams=("坤", "坤"),
            element=WuXing.TU,
            yin_yang=YinYang.YIN,
            nature="柔顺",
            gua_ci="坤：元，亨，利牝马之贞。君子有攸往，先迷后得主，利西南得朋，东北丧朋。安贞吉。",
            tuan_ci="至哉坤元，万物资生，乃顺承天。坤厚载物，德合无疆。含弘光大，品物咸亨。牝马地类，行地无疆，柔顺利贞。君子攸行，先迷失道，后顺得常。西南得朋，乃与类行；东北丧朋，乃终有庆。安贞之吉，应地无疆。",
            xiang_ci="地势坤，君子以厚德载物。",
            meaning="坤卦象征地，代表柔顺、包容、承载的力量。是纯阴之卦，具有孕育万物的能力。",
            life_wisdom="地道柔顺，君子应当效法大地的品德，厚德载物，包容万物。在人生中要有包容精神，善于配合，懂得承载。",
            strategic_advice="适合配合他人，发挥支持作用。要发挥包容力和承载力，但要注意不可过于被动，需要适时主动。",
            special_ability="增强所有阴性行动的效果，提升包容力和承载力",
            synergy_guas=["乾为天", "巽为风", "坎为水"],
            counter_guas=["乾为天"]  # 对立统一
        )
        
        # 屯卦 - 第3卦
        guas["水雷屯"] = GuaPhilosophy(
            name="水雷屯",
            number=3,
            trigrams=("坎", "震"),
            element=WuXing.SHUI,
            yin_yang=YinYang.YANG,
            nature="艰难",
            gua_ci="屯：元，亨，利，贞。勿用，有攸往，利建侯。",
            tuan_ci="屯，刚柔始交而难生，动乎险中，大亨贞。雷雨之动满盈，天造草昧，宜建侯而不宁。",
            xiang_ci="云雷，屯；君子以经纶。",
            meaning="屯卦象征初生的艰难，如雷在水中，动而遇险。代表事物初创时期的困难。",
            life_wisdom="万事开头难，但正是在困难中才能显示出真正的品格。要有坚持不懈的精神，在困难中寻找机会。",
            strategic_advice="适合在困难中坚持，积累实力。要善于在混乱中建立秩序，但不宜急于求成。",
            special_ability="在困难情况下获得额外资源，提升在逆境中的适应能力",
            synergy_guas=["蒙山水蒙", "需水天需"],
            counter_guas=["既济水火既济"]
        )
        
        # 蒙卦 - 第4卦
        guas["山水蒙"] = GuaPhilosophy(
            name="山水蒙",
            number=4,
            trigrams=("艮", "坎"),
            element=WuXing.TU,
            yin_yang=YinYang.YIN,
            nature="启蒙",
            gua_ci="蒙：亨。匪我求童蒙，童蒙求我。初噬告，再三渎，渎则不告。利贞。",
            tuan_ci="蒙，山下有险，险而止，蒙。蒙亨，以亨行时中也。匪我求童蒙，童蒙求我，志应也。初噬告，以刚中也。再三渎，渎则不告，渎蒙也。蒙以养正，圣功也。",
            xiang_ci="山下出泉，蒙；君子以果行育德。",
            meaning="蒙卦象征启蒙教育，如山下有泉水，需要引导才能流出。代表学习和教育的过程。",
            life_wisdom="学而时习之，不亦说乎。真正的学习需要主动求知，老师的作用是启发而非灌输。",
            strategic_advice="适合学习和教育，要保持谦逊的学习态度。在教导他人时要因材施教，循序渐进。",
            special_ability="增强学习效果，提升智慧获得速度",
            synergy_guas=["水雷屯", "风山渐"],
            counter_guas=["火泽睽"]
        )
        
        # 需卦 - 第5卦
        guas["水天需"] = GuaPhilosophy(
            name="水天需",
            number=5,
            trigrams=("坎", "乾"),
            element=WuXing.SHUI,
            yin_yang=YinYang.YANG,
            nature="等待",
            gua_ci="需：有孚，光亨，贞吉。利涉大川。",
            tuan_ci="需，须也，险在前也。刚健而不陷，其义不困穷矣。需有孚，光亨，贞吉。位乎天位，以正中也。利涉大川，往有功也。",
            xiang_ci="云上于天，需；君子以饮食宴乐。",
            meaning="需卦象征等待时机，如云聚于天，等待降雨。代表在困难面前的耐心等待。",
            life_wisdom="时机未到时要耐心等待，但等待不是消极的，而是积极的准备。君子待时而动，不急不躁。",
            strategic_advice="适合等待时机，积蓄力量。要保持信心和耐心，在等待中完善自己。",
            special_ability="在等待期间获得额外收益，提升时机把握能力",
            synergy_guas=["天水讼", "水雷屯"],
            counter_guas=["火山旅"]
        )
        
        # 讼卦 - 第6卦
        guas["天水讼"] = GuaPhilosophy(
            name="天水讼",
            number=6,
            trigrams=("乾", "坎"),
            element=WuXing.JIN,
            yin_yang=YinYang.YANG,
            nature="争讼",
            gua_ci="讼：有孚，窒。惕中吉。终凶。利见大人，不利涉大川。",
            tuan_ci="讼，上刚下险，险而健，讼。讼有孚窒，惕中吉，刚来而得中也。终凶，讼不可成也。利见大人，尚中正也。不利涉大川，入于渊也。",
            xiang_ci="天与水违行，讼；君子以作事谋始。",
            meaning="讼卦象征争讼冲突，如天与水背道而驰。代表矛盾和争执的状态。",
            life_wisdom="争讼虽然有时不可避免，但要慎重对待。最好的解决方式是预防，凡事谋定而后动。",
            strategic_advice="适合解决冲突，但要谨慎行事。要寻求公正的仲裁，避免意气用事。",
            special_ability="在冲突中获得优势，提升辩论和谈判能力",
            synergy_guas=["水天需", "火水未济"],
            counter_guas=["地水师"]
        )
        
        # 师卦 - 第7卦
        guas["地水师"] = GuaPhilosophy(
            name="地水师",
            number=7,
            trigrams=("坤", "坎"),
            element=WuXing.TU,
            yin_yang=YinYang.YIN,
            nature="军旅",
            gua_ci="师：贞，丈人，吉无咎。",
            tuan_ci="师，众也，贞正也，能以众正，可以王矣。刚中而应，行险而顺，以此毒天下，而民从之，吉又何咎矣。",
            xiang_ci="地中有水，师；君子以容民畜众。",
            meaning="师卦象征军队，如地中蓄水，聚众成军。代表组织和领导的智慧。",
            life_wisdom="领导众人需要德才兼备，要有包容心和组织能力。正义的事业才能得到民众的支持。",
            strategic_advice="适合组织团队，发挥领导作用。要以德服人，建立威信，但要避免滥用权力。",
            special_ability="增强团队协作效果，提升组织领导能力",
            synergy_guas=["天水讼", "水地比"],
            counter_guas=["火天大有"]
        )
        
        # 比卦 - 第8卦
        guas["水地比"] = GuaPhilosophy(
            name="水地比",
            number=8,
            trigrams=("坎", "坤"),
            element=WuXing.SHUI,
            yin_yang=YinYang.YIN,
            nature="亲比",
            gua_ci="比：吉。原筮元永贞，无咎。不宁方来，后夫凶。",
            tuan_ci="比，吉也，比，辅也，下顺从也。原筮元永贞，无咎，以刚中也。不宁方来，上下应也。后夫凶，其道穷也。",
            xiang_ci="地上有水，比；先王以建万国，亲诸侯。",
            meaning="比卦象征亲近团结，如水在地上，滋润大地。代表和谐相处的智慧。",
            life_wisdom="人际关系的和谐需要主动亲近，以诚待人。要建立互信互助的关系网络。",
            strategic_advice="适合建立联盟，加强合作。要主动示好，但要选择合适的伙伴。",
            special_ability="增强合作效果，提升人际关系处理能力",
            synergy_guas=["地水师", "风地观"],
            counter_guas=["火雷噬嗑"]
        )
        
        # 继续添加更多卦象...
        # 这里只展示前8卦作为示例，实际应包含全部64卦
        
        return guas
    
    def _initialize_yaos_philosophy(self) -> Dict[str, List[YaoPhilosophy]]:
        """初始化爻辞哲学内涵"""
        yaos = {}
        
        # 乾卦六爻
        yaos["乾为天"] = [
            YaoPhilosophy(
                position=1,
                yao_name="初九",
                yao_ci="潜龙勿用。",
                xiang_ci="潜龙勿用，阳在下也。",
                meaning="如潜伏的龙，时机未到，不宜行动。",
                life_situation="人生初期或事业起步阶段，实力尚未充分展现。",
                action_guidance="要韬光养晦，积蓄实力，等待时机。不要急于表现自己。",
                game_effect={"qi": 1, "patience": 1},
                trigger_condition="在地部时"
            ),
            YaoPhilosophy(
                position=2,
                yao_name="九二",
                yao_ci="见龙在田，利见大人。",
                xiang_ci="见龙在田，德施普也。",
                meaning="龙出现在田野，适合拜见贤人。",
                life_situation="才能开始显现，得到他人认可的阶段。",
                action_guidance="要主动学习，寻求指导，建立良好的人际关系。",
                game_effect={"dao_xing": 1, "social": 1},
                trigger_condition="在人部时"
            ),
            YaoPhilosophy(
                position=3,
                yao_name="九三",
                yao_ci="君子终日乾乾，夕惕若，厉无咎。",
                xiang_ci="终日乾乾，反复道也。",
                meaning="君子整日勤奋不懈，晚上也保持警惕。",
                life_situation="处于关键转折点，需要格外谨慎的时期。",
                action_guidance="要勤奋努力，时刻保持警觉，反省自己的行为。",
                game_effect={"qi": 2, "vigilance": 1},
                trigger_condition="每回合结束时"
            ),
            YaoPhilosophy(
                position=4,
                yao_name="九四",
                yao_ci="或跃在渊，无咎。",
                xiang_ci="或跃在渊，进无咎也。",
                meaning="可以跃起，也可以停在深渊，都没有过错。",
                life_situation="面临重大选择，进退都有可能的时期。",
                action_guidance="要审时度势，根据情况灵活选择进退。",
                game_effect={"flexibility": 2, "choice": 1},
                trigger_condition="在人部时可选择移动"
            ),
            YaoPhilosophy(
                position=5,
                yao_name="九五",
                yao_ci="飞龙在天，利见大人。",
                xiang_ci="飞龙在天，大人造也。",
                meaning="龙飞在天空，适合成为或拜见大人物。",
                life_situation="事业达到巅峰，具有领导地位的时期。",
                action_guidance="要发挥领导作用，造福他人，但要保持谦逊。",
                game_effect={"dao_xing": 2, "leadership": 2},
                trigger_condition="在天部时"
            ),
            YaoPhilosophy(
                position=6,
                yao_name="上九",
                yao_ci="亢龙有悔。",
                xiang_ci="亢龙有悔，盈不可久也。",
                meaning="过于高亢的龙会有悔恨。",
                life_situation="达到极盛状态，需要考虑退让的时期。",
                action_guidance="要知进退，适可而止，避免过度膨胀。",
                game_effect={"wisdom": 2, "moderation": 1},
                trigger_condition="道行达到上限时"
            )
        ]
        
        # 坤卦六爻
        yaos["坤为地"] = [
            YaoPhilosophy(
                position=1,
                yao_name="初六",
                yao_ci="履霜，坚冰至。",
                xiang_ci="履霜坚冰，阴始凝也。驯致其道，至坚冰也。",
                meaning="踩到霜，预示坚冰将至。",
                life_situation="事物发展的初期征象，需要警觉的时期。",
                action_guidance="要善于观察细微变化，防微杜渐。",
                game_effect={"observation": 1, "preparation": 1},
                trigger_condition="回合开始时"
            ),
            YaoPhilosophy(
                position=2,
                yao_name="六二",
                yao_ci="直，方，大，不习无不利。",
                xiang_ci="六二之动，直以方也。不习无不利，地道光也。",
                meaning="正直、方正、宽大，不用学习就无所不利。",
                life_situation="品德纯正，自然而然就能成功的状态。",
                action_guidance="要保持本性，以德服人，自然会有好结果。",
                game_effect={"virtue": 2, "natural_success": 1},
                trigger_condition="品德行为时"
            )
            # 其他爻辞...
        ]
        
        return yaos
    
    def _initialize_gua_relationships(self) -> Dict[str, Dict[str, List[str]]]:
        """初始化卦象关系"""
        relationships = {}
        
        # 相综关系（颠倒卦）
        comprehensive_pairs = [
            ("乾为天", "坤为地"),
            ("水雷屯", "山水蒙"),
            ("水天需", "天水讼"),
            ("地水师", "水地比")
        ]
        
        # 相错关系（阴阳互换）
        error_pairs = [
            ("乾为天", "坤为地"),
            ("震为雷", "巽为风"),
            ("坎为水", "离为火"),
            ("艮为山", "兑为泽")
        ]
        
        # 互卦关系
        mutual_relationships = {
            "乾为天": "乾为天",
            "坤为地": "坤为地",
            "水雷屯": "水火既济",
            "山水蒙": "火水未济"
        }
        
        for gua_name in self.guas_philosophy.keys():
            relationships[gua_name] = {
                "comprehensive": [],
                "error": [],
                "mutual": [],
                "sequence": [],  # 序卦关系
                "palace": []     # 同宫关系
            }
        
        return relationships
    
    def get_gua_philosophy(self, gua_name: str) -> Optional[GuaPhilosophy]:
        """获取卦象哲学内涵"""
        return self.guas_philosophy.get(gua_name)
    
    def get_yao_philosophy(self, gua_name: str, yao_position: int) -> Optional[YaoPhilosophy]:
        """获取爻辞哲学内涵"""
        yaos = self.yaos_philosophy.get(gua_name, [])
        if 1 <= yao_position <= len(yaos):
            return yaos[yao_position - 1]
        return None
    
    def get_life_wisdom(self, gua_name: str) -> str:
        """获取人生智慧"""
        gua = self.get_gua_philosophy(gua_name)
        return gua.life_wisdom if gua else "变化是永恒的真理。"
    
    def get_strategic_advice(self, gua_name: str) -> str:
        """获取策略建议"""
        gua = self.get_gua_philosophy(gua_name)
        return gua.strategic_advice if gua else "顺应变化，把握时机。"
    
    def get_synergy_guas(self, gua_name: str) -> List[str]:
        """获取协同卦象"""
        gua = self.get_gua_philosophy(gua_name)
        return gua.synergy_guas if gua else []
    
    def calculate_gua_compatibility(self, gua1: str, gua2: str) -> float:
        """计算卦象兼容性"""
        gua1_info = self.get_gua_philosophy(gua1)
        gua2_info = self.get_gua_philosophy(gua2)
        
        if not gua1_info or not gua2_info:
            return 0.5
        
        compatibility = 0.5
        
        # 五行相生相克
        if self._wuxing_generates(gua1_info.element, gua2_info.element):
            compatibility += 0.3
        elif self._wuxing_restrains(gua1_info.element, gua2_info.element):
            compatibility -= 0.2
        
        # 阴阳平衡
        if gua1_info.yin_yang != gua2_info.yin_yang:
            compatibility += 0.2
        
        # 协同关系
        if gua2 in gua1_info.synergy_guas:
            compatibility += 0.4
        
        # 相克关系
        if gua2 in gua1_info.counter_guas:
            compatibility -= 0.3
        
        return max(0.0, min(1.0, compatibility))
    
    def _wuxing_generates(self, element1: WuXing, element2: WuXing) -> bool:
        """检查五行相生关系"""
        generation_cycle = {
            WuXing.MU: WuXing.HUO,
            WuXing.HUO: WuXing.TU,
            WuXing.TU: WuXing.JIN,
            WuXing.JIN: WuXing.SHUI,
            WuXing.SHUI: WuXing.MU
        }
        return generation_cycle.get(element1) == element2
    
    def _wuxing_restrains(self, element1: WuXing, element2: WuXing) -> bool:
        """检查五行相克关系"""
        restraint_cycle = {
            WuXing.MU: WuXing.TU,
            WuXing.TU: WuXing.SHUI,
            WuXing.SHUI: WuXing.HUO,
            WuXing.HUO: WuXing.JIN,
            WuXing.JIN: WuXing.MU
        }
        return restraint_cycle.get(element1) == element2

# 全局64卦系统实例
complete_guas_system = Complete64GuasSystem()