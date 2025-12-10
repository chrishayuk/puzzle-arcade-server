"""Game constants and static data.

This module contains immutable game data arrays used across different puzzle types.
"""

from typing import Final

# Einstein's Puzzle attributes
EINSTEIN_COLORS: Final[list[str]] = ["Red", "Green", "Blue", "Yellow", "White"]
EINSTEIN_NATIONALITIES: Final[list[str]] = ["British", "Swedish", "Danish", "Norwegian", "German"]
EINSTEIN_DRINKS: Final[list[str]] = ["Tea", "Coffee", "Milk", "Beer", "Water"]
EINSTEIN_SMOKES: Final[list[str]] = ["Pall Mall", "Dunhill", "Blend", "Blue Master", "Prince"]
EINSTEIN_PETS: Final[list[str]] = ["Dog", "Bird", "Cat", "Horse", "Fish"]

# Einstein attribute names (for iteration)
EINSTEIN_ATTRIBUTES: Final[list[str]] = ["color", "nationality", "drink", "smoke", "pet"]

# Logic Grid categories
LOGIC_GRID_PEOPLE: Final[list[str]] = ["Alice", "Bob", "Carol", "Dave", "Eve"]
LOGIC_GRID_COLORS: Final[list[str]] = ["Red", "Blue", "Green", "Yellow", "Purple"]
LOGIC_GRID_PETS: Final[list[str]] = ["Cat", "Dog", "Bird", "Fish", "Rabbit"]
LOGIC_GRID_DRINKS: Final[list[str]] = ["Coffee", "Tea", "Juice", "Water", "Milk"]

# Logic Grid category names (for iteration)
LOGIC_GRID_CATEGORIES: Final[list[str]] = ["person", "color", "pet", "drink"]

# Scheduler task names
SCHEDULER_TASK_NAMES: Final[list[str]] = [
    "Task A",
    "Task B",
    "Task C",
    "Task D",
    "Task E",
    "Task F",
    "Task G",
    "Task H",
]
