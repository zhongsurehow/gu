"""
64卦卡牌生成器
自动生成完整的64卦卡牌系统，每卦包含深度的易经智慧
现已升级为基于真实易经爻辞的系统
"""

from card_base import GuaCard, YaoCiTask
from yijing_mechanics import YinYang, WuXing
from authentic_yao_ci_generator import generate_authentic_yao_ci_tasks

# 64卦基础信息
GUA_64_INFO = {
    # 乾宫八卦
    "乾为天": {"trigrams": ("乾", "乾"), "nature": "刚健", "element": WuXing.JIN, "yin_yang": YinYang.YANG},
    "天风姤": {"trigrams": ("乾", "巽"), "nature": "遇合", "element": WuXing.JIN, "yin_yang": YinYang.YANG},
    "天山遁": {"trigrams": ("乾", "艮"), "nature": "退避", "element": WuXing.JIN, "yin_yang": YinYang.YANG},
    "天地否": {"trigrams": ("乾", "坤"), "nature": "闭塞", "element": WuXing.JIN, "yin_yang": YinYang.YANG},
    "风地观": {"trigrams": ("巽", "坤"), "nature": "观察", "element": WuXing.MU, "yin_yang": YinYang.YIN},
    "山地剥": {"trigrams": ("艮", "坤"), "nature": "剥落", "element": WuXing.TU, "yin_yang": YinYang.YANG},
    "火地晋": {"trigrams": ("离", "坤"), "nature": "上进", "element": WuXing.HUO, "yin_yang": YinYang.YIN},
    "火天大有": {"trigrams": ("离", "乾"), "nature": "大有", "element": WuXing.HUO, "yin_yang": YinYang.YIN},
    
    # 坤宫八卦
    "坤为地": {"trigrams": ("坤", "坤"), "nature": "柔顺", "element": WuXing.TU, "yin_yang": YinYang.YIN},
    "地雷复": {"trigrams": ("坤", "震"), "nature": "复归", "element": WuXing.TU, "yin_yang": YinYang.YIN},
    "地泽临": {"trigrams": ("坤", "兑"), "nature": "临近", "element": WuXing.TU, "yin_yang": YinYang.YIN},
    "地天泰": {"trigrams": ("坤", "乾"), "nature": "通泰", "element": WuXing.TU, "yin_yang": YinYang.YIN},
    "雷天大壮": {"trigrams": ("震", "乾"), "nature": "壮盛", "element": WuXing.MU, "yin_yang": YinYang.YANG},
    "泽天夬": {"trigrams": ("兑", "乾"), "nature": "决断", "element": WuXing.JIN, "yin_yang": YinYang.YIN},
    "水天需": {"trigrams": ("坎", "乾"), "nature": "等待", "element": WuXing.SHUI, "yin_yang": YinYang.YANG},
    "水地比": {"trigrams": ("坎", "坤"), "nature": "亲比", "element": WuXing.SHUI, "yin_yang": YinYang.YANG},
    
    # 震宫八卦
    "震为雷": {"trigrams": ("震", "震"), "nature": "震动", "element": WuXing.MU, "yin_yang": YinYang.YANG},
    "雷地豫": {"trigrams": ("震", "坤"), "nature": "愉悦", "element": WuXing.MU, "yin_yang": YinYang.YANG},
    "雷水解": {"trigrams": ("震", "坎"), "nature": "解脱", "element": WuXing.MU, "yin_yang": YinYang.YANG},
    "雷风恒": {"trigrams": ("震", "巽"), "nature": "恒久", "element": WuXing.MU, "yin_yang": YinYang.YANG},
    "地风升": {"trigrams": ("坤", "巽"), "nature": "上升", "element": WuXing.TU, "yin_yang": YinYang.YIN},
    "水风井": {"trigrams": ("坎", "巽"), "nature": "井泉", "element": WuXing.SHUI, "yin_yang": YinYang.YANG},
    "泽风大过": {"trigrams": ("兑", "巽"), "nature": "大过", "element": WuXing.JIN, "yin_yang": YinYang.YIN},
    "泽雷随": {"trigrams": ("兑", "震"), "nature": "随从", "element": WuXing.JIN, "yin_yang": YinYang.YIN},
    
    # 巽宫八卦
    "巽为风": {"trigrams": ("巽", "巽"), "nature": "巽入", "element": WuXing.MU, "yin_yang": YinYang.YIN},
    "风天小畜": {"trigrams": ("巽", "乾"), "nature": "小畜", "element": WuXing.MU, "yin_yang": YinYang.YIN},
    "风火家人": {"trigrams": ("巽", "离"), "nature": "家庭", "element": WuXing.MU, "yin_yang": YinYang.YIN},
    "风雷益": {"trigrams": ("巽", "震"), "nature": "增益", "element": WuXing.MU, "yin_yang": YinYang.YIN},
    "天雷无妄": {"trigrams": ("乾", "震"), "nature": "无妄", "element": WuXing.JIN, "yin_yang": YinYang.YANG},
    "火雷噬嗑": {"trigrams": ("离", "震"), "nature": "咬合", "element": WuXing.HUO, "yin_yang": YinYang.YIN},
    "山雷颐": {"trigrams": ("艮", "震"), "nature": "颐养", "element": WuXing.TU, "yin_yang": YinYang.YANG},
    "山风蛊": {"trigrams": ("艮", "巽"), "nature": "蛊惑", "element": WuXing.TU, "yin_yang": YinYang.YANG},
    
    # 坎宫八卦
    "坎为水": {"trigrams": ("坎", "坎"), "nature": "险陷", "element": WuXing.SHUI, "yin_yang": YinYang.YANG},
    "水泽节": {"trigrams": ("坎", "兑"), "nature": "节制", "element": WuXing.SHUI, "yin_yang": YinYang.YANG},
    "水雷屯": {"trigrams": ("坎", "震"), "nature": "屯积", "element": WuXing.SHUI, "yin_yang": YinYang.YANG},
    "水火既济": {"trigrams": ("坎", "离"), "nature": "既济", "element": WuXing.SHUI, "yin_yang": YinYang.YANG},
    "泽火革": {"trigrams": ("兑", "离"), "nature": "变革", "element": WuXing.JIN, "yin_yang": YinYang.YIN},
    "雷火丰": {"trigrams": ("震", "离"), "nature": "丰盛", "element": WuXing.MU, "yin_yang": YinYang.YANG},
    "地火明夷": {"trigrams": ("坤", "离"), "nature": "明夷", "element": WuXing.TU, "yin_yang": YinYang.YIN},
    "地水师": {"trigrams": ("坤", "坎"), "nature": "师众", "element": WuXing.TU, "yin_yang": YinYang.YIN},
    
    # 离宫八卦
    "离为火": {"trigrams": ("离", "离"), "nature": "光明", "element": WuXing.HUO, "yin_yang": YinYang.YIN},
    "火山旅": {"trigrams": ("离", "艮"), "nature": "旅行", "element": WuXing.HUO, "yin_yang": YinYang.YIN},
    "火风鼎": {"trigrams": ("离", "巽"), "nature": "鼎新", "element": WuXing.HUO, "yin_yang": YinYang.YIN},
    "火水未济": {"trigrams": ("离", "坎"), "nature": "未济", "element": WuXing.HUO, "yin_yang": YinYang.YIN},
    "山水蒙": {"trigrams": ("艮", "坎"), "nature": "蒙昧", "element": WuXing.TU, "yin_yang": YinYang.YANG},
    "风水涣": {"trigrams": ("巽", "坎"), "nature": "涣散", "element": WuXing.MU, "yin_yang": YinYang.YIN},
    "天水讼": {"trigrams": ("乾", "坎"), "nature": "争讼", "element": WuXing.JIN, "yin_yang": YinYang.YANG},
    "天火同人": {"trigrams": ("乾", "离"), "nature": "同人", "element": WuXing.JIN, "yin_yang": YinYang.YANG},
    
    # 艮宫八卦
    "艮为山": {"trigrams": ("艮", "艮"), "nature": "静止", "element": WuXing.TU, "yin_yang": YinYang.YANG},
    "山火贲": {"trigrams": ("艮", "离"), "nature": "装饰", "element": WuXing.TU, "yin_yang": YinYang.YANG},
    "山天大畜": {"trigrams": ("艮", "乾"), "nature": "大畜", "element": WuXing.TU, "yin_yang": YinYang.YANG},
    "山泽损": {"trigrams": ("艮", "兑"), "nature": "损减", "element": WuXing.TU, "yin_yang": YinYang.YANG},
    "火泽睽": {"trigrams": ("离", "兑"), "nature": "睽违", "element": WuXing.HUO, "yin_yang": YinYang.YIN},
    "天泽履": {"trigrams": ("乾", "兑"), "nature": "履行", "element": WuXing.JIN, "yin_yang": YinYang.YANG},
    "风泽中孚": {"trigrams": ("巽", "兑"), "nature": "中孚", "element": WuXing.MU, "yin_yang": YinYang.YIN},
    "风山渐": {"trigrams": ("巽", "艮"), "nature": "渐进", "element": WuXing.MU, "yin_yang": YinYang.YIN},
    
    # 兑宫八卦
    "兑为泽": {"trigrams": ("兑", "兑"), "nature": "喜悦", "element": WuXing.JIN, "yin_yang": YinYang.YIN},
    "泽水困": {"trigrams": ("兑", "坎"), "nature": "困顿", "element": WuXing.JIN, "yin_yang": YinYang.YIN},
    "泽地萃": {"trigrams": ("兑", "坤"), "nature": "萃聚", "element": WuXing.JIN, "yin_yang": YinYang.YIN},
    "泽山咸": {"trigrams": ("兑", "艮"), "nature": "感应", "element": WuXing.JIN, "yin_yang": YinYang.YIN},
    "水山蹇": {"trigrams": ("坎", "艮"), "nature": "蹇难", "element": WuXing.SHUI, "yin_yang": YinYang.YANG},
    "地山谦": {"trigrams": ("坤", "艮"), "nature": "谦逊", "element": WuXing.TU, "yin_yang": YinYang.YIN},
    "雷山小过": {"trigrams": ("震", "艮"), "nature": "小过", "element": WuXing.MU, "yin_yang": YinYang.YANG},
    "雷泽归妹": {"trigrams": ("震", "兑"), "nature": "归妹", "element": WuXing.MU, "yin_yang": YinYang.YANG},
}

def generate_yao_ci_tasks(gua_name: str, gua_info: dict) -> list[YaoCiTask]:
    """为每个卦生成真实的爻辞任务"""
    # 尝试使用真实爻辞系统
    try:
        authentic_tasks = generate_authentic_yao_ci_tasks(gua_name)
        if authentic_tasks and len(authentic_tasks) == 6:
            return authentic_tasks
        elif authentic_tasks:
            print(f"警告: {gua_name} 的真实爻辞任务数量为 {len(authentic_tasks)}，需要6个")
    except Exception as e:
        print(f"真实爻辞系统生成失败: {e}")
    
    # 如果没有真实爻辞数据，使用原有的模板化系统作为后备
    nature = gua_info["nature"]
    element = gua_info["element"]
    yin_yang = gua_info["yin_yang"]
    
    # 根据卦的属性生成不同的任务
    tasks = []
    
    # 地部任务（初爻、二爻）
    tasks.append(YaoCiTask(
        level='地', 
        name=f'初爻：{nature}之始',
        description=f'获得{element.value}属性亲和力+1，{yin_yang.value}气+1',
        reward_dao_xing=0, 
        reward_cheng_yi=1
    ))
    
    tasks.append(YaoCiTask(
        level='地', 
        name=f'二爻：{nature}渐显',
        description=f'抽取1张卡牌，若为{element.value}属性则额外获得1点气',
        reward_dao_xing=1, 
        reward_cheng_yi=0
    ))
    
    # 人部任务（三爻、四爻）
    tasks.append(YaoCiTask(
        level='人', 
        name=f'三爻：{nature}之变',
        description=f'获得2点气，若阴阳平衡则额外获得1点道行',
        reward_dao_xing=0, 
        reward_cheng_yi=1
    ))
    
    tasks.append(YaoCiTask(
        level='人', 
        name=f'四爻：{nature}近成',
        description=f'获得1点道行，可选择转化1点{yin_yang.value}气为对立属性',
        reward_dao_xing=1, 
        reward_cheng_yi=0
    ))
    
    # 天部任务（五爻、上爻）
    tasks.append(YaoCiTask(
        level='天', 
        name=f'五爻：{nature}大成',
        description=f'获得2点道行，激活{element.value}行相生效果',
        reward_dao_xing=2, 
        reward_cheng_yi=0
    ))
    
    tasks.append(YaoCiTask(
        level='天', 
        name=f'上爻：{nature}极致',
        description=f'获得3点诚意，但需注意物极必反',
        reward_dao_xing=0, 
        reward_cheng_yi=3
    ))
    
    return tasks

def generate_all_64_guas() -> dict[str, GuaCard]:
    """生成全部64卦卡牌"""
    all_cards = {}
    
    for gua_name, gua_info in GUA_64_INFO.items():
        tasks = generate_yao_ci_tasks(gua_name, gua_info)
        
        card = GuaCard(
            name=gua_name,
            associated_guas=gua_info["trigrams"],
            tasks=tasks
        )
        
        all_cards[gua_name] = card
    
    return all_cards

# 生成所有卡牌
ALL_64_GUAS = generate_all_64_guas()

# 按宫分组
QIAN_GONG = [ALL_64_GUAS[name] for name in ["乾为天", "天风姤", "天山遁", "天地否", "风地观", "山地剥", "火地晋", "火天大有"]]
KUN_GONG = [ALL_64_GUAS[name] for name in ["坤为地", "地雷复", "地泽临", "地天泰", "雷天大壮", "泽天夬", "水天需", "水地比"]]
ZHEN_GONG = [ALL_64_GUAS[name] for name in ["震为雷", "雷地豫", "雷水解", "雷风恒", "地风升", "水风井", "泽风大过", "泽雷随"]]
XUN_GONG = [ALL_64_GUAS[name] for name in ["巽为风", "风天小畜", "风火家人", "风雷益", "天雷无妄", "火雷噬嗑", "山雷颐", "山风蛊"]]
KAN_GONG = [ALL_64_GUAS[name] for name in ["坎为水", "水泽节", "水雷屯", "水火既济", "泽火革", "雷火丰", "地火明夷", "地水师"]]
LI_GONG = [ALL_64_GUAS[name] for name in ["离为火", "火山旅", "火风鼎", "火水未济", "山水蒙", "风水涣", "天水讼", "天火同人"]]
GEN_GONG = [ALL_64_GUAS[name] for name in ["艮为山", "山火贲", "山天大畜", "山泽损", "火泽睽", "天泽履", "风泽中孚", "风山渐"]]
DUI_GONG = [ALL_64_GUAS[name] for name in ["兑为泽", "泽水困", "泽地萃", "泽山咸", "水山蹇", "地山谦", "雷山小过", "雷泽归妹"]]

# 完整卡组（可根据需要选择子集）
COMPLETE_64_DECK = list(ALL_64_GUAS.values())