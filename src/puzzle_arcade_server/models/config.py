"""Configuration models for games."""

from pydantic import BaseModel, Field

from .enums import DifficultyLevel


class GameConfig(BaseModel):
    """Base configuration for all games."""

    difficulty: DifficultyLevel = Field(default=DifficultyLevel.EASY, description="Game difficulty level")


class SudokuConfig(GameConfig):
    """Configuration for Sudoku game."""

    cells_to_remove: int = Field(ge=0, le=64, description="Number of cells to remove from solution")

    @classmethod
    def from_difficulty(cls, difficulty: DifficultyLevel) -> "SudokuConfig":
        """Create config from difficulty level."""
        cells_map = {
            DifficultyLevel.EASY: 35,
            DifficultyLevel.MEDIUM: 45,
            DifficultyLevel.HARD: 55,
        }
        return cls(difficulty=difficulty, cells_to_remove=cells_map[difficulty])


class KenKenConfig(GameConfig):
    """Configuration for KenKen game."""

    size: int = Field(ge=3, le=9, description="Grid size (NxN)")
    num_cages: int = Field(ge=1, description="Number of cages")

    @classmethod
    def from_difficulty(cls, difficulty: DifficultyLevel) -> "KenKenConfig":
        """Create config from difficulty level."""
        config_map = {
            DifficultyLevel.EASY: {"size": 4, "num_cages": 8},
            DifficultyLevel.MEDIUM: {"size": 5, "num_cages": 12},
            DifficultyLevel.HARD: {"size": 6, "num_cages": 18},
        }
        params = config_map[difficulty]
        return cls(difficulty=difficulty, **params)


class KakuroConfig(GameConfig):
    """Configuration for Kakuro game."""

    size: int = Field(ge=4, le=10, description="Grid size")
    num_runs: int = Field(ge=1, description="Number of runs (horizontal + vertical)")

    @classmethod
    def from_difficulty(cls, difficulty: DifficultyLevel) -> "KakuroConfig":
        """Create config from difficulty level."""
        config_map = {
            DifficultyLevel.EASY: {"size": 4, "num_runs": 6},
            DifficultyLevel.MEDIUM: {"size": 6, "num_runs": 10},
            DifficultyLevel.HARD: {"size": 8, "num_runs": 16},
        }
        params = config_map[difficulty]
        return cls(difficulty=difficulty, **params)


class SchedulerConfig(GameConfig):
    """Configuration for Scheduler game."""

    num_tasks: int = Field(ge=1, le=20, description="Number of tasks")
    num_workers: int = Field(ge=1, le=10, description="Number of workers")
    dependency_prob: float = Field(ge=0.0, le=1.0, description="Probability of task dependencies")

    @classmethod
    def from_difficulty(cls, difficulty: DifficultyLevel) -> "SchedulerConfig":
        """Create config from difficulty level."""
        config_map = {
            DifficultyLevel.EASY: {"num_tasks": 4, "num_workers": 2, "dependency_prob": 0.3},
            DifficultyLevel.MEDIUM: {"num_tasks": 6, "num_workers": 2, "dependency_prob": 0.4},
            DifficultyLevel.HARD: {"num_tasks": 8, "num_workers": 3, "dependency_prob": 0.5},
        }
        params = config_map[difficulty]
        return cls(difficulty=difficulty, **params)


class KnapsackConfig(GameConfig):
    """Configuration for Knapsack game."""

    num_items: int = Field(ge=1, le=20, description="Number of items")
    max_weight: int = Field(ge=1, description="Maximum knapsack capacity")

    @classmethod
    def from_difficulty(cls, difficulty: DifficultyLevel) -> "KnapsackConfig":
        """Create config from difficulty level."""
        config_map = {
            DifficultyLevel.EASY: {"num_items": 5, "max_weight": 20},
            DifficultyLevel.MEDIUM: {"num_items": 8, "max_weight": 35},
            DifficultyLevel.HARD: {"num_items": 12, "max_weight": 50},
        }
        params = config_map[difficulty]
        return cls(difficulty=difficulty, **params)


class MinesweeperConfig(GameConfig):
    """Configuration for Minesweeper game."""

    size: int = Field(ge=4, le=20, description="Grid size (NxN)")
    mines: int = Field(ge=1, description="Number of mines")

    @classmethod
    def from_difficulty(cls, difficulty: DifficultyLevel) -> "MinesweeperConfig":
        """Create config from difficulty level."""
        config_map = {
            DifficultyLevel.EASY: {"size": 6, "mines": 6},
            DifficultyLevel.MEDIUM: {"size": 8, "mines": 12},
            DifficultyLevel.HARD: {"size": 10, "mines": 20},
        }
        params = config_map[difficulty]
        return cls(difficulty=difficulty, **params)


class NurikabeConfig(GameConfig):
    """Configuration for Nurikabe game."""

    size: int = Field(ge=4, le=12, description="Grid size (NxN)")
    num_islands: int = Field(ge=1, description="Number of islands")

    @classmethod
    def from_difficulty(cls, difficulty: DifficultyLevel) -> "NurikabeConfig":
        """Create config from difficulty level."""
        config_map = {
            DifficultyLevel.EASY: {"size": 6, "num_islands": 3},
            DifficultyLevel.MEDIUM: {"size": 8, "num_islands": 4},
            DifficultyLevel.HARD: {"size": 10, "num_islands": 5},
        }
        params = config_map[difficulty]
        return cls(difficulty=difficulty, **params)


class LightsOutConfig(GameConfig):
    """Configuration for Lights Out game."""

    size: int = Field(ge=3, le=10, description="Grid size (NxN)")
    num_presses: int = Field(ge=1, description="Number of initial presses to create puzzle")

    @classmethod
    def from_difficulty(cls, difficulty: DifficultyLevel) -> "LightsOutConfig":
        """Create config from difficulty level."""
        config_map = {
            DifficultyLevel.EASY: {"size": 5, "num_presses": 3},
            DifficultyLevel.MEDIUM: {"size": 6, "num_presses": 5},
            DifficultyLevel.HARD: {"size": 7, "num_presses": 7},
        }
        params = config_map[difficulty]
        return cls(difficulty=difficulty, **params)


class BinaryConfig(GameConfig):
    """Configuration for Binary Puzzle game."""

    size: int = Field(ge=4, le=14, description="Grid size (NxN, must be even)")

    @classmethod
    def from_difficulty(cls, difficulty: DifficultyLevel) -> "BinaryConfig":
        """Create config from difficulty level."""
        config_map = {
            DifficultyLevel.EASY: {"size": 6},
            DifficultyLevel.MEDIUM: {"size": 8},
            DifficultyLevel.HARD: {"size": 10},
        }
        params = config_map[difficulty]
        return cls(difficulty=difficulty, **params)


class FutoshikiConfig(GameConfig):
    """Configuration for Futoshiki game."""

    size: int = Field(ge=4, le=9, description="Grid size (NxN)")

    @classmethod
    def from_difficulty(cls, difficulty: DifficultyLevel) -> "FutoshikiConfig":
        """Create config from difficulty level."""
        config_map = {
            DifficultyLevel.EASY: {"size": 4},
            DifficultyLevel.MEDIUM: {"size": 5},
            DifficultyLevel.HARD: {"size": 6},
        }
        params = config_map[difficulty]
        return cls(difficulty=difficulty, **params)


class NonogramConfig(GameConfig):
    """Configuration for Nonogram game."""

    size: int = Field(ge=5, le=10, description="Grid size (NxN)")

    @classmethod
    def from_difficulty(cls, difficulty: DifficultyLevel) -> "NonogramConfig":
        """Create config from difficulty level."""
        config_map = {
            DifficultyLevel.EASY: {"size": 5},
            DifficultyLevel.MEDIUM: {"size": 7},
            DifficultyLevel.HARD: {"size": 10},
        }
        params = config_map[difficulty]
        return cls(difficulty=difficulty, **params)


class MastermindConfig(GameConfig):
    """Configuration for Mastermind game."""

    code_length: int = Field(ge=3, le=6, description="Length of the secret code")
    num_colors: int = Field(ge=4, le=8, description="Number of available colors")
    max_guesses: int = Field(ge=8, le=15, description="Maximum number of guesses allowed")

    @classmethod
    def from_difficulty(cls, difficulty: DifficultyLevel) -> "MastermindConfig":
        """Create config from difficulty level."""
        config_map = {
            DifficultyLevel.EASY: {"code_length": 4, "num_colors": 6, "max_guesses": 12},
            DifficultyLevel.MEDIUM: {"code_length": 5, "num_colors": 7, "max_guesses": 12},
            DifficultyLevel.HARD: {"code_length": 6, "num_colors": 8, "max_guesses": 15},
        }
        params = config_map[difficulty]
        return cls(difficulty=difficulty, **params)


class LogicGridConfig(GameConfig):
    """Configuration for Logic Grid game."""

    num_people: int = Field(ge=3, le=5, description="Number of people")
    num_attributes: int = Field(ge=3, le=5, description="Number of attributes per category")

    @classmethod
    def from_difficulty(cls, difficulty: DifficultyLevel) -> "LogicGridConfig":
        """Create config from difficulty level."""
        config_map = {
            DifficultyLevel.EASY: {"num_people": 3, "num_attributes": 3},
            DifficultyLevel.MEDIUM: {"num_people": 4, "num_attributes": 4},
            DifficultyLevel.HARD: {"num_people": 5, "num_attributes": 5},
        }
        params = config_map[difficulty]
        return cls(difficulty=difficulty, **params)


class SlitherlinkConfig(GameConfig):
    """Configuration for Slitherlink game."""

    size: int = Field(ge=5, le=10, description="Grid size (NxN)")

    @classmethod
    def from_difficulty(cls, difficulty: DifficultyLevel) -> "SlitherlinkConfig":
        """Create config from difficulty level."""
        config_map = {
            DifficultyLevel.EASY: {"size": 5},
            DifficultyLevel.MEDIUM: {"size": 7},
            DifficultyLevel.HARD: {"size": 10},
        }
        params = config_map[difficulty]
        return cls(difficulty=difficulty, **params)


class KillerSudokuConfig(GameConfig):
    """Configuration for Killer Sudoku game."""

    num_cages: int = Field(ge=15, le=35, description="Number of cages")

    @classmethod
    def from_difficulty(cls, difficulty: DifficultyLevel) -> "KillerSudokuConfig":
        """Create config from difficulty level."""
        config_map = {
            DifficultyLevel.EASY: {"num_cages": 20},
            DifficultyLevel.MEDIUM: {"num_cages": 25},
            DifficultyLevel.HARD: {"num_cages": 30},
        }
        params = config_map[difficulty]
        return cls(difficulty=difficulty, **params)


class HidatoConfig(GameConfig):
    """Configuration for Hidato game."""

    size: int = Field(ge=5, le=9, description="Grid size (NxN)")
    num_clues: int = Field(ge=2, description="Number of clue numbers to reveal")

    @classmethod
    def from_difficulty(cls, difficulty: DifficultyLevel) -> "HidatoConfig":
        """Create config from difficulty level."""
        config_map = {
            DifficultyLevel.EASY: {"size": 5, "num_clues": 8},
            DifficultyLevel.MEDIUM: {"size": 7, "num_clues": 12},
            DifficultyLevel.HARD: {"size": 9, "num_clues": 15},
        }
        params = config_map[difficulty]
        return cls(difficulty=difficulty, **params)


class TentsConfig(GameConfig):
    """Configuration for Tents and Trees game."""

    size: int = Field(ge=6, le=10, description="Grid size (NxN)")
    num_trees: int = Field(ge=4, description="Number of tree-tent pairs")

    @classmethod
    def from_difficulty(cls, difficulty: DifficultyLevel) -> "TentsConfig":
        """Create config from difficulty level."""
        config_map = {
            DifficultyLevel.EASY: {"size": 6, "num_trees": 6},
            DifficultyLevel.MEDIUM: {"size": 8, "num_trees": 10},
            DifficultyLevel.HARD: {"size": 10, "num_trees": 15},
        }
        params = config_map[difficulty]
        return cls(difficulty=difficulty, **params)


class FillominoConfig(GameConfig):
    """Configuration for Fillomino game."""

    size: int = Field(ge=6, le=10, description="Grid size (NxN)")
    num_clues: int = Field(ge=4, description="Number of clue numbers to reveal")

    @classmethod
    def from_difficulty(cls, difficulty: DifficultyLevel) -> "FillominoConfig":
        """Create config from difficulty level."""
        config_map = {
            DifficultyLevel.EASY: {"size": 6, "num_clues": 8},
            DifficultyLevel.MEDIUM: {"size": 8, "num_clues": 10},
            DifficultyLevel.HARD: {"size": 10, "num_clues": 12},
        }
        params = config_map[difficulty]
        return cls(difficulty=difficulty, **params)


class StarBattleConfig(GameConfig):
    """Configuration for Star Battle game."""

    size: int = Field(ge=6, le=10, description="Grid size (NxN)")
    stars_per_row: int = Field(ge=1, le=2, description="Number of stars per row/column/region")

    @classmethod
    def from_difficulty(cls, difficulty: DifficultyLevel) -> "StarBattleConfig":
        """Create config from difficulty level."""
        config_map = {
            DifficultyLevel.EASY: {"size": 6, "stars_per_row": 1},
            DifficultyLevel.MEDIUM: {"size": 8, "stars_per_row": 2},
            DifficultyLevel.HARD: {"size": 10, "stars_per_row": 2},
        }
        params = config_map[difficulty]
        return cls(difficulty=difficulty, **params)


class SokobanConfig(GameConfig):
    """Configuration for Sokoban game."""

    size: int = Field(ge=6, le=10, description="Grid size (NxN)")
    num_boxes: int = Field(ge=2, le=6, description="Number of boxes to push")

    @classmethod
    def from_difficulty(cls, difficulty: DifficultyLevel) -> "SokobanConfig":
        """Create config from difficulty level."""
        config_map = {
            DifficultyLevel.EASY: {"size": 6, "num_boxes": 2},
            DifficultyLevel.MEDIUM: {"size": 8, "num_boxes": 3},
            DifficultyLevel.HARD: {"size": 10, "num_boxes": 4},
        }
        params = config_map[difficulty]
        return cls(difficulty=difficulty, **params)
