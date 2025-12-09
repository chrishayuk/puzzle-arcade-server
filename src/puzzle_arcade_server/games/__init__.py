"""Puzzle game implementations."""

from .binary import BinaryPuzzleGame
from .futoshiki import FutoshikiGame
from .kakuro import KakuroGame
from .kenken import KenKenGame
from .killer_sudoku import KillerSudokuGame
from .lights_out import LightsOutGame
from .logic_grid import LogicGridGame
from .mastermind import MastermindGame
from .nonogram import NonogramGame
from .slitherlink import SlitherlinkGame
from .sudoku import SudokuGame

# Registry of available games
AVAILABLE_GAMES = {
    "sudoku": SudokuGame,
    "kenken": KenKenGame,
    "kakuro": KakuroGame,
    "binary": BinaryPuzzleGame,
    "futoshiki": FutoshikiGame,
    "nonogram": NonogramGame,
    "logic": LogicGridGame,
    "killer": KillerSudokuGame,
    "lights": LightsOutGame,
    "mastermind": MastermindGame,
    "slither": SlitherlinkGame,
}

__all__ = [
    "SudokuGame",
    "KenKenGame",
    "KakuroGame",
    "BinaryPuzzleGame",
    "FutoshikiGame",
    "NonogramGame",
    "LogicGridGame",
    "KillerSudokuGame",
    "LightsOutGame",
    "MastermindGame",
    "SlitherlinkGame",
    "AVAILABLE_GAMES",
]
