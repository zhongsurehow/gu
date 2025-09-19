from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum
import random

class StrategyCategory(Enum):
    SHENG_ZHAN = "胜战计"  # 第1-6计：优势时使用
    DI_ZHAN = "敌战计"    # 第7-12计：对敌时使用
    GONG_ZHAN = "攻战计"  # 第13-18计：攻击时使用
    HUN_ZHAN = "混战计"   # 第19-24计：混乱时使用
    BING_ZHAN = "并战计"  # 第25-30计：合并时使用
    BAI_ZHAN = "败战计"   # 第31-36计：劣势时使用

class StrategyType(Enum):
    # 胜战计
    MAN_TIAN_GUO_HAI = 1    # 瞒天过海
    WEI_WEI_JIU_ZHAO = 2    # 围魏救赵
    JIE_DAO_SHA_REN = 3     # 借刀杀人
    YI_YI_DAI_LAO = 4       # 以逸待劳
    CHEN_HUO_DA_JIE = 5     # 趁火打劫
    SHENG_DONG_JI_XI = 6    # 声东击西
    
    # 敌战计
    WU_ZHONG_SHENG_YOU = 7  # 无中生有
    AN_DU_CHEN_CANG = 8     # 暗度陈仓
    GE_AN_GUAN_HUO = 9      # 隔岸观火
    XIAO_LI_CANG_DAO = 10   # 笑里藏刀
    LI_DAI_TAO_JIANG = 11   # 李代桃僵
    SHUN_SHOU_QIAN_YANG = 12 # 顺手牵羊
    
    # 攻战计
    DA_CAO_JING_SHE = 13    # 打草惊蛇
    JIE_SHI_HUAN_HUN = 14   # 借尸还魂
    DIAO_HU_LI_SHAN = 15    # 调虎离山
    YU_QIN_GU_ZONG = 16     # 欲擒故纵
    PAO_ZHUAN_YIN_YU = 17   # 抛砖引玉
    QIN_ZEI_QIN_WANG = 18   # 擒贼擒王
    
    # 混战计
    FU_DI_CHOU_XIN = 19     # 釜底抽薪
    HUN_SHUI_MO_YU = 20     # 浑水摸鱼
    JIN_CHAN_TUO_QIAO = 21  # 金蝉脱壳
    GUAN_MEN_ZHU_ZEI = 22   # 关门捉贼
    YUAN_JIAO_JIN_GONG = 23 # 远交近攻
    JIA_TU_FA_GUO = 24      # 假途伐虢
    
    # 并战计
    TOU_LIANG_HUAN_ZHU = 25 # 偷梁换柱
    ZHI_SANG_MA_HUAI = 26   # 指桑骂槐
    JIA_CHI_BU_DIAN = 27    # 假痴不癫
    SHANG_WU_CHOU_TI = 28   # 上屋抽梯
    SHU_SHANG_KAI_HUA = 29  # 树上开花
    FAN_KE_WEI_ZHU = 30     # 反客为主
    
    # 败战计
    MEI_REN_JI = 31         # 美人计
    KONG_CHENG_JI = 32      # 空城计
    FAN_JIAN_JI = 33        # 反间计
    KU_ROU_JI = 34          # 苦肉计
    LIAN_HUAN_JI = 35       # 连环计
    ZOU_WEI_SHANG = 36      # 走为上

@dataclass
class ThirtySixStrategy:
    strategy_type: StrategyType
    name: str
    category: StrategyCategory
    description: str
    conditions: List[str]
    effects: List[str]
    cost: Dict[str, int]
    cooldown: int
    success_rate: float
    yijing_basis: str = ""
    hidden: bool = False

@dataclass
class StrategyState:
    available_strategies: List[StrategyType]
    cooldowns: Dict[StrategyType, int]
    used_strategies: List[StrategyType]
    strategy_memory: Dict[StrategyType, Dict[str, Any]]

class ThirtySixStrategiesSystem:
    def __init__(self):
        self.strategies: Dict[StrategyType, ThirtySixStrategy] = {}
        self.player_states: Dict[str, StrategyState] = {}
        self._initialize_strategies()
    
    def _initialize_strategies(self):
        """初始化完整的三十六计"""
        strategies = [
            # 胜战计（第1-6计）
            ThirtySixStrategy(
                strategy_type=StrategyType.MAN_TIAN_GUO_HAI,
                name="瞒天过海",
                category=StrategyCategory.SHENG_ZHAN,
                description="备周则意怠，常见则不疑",
                conditions=["拥有隐藏信息能力", "对手信任度>30"],
                effects=["隐藏真实意图3回合", "下次行动成功率+30%"],
                cost={"修为": 20, "阴阳值": 10},
                cooldown=5,
                success_rate=0.7,
                yijing_basis="坤卦：地势坤，厚德载物，隐而不发"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.WEI_WEI_JIU_ZHAO,
                name="围魏救赵",
                category=StrategyCategory.SHENG_ZHAN,
                description="共敌不如分敌，敌阳不如敌阴",
                conditions=["存在多个对手", "拥有机动能力"],
                effects=["迫使对手改变目标", "获得战略主动权"],
                cost={"修为": 25, "五行能量": 15},
                cooldown=4,
                success_rate=0.65,
                yijing_basis="震卦：雷出地奋，动而有威"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.JIE_DAO_SHA_REN,
                name="借刀杀人",
                category=StrategyCategory.SHENG_ZHAN,
                description="敌已明，友未定，引友杀敌",
                conditions=["存在第三方势力", "能够影响第三方"],
                effects=["让第三方攻击目标", "自身不承担风险"],
                cost={"修为": 30, "声誉": 10},
                cooldown=6,
                success_rate=0.6,
                yijing_basis="巽卦：风行于地，顺势而为"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.YI_YI_DAI_LAO,
                name="以逸待劳",
                category=StrategyCategory.SHENG_ZHAN,
                description="困敌之势，不以战",
                conditions=["拥有防御优势", "对手处于攻势"],
                effects=["恢复资源", "对手消耗增加50%"],
                cost={"修为": 15},
                cooldown=3,
                success_rate=0.8,
                yijing_basis="艮卦：山止于上，静而待动"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.CHEN_HUO_DA_JIE,
                name="趁火打劫",
                category=StrategyCategory.SHENG_ZHAN,
                description="敌之害大，就势取利",
                conditions=["对手处于困境", "拥有攻击能力"],
                effects=["攻击效果翻倍", "获得额外资源"],
                cost={"修为": 20, "阴阳值": 15},
                cooldown=4,
                success_rate=0.75,
                yijing_basis="离卦：火附于木，势不可挡"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.SHENG_DONG_JI_XI,
                name="声东击西",
                category=StrategyCategory.SHENG_ZHAN,
                description="敌志乱萃，不虞",
                conditions=["拥有多个行动选项", "对手注意力分散"],
                effects=["真实目标成功率+40%", "对手防御-20%"],
                cost={"修为": 25, "五行能量": 10},
                cooldown=5,
                success_rate=0.7,
                yijing_basis="震卦：雷出地奋，声势并用"
            ),
            
            # 敌战计（第7-12计）
            ThirtySixStrategy(
                strategy_type=StrategyType.WU_ZHONG_SHENG_YOU,
                name="无中生有",
                category=StrategyCategory.DI_ZHAN,
                description="诳也，非诳也，实其所诳也",
                conditions=["拥有创造能力", "对手信息不足"],
                effects=["创造虚假威胁", "获得心理优势"],
                cost={"修为": 30, "阴阳值": 20},
                cooldown=6,
                success_rate=0.6,
                yijing_basis="乾卦：天行健，无中生有"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.AN_DU_CHEN_CANG,
                name="暗度陈仓",
                category=StrategyCategory.DI_ZHAN,
                description="示之以动，利其静而有主",
                conditions=["拥有隐蔽行动能力", "对手被表面行动吸引"],
                effects=["隐蔽行动成功率+50%", "获得战略突破"],
                cost={"修为": 35, "五行能量": 20},
                cooldown=7,
                success_rate=0.65,
                yijing_basis="坎卦：水流就下，暗中行事"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.GE_AN_GUAN_HUO,
                name="隔岸观火",
                category=StrategyCategory.DI_ZHAN,
                description="阳乖序乱，阴以待逆",
                conditions=["存在多方冲突", "自身保持中立"],
                effects=["避免损失", "等待最佳时机"],
                cost={"修为": 10},
                cooldown=2,
                success_rate=0.9,
                yijing_basis="离卦：火在山上，远观其变"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.XIAO_LI_CANG_DAO,
                name="笑里藏刀",
                category=StrategyCategory.DI_ZHAN,
                description="信而安之，阴以图之",
                conditions=["与目标建立信任", "拥有隐藏敌意"],
                effects=["背叛攻击伤害+100%", "目标防御-50%"],
                cost={"修为": 40, "声誉": 20},
                cooldown=8,
                success_rate=0.8,
                yijing_basis="兑卦：泽上于天，外柔内刚"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.LI_DAI_TAO_JIANG,
                name="李代桃僵",
                category=StrategyCategory.DI_ZHAN,
                description="势必有损，损阴以益阳",
                conditions=["拥有可牺牲资源", "需要保护核心利益"],
                effects=["保护重要资源", "转移对手注意力"],
                cost={"次要资源": 50},
                cooldown=4,
                success_rate=0.85,
                yijing_basis="损卦：山下有泽，损己利人"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.SHUN_SHOU_QIAN_YANG,
                name="顺手牵羊",
                category=StrategyCategory.DI_ZHAN,
                description="微隙在所必乘，微利在所必得",
                conditions=["发现小机会", "拥有快速行动能力"],
                effects=["获得小额资源", "不引起注意"],
                cost={"修为": 5},
                cooldown=1,
                success_rate=0.95,
                yijing_basis="巽卦：风行于地，顺势而取"
            ),
            
            # 攻战计（第13-18计）
            ThirtySixStrategy(
                strategy_type=StrategyType.DA_CAO_JING_SHE,
                name="打草惊蛇",
                category=StrategyCategory.GONG_ZHAN,
                description="疑以叩实，察而后动",
                conditions=["需要试探对手", "拥有侦察能力"],
                effects=["获得对手信息", "暴露对手隐藏计划"],
                cost={"修为": 15, "五行能量": 10},
                cooldown=3,
                success_rate=0.8,
                yijing_basis="震卦：雷出地奋，惊而后动"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.JIE_SHI_HUAN_HUN,
                name="借尸还魂",
                category=StrategyCategory.GONG_ZHAN,
                description="有用者，不可借；不能用者，求借",
                conditions=["存在废弃资源", "能够重新激活"],
                effects=["重新利用失效资源", "获得意外优势"],
                cost={"修为": 25, "阴阳值": 15},
                cooldown=5,
                success_rate=0.7,
                yijing_basis="坤卦：地势坤，厚德载物"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.DIAO_HU_LI_SHAN,
                name="调虎离山",
                category=StrategyCategory.GONG_ZHAN,
                description="待天以困之，用人以诱之",
                conditions=["对手有弱点", "能够制造诱饵"],
                effects=["使对手离开有利位置", "创造攻击机会"],
                cost={"修为": 30, "五行能量": 20},
                cooldown=6,
                success_rate=0.65,
                yijing_basis="艮卦：山上有山，调离其位"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.YU_QIN_GU_ZONG,
                name="欲擒故纵",
                category=StrategyCategory.GONG_ZHAN,
                description="逼则反兵，走则减势",
                conditions=["拥有控制能力", "对手有贪婪倾向"],
                effects=["诱导对手深入", "设置完美陷阱"],
                cost={"修为": 35, "阴阳值": 25},
                cooldown=7,
                success_rate=0.6,
                yijing_basis="巽卦：风行于地，顺而入之"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.PAO_ZHUAN_YIN_YU,
                name="抛砖引玉",
                category=StrategyCategory.GONG_ZHAN,
                description="类以诱之，击蒙也",
                conditions=["拥有诱饵", "对手有欲望"],
                effects=["获得更大利益", "以小博大"],
                cost={"小额资源": 20},
                cooldown=4,
                success_rate=0.75,
                yijing_basis="兑卦：泽上于天，以小博大"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.QIN_ZEI_QIN_WANG,
                name="擒贼擒王",
                category=StrategyCategory.GONG_ZHAN,
                description="摧其坚，夺其魁",
                conditions=["识别敌方核心", "拥有精准打击能力"],
                effects=["瓦解敌方组织", "获得决定性优势"],
                cost={"修为": 50, "五行能量": 30},
                cooldown=8,
                success_rate=0.55,
                yijing_basis="乾卦：天行健，直击要害"
            ),
            
            # 混战计（第19-24计）
            ThirtySixStrategy(
                strategy_type=StrategyType.FU_DI_CHOU_XIN,
                name="釜底抽薪",
                category=StrategyCategory.HUN_ZHAN,
                description="不敌其力，而消其势",
                conditions=["识别对手根基", "拥有破坏能力"],
                effects=["摧毁对手根基", "从根本上削弱敌人"],
                cost={"修为": 40, "五行能量": 25},
                cooldown=7,
                success_rate=0.6,
                yijing_basis="坎卦：水流就下，断其根源"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.HUN_SHUI_MO_YU,
                name="浑水摸鱼",
                category=StrategyCategory.HUN_ZHAN,
                description="乘其阴乱，利其弱而无主",
                conditions=["局势混乱", "拥有机动能力"],
                effects=["在混乱中获利", "避免直接冲突"],
                cost={"修为": 20, "阴阳值": 15},
                cooldown=4,
                success_rate=0.8,
                yijing_basis="坎卦：水洊至，习坎"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.JIN_CHAN_TUO_QIAO,
                name="金蝉脱壳",
                category=StrategyCategory.HUN_ZHAN,
                description="存其形，完其势；友不疑，敌不动",
                conditions=["需要脱身", "拥有替身或掩护"],
                effects=["安全撤退", "保存实力"],
                cost={"修为": 30, "阴阳值": 20},
                cooldown=6,
                success_rate=0.75,
                yijing_basis="巽卦：风行于地，变化莫测",
                hidden=True
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.GUAN_MEN_ZHU_ZEI,
                name="关门捉贼",
                category=StrategyCategory.HUN_ZHAN,
                description="小敌困之，剥，不利有攸往",
                conditions=["对手被包围", "拥有封锁能力"],
                effects=["困住敌人", "逐步消耗"],
                cost={"修为": 35, "五行能量": 25},
                cooldown=6,
                success_rate=0.7,
                yijing_basis="艮卦：山山相连，困而击之"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.YUAN_JIAO_JIN_GONG,
                name="远交近攻",
                category=StrategyCategory.HUN_ZHAN,
                description="形禁势格，利从近取",
                conditions=["存在远近不同势力", "拥有外交能力"],
                effects=["获得远方盟友", "孤立近敌"],
                cost={"修为": 25, "声誉": 15},
                cooldown=5,
                success_rate=0.65,
                yijing_basis="离卦：火附于木，远近有别"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.JIA_TU_FA_GUO,
                name="假途伐虢",
                category=StrategyCategory.HUN_ZHAN,
                description="两大之间，敌胁以从",
                conditions=["存在中间势力", "拥有借道能力"],
                effects=["借道攻击", "一石二鸟"],
                cost={"修为": 40, "五行能量": 20},
                cooldown=7,
                success_rate=0.6,
                yijing_basis="坤卦：地势坤，借道而行"
            ),
            
            # 并战计（第25-30计）
            ThirtySixStrategy(
                strategy_type=StrategyType.TOU_LIANG_HUAN_ZHU,
                name="偷梁换柱",
                category=StrategyCategory.BING_ZHAN,
                description="频更其阵，抽其劲，待其自败",
                conditions=["能够替换关键要素", "对手依赖某些支撑"],
                effects=["暗中改变局势", "对手失去支撑"],
                cost={"修为": 45, "阴阳值": 30},
                cooldown=8,
                success_rate=0.55,
                yijing_basis="巽卦：风行于地，暗中替换",
                hidden=True
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.ZHI_SANG_MA_HUAI,
                name="指桑骂槐",
                category=StrategyCategory.BING_ZHAN,
                description="大凌小者，警以诱之",
                conditions=["存在替代目标", "需要警告他人"],
                effects=["间接威慑", "避免直接冲突"],
                cost={"修为": 20, "声誉": 10},
                cooldown=3,
                success_rate=0.85,
                yijing_basis="震卦：雷出地奋，警示他人"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.JIA_CHI_BU_DIAN,
                name="假痴不癫",
                category=StrategyCategory.BING_ZHAN,
                description="宁伪作不知不为，不伪作假知妄为",
                conditions=["需要隐藏实力", "对手轻视自己"],
                effects=["降低对手警惕", "积蓄力量"],
                cost={"修为": 15, "声誉": 20},
                cooldown=4,
                success_rate=0.9,
                yijing_basis="坤卦：地势坤，厚德载物",
                hidden=True
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.SHANG_WU_CHOU_TI,
                name="上屋抽梯",
                category=StrategyCategory.BING_ZHAN,
                description="假之以便，唆之使前",
                conditions=["对手依赖退路", "能够切断后路"],
                effects=["断敌退路", "迫其决战"],
                cost={"修为": 35, "五行能量": 25},
                cooldown=6,
                success_rate=0.65,
                yijing_basis="艮卦：山上有山，断其退路"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.SHU_SHANG_KAI_HUA,
                name="树上开花",
                category=StrategyCategory.BING_ZHAN,
                description="借局布势，力小势大",
                conditions=["实力不足", "能够制造假象"],
                effects=["以弱示强", "获得心理优势"],
                cost={"修为": 25, "阴阳值": 20},
                cooldown=5,
                success_rate=0.7,
                yijing_basis="巽卦：风行于地，虚张声势"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.FAN_KE_WEI_ZHU,
                name="反客为主",
                category=StrategyCategory.BING_ZHAN,
                description="乘隙插足，扼其主机",
                conditions=["处于客方地位", "发现主方弱点"],
                effects=["夺取主导权", "逆转地位"],
                cost={"修为": 50, "五行能量": 35},
                cooldown=9,
                success_rate=0.5,
                yijing_basis="震卦：雷出地奋，反转局势"
            ),
            
            # 败战计（第31-36计）
            ThirtySixStrategy(
                strategy_type=StrategyType.MEI_REN_JI,
                name="美人计",
                category=StrategyCategory.BAI_ZHAN,
                description="兵强者，攻其将；将智者，伐其情",
                conditions=["对手有弱点", "拥有诱惑手段"],
                effects=["利用对手弱点", "获得内部信息"],
                cost={"修为": 40, "声誉": 25},
                cooldown=8,
                success_rate=0.6,
                yijing_basis="兑卦：泽上于天，以柔克刚"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.KONG_CHENG_JI,
                name="空城计",
                category=StrategyCategory.BAI_ZHAN,
                description="虚者虚之，疑中生疑",
                conditions=["实力不足", "对手多疑"],
                effects=["以弱示强", "制造威慑"],
                cost={"修为": 30, "阴阳值": 25},
                cooldown=7,
                success_rate=0.4,
                yijing_basis="乾卦：天行健，以虚示实"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.FAN_JIAN_JI,
                name="反间计",
                category=StrategyCategory.BAI_ZHAN,
                description="疑中之疑，比之自内，不自失也",
                conditions=["对手内部有矛盾", "能够传递假信息"],
                effects=["挑拨对手内部", "获得内部盟友"],
                cost={"修为": 45, "阴阳值": 30},
                cooldown=8,
                success_rate=0.55,
                yijing_basis="坎卦：水洊至，反间用间",
                hidden=True
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.KU_ROU_JI,
                name="苦肉计",
                category=StrategyCategory.BAI_ZHAN,
                description="人不自害，受害必真",
                conditions=["需要获得信任", "愿意承受损失"],
                effects=["获得对手信任", "潜入敌方"],
                cost={"生命值": 30, "修为": 20},
                cooldown=10,
                success_rate=0.8,
                yijing_basis="坤卦：地势坤，自我牺牲"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.LIAN_HUAN_JI,
                name="连环计",
                category=StrategyCategory.BAI_ZHAN,
                description="将多兵众，不可以敌，使其自累",
                conditions=["面对强敌", "能够设计连环陷阱"],
                effects=["多重打击", "连锁反应"],
                cost={"修为": 60, "五行能量": 40},
                cooldown=12,
                success_rate=0.45,
                yijing_basis="离卦：火附于木，连环相克"
            ),
            ThirtySixStrategy(
                strategy_type=StrategyType.ZOU_WEI_SHANG,
                name="走为上",
                category=StrategyCategory.BAI_ZHAN,
                description="全师避敌，左次无咎，未失常也",
                conditions=["无法获胜", "拥有撤退能力"],
                effects=["安全撤退", "保存实力"],
                cost={"修为": 10, "声誉": 15},
                cooldown=2,
                success_rate=0.95,
                yijing_basis="坤卦：地势坤，保存实力"
            )
        ]
        
        for strategy in strategies:
            self.strategies[strategy.strategy_type] = strategy
    
    def get_available_strategies(self, player_id: str, game_state: Dict[str, Any]) -> List[StrategyType]:
        """获取玩家可用的策略"""
        if player_id not in self.player_states:
            self.player_states[player_id] = StrategyState(
                available_strategies=[],
                cooldowns={},
                used_strategies=[],
                strategy_memory={}
            )
        
        player_state = self.player_states[player_id]
        available = []
        
        for strategy_type, strategy in self.strategies.items():
            # 检查冷却时间
            if strategy_type in player_state.cooldowns and player_state.cooldowns[strategy_type] > 0:
                continue
            
            # 检查使用条件
            if self._check_conditions(strategy, game_state, player_id):
                available.append(strategy_type)
        
        return available
    
    def _check_conditions(self, strategy: ThirtySixStrategy, game_state: Dict[str, Any], player_id: str) -> bool:
        """检查策略使用条件"""
        # 这里应该根据具体的游戏状态来检查条件
        # 简化实现，返回True表示条件满足
        return True
    
    def execute_strategy(self, player_id: str, strategy_type: StrategyType, target_player: str = None, game_state: Dict[str, Any] = None) -> Dict[str, Any]:
        """执行策略"""
        if strategy_type not in self.strategies:
            return {"success": False, "message": "策略不存在"}
        
        strategy = self.strategies[strategy_type]
        
        # 检查是否可以使用
        available_strategies = self.get_available_strategies(player_id, game_state or {})
        if strategy_type not in available_strategies:
            return {"success": False, "message": "策略当前不可用"}
        
        # 执行策略
        success = random.random() < strategy.success_rate
        
        if success:
            effects = self._apply_strategy_effects(strategy, player_id, target_player, game_state)
            
            # 设置冷却时间
            if player_id not in self.player_states:
                self.player_states[player_id] = StrategyState([], {}, [], {})
            
            self.player_states[player_id].cooldowns[strategy_type] = strategy.cooldown
            self.player_states[player_id].used_strategies.append(strategy_type)
            
            return {
                "success": True,
                "strategy": strategy.name,
                "description": strategy.description,
                "effects": effects,
                "yijing_basis": strategy.yijing_basis
            }
        else:
            return {
                "success": False,
                "message": f"{strategy.name}执行失败",
                "description": strategy.description
            }
    
    def _apply_strategy_effects(self, strategy: ThirtySixStrategy, player_id: str, target_player: str, game_state: Dict[str, Any]) -> List[str]:
        """应用策略效果"""
        # 这里应该根据具体的策略效果来修改游戏状态
        # 简化实现，返回效果描述
        return strategy.effects
    
    def update_cooldowns(self, player_id: str):
        """更新冷却时间"""
        if player_id in self.player_states:
            player_state = self.player_states[player_id]
            for strategy_type in list(player_state.cooldowns.keys()):
                player_state.cooldowns[strategy_type] -= 1
                if player_state.cooldowns[strategy_type] <= 0:
                    del player_state.cooldowns[strategy_type]
    
    def get_strategy_info(self, strategy_type: StrategyType) -> Optional[ThirtySixStrategy]:
        """获取策略信息"""
        return self.strategies.get(strategy_type)
    
    def get_strategies_by_category(self, category: StrategyCategory) -> List[ThirtySixStrategy]:
        """按类别获取策略"""
        return [strategy for strategy in self.strategies.values() if strategy.category == category]
    
    def get_player_strategy_summary(self, player_id: str) -> Dict[str, Any]:
        """获取玩家策略使用摘要"""
        if player_id not in self.player_states:
            return {"used_strategies": [], "cooldowns": {}, "available_count": 36}
        
        player_state = self.player_states[player_id]
        return {
            "used_strategies": [self.strategies[st].name for st in player_state.used_strategies],
            "cooldowns": {self.strategies[st].name: cd for st, cd in player_state.cooldowns.items()},
            "available_count": len(self.strategies) - len(player_state.cooldowns)
        }