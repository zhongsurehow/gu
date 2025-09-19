from game_state import Avatar, AvatarName, BonusType
from card_base import YaoCiTask

# This file centralizes game data for easy modification and collaboration.

# --- Data Definitions for Gua Zone Bonuses ---
GUA_ZONE_BONUSES = {
    "乾": {"bonus": BonusType.EXTRA_AP, "desc": "+1 AP during Action Phase"},
    "坤": {"bonus": BonusType.EXTRA_QI, "desc": "+2 Qi during Qi Phase"},
    "离": {"bonus": BonusType.DRAW_CARD, "desc": "Draw 1 card during End Phase"},
    "艮": {"bonus": BonusType.HAND_LIMIT, "desc": "+2 Hand Limit"},
    "震": {"bonus": BonusType.EXTRA_INFLUENCE, "desc": "Place 1 extra influence"},
    "巽": {"bonus": BonusType.FREE_STUDY, "desc": "Perform one free Study action"},
    "坎": {"bonus": BonusType.QI_DISCOUNT, "desc": "All Qi costs are reduced by 1"},
    "兑": {"bonus": BonusType.DAO_XING_ON_TASK, "desc": "+1 Dao Xing when completing a task"},
}

# --- Avatar Definitions ---
EMPEROR_AVATAR = Avatar(
    name=AvatarName.EMPEROR,
    description="您是前朝皇室的末裔，身负着复兴王朝、再定乾坤的沉重使命。",
    ability_description="王权: 在您的“演卦阶段”，您可以花费1点AP和3点“阴阳之气”，直接在一个您已拥有影响力标记的卦区，再额外放置一个影响力标记。"
)

HERMIT_AVATAR = Avatar(
    name=AvatarName.HERMIT,
    description="您曾是名满天下的智者，却看破了红尘纷争，选择归隐山林。",
    ability_description="逍遥游: 您执行“升沉”移动时，所需花费的“阴阳之气”-1。在您的“归元阶段”，若您本回合没有放置任何“影响力标记”，您可以摸一张卦牌。"
)

# --- Game Deck Construction ---
from cards_data import ALL_CARDS
from generate_64_guas import COMPLETE_64_DECK, QIAN_GONG, KUN_GONG

# 可选择不同的卡组配置
# 选项1：使用原有的少量卡牌（适合快速游戏）
BASIC_DECK = ALL_CARDS

# 选项2：使用乾坤两宫（16张卡，平衡的游戏体验）
BALANCED_DECK = QIAN_GONG + KUN_GONG

# 选项3：使用完整64卦（完整易经体验）
FULL_DECK = COMPLETE_64_DECK

# 当前使用的卡组（可根据需要切换）
GAME_DECK = BALANCED_DECK  # 默认使用平衡卡组

# For testing purposes, we provide easy access to a specific card.
QIAN_WEI_TIAN = GAME_DECK[0] if GAME_DECK else None

# --- Generic Task Pool for "Scry" Action ---
GENERIC_YAO_CI_POOL = [
    YaoCiTask(level='地', name='【衍化】地脉震动', description='Gain 2 阴阳之气.', reward_dao_xing=0, reward_cheng_yi=0),
    YaoCiTask(level='人', name='【衍化】人潮熙攘', description='Draw 1 card.', reward_dao_xing=0, reward_cheng_yi=0),
    YaoCiTask(level='天', name='【衍化】天星闪耀', description='Gain 2 道行.', reward_dao_xing=0, reward_cheng_yi=0),
]
