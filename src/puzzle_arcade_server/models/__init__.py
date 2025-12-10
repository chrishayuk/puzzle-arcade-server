"""Pydantic models and enums for the Puzzle Arcade server."""

from .base import GridPosition, MoveResult
from .config import (
    BinaryConfig,
    FutoshikiConfig,
    GameConfig,
    KakuroConfig,
    KenKenConfig,
    KillerSudokuConfig,
    KnapsackConfig,
    LightsOutConfig,
    LogicGridConfig,
    MastermindConfig,
    MinesweeperConfig,
    NonogramConfig,
    NurikabeConfig,
    SchedulerConfig,
    SlitherlinkConfig,
    SudokuConfig,
)
from .enums import (
    ArithmeticOperation,
    CellState,
    ConnectionState,
    DifficultyLevel,
    GameCommand,
    KnapsackAction,
    MinesweeperAction,
    NurikabeColor,
    SchedulerAction,
)
from .games import Cage, HouseAssignment, Item, LogicGridCategories, PersonAttributes, Task

__all__ = [
    # Enums
    "ArithmeticOperation",
    "CellState",
    "ConnectionState",
    "DifficultyLevel",
    "GameCommand",
    "KnapsackAction",
    "MinesweeperAction",
    "NurikabeColor",
    "SchedulerAction",
    # Base models
    "MoveResult",
    "GridPosition",
    "GameConfig",
    "LightsOutConfig",
    "FutoshikiConfig",
    "SudokuConfig",
    "BinaryConfig",
    "MastermindConfig",
    "KakuroConfig",
    "NonogramConfig",
    "KnapsackConfig",
    "SchedulerConfig",
    "MinesweeperConfig",
    "LogicGridConfig",
    "SlitherlinkConfig",
    "KenKenConfig",
    "KillerSudokuConfig",
    "NurikabeConfig",
    # Game-specific models
    "Task",
    "Item",
    "Cage",
    "HouseAssignment",
    "LogicGridCategories",
    "PersonAttributes",
]
