from typing import Dict, Any
from typing import Dict, Any

# No game state imports are needed here, as the logic only needs the
# final generated action menu. This keeps the bot logic decoupled.

def get_bot_choice(valid_actions: Dict[int, Dict[str, Any]]) -> int:
    """
    A very simple bot logic.
    It will choose the first available action that is not 'pass'.
    If 'pass' is the only option, it will choose that.
    """
    # Find the first non-pass action
    for key, action_data in valid_actions.items():
        if action_data["action"] != "pass":
            return key

    # If only "pass" is available, find its key and return it
    for key, action_data in valid_actions.items():
        if action_data["action"] == "pass":
            return key

    # Fallback, should not be reached if "pass" is always an option
    return 1
