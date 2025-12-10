"""Tests for base Pydantic models."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pydantic import ValidationError

from puzzle_arcade_server.models.base import GridPosition, MoveResult


class TestGridPosition:
    """Test suite for GridPosition model."""

    def test_creation(self):
        """Test GridPosition creation."""
        pos = GridPosition(row=1, col=1)
        assert pos.row == 1
        assert pos.col == 1

    def test_to_zero_indexed(self):
        """Test conversion to 0-indexed coordinates."""
        pos = GridPosition(row=3, col=5)
        zero_row, zero_col = pos.to_zero_indexed()
        assert zero_row == 2
        assert zero_col == 4

    def test_from_zero_indexed(self):
        """Test creation from 0-indexed coordinates."""
        pos = GridPosition.from_zero_indexed(2, 4)
        assert pos.row == 3
        assert pos.col == 5

    def test_roundtrip_conversion(self):
        """Test that conversion back and forth preserves values."""
        original = GridPosition(row=7, col=9)
        zero_row, zero_col = original.to_zero_indexed()
        back = GridPosition.from_zero_indexed(zero_row, zero_col)
        assert back.row == original.row
        assert back.col == original.col


class TestMoveResult:
    """Test suite for MoveResult model."""

    def test_success_result(self):
        """Test successful move result."""
        result = MoveResult(success=True, message="Move successful")
        assert result.success is True
        assert result.message == "Move successful"
        assert result.state_changed is False
        assert result.game_over is False

    def test_failure_result(self):
        """Test failed move result."""
        result = MoveResult(success=False, message="Invalid move")
        assert result.success is False
        assert result.message == "Invalid move"

    def test_state_changed(self):
        """Test move result with state change."""
        result = MoveResult(success=True, message="Placed number", state_changed=True)
        assert result.state_changed is True

    def test_game_over(self):
        """Test move result with game over."""
        result = MoveResult(success=True, message="You won!", game_over=True)
        assert result.game_over is True

    def test_immutability(self):
        """Test that MoveResult is immutable (frozen)."""
        result = MoveResult(success=True, message="Test")
        try:
            result.success = False
            msg = "Should not be able to modify frozen model"
            raise AssertionError(msg)
        except (ValidationError, TypeError, AttributeError):
            # Expected - model is frozen
            pass
