# This file makes the 'cards_data' directory a Python package.
# It's used to aggregate all the individual card definitions.

from .qian import QIAN_WEI_TIAN
from .kun import KUN_WEI_DI
from .zhen import ZHEN_WEI_LEI, LEI_DONG_JIU_TIAN, ZHEN_JING_BAI_LI

# Expanded card collection with multiple cards per gua
ALL_CARDS = [
    # 乾卦系列
    QIAN_WEI_TIAN,
    
    # 坤卦系列  
    KUN_WEI_DI,
    
    # 震卦系列 (新增)
    ZHEN_WEI_LEI,
    LEI_DONG_JIU_TIAN,
    ZHEN_JING_BAI_LI,
]
