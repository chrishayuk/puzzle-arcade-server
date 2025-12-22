"""Tests for game configuration classes."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


# Import all config classes
from chuk_puzzles_gym.games.binary.config import BinaryConfig
from chuk_puzzles_gym.games.bridges.config import BridgesConfig
from chuk_puzzles_gym.games.einstein.config import EinsteinConfig
from chuk_puzzles_gym.games.fillomino.config import FillominoConfig
from chuk_puzzles_gym.games.hidato.config import HidatoConfig
from chuk_puzzles_gym.games.hitori.config import HitoriConfig
from chuk_puzzles_gym.games.shikaku.config import ShikakuConfig
from chuk_puzzles_gym.games.star_battle.config import StarBattleConfig
from chuk_puzzles_gym.models import DifficultyLevel


class TestBinaryConfig:
    """Tests for BinaryConfig."""

    def test_from_difficulty_easy(self):
        """Test creating config from easy difficulty."""
        config = BinaryConfig.from_difficulty(DifficultyLevel.EASY)
        assert config.difficulty == DifficultyLevel.EASY
        assert config.size == 6

    def test_from_difficulty_medium(self):
        """Test creating config from medium difficulty."""
        config = BinaryConfig.from_difficulty(DifficultyLevel.MEDIUM)
        assert config.difficulty == DifficultyLevel.MEDIUM
        assert config.size == 8

    def test_from_difficulty_hard(self):
        """Test creating config from hard difficulty."""
        config = BinaryConfig.from_difficulty(DifficultyLevel.HARD)
        assert config.difficulty == DifficultyLevel.HARD
        assert config.size == 10


class TestBridgesConfig:
    """Tests for BridgesConfig."""

    def test_from_difficulty_easy(self):
        """Test creating config from easy difficulty."""
        config = BridgesConfig.from_difficulty(DifficultyLevel.EASY)
        assert config.difficulty == DifficultyLevel.EASY
        assert config.size == 5
        assert config.num_islands == 5

    def test_from_difficulty_medium(self):
        """Test creating config from medium difficulty."""
        config = BridgesConfig.from_difficulty(DifficultyLevel.MEDIUM)
        assert config.difficulty == DifficultyLevel.MEDIUM
        assert config.size == 7
        assert config.num_islands == 8

    def test_from_difficulty_hard(self):
        """Test creating config from hard difficulty."""
        config = BridgesConfig.from_difficulty(DifficultyLevel.HARD)
        assert config.difficulty == DifficultyLevel.HARD
        assert config.size == 9
        assert config.num_islands == 12


class TestEinsteinConfig:
    """Tests for EinsteinConfig."""

    def test_from_difficulty_easy(self):
        """Test creating config from easy difficulty."""
        config = EinsteinConfig.from_difficulty(DifficultyLevel.EASY)
        assert config.difficulty == DifficultyLevel.EASY
        assert config.num_clues == 12

    def test_from_difficulty_medium(self):
        """Test creating config from medium difficulty."""
        config = EinsteinConfig.from_difficulty(DifficultyLevel.MEDIUM)
        assert config.difficulty == DifficultyLevel.MEDIUM
        assert config.num_clues == 10

    def test_from_difficulty_hard(self):
        """Test creating config from hard difficulty."""
        config = EinsteinConfig.from_difficulty(DifficultyLevel.HARD)
        assert config.difficulty == DifficultyLevel.HARD
        assert config.num_clues == 8


class TestFillominoConfig:
    """Tests for FillominoConfig."""

    def test_from_difficulty_easy(self):
        """Test creating config from easy difficulty."""
        config = FillominoConfig.from_difficulty(DifficultyLevel.EASY)
        assert config.difficulty == DifficultyLevel.EASY
        assert config.size == 6

    def test_from_difficulty_medium(self):
        """Test creating config from medium difficulty."""
        config = FillominoConfig.from_difficulty(DifficultyLevel.MEDIUM)
        assert config.difficulty == DifficultyLevel.MEDIUM
        assert config.size == 8

    def test_from_difficulty_hard(self):
        """Test creating config from hard difficulty."""
        config = FillominoConfig.from_difficulty(DifficultyLevel.HARD)
        assert config.difficulty == DifficultyLevel.HARD
        assert config.size == 10


class TestHidatoConfig:
    """Tests for HidatoConfig."""

    def test_from_difficulty_easy(self):
        """Test creating config from easy difficulty."""
        config = HidatoConfig.from_difficulty(DifficultyLevel.EASY)
        assert config.difficulty == DifficultyLevel.EASY
        assert config.size == 5

    def test_from_difficulty_medium(self):
        """Test creating config from medium difficulty."""
        config = HidatoConfig.from_difficulty(DifficultyLevel.MEDIUM)
        assert config.difficulty == DifficultyLevel.MEDIUM
        assert config.size == 7

    def test_from_difficulty_hard(self):
        """Test creating config from hard difficulty."""
        config = HidatoConfig.from_difficulty(DifficultyLevel.HARD)
        assert config.difficulty == DifficultyLevel.HARD
        assert config.size == 9


class TestHitoriConfig:
    """Tests for HitoriConfig."""

    def test_from_difficulty_easy(self):
        """Test creating config from easy difficulty."""
        config = HitoriConfig.from_difficulty(DifficultyLevel.EASY)
        assert config.difficulty == DifficultyLevel.EASY
        assert config.size == 4

    def test_from_difficulty_medium(self):
        """Test creating config from medium difficulty."""
        config = HitoriConfig.from_difficulty(DifficultyLevel.MEDIUM)
        assert config.difficulty == DifficultyLevel.MEDIUM
        assert config.size == 5

    def test_from_difficulty_hard(self):
        """Test creating config from hard difficulty."""
        config = HitoriConfig.from_difficulty(DifficultyLevel.HARD)
        assert config.difficulty == DifficultyLevel.HARD
        assert config.size == 6


class TestShikakuConfig:
    """Tests for ShikakuConfig."""

    def test_from_difficulty_easy(self):
        """Test creating config from easy difficulty."""
        config = ShikakuConfig.from_difficulty(DifficultyLevel.EASY)
        assert config.difficulty == DifficultyLevel.EASY
        assert config.size == 5
        assert config.num_clues == 5

    def test_from_difficulty_medium(self):
        """Test creating config from medium difficulty."""
        config = ShikakuConfig.from_difficulty(DifficultyLevel.MEDIUM)
        assert config.difficulty == DifficultyLevel.MEDIUM
        assert config.size == 7
        assert config.num_clues == 7

    def test_from_difficulty_hard(self):
        """Test creating config from hard difficulty."""
        config = ShikakuConfig.from_difficulty(DifficultyLevel.HARD)
        assert config.difficulty == DifficultyLevel.HARD
        assert config.size == 9
        assert config.num_clues == 10


class TestStarBattleConfig:
    """Tests for StarBattleConfig."""

    def test_from_difficulty_easy(self):
        """Test creating config from easy difficulty."""
        config = StarBattleConfig.from_difficulty(DifficultyLevel.EASY)
        assert config.difficulty == DifficultyLevel.EASY
        assert config.size == 6

    def test_from_difficulty_medium(self):
        """Test creating config from medium difficulty."""
        config = StarBattleConfig.from_difficulty(DifficultyLevel.MEDIUM)
        assert config.difficulty == DifficultyLevel.MEDIUM
        assert config.size == 8

    def test_from_difficulty_hard(self):
        """Test creating config from hard difficulty."""
        config = StarBattleConfig.from_difficulty(DifficultyLevel.HARD)
        assert config.difficulty == DifficultyLevel.HARD
        assert config.size == 10
