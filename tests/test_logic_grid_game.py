"""Tests for Logic Grid game logic."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from puzzle_arcade_server.games.logic_grid import LogicGridGame


class TestLogicGridGame:
    """Test suite for LogicGridGame class."""

    async def test_initialization(self):
        """Test game initialization."""
        game = LogicGridGame("easy")
        assert game.difficulty == "easy"
        assert game.num_people == 3

    async def test_difficulty_sizes(self):
        """Test different difficulty sizes."""
        for difficulty, expected_size in [("easy", 3), ("medium", 4), ("hard", 5)]:
            game = LogicGridGame(difficulty)
            assert game.num_people == expected_size

    async def test_generate_puzzle(self):
        """Test puzzle generation."""
        game = LogicGridGame("easy")
        await game.generate_puzzle()

        # Check solution generated
        assert len(game.solution) == game.num_people

        # Check clues generated
        assert len(game.clues) > 0

        # Check categories
        assert hasattr(game.categories, "person")
        assert len(game.categories.person) == game.num_people

    async def test_mark_connection(self):
        """Test marking connections."""
        game = LogicGridGame("easy")
        await game.generate_puzzle()

        # Get a valid connection from solution
        person = list(game.solution.keys())[0]
        color = game.solution[person].color

        result = await game.validate_move("person", person, "color", color, True)
        success, _msg = result.success, result.message
        assert success

    async def test_mark_exclusion(self):
        """Test marking exclusions."""
        game = LogicGridGame("easy")
        await game.generate_puzzle()

        # Mark an exclusion
        person = list(game.solution.keys())[0]
        # Get a color that doesn't belong to this person
        wrong_color = None
        for c in game.categories.color:
            if c != game.solution[person].color:
                wrong_color = c
                break

        if wrong_color:
            result = await game.validate_move("person", person, "color", wrong_color, False)
            success, _msg = result.success, result.message
            assert success

    async def test_is_complete(self):
        """Test completion check."""
        game = LogicGridGame("easy")
        await game.generate_puzzle()

        assert not game.is_complete()

        # Mark all correct connections
        for person, attrs in game.solution.items():
            await game.validate_move("person", person, "color", attrs.color, True)
            await game.validate_move("person", person, "pet", attrs.pet, True)
            await game.validate_move("person", person, "drink", attrs.drink, True)

        assert game.is_complete()

    async def test_get_hint(self):
        """Test hint generation."""
        game = LogicGridGame("easy")
        await game.generate_puzzle()

        hint = await game.get_hint()
        if hint:
            hint_data, hint_message = hint
            assert isinstance(hint_message, str)
            assert len(hint_message) > 0

    async def test_render_grid(self):
        """Test grid rendering."""
        game = LogicGridGame("easy")
        await game.generate_puzzle()

        grid_str = game.render_grid()
        assert isinstance(grid_str, str)
        assert "CLUES:" in grid_str.upper()

    async def test_name_and_description(self):
        """Test name and description."""
        game = LogicGridGame("easy")
        assert game.name == "Logic Grid"
        assert len(game.description) > 0

    async def test_get_rules(self):
        """Test rules retrieval."""
        game = LogicGridGame("easy")
        rules = game.get_rules()
        assert "LOGIC GRID" in rules.upper()

    async def test_get_commands(self):
        """Test commands retrieval."""
        game = LogicGridGame("easy")
        commands = game.get_commands()
        assert "connect" in commands.lower()
        assert "exclude" in commands.lower()

    async def test_invalid_category(self):
        """Test invalid category handling."""
        game = LogicGridGame("easy")
        await game.generate_puzzle()

        result = await game.validate_move("invalid", "val1", "person", "Alice", True)
        success, msg = result.success, result.message
        assert not success
        assert "Invalid category" in msg

    async def test_same_category(self):
        """Test same category handling."""
        game = LogicGridGame("easy")
        await game.generate_puzzle()

        result = await game.validate_move("person", "Alice", "person", "Bob", True)
        success, msg = result.success, result.message
        assert not success
        assert "same category" in msg.lower()

    async def test_invalid_value(self):
        """Test invalid value handling."""
        game = LogicGridGame("easy")
        await game.generate_puzzle()

        result = await game.validate_move("person", "InvalidName", "color", "Red", True)
        success, msg = result.success, result.message
        assert not success
        assert "Invalid" in msg

    async def test_constraint_types(self):
        """Test constraint types metadata."""
        game = LogicGridGame("easy")
        constraint_types = game.constraint_types
        assert isinstance(constraint_types, list)
        assert len(constraint_types) > 0
        assert all(isinstance(ct, str) for ct in constraint_types)

    async def test_business_analogies(self):
        """Test business analogies metadata."""
        game = LogicGridGame("easy")
        analogies = game.business_analogies
        assert isinstance(analogies, list)
        assert len(analogies) > 0
        assert all(isinstance(a, str) for a in analogies)

    async def test_complexity_profile(self):
        """Test complexity profile metadata."""
        game = LogicGridGame("easy")
        profile = game.complexity_profile
        assert isinstance(profile, dict)
        assert "reasoning_type" in profile
        assert "search_space" in profile
        assert "constraint_density" in profile
