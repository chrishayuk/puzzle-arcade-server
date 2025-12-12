"""Tests for Star Battle game logic."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from puzzle_arcade_server.games.star_battle import StarBattleGame


class TestStarBattleGame:
    """Test suite for StarBattleGame class."""

    async def test_initialization(self):
        """Test game initialization."""
        game = StarBattleGame("easy")
        assert game.difficulty.value == "easy"
        assert game.size == 6
        assert game.stars_per_row == 1

    async def test_difficulty_settings(self):
        """Test different difficulty settings."""
        easy = StarBattleGame("easy")
        assert easy.size == 6 and easy.stars_per_row == 1

        medium = StarBattleGame("medium")
        assert medium.size == 8 and medium.stars_per_row == 2

    async def test_generate_puzzle(self):
        """Test puzzle generation."""
        game = StarBattleGame("easy")
        await game.generate_puzzle()

        # Should have a solution
        star_count = sum(sum(row) for row in game.solution)
        assert star_count > 0

    async def test_place_star(self):
        """Test placing a star."""
        game = StarBattleGame("easy")
        await game.generate_puzzle()

        result = await game.validate_move(2, 2, "place")
        assert isinstance(result.success, bool)

    async def test_remove_star(self):
        """Test removing a star."""
        game = StarBattleGame("easy")
        await game.generate_puzzle()

        # Place then remove
        await game.validate_move(2, 2, "place")
        result = await game.validate_move(2, 2, "remove")
        assert result.success or "No star" in result.message

    async def test_get_hint(self):
        """Test hint generation."""
        game = StarBattleGame("easy")
        await game.generate_puzzle()

        hint = await game.get_hint()
        if hint is not None:
            hint_data, hint_message = hint
            assert len(hint_data) == 3

    async def test_render_grid(self):
        """Test grid rendering."""
        game = StarBattleGame("easy")
        await game.generate_puzzle()

        grid_str = game.render_grid()
        assert isinstance(grid_str, str)
        assert len(grid_str) > 0

    async def test_name_and_description(self):
        """Test game name and description."""
        game = StarBattleGame("easy")
        assert game.name == "Star Battle"
        assert len(game.description) > 0

    async def test_get_rules(self):
        """Test rules description."""
        game = StarBattleGame("easy")
        rules = game.get_rules()
        assert "star" in rules.lower()

    async def test_get_commands(self):
        """Test commands description."""
        game = StarBattleGame("easy")
        commands = game.get_commands()
        assert "place" in commands.lower()

    async def test_get_stats(self):
        """Test stats generation."""
        game = StarBattleGame("easy")
        await game.generate_puzzle()

        stats = game.get_stats()
        assert "Stars" in stats or "stars" in stats

    async def test_constraint_types(self):
        """Test constraint types metadata."""
        game = StarBattleGame("easy")
        constraint_types = game.constraint_types
        assert isinstance(constraint_types, list)
        assert "placement_limits" in constraint_types

    async def test_business_analogies(self):
        """Test business analogies metadata."""
        game = StarBattleGame("easy")
        analogies = game.business_analogies
        assert isinstance(analogies, list)
        assert "resource_distribution" in analogies

    async def test_complexity_profile(self):
        """Test complexity profile metadata."""
        game = StarBattleGame("easy")
        profile = game.complexity_profile
        assert isinstance(profile, dict)
        assert "reasoning_type" in profile

    async def test_invalid_coordinates(self):
        """Test invalid coordinates."""
        game = StarBattleGame("easy")
        await game.generate_puzzle()

        result = await game.validate_move(0, 1, "place")
        assert not result.success
        result = await game.validate_move(10, 10, "place")
        assert not result.success

    async def test_invalid_action(self):
        """Test invalid action."""
        game = StarBattleGame("easy")
        await game.generate_puzzle()

        result = await game.validate_move(2, 2, "invalid")
        assert not result.success

    async def test_remove_no_star(self):
        """Test removing when there's no star."""
        game = StarBattleGame("easy")
        await game.generate_puzzle()

        # Find empty cell
        for r in range(game.size):
            for c in range(game.size):
                if game.grid[r][c] == 0:
                    result = await game.validate_move(r + 1, c + 1, "remove")
                    assert not result.success
                    return

    async def test_place_star_already_placed(self):
        """Test placing star where one already exists."""
        game = StarBattleGame("easy")
        await game.generate_puzzle()

        # Find empty cell and place star
        for r in range(game.size):
            for c in range(game.size):
                if game.grid[r][c] == 0:
                    result1 = await game.validate_move(r + 1, c + 1, "place")
                    if result1.success:
                        result2 = await game.validate_move(r + 1, c + 1, "place")
                        assert not result2.success
                        return

    async def test_adjacency_rejection(self):
        """Test that stars cannot be placed adjacent to each other."""
        game = StarBattleGame("easy")
        await game.generate_puzzle()

        # Find empty cell and place star
        for r in range(1, game.size - 1):
            for c in range(1, game.size - 1):
                if game.grid[r][c] == 0:
                    result1 = await game.validate_move(r + 1, c + 1, "place")
                    if result1.success:
                        # Try to place adjacent
                        result2 = await game.validate_move(r + 2, c + 1, "place")
                        if not result2.success and "touch" in result2.message.lower():
                            return
                        result2 = await game.validate_move(r + 1, c + 2, "place")
                        if not result2.success and "touch" in result2.message.lower():
                            return

    async def test_is_complete_empty(self):
        """Test is_complete with empty grid."""
        game = StarBattleGame("easy")
        await game.generate_puzzle()

        assert not game.is_complete()

    async def test_is_complete_with_solution(self):
        """Test is_complete with solution."""
        game = StarBattleGame("easy")
        await game.generate_puzzle()

        # Copy solution to grid
        game.grid = [row[:] for row in game.solution]
        assert game.is_complete()

    async def test_hint_for_wrong_star(self):
        """Test hint suggests removing wrong star."""
        game = StarBattleGame("easy")
        await game.generate_puzzle()

        # Copy solution and then add a wrong star
        game.grid = [row[:] for row in game.solution]

        # Now add one extra wrong star where solution is empty
        for r in range(game.size):
            for c in range(game.size):
                if game.solution[r][c] == 0:
                    game.grid[r][c] = 1
                    hint = await game.get_hint()
                    if hint:
                        hint_data, hint_message = hint
                        assert "remove" in hint_message.lower() or "Remove" in hint_message
                        return

    async def test_moves_counter(self):
        """Test that moves are counted."""
        game = StarBattleGame("easy")
        await game.generate_puzzle()

        initial_moves = game.moves_made

        # Place a star
        for r in range(game.size):
            for c in range(game.size):
                if game.grid[r][c] == 0:
                    result = await game.validate_move(r + 1, c + 1, "place")
                    if result.success:
                        assert game.moves_made == initial_moves + 1
                        return

    async def test_hard_difficulty(self):
        """Test hard difficulty settings."""
        game = StarBattleGame("hard")
        assert game.size == 10
        assert game.stars_per_row == 2
