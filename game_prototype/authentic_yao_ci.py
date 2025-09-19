#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真实易经爻辞数据
基于《周易》原文，为每一卦的每一爻提供真实的爻辞内容和现代解读
"""

from dataclasses import dataclass
from typing import Dict, List
from card_base import YaoCiTask

@dataclass
class AuthenticYaoCi:
    """真实爻辞数据结构"""
    position: str  # 初九、六二等
    original_text: str  # 原文爻辞
    interpretation: str  # 现代解读
    game_effect: str  # 游戏效果描述
    condition: str  # 触发条件
    reward_dao_xing: int
    reward_cheng_yi: int
    special_effect: str  # 特殊效果

# 乾卦 - 天行健，君子以自强不息
QIAN_YAO_CI = [
    AuthenticYaoCi(
        position="初九",
        original_text="潜龙勿用",
        interpretation="龙潜在深渊，暂时不要行动。时机未到，需要韬光养晦，积蓄力量。",
        game_effect="本回合不获得道行，但在回合结束时获得大量气和诚意",
        condition="主动选择不进行任何获得道行的行动",
        reward_dao_xing=0,
        reward_cheng_yi=3,
        special_effect="获得2点阴气和2点阳气，下回合行动效果+1"
    ),
    AuthenticYaoCi(
        position="九二",
        original_text="见龙在田，利见大人",
        interpretation="龙出现在田野，有利于见到德高望重的人。开始展现才能，寻求贵人相助。",
        game_effect="若场上有其他玩家道行比你高，获得额外奖励",
        condition="存在道行比自己高的玩家",
        reward_dao_xing=1,
        reward_cheng_yi=1,
        special_effect="可以查看道行最高玩家的一张手牌"
    ),
    AuthenticYaoCi(
        position="九三",
        original_text="君子终日乾乾，夕惕若厉，无咎",
        interpretation="君子整天勤奋努力，晚上也保持警惕，虽然危险但无过失。",
        game_effect="每回合结束时，若本回合进行了3次或以上行动，获得奖励",
        condition="本回合执行了3个或以上的行动",
        reward_dao_xing=2,
        reward_cheng_yi=0,
        special_effect="下回合可以额外执行一次行动"
    ),
    AuthenticYaoCi(
        position="九四",
        original_text="或跃在渊，无咎",
        interpretation="或许跳跃到深渊上空，没有过失。进退两难时的谨慎选择。",
        game_effect="可以选择冒险行动或保守行动，结果不同",
        condition="面临重要决策时",
        reward_dao_xing=1,
        reward_cheng_yi=1,
        special_effect="选择冒险：50%概率获得双倍奖励或失去1点道行；选择保守：稳定获得奖励"
    ),
    AuthenticYaoCi(
        position="九五",
        original_text="飞龙在天，利见大人",
        interpretation="飞龙在天空，有利于见到德高望重的人。达到巅峰，发挥最大影响力。",
        game_effect="若你的道行全场最高，激活强大效果",
        condition="道行为全场最高",
        reward_dao_xing=3,
        reward_cheng_yi=1,
        special_effect="所有其他玩家必须向你支付1点诚意，你获得领袖地位"
    ),
    AuthenticYaoCi(
        position="上九",
        original_text="亢龙有悔",
        interpretation="高傲的龙会有悔恨。过于刚强会导致失败，盛极而衰。",
        game_effect="若你的道行超过70点，必须支付代价但获得深刻领悟",
        condition="道行超过70点",
        reward_dao_xing=-2,
        reward_cheng_yi=5,
        special_effect="获得'智者'称号，之后的占卜结果准确率+50%"
    )
]

# 坤卦 - 地势坤，君子以厚德载物
KUN_YAO_CI = [
    AuthenticYaoCi(
        position="初六",
        original_text="履霜，坚冰至",
        interpretation="踩到霜，坚冰就要到了。微小的征兆预示着重大变化。",
        game_effect="预警机制：可以预知下一轮的危险",
        condition="回合开始时触发",
        reward_dao_xing=0,
        reward_cheng_yi=2,
        special_effect="下回合开始时，可以查看所有玩家将要执行的第一个行动"
    ),
    AuthenticYaoCi(
        position="六二",
        original_text="直方大，不习无不利",
        interpretation="正直、方正、宽大，不用学习就没有不利的。天性纯良，自然而然。",
        game_effect="被动效果：所有基础行动效果+1",
        condition="无特殊条件",
        reward_dao_xing=1,
        reward_cheng_yi=1,
        special_effect="本回合所有获得资源的行动额外+1"
    ),
    AuthenticYaoCi(
        position="六三",
        original_text="含章可贞，或从王事，无成有终",
        interpretation="含蓄美德可以坚持，或许从事王室事务，不求成功但有好结果。",
        game_effect="支持他人：为其他玩家的行动提供加成",
        condition="选择协助其他玩家",
        reward_dao_xing=0,
        reward_cheng_yi=2,
        special_effect="选择一名玩家，其下次行动效果翻倍，你获得其一半收益"
    ),
    AuthenticYaoCi(
        position="六四",
        original_text="括囊，无咎无誉",
        interpretation="扎紧口袋，没有过失也没有赞誉。保持低调，避免是非。",
        game_effect="防御姿态：免疫负面效果",
        condition="选择防御模式",
        reward_dao_xing=0,
        reward_cheng_yi=1,
        special_effect="本回合免疫所有负面效果和攻击，但不能主动行动"
    ),
    AuthenticYaoCi(
        position="六五",
        original_text="黄裳，元吉",
        interpretation="黄色的衣裳，大吉。居中守正，德行完美。",
        game_effect="完美平衡：阴阳调和获得最大收益",
        condition="阴阳平衡度达到90%以上",
        reward_dao_xing=2,
        reward_cheng_yi=2,
        special_effect="激活'中庸之道'，本回合所有行动都获得最佳结果"
    ),
    AuthenticYaoCi(
        position="上六",
        original_text="龙战于野，其血玄黄",
        interpretation="龙在野外战斗，血流成河。阴极而阳生，激烈的转化。",
        game_effect="极限转化：阴阳属性发生剧烈变化",
        condition="阴阳严重失衡时",
        reward_dao_xing=1,
        reward_cheng_yi=0,
        special_effect="强制触发太极转化，阴阳属性互换，获得'涅槃重生'状态"
    )
]

# 震卦 - 洊雷，震；君子以恐惧修省
ZHEN_YAO_CI = [
    AuthenticYaoCi(
        position="初九",
        original_text="震来虩虩，后笑言哑哑，吉",
        interpretation="雷声来时恐惧战栗，过后谈笑风生，吉利。",
        game_effect="先苦后甜：承受损失后获得更大收益",
        condition="主动承受1点道行损失",
        reward_dao_xing=3,
        reward_cheng_yi=1,
        special_effect="获得'雷霆万钧'状态，下次行动威力翻倍"
    ),
    AuthenticYaoCi(
        position="六二",
        original_text="震来厉，亿丧贝，跻于九陵，勿逐，七日得",
        interpretation="雷声带来危险，失去财物，逃到高山，不要追赶，七天后会得到。",
        game_effect="暂时损失，延迟获得：失去资源但几回合后获得更多",
        condition="愿意延迟满足",
        reward_dao_xing=-1,
        reward_cheng_yi=0,
        special_effect="3回合后获得5点道行和3点诚意"
    ),
    AuthenticYaoCi(
        position="六三",
        original_text="震苏苏，震行无眚",
        interpretation="雷声使人清醒，在震动中行动没有灾祸。",
        game_effect="觉醒状态：在混乱中保持清醒",
        condition="场上存在负面状态时",
        reward_dao_xing=2,
        reward_cheng_yi=1,
        special_effect="免疫所有混乱和负面状态，行动精准度+100%"
    ),
    AuthenticYaoCi(
        position="九四",
        original_text="震遂泥",
        interpretation="雷声后陷入泥泞。行动受阻，进退两难。",
        game_effect="行动受限：本回合行动次数减半但威力增强",
        condition="无特殊条件",
        reward_dao_xing=1,
        reward_cheng_yi=2,
        special_effect="本回合只能执行一次行动，但效果翻倍"
    ),
    AuthenticYaoCi(
        position="六五",
        original_text="震往来厉，亿无丧，有事",
        interpretation="雷声往来危险，但不会有损失，有事情要做。",
        game_effect="危机管理：在危险中寻找机会",
        condition="面临危险或挑战时",
        reward_dao_xing=2,
        reward_cheng_yi=0,
        special_effect="将一个负面事件转化为正面机会"
    ),
    AuthenticYaoCi(
        position="上六",
        original_text="震索索，视矍矍，征凶。震不于其躬，于其邻，无咎，婚媾有言",
        interpretation="雷声使人战栗，目光惊恐，出征凶险。雷不在自己身上而在邻居身上，无咎，婚姻有话说。",
        game_effect="转移风险：将自己的负面效果转移给他人",
        condition="存在负面状态时",
        reward_dao_xing=0,
        reward_cheng_yi=1,
        special_effect="选择一名其他玩家，将自己的一个负面状态转移给他"
    )
]

# 巽卦 - 随风，巽；君子以申命行事
XUN_YAO_CI = [
    AuthenticYaoCi(
        position="初六",
        original_text="进退，利武人之贞",
        interpretation="进退不定，有利于武人的坚持。",
        game_effect="灵活应变：可以改变已做出的决定",
        condition="本回合已执行过行动",
        reward_dao_xing=1,
        reward_cheng_yi=0,
        special_effect="可以撤销本回合的最后一个行动并重新选择"
    ),
    AuthenticYaoCi(
        position="九二",
        original_text="巽在床下，用史巫纷若，吉，无咎",
        interpretation="风在床下，用史官巫师众多，吉利，无咎。",
        game_effect="寻求指导：获得多种选择方案",
        condition="面临重要决策时",
        reward_dao_xing=0,
        reward_cheng_yi=2,
        special_effect="获得3个不同的行动选项，可以选择其中最优的执行"
    ),
    AuthenticYaoCi(
        position="九三",
        original_text="频巽，吝",
        interpretation="频繁地顺从，有些羞耻。过度迎合失去自我。",
        game_effect="过度适应：获得短期利益但损失长期发展",
        condition="连续3回合都选择了保守行动",
        reward_dao_xing=0,
        reward_cheng_yi=3,
        special_effect="立即获得资源，但下回合行动效果-50%"
    ),
    AuthenticYaoCi(
        position="六四",
        original_text="悔亡，田获三品",
        interpretation="悔恨消失，田猎获得三种猎物。",
        game_effect="多重收获：一次行动获得多种奖励",
        condition="成功完成一个复杂任务",
        reward_dao_xing=1,
        reward_cheng_yi=1,
        special_effect="额外获得1点阴气、1点阳气和1张卡牌"
    ),
    AuthenticYaoCi(
        position="九五",
        original_text="贞吉，悔亡，无不利。无初有终，先庚三日，后庚三日，吉",
        interpretation="坚持吉利，悔恨消失，没有不利。没有开始但有结果，变革前三天后三天，吉利。",
        game_effect="完美时机：选择最佳时机行动获得最大收益",
        condition="等待最佳时机",
        reward_dao_xing=3,
        reward_cheng_yi=2,
        special_effect="可以延迟1-3回合执行行动，延迟越久效果越强"
    ),
    AuthenticYaoCi(
        position="上九",
        original_text="巽在床下，丧其资斧，贞凶",
        interpretation="风在床下，失去资财工具，坚持凶险。过度顺从导致损失。",
        game_effect="失去自我：过度迎合他人导致损失",
        condition="本回合所有行动都是为了帮助他人",
        reward_dao_xing=-1,
        reward_cheng_yi=0,
        special_effect="失去1点道行，但获得'觉悟'状态，之后不再受他人影响"
    )
]

# 坎卦 - 习坎，有孚，维心亨，行有尚
KAN_YAO_CI = [
    AuthenticYaoCi(
        position="初六",
        original_text="习坎，入于坎窞，凶",
        interpretation="重重险阻，陷入坎坑，凶险。",
        game_effect="陷入困境：暂时无法行动但获得经验",
        condition="遭遇失败或挫折时",
        reward_dao_xing=0,
        reward_cheng_yi=2,
        special_effect="跳过下回合，但之后的行动成功率+30%"
    ),
    AuthenticYaoCi(
        position="九二",
        original_text="坎有险，求小得",
        interpretation="坎中有险，寻求小的收获。",
        game_effect="谨慎求进：小步前进积累优势",
        condition="选择保守策略",
        reward_dao_xing=1,
        reward_cheng_yi=1,
        special_effect="每回合稳定获得少量资源，连续5回合后获得大奖励"
    ),
    AuthenticYaoCi(
        position="六三",
        original_text="来之坎坎，险且枕，入于坎窞，勿用",
        interpretation="来到重重险阻，危险而且要休息，陷入坎坑，不要行动。",
        game_effect="等待时机：暂停行动等待更好机会",
        condition="主动选择等待",
        reward_dao_xing=0,
        reward_cheng_yi=1,
        special_effect="下回合可以执行双倍行动，且成功率大幅提升"
    ),
    AuthenticYaoCi(
        position="六四",
        original_text="樽酒簋贰，用缶，纳约自牖，终无咎",
        interpretation="一樽酒两簋饭，用瓦器，从窗户递进约定，最终无咎。",
        game_effect="简朴诚信：用最简单的方式达成目标",
        condition="选择最简单直接的方案",
        reward_dao_xing=1,
        reward_cheng_yi=2,
        special_effect="忽略所有复杂条件，直接获得基础奖励"
    ),
    AuthenticYaoCi(
        position="九五",
        original_text="坎不盈，祗既平，无咎",
        interpretation="坎坑不满，只要平整就无咎。适度即可，不求过满。",
        game_effect="适度原则：保持平衡避免极端",
        condition="各项资源都保持中等水平",
        reward_dao_xing=2,
        reward_cheng_yi=1,
        special_effect="所有资源自动调整到平衡状态，获得'中庸'加成"
    ),
    AuthenticYaoCi(
        position="上六",
        original_text="系用徽纆，寘于丛棘，三岁不得，凶",
        interpretation="用绳索捆绑，放在荆棘丛中，三年得不到，凶险。",
        game_effect="长期困顿：承受长期损失但最终获得解脱",
        condition="连续多回合处于不利状态",
        reward_dao_xing=-1,
        reward_cheng_yi=0,
        special_effect="3回合后自动解除所有负面状态，获得'重获自由'大奖励"
    )
]

# 离卦 - 明两作，离；大人以继明照于四方
LI_YAO_CI = [
    AuthenticYaoCi(
        position="初九",
        original_text="履错然，敬之无咎",
        interpretation="脚步错乱，恭敬对待就无咎。开始时的混乱需要谨慎。",
        game_effect="谨慎开始：初期行动需要额外小心",
        condition="回合开始时",
        reward_dao_xing=0,
        reward_cheng_yi=1,
        special_effect="本回合第一个行动失败不会有负面后果"
    ),
    AuthenticYaoCi(
        position="六二",
        original_text="黄离，元吉",
        interpretation="黄色的光明，大吉。中正光明，德行完美。",
        game_effect="光明正大：正直行为获得额外奖励",
        condition="选择最正直的行动方案",
        reward_dao_xing=2,
        reward_cheng_yi=2,
        special_effect="获得'光明'状态，所有行动都被视为最优选择"
    ),
    AuthenticYaoCi(
        position="九三",
        original_text="日昃之离，不鼓缶而歌，则大耋之嗟，凶",
        interpretation="夕阳西下的光明，不敲瓦盆唱歌，就会有老年的叹息，凶险。",
        game_effect="及时行乐：把握当下机会否则后悔",
        condition="面临时间限制的机会",
        reward_dao_xing=1,
        reward_cheng_yi=0,
        special_effect="必须立即做出选择：获得奖励或失去机会"
    ),
    AuthenticYaoCi(
        position="九四",
        original_text="突如其来如，焚如，死如，弃如",
        interpretation="突然而来，燃烧，死亡，抛弃。光明过盛导致毁灭。",
        game_effect="过度光明：力量过强导致反噬",
        condition="道行或资源过多时",
        reward_dao_xing=-2,
        reward_cheng_yi=1,
        special_effect="失去部分资源，但获得'涅槃'状态，重生后更强"
    ),
    AuthenticYaoCi(
        position="六五",
        original_text="出涕沱若，戚嗟若，吉",
        interpretation="眼泪如雨下，忧戚叹息，吉利。真情流露获得认同。",
        game_effect="真情感动：真诚的情感表达获得他人支持",
        condition="主动表达真实情感",
        reward_dao_xing=1,
        reward_cheng_yi=3,
        special_effect="获得所有其他玩家的1点诚意支持"
    ),
    AuthenticYaoCi(
        position="上九",
        original_text="王用出征，有嘉折首，获匪其丑，无咎",
        interpretation="王用来出征，有好的斩获首级，俘获的不是其同类，无咎。",
        game_effect="正义之战：对抗邪恶获得胜利",
        condition="对抗负面状态或恶意行为",
        reward_dao_xing=3,
        reward_cheng_yi=1,
        special_effect="清除场上所有负面状态，获得'正义'称号"
    )
]

# 艮卦 - 兼山，艮；君子以思不出其位
GEN_YAO_CI = [
    AuthenticYaoCi(
        position="初六",
        original_text="艮其趾，无咎，利永贞",
        interpretation="止住脚趾，无咎，有利于长久坚持。",
        game_effect="及时止步：避免过度行动",
        condition="主动选择停止当前行动",
        reward_dao_xing=0,
        reward_cheng_yi=2,
        special_effect="避免一次可能的负面后果，获得'智慧'点数"
    ),
    AuthenticYaoCi(
        position="六二",
        original_text="艮其腓，不拯其随，其心不快",
        interpretation="止住小腿，不能拯救跟随者，心中不快。",
        game_effect="力不从心：想帮助他人但能力有限",
        condition="尝试帮助他人但失败",
        reward_dao_xing=0,
        reward_cheng_yi=1,
        special_effect="获得'同情心'，下次帮助他人的行动必定成功"
    ),
    AuthenticYaoCi(
        position="九三",
        original_text="艮其限，列其夤，厉薰心",
        interpretation="止住腰部，分裂脊梁，危险熏心。",
        game_effect="强行停止：违背本性的停止带来痛苦",
        condition="被迫停止重要行动",
        reward_dao_xing=-1,
        reward_cheng_yi=0,
        special_effect="承受痛苦但获得'坚韧'，之后的挫折抗性+50%"
    ),
    AuthenticYaoCi(
        position="六四",
        original_text="艮其身，无咎",
        interpretation="止住身体，无咎。恰到好处的停止。",
        game_effect="完美控制：精确控制自己的行动",
        condition="在最佳时机停止行动",
        reward_dao_xing=1,
        reward_cheng_yi=1,
        special_effect="获得'自控力'，可以精确控制所有行动的强度"
    ),
    AuthenticYaoCi(
        position="六五",
        original_text="艮其辅，言有序，悔亡",
        interpretation="止住面颊，说话有条理，悔恨消失。",
        game_effect="谨言慎行：控制言语获得好结果",
        condition="选择谨慎的沟通方式",
        reward_dao_xing=1,
        reward_cheng_yi=2,
        special_effect="获得'口才'，可以影响其他玩家的决策"
    ),
    AuthenticYaoCi(
        position="上九",
        original_text="敦艮，吉",
        interpretation="厚重的停止，吉利。彻底的静止带来安宁。",
        game_effect="大彻大悟：完全的静止带来智慧",
        condition="连续2回合不执行任何行动",
        reward_dao_xing=3,
        reward_cheng_yi=3,
        special_effect="获得'大智慧'状态，之后所有决策都是最优的"
    )
]

# 兑卦 - 丽泽，兑；君子以朋友讲习
DUI_YAO_CI = [
    AuthenticYaoCi(
        position="初九",
        original_text="和兑，吉",
        interpretation="和谐喜悦，吉利。内心平和带来好运。",
        game_effect="和谐共处：与他人和谐相处获得奖励",
        condition="本回合没有与任何玩家发生冲突",
        reward_dao_xing=1,
        reward_cheng_yi=1,
        special_effect="所有玩家都获得1点诚意，你额外获得1点道行"
    ),
    AuthenticYaoCi(
        position="九二",
        original_text="孚兑，吉，悔亡",
        interpretation="诚信喜悦，吉利，悔恨消失。真诚带来快乐。",
        game_effect="真诚交流：诚实的交流获得信任",
        condition="主动分享真实信息",
        reward_dao_xing=1,
        reward_cheng_yi=2,
        special_effect="与所有玩家建立'信任'关系，合作行动效果+50%"
    ),
    AuthenticYaoCi(
        position="六三",
        original_text="来兑，凶",
        interpretation="前来寻求喜悦，凶险。过度追求快乐有害。",
        game_effect="过度享乐：追求短期快乐损害长期利益",
        condition="连续选择获得即时奖励的行动",
        reward_dao_xing=0,
        reward_cheng_yi=2,
        special_effect="立即获得奖励，但下回合行动受限"
    ),
    AuthenticYaoCi(
        position="九四",
        original_text="商兑，未宁，介疾有喜",
        interpretation="商量喜悦，还不安宁，但疾病中有喜事。",
        game_effect="苦中作乐：在困难中寻找快乐",
        condition="处于不利状态时",
        reward_dao_xing=1,
        reward_cheng_yi=1,
        special_effect="将一个负面状态转化为正面效果"
    ),
    AuthenticYaoCi(
        position="九五",
        original_text="孚于剥，有厉",
        interpretation="诚信于剥落，有危险。过分信任有风险。",
        game_effect="盲目信任：过度信任他人可能受害",
        condition="完全信任其他玩家的建议",
        reward_dao_xing=0,
        reward_cheng_yi=1,
        special_effect="50%概率获得大奖励，50%概率被欺骗失去资源"
    ),
    AuthenticYaoCi(
        position="上六",
        original_text="引兑",
        interpretation="引导喜悦。成为快乐的源泉。",
        game_effect="传播快乐：为他人带来快乐自己也受益",
        condition="帮助其他玩家获得奖励",
        reward_dao_xing=2,
        reward_cheng_yi=1,
        special_effect="每当其他玩家获得奖励时，你也获得一半的奖励"
    )
]

# 汇总所有卦的爻辞数据
AUTHENTIC_YAO_CI_DATA = {
    "乾为天": QIAN_YAO_CI,
    "坤为地": KUN_YAO_CI,
    "震为雷": ZHEN_YAO_CI,
    "巽为风": XUN_YAO_CI,
    "坎为水": KAN_YAO_CI,
    "离为火": LI_YAO_CI,
    "艮为山": GEN_YAO_CI,
    "兑为泽": DUI_YAO_CI,
}

def get_authentic_yao_ci_tasks(gua_name: str) -> List[YaoCiTask]:
    """根据卦名获取真实爻辞任务"""
    if gua_name not in AUTHENTIC_YAO_CI_DATA:
        # 如果没有具体的爻辞数据，返回空列表或默认任务
        return []
    
    yao_ci_list = AUTHENTIC_YAO_CI_DATA[gua_name]
    tasks = []
    
    for yao_ci in yao_ci_list:
        task = YaoCiTask(
            level=yao_ci.position,
            name=f"{yao_ci.position}：{yao_ci.original_text}",
            description=f"{yao_ci.interpretation}\n游戏效果：{yao_ci.game_effect}",
            reward_dao_xing=yao_ci.reward_dao_xing,
            reward_cheng_yi=yao_ci.reward_cheng_yi
        )
        tasks.append(task)
    
    return tasks