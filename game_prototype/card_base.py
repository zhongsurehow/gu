import collections
from typing import NamedTuple

# This file defines the fundamental building blocks of a card,
# with no other project dependencies, to avoid circular imports.

class YaoCiTask(NamedTuple):
    """A data structure to hold the details of a single task on a card."""
    level: str
    name: str
    description: str
    reward_dao_xing: int
    reward_cheng_yi: int

class GuaCard:
    """Represents a Gua Card with its 6 Yao Ci tasks."""
    def __init__(self, name: str, associated_guas: tuple[str, str], tasks: list[YaoCiTask]):
        if len(tasks) != 6:
            raise ValueError("A GuaCard must have exactly 6 tasks.")
        self.name = name
        self.associated_guas = associated_guas
        self.tasks = tasks
