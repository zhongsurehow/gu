import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from card_base import GuaCard, YaoCiTask

# --- 坤为地 (Kun as Earth) ---

kun_wei_di_tasks = [
    YaoCiTask(level='地', name='初六：履霜，坚冰至。',
              description='Gain 2 阴阳之气.',
              reward_dao_xing=0, reward_cheng_yi=0), # Effect is direct
    YaoCiTask(level='地', name='六二：直，方，大。',
              description='Gain 1 道行 for every 3 阴阳之气 you have (max 3).',
              reward_dao_xing=0, reward_cheng_yi=0), # Effect is direct
    YaoCiTask(level='人', name='六三：含章可贞。',
              description='If you have not performed a 升沉 move this turn, gain 1 诚意.',
              reward_dao_xing=0, reward_cheng_yi=0), # Effect is conditional
    YaoCiTask(level='人', name='六四：括囊，无咎无誉。',
              description='If you have 6 or more cards in hand, gain 3 道行.',
              reward_dao_xing=0, reward_cheng_yi=0), # Effect is conditional
    YaoCiTask(level='天', name='六五：黄裳，元吉。',
              description='Gain 2 道行 for each zone you currently control.',
              reward_dao_xing=0, reward_cheng_yi=1), # Base reward for a high-level task
    YaoCiTask(level='天', name='上六：龙战于野。',
              description='Choose another player. You both gain 4 道行.',
              reward_dao_xing=0, reward_cheng_yi=0), # Effect is direct
]

KUN_WEI_DI = GuaCard(
    name="坤为地",
    associated_guas=("坤", "坤"),
    tasks=kun_wei_di_tasks
)
