"""Base Pydantic models for the Puzzle Arcade server."""

from pydantic import BaseModel, ConfigDict, Field


class GridPosition(BaseModel):
    """A position on a game grid (1-indexed for user-facing coordinates)."""

    row: int = Field(ge=1, description="Row number (1-indexed)")
    col: int = Field(ge=1, description="Column number (1-indexed)")

    def to_zero_indexed(self) -> tuple[int, int]:
        """Convert to 0-indexed coordinates for internal use."""
        return (self.row - 1, self.col - 1)

    @classmethod
    def from_zero_indexed(cls, row: int, col: int) -> "GridPosition":
        """Create from 0-indexed coordinates."""
        return cls(row=row + 1, col=col + 1)


class MoveResult(BaseModel):
    """Result of a game move or action."""

    model_config = ConfigDict(frozen=True)  # Immutable result

    success: bool = Field(description="Whether the move was successful")
    message: str = Field(description="Message to display to the user")
    state_changed: bool = Field(default=False, description="Whether game state was modified")
    game_over: bool = Field(default=False, description="Whether the game has ended")
