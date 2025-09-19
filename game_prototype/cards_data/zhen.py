"""
震卦相关卡牌定义
震为雷，代表动、震动、奋起
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from card_base import GuaCard, YaoCiTask

# 震为雷 - 主卦牌
ZHEN_WEI_LEI = GuaCard(
    name="震为雷",
    associated_guas=("震", "震"),
    tasks=[
        YaoCiTask(level='地', name='雷动地脉', description='获得2点气', reward_dao_xing=0, reward_cheng_yi=1),
        YaoCiTask(level='地', name='震惊百里', description='抽取1张卡牌', reward_dao_xing=1, reward_cheng_yi=0),
        YaoCiTask(level='人', name='雷鸣警世', description='获得1点道行', reward_dao_xing=1, reward_cheng_yi=0),
        YaoCiTask(level='人', name='奋发图强', description='获得3点气', reward_dao_xing=0, reward_cheng_yi=1),
        YaoCiTask(level='天', name='雷动九天', description='获得2点道行', reward_dao_xing=2, reward_cheng_yi=0),
        YaoCiTask(level='天', name='震撼天地', description='获得1点道行和2点诚意', reward_dao_xing=1, reward_cheng_yi=2),
    ]
)

# 雷动九天 - 震卦专属卡牌
LEI_DONG_JIU_TIAN = GuaCard(
    name="雷动九天",
    associated_guas=("震", "乾"),
    tasks=[
        YaoCiTask(level='地', name='雷起云涌', description='获得1点气', reward_dao_xing=0, reward_cheng_yi=1),
        YaoCiTask(level='地', name='震动山河', description='获得1点道行', reward_dao_xing=1, reward_cheng_yi=0),
        YaoCiTask(level='人', name='雷霆万钧', description='获得2点气', reward_dao_xing=0, reward_cheng_yi=1),
        YaoCiTask(level='人', name='威震四方', description='获得1点道行', reward_dao_xing=1, reward_cheng_yi=0),
        YaoCiTask(level='天', name='九天雷动', description='获得3点道行', reward_dao_xing=3, reward_cheng_yi=0),
        YaoCiTask(level='天', name='雷帝降临', description='获得2点道行和1点诚意', reward_dao_xing=2, reward_cheng_yi=1),
    ]
)

# 震惊百里 - 震卦辅助卡牌
ZHEN_JING_BAI_LI = GuaCard(
    name="震惊百里",
    associated_guas=("震", "坤"),
    tasks=[
        YaoCiTask(level='地', name='地动山摇', description='获得1点气', reward_dao_xing=0, reward_cheng_yi=1),
        YaoCiTask(level='地', name='震慑群雄', description='抽取1张卡牌', reward_dao_xing=0, reward_cheng_yi=1),
        YaoCiTask(level='人', name='雷声阵阵', description='获得2点气', reward_dao_xing=0, reward_cheng_yi=1),
        YaoCiTask(level='人', name='震古烁今', description='获得1点道行', reward_dao_xing=1, reward_cheng_yi=0),
        YaoCiTask(level='天', name='雷鸣天下', description='获得2点道行', reward_dao_xing=2, reward_cheng_yi=0),
        YaoCiTask(level='天', name='震撼人心', description='获得1点道行和1点诚意', reward_dao_xing=1, reward_cheng_yi=1),
    ]
)