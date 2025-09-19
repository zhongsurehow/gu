import random
import copy
from typing import Dict, Any, Optional
from game_state import GameState, Zone, Player, AvatarName, BonusType, Modifiers
from card_base import GuaCard, YaoCiTask
from game_data import GAME_DECK, GENERIC_YAO_CI_POOL
from yijing_actions import (
    enhanced_play_card, enhanced_meditate, enhanced_study,
    biangua_transformation, wuxing_interaction, divine_fortune, consult_yijing
)
from wisdom_system import wisdom_system
from tutorial_system import tutorial_system, TutorialType
from achievement_system import achievement_system
from enhanced_cards import enhanced_card_system, CardType

def check_zone_control(gs: GameState, zone_name: str): # This function mutates state, which is an exception to the pattern for now for simplicity.
    """Check and update zone control based on influence markers."""
    zone_data = gs.board.gua_zones[zone_name]
    markers = zone_data["markers"]
    
    if not markers:
        zone_data["controller"] = None
        return
    
    # Find player with most influence
    max_influence = max(markers.values())
    players_with_max = [player for player, influence in markers.items() if influence == max_influence]
    
    # Check if control threshold is met (simplified: need more than half of base limit)
    control_threshold = gs.board.base_limit // 2 + 1
    
    if len(players_with_max) == 1 and max_influence >= control_threshold:
        zone_data["controller"] = players_with_max[0]
    else:
        zone_data["controller"] = None

def play_card(game_state: GameState, card_index: int, zone_choice: str, mods: Modifiers) -> Optional[GameState]:
    new_state = copy.deepcopy(game_state)
    player = new_state.get_current_player()
    if not (0 <= card_index < len(player.hand)): return None
    card_to_play = player.hand.pop(card_index)
    if zone_choice not in card_to_play.associated_guas: return None
    player.current_task_card = card_to_play
    influence_to_place = 1 + mods.extra_influence
    zone_markers = new_state.board.gua_zones[zone_choice]["markers"]
    zone_markers[player.name] = zone_markers.get(player.name, 0) + influence_to_place
    player.placed_influence_this_turn = True
    check_zone_control(new_state, zone_choice)
    
    # Update achievement tracking
    card_rarity = getattr(card_to_play, 'rarity', 'common')  # Default to common if no rarity
    achievement_system.on_card_played(player.name, card_rarity)
    
    return new_state

def move(game_state: GameState, target_zone_str: str, mods: Modifiers) -> Optional[GameState]:
    new_state = copy.deepcopy(game_state)
    player = new_state.get_current_player()
    
    # Convert string to Zone enum
    try:
        target_zone = Zone(target_zone_str)
    except ValueError:
        return None
    
    # Check if player has enough Qi
    qi_cost = max(1 - mods.qi_discount, 0)
    if player.qi < qi_cost:
        return None
    
    # Move player
    player.position = target_zone
    player.qi -= qi_cost
    new_state.board.player_positions[player.name] = target_zone
    
    return new_state

def study(game_state: GameState, mods: Modifiers) -> GameState:
    """Study to draw cards and gain knowledge."""
    new_state = copy.deepcopy(game_state)
    current_player = new_state.get_current_player()
    
    # Draw more cards based on modifiers and position
    cards_to_draw = 2 + mods.extra_card_draw  # Increased base draw
    if current_player.position == Zone.REN:  # Human realm bonus for learning
        cards_to_draw += 1
    
    available_cards = [card for card in GAME_DECK if card not in current_player.hand]
    
    # Allow drawing duplicate cards to increase deck variety
    for _ in range(cards_to_draw):
        if GAME_DECK:  # Draw from full deck, allowing duplicates
            card = random.choice(GAME_DECK)
            current_player.hand.append(card)
    
    # Bonus: gain some dao_xing from studying
    if len(current_player.hand) >= 5:  # Reward for accumulating knowledge
        current_player.dao_xing += 1
    
    # Check for wisdom triggers
    triggered_quotes = wisdom_system.check_wisdom_triggers(current_player, "study", {})
    for quote in triggered_quotes:
        wisdom_system.display_wisdom_activation(quote)
        wisdom_system.apply_wisdom_effects(current_player, quote)
    
    # Update achievement tracking
    achievement_system.on_study(current_player.name)
    
    return new_state

def meditate(game_state: GameState, mods: Modifiers) -> Optional[GameState]:
    """Meditate to gain Qi and potentially other benefits."""
    new_state = copy.deepcopy(game_state)
    player = new_state.get_current_player()
    
    # Gain more Qi based on position and modifiers
    qi_gain = 3  # Increased base gain
    if player.position == Zone.TIAN:
        qi_gain = 4
    elif player.position == Zone.REN:
        qi_gain = 3
    elif player.position == Zone.DI:
        qi_gain = 2
    
    player.qi += qi_gain
    
    # Bonus: chance to gain cheng_yi when meditating
    if player.qi >= 10:  # If player has accumulated qi
        player.cheng_yi += 1
        player.qi -= 2  # Small cost for the bonus
    
    # Check for wisdom triggers
    triggered_quotes = wisdom_system.check_wisdom_triggers(player, "meditate", {})
    for quote in triggered_quotes:
        wisdom_system.display_wisdom_activation(quote)
        wisdom_system.apply_wisdom_effects(player, quote)
    
    # Update achievement tracking
    achievement_system.on_meditation(player.name)
    
    return new_state

def get_valid_actions(game_state: GameState, player: Player, ap: int, mods: Modifiers, **flags) -> Dict[int, Dict[str, Any]]:
    """Return a dictionary of valid actions for the current player."""
    actions = {}
    action_id = 1
    
    # Always allow pass action
    actions[action_id] = {
        "action": "pass",
        "cost": 0,
        "description": "Pass turn",
        "args": []
    }
    action_id += 1
    
    # Enhanced play card actions (with Yijing effects)
    for i, card in enumerate(player.hand):
        if ap >= 1:  # Playing a card costs 1 AP
            for gua in card.associated_guas:
                actions[action_id] = {
                    "action": enhanced_play_card,
                    "cost": 1,
                    "description": f"Play {card.name} to {gua} [阴阳]",
                    "args": [i, gua]
                }
                action_id += 1
    
    # Move action
    if ap >= 1 and player.qi >= 1:  # Moving costs 1 AP and 1 Qi
        for zone in Zone:
            if zone != player.position:
                actions[action_id] = {
                    "action": move,
                    "cost": 1,
                    "description": f"Move to {zone.value}",
                    "args": [zone.value]
                }
                action_id += 1
    
    # Enhanced study action (with Yijing wisdom)
    if ap >= 1:
        actions[action_id] = {
            "action": enhanced_study,
            "cost": 1,
            "description": "Study (draw cards, gain wisdom) [书]",
            "args": []
        }
        action_id += 1
    
    # Enhanced meditate action (with Yijing cultivation)
    if ap >= 1:
        actions[action_id] = {
            "action": enhanced_meditate,
            "cost": 1,
            "description": "Meditate (cultivate Qi, balance Yin-Yang) 🧘",
            "args": []
        }
        action_id += 1
    
    # Biangua transformation (change hexagram)
    if ap >= 1 and player.cheng_yi >= 3:
        actions[action_id] = {
            "action": "biangua_prompt",
            "cost": 1,
            "description": "Biangua (transform hexagram) 🔄",
            "args": []
        }
        action_id += 1
    
    # Divine fortune (占卜运势)
    if ap >= 1 and player.qi >= 3:
        actions[action_id] = {
            "action": divine_fortune,
            "cost": 1,
            "description": "Divine Fortune (占卜运势) 🔮",
            "args": []
        }
        action_id += 1
    
    # View wisdom progress (no cost)
    actions[action_id] = {
        "action": "wisdom_progress",
        "cost": 0,
        "description": "View Wisdom Progress (查看智慧收集进度) [卷]",
        "args": []
    }
    action_id += 1
    
    # Tutorial system actions (no cost)
    actions[action_id] = {
        "action": "tutorial_menu",
        "cost": 0,
        "description": "Tutorial Menu (教学菜单) 🎓",
        "args": []
    }
    action_id += 1
    
    actions[action_id] = {
        "action": "learning_progress",
        "cost": 0,
        "description": "Learning Progress (学习进度) [统计]",
        "args": []
    }
    action_id += 1
    
    # Achievement system actions (no cost)
    actions[action_id] = {
        "action": "achievement_progress",
        "cost": 0,
        "description": "Achievement Progress (成就进度) 🏆",
        "args": []
    }
    action_id += 1
    
    actions[action_id] = {
        "action": "achievement_list",
        "cost": 0,
        "description": "Achievement List (成就列表) [目标]",
        "args": []
    }
    action_id += 1
    
    # Enhanced card system actions
    actions[action_id] = {
        "action": "view_enhanced_cards",
        "cost": 0,
        "description": "View Enhanced Cards (查看增强卡牌) [卡牌]",
        "args": []
    }
    action_id += 1
    
    if ap >= 1:
        actions[action_id] = {
            "action": "use_enhanced_card",
            "cost": 1,
            "description": "Use Enhanced Card (使用增强卡牌) [闪]",
            "args": []
        }
        action_id += 1
    
    # Consult Yijing for guidance
    if ap >= 1 and player.dao_xing >= 2:
        actions[action_id] = {
            "action": "consult_yijing_prompt",
            "cost": 1,
            "description": "Consult Yijing (咨询易经) [卷]",
            "args": []
        }
        action_id += 1
    
    return actions
