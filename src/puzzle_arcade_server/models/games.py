"""Game-specific Pydantic models."""

from pydantic import BaseModel, ConfigDict, Field

from .enums import ArithmeticOperation


class Task(BaseModel):
    """A task in the Scheduler game."""

    model_config = ConfigDict(frozen=False)  # Allow mutation for game state

    id: int = Field(ge=0, description="Task ID")
    name: str = Field(min_length=1, description="Task name")
    duration: int = Field(gt=0, description="Task duration in time units")
    dependencies: list[int] = Field(default_factory=list, description="List of task IDs this task depends on")


class Item(BaseModel):
    """An item in the Knapsack game."""

    model_config = ConfigDict(frozen=True)  # Items don't change once created

    name: str = Field(min_length=1, description="Item name")
    weight: int = Field(gt=0, description="Item weight")
    value: int = Field(gt=0, description="Item value")


class Cage(BaseModel):
    """A cage in KenKen game."""

    model_config = ConfigDict(frozen=True)  # Cages don't change once created

    cells: list[tuple[int, int]] = Field(min_length=1, description="List of cell coordinates (0-indexed)")
    operation: ArithmeticOperation | None = Field(description="Arithmetic operation for the cage")
    target: int = Field(description="Target value for the cage")


class HouseAssignment(BaseModel):
    """Attribute assignments for a house in Einstein's Puzzle."""

    model_config = ConfigDict(frozen=False)  # Allow mutation during gameplay

    color: str | None = None
    nationality: str | None = None
    drink: str | None = None
    smoke: str | None = None
    pet: str | None = None

    def is_complete(self) -> bool:
        """Check if all attributes are assigned."""
        return all(
            [
                self.color is not None,
                self.nationality is not None,
                self.drink is not None,
                self.smoke is not None,
                self.pet is not None,
            ]
        )

    def get_attribute(self, attr_type: str) -> str | None:
        """Get attribute value by type."""
        return getattr(self, attr_type.lower(), None)

    def set_attribute(self, attr_type: str, value: str) -> None:
        """Set attribute value by type."""
        setattr(self, attr_type.lower(), value)


class LogicGridCategories(BaseModel):
    """Categories for Logic Grid puzzle."""

    model_config = ConfigDict(frozen=True)

    person: list[str]
    color: list[str]
    pet: list[str]
    drink: list[str]


class PersonAttributes(BaseModel):
    """Attributes for a person in Logic Grid puzzle."""

    model_config = ConfigDict(frozen=False)

    color: str
    pet: str
    drink: str
