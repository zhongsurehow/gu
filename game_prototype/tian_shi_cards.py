# This file defines the "天时" (Mandate of Heaven) cards.
# These cards introduce a global rule that affects all players for one round.

# In a full implementation, this could be a class with methods,
# but for the prototype, a list of dictionaries is simple and effective.
TIAN_SHI_CARDS = [
    {
        "name": "丰年",
        "desc": "Bountiful Year: All players gain an additional +1 Qi during the Qi Phase.",
        "effect_type": "MODIFY_QI_GAIN",
        "value": 1
    },
    {
        "name": "兵乱",
        "desc": "Warring Times: The 'empower' action costs an additional +1 Qi.",
        "effect_type": "MODIFY_ACTION_COST",
        "action": "empower",
        "cost_change": 1
    },
    {
        "name": "文昌",
        "desc": "Flourishing Culture: The 'study' action allows drawing 3 cards instead of 2.",
        "effect_type": "MODIFY_ACTION_EFFECT",
        "action": "study",
        "value": 3 # The new total number of cards to draw
    },
    {
        "name": "无为",
        "desc": "Inaction: The heavens are silent. No effect this round.",
        "effect_type": "NO_EFFECT"
    },
]
