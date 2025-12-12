"""Tests for Hidato (Number Snake) game logic."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from puzzle_arcade_server.games.hidato import HidatoGame


class TestHidatoGame:
    """Test suite for HidatoGame class."""

    async def test_initialization(self):
        """Test game initialization."""
        game = HidatoGame("easy")
        assert game.difficulty.value == "easy"
        assert game.size == 5
        assert game.total_numbers == 25

    async def test_difficulty_sizes(self):
        """Test different difficulty sizes."""
        for difficulty, expected_size in [("easy", 5), ("medium", 7), ("hard", 9)]:
            game = HidatoGame(difficulty)
            assert game.size == expected_size
            assert game.total_numbers == expected_size * expected_size

    async def test_generate_puzzle(self):
        """Test puzzle generation."""
        game = HidatoGame("easy")
        await game.generate_puzzle()

        # Solution should contain numbers 1 to total_numbers
        solution_numbers = set()
        for row in game.solution:
            for cell in row:
                solution_numbers.add(cell)

        assert solution_numbers == set(range(1, game.total_numbers + 1))

        # Grid should have some clues
        clue_count = sum(1 for row in game.grid for cell in row if cell != 0)
        assert clue_count >= 2  # At least first and last

    async def test_place_number(self):
        """Test placing a number."""
        game = HidatoGame("easy")
        await game.generate_puzzle()

        # Find an empty cell
        for r in range(game.size):
            for c in range(game.size):
                if game.grid[r][c] == 0:
                    # Try placing the correct solution value
                    correct_value = game.solution[r][c]
                    result = await game.validate_move(r + 1, c + 1, correct_value)
                    assert result.success
                    assert game.grid[r][c] == correct_value
                    return

    async def test_clear_cell(self):
        """Test clearing a cell."""
        game = HidatoGame("easy")
        await game.generate_puzzle()

        # Find an empty cell and place a number
        for r in range(game.size):
            for c in range(game.size):
                if game.grid[r][c] == 0:
                    await game.validate_move(r + 1, c + 1, 5)
                    # Now clear it
                    result = await game.validate_move(r + 1, c + 1, 0)
                    assert result.success
                    assert game.grid[r][c] == 0
                    return

    async def test_cannot_modify_initial_cells(self):
        """Test that initial clue cells cannot be modified."""
        game = HidatoGame("easy")
        await game.generate_puzzle()

        # Find an initial clue cell
        for r in range(game.size):
            for c in range(game.size):
                if game.initial_grid[r][c] != 0:
                    result = await game.validate_move(r + 1, c + 1, 999)
                    assert not result.success
                    assert "Cannot modify initial clue" in result.message
                    return

    async def test_invalid_coordinates(self):
        """Test invalid coordinate handling."""
        game = HidatoGame("easy")
        await game.generate_puzzle()

        result = await game.validate_move(0, 1, 1)
        assert not result.success

        result = await game.validate_move(game.size + 1, 1, 1)
        assert not result.success

    async def test_invalid_number_range(self):
        """Test invalid number range."""
        game = HidatoGame("easy")
        await game.generate_puzzle()

        result = await game.validate_move(1, 1, game.total_numbers + 1)
        assert not result.success

        result = await game.validate_move(1, 1, -1)
        assert not result.success

    async def test_duplicate_number_rejection(self):
        """Test that duplicate numbers are rejected."""
        game = HidatoGame("easy")
        await game.generate_puzzle()

        # Find the first clue number
        first_num = None
        for row in game.grid:
            for cell in row:
                if cell != 0:
                    first_num = cell
                    break
            if first_num:
                break

        # Try to place the same number elsewhere
        for r in range(game.size):
            for c in range(game.size):
                if game.grid[r][c] == 0:
                    result = await game.validate_move(r + 1, c + 1, first_num)
                    assert not result.success
                    assert "already used" in result.message
                    return

    async def test_get_hint(self):
        """Test hint generation."""
        game = HidatoGame("easy")
        await game.generate_puzzle()

        hint = await game.get_hint()
        assert hint is not None

        hint_data, hint_message = hint
        row, col, num = hint_data
        assert 1 <= row <= game.size
        assert 1 <= col <= game.size
        assert 1 <= num <= game.total_numbers

    async def test_render_grid(self):
        """Test grid rendering."""
        game = HidatoGame("easy")
        await game.generate_puzzle()

        grid_str = game.render_grid()
        assert isinstance(grid_str, str)
        assert len(grid_str) > 0
        assert "." in grid_str  # Empty cells

    async def test_name_and_description(self):
        """Test game name and description."""
        game = HidatoGame("easy")
        assert game.name == "Hidato"
        assert len(game.description) > 0

    async def test_get_rules(self):
        """Test rules description."""
        game = HidatoGame("easy")
        rules = game.get_rules()
        assert "consecutive" in rules.lower()
        assert "adjacent" in rules.lower()

    async def test_get_commands(self):
        """Test commands description."""
        game = HidatoGame("easy")
        commands = game.get_commands()
        assert "place" in commands.lower()
        assert "hint" in commands.lower()

    async def test_get_stats(self):
        """Test stats generation."""
        game = HidatoGame("easy")
        await game.generate_puzzle()

        stats = game.get_stats()
        assert "Moves" in stats or "moves" in stats
        assert "Filled" in stats or "filled" in stats

    async def test_moves_counter(self):
        """Test that moves are counted."""
        game = HidatoGame("easy")
        await game.generate_puzzle()

        initial_moves = game.moves_made
        assert initial_moves == 0

        # Find an empty cell and place the correct number from solution
        for r in range(game.size):
            for c in range(game.size):
                if game.grid[r][c] == 0:
                    correct_num = game.solution[r][c]
                    result = await game.validate_move(r + 1, c + 1, correct_num)
                    if result.success:
                        assert game.moves_made == initial_moves + 1
                        return

    async def test_get_neighbors(self):
        """Test neighbor calculation."""
        game = HidatoGame("easy")

        # Corner cell
        neighbors = game._get_neighbors(0, 0)
        assert len(neighbors) == 3  # Corner has 3 neighbors

        # Edge cell
        neighbors = game._get_neighbors(0, 1)
        assert len(neighbors) == 5  # Edge has 5 neighbors

        # Center cell (if grid is large enough)
        if game.size > 2:
            neighbors = game._get_neighbors(1, 1)
            assert len(neighbors) == 8  # Center has 8 neighbors

    async def test_solution_path_adjacency(self):
        """Test that solution forms a valid path."""
        game = HidatoGame("easy")
        await game.generate_puzzle()

        # Check that each consecutive number is adjacent
        for num in range(1, game.total_numbers):
            pos_current = None
            pos_next = None

            # Find positions of num and num+1
            for r in range(game.size):
                for c in range(game.size):
                    if game.solution[r][c] == num:
                        pos_current = (r, c)
                    if game.solution[r][c] == num + 1:
                        pos_next = (r, c)

            assert pos_current is not None
            assert pos_next is not None

            # Check they're adjacent (including diagonally)
            neighbors = game._get_neighbors(pos_current[0], pos_current[1])
            assert pos_next in neighbors

    async def test_is_complete_empty_grid(self):
        """Test completion check on empty grid."""
        game = HidatoGame("easy")
        await game.generate_puzzle()

        assert not game.is_complete()

    async def test_is_complete_with_solution(self):
        """Test completion check with correct solution."""
        game = HidatoGame("easy")
        await game.generate_puzzle()

        # Copy solution to grid
        game.grid = [row[:] for row in game.solution]

        assert game.is_complete()

    async def test_constraint_types(self):
        """Test constraint types metadata."""
        game = HidatoGame("easy")
        constraint_types = game.constraint_types
        assert isinstance(constraint_types, list)
        assert len(constraint_types) > 0
        assert all(isinstance(ct, str) for ct in constraint_types)
        assert "sequential_adjacency" in constraint_types
        assert "hamiltonian_path" in constraint_types

    async def test_business_analogies(self):
        """Test business analogies metadata."""
        game = HidatoGame("easy")
        analogies = game.business_analogies
        assert isinstance(analogies, list)
        assert len(analogies) > 0
        assert all(isinstance(a, str) for a in analogies)
        assert "route_optimization" in analogies

    async def test_complexity_profile(self):
        """Test complexity profile metadata."""
        game = HidatoGame("easy")
        profile = game.complexity_profile
        assert isinstance(profile, dict)
        assert "reasoning_type" in profile
        assert "search_space" in profile
        assert "constraint_density" in profile
        assert profile["reasoning_type"] == "deductive"
