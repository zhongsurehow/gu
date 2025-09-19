import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from card_base import GuaCard, YaoCiTask

# --- 乾为天 (Qian as Heaven) ---

qian_wei_tian_tasks = [
    YaoCiTask(level='地', name='初九：潜龙勿用。',
              description='在您的回合中，您可以选择跳过您的所有行动，并获得3点“道行”和1张额外的卦牌。',
              reward_dao_xing=1, reward_cheng_yi=0),
    YaoCiTask(level='地', name='九二：见龙在田，利见大人。',
              description='当您在某个“地部卦区”放置“影响力标记”时，可以额外放置1个。',
              reward_dao_xing=1, reward_cheng_yi=0),
    YaoCiTask(level='人', name='九三：君子终日乾乾，夕惕若，厉无咎。',
              description='在您的回合结束时，若您本回合没有获得任何“道行”，则您可以获得2点“道行”。',
              reward_dao_xing=0, reward_cheng_yi=1),
    YaoCiTask(level='人', name='九四：或跃在渊，无咎。',
              description='支付3点“道行”，您可以立即从“人部”移动至“天部”，此次移动不消耗AP。',
              reward_dao_xing=0, reward_cheng_yi=1),
    YaoCiTask(level='天', name='九五：飞龙在天，利见大人。',
              description='在您的回合中，指定另一名玩家，您可以立即获得等同于其手牌数量的“道行”。',
              reward_dao_xing=0, reward_cheng_yi=2),
    YaoCiTask(level='天', name='上九：亢龙有悔。',
              description='若您是当前“道行”最高的玩家，您必须立刻弃掉所有手牌。此为盛极而衰之兆。',
              reward_dao_xing=0, reward_cheng_yi=5),
]

QIAN_WEI_TIAN = GuaCard(
    name="乾为天",
    associated_guas=("乾", "乾"),
    tasks=qian_wei_tian_tasks
)
