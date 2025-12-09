"""Tests for Killer Sudoku puzzle game."""

from puzzle_arcade_server.games.killer_sudoku import KillerSudokuGame


class TestKillerSudokuGame:
    """Test suite for Killer Sudoku game."""

    def test_initialization(self):
        """Test game initialization."""
        game = KillerSudokuGame("easy")
        assert game.difficulty == "easy"
        assert game.size == 9
        assert game.name == "Killer Sudoku"
        assert "Kakuro" in game.description

    def test_generate_puzzle(self):
        """Test puzzle generation."""
        game = KillerSudokuGame("easy")
        game.generate_puzzle()

        assert game.game_started is True
        assert game.moves_made == 0
        assert len(game.grid) == 9
        assert len(game.grid[0]) == 9
        assert len(game.solution) == 9
        assert len(game.cages) > 0

        # Grid should start empty
        assert all(cell == 0 for row in game.grid for cell in row)

    def test_generate_cages(self):
        """Test cage generation."""
        game = KillerSudokuGame("easy")
        game.solution = [[1, 2, 3, 4, 5, 6, 7, 8, 9] for _ in range(9)]
        game._generate_cages()

        # Should have cages
        assert len(game.cages) > 0

        # Each cage should have cells and target sum
        for cells, target_sum in game.cages:
            assert len(cells) >= 1  # At least 1 cell per cage
            assert target_sum > 0

            # Target sum should match solution
            actual_sum = sum(game.solution[r][c] for r, c in cells)
            assert actual_sum == target_sum

    def test_is_valid_move_row_conflict(self):
        """Test move validation with row conflict."""
        game = KillerSudokuGame("easy")
        game.generate_puzzle()

        game.grid[0][0] = 5
        assert game.is_valid_move(0, 1, 5) is False  # Same row

    def test_is_valid_move_column_conflict(self):
        """Test move validation with column conflict."""
        game = KillerSudokuGame("easy")
        game.generate_puzzle()

        game.grid[0][0] = 5
        assert game.is_valid_move(1, 0, 5) is False  # Same column

    def test_is_valid_move_box_conflict(self):
        """Test move validation with 3x3 box conflict."""
        game = KillerSudokuGame("easy")
        game.generate_puzzle()

        game.grid[0][0] = 5
        assert game.is_valid_move(1, 1, 5) is False  # Same 3x3 box

    def test_is_valid_move_success(self):
        """Test successful move validation."""
        game = KillerSudokuGame("easy")
        game.generate_puzzle()

        game.grid[0][0] = 5
        assert game.is_valid_move(0, 4, 1) is True  # Different box, row, col

    def test_check_cage_constraints_duplicate(self):
        """Test cage constraint with duplicate values."""
        game = KillerSudokuGame("easy")
        game.cages = [
            ([(0, 0), (0, 1), (0, 2)], 6),  # Target sum 6
        ]
        game.grid = [[0 for _ in range(9)] for _ in range(9)]

        # Place duplicate in cage
        game.grid[0][0] = 2
        game.grid[0][1] = 2

        assert game._check_cage_constraints(game.grid, 0, 1) is False

    def test_check_cage_constraints_exceed_sum(self):
        """Test cage constraint when sum is exceeded."""
        game = KillerSudokuGame("easy")
        game.cages = [
            ([(0, 0), (0, 1)], 5),  # Target sum 5
        ]
        game.grid = [[0 for _ in range(9)] for _ in range(9)]

        # Place values that exceed target
        game.grid[0][0] = 3
        game.grid[0][1] = 3  # Total would be 6 > 5

        assert game._check_cage_constraints(game.grid, 0, 1) is False

    def test_check_cage_constraints_correct(self):
        """Test cage constraint with correct values."""
        game = KillerSudokuGame("easy")
        game.cages = [
            ([(0, 0), (0, 1)], 5),  # Target sum 5
        ]
        game.grid = [[0 for _ in range(9)] for _ in range(9)]

        # Place values that match target
        game.grid[0][0] = 2
        game.grid[0][1] = 3  # Total 5

        assert game._check_cage_constraints(game.grid, 0, 1) is True

    def test_validate_move_success(self):
        """Test successful move placement."""
        game = KillerSudokuGame("easy")
        game.generate_puzzle()

        success, message = game.validate_move(1, 1, 5)
        assert success is True
        assert "successfully" in message.lower()

    def test_validate_move_invalid_coordinates(self):
        """Test move with invalid coordinates."""
        game = KillerSudokuGame("easy")
        game.generate_puzzle()

        success, message = game.validate_move(0, 0, 5)
        assert success is False
        assert "Invalid coordinates" in message

        success, message = game.validate_move(10, 10, 5)
        assert success is False
        assert "Invalid coordinates" in message

    def test_validate_move_clear_cell(self):
        """Test clearing a cell."""
        game = KillerSudokuGame("easy")
        game.generate_puzzle()

        game.grid[0][0] = 5
        success, message = game.validate_move(1, 1, 0)
        assert success is True
        assert "cleared" in message.lower()

    def test_validate_move_invalid_number(self):
        """Test move with invalid number."""
        game = KillerSudokuGame("easy")
        game.generate_puzzle()

        success, message = game.validate_move(1, 1, 10)
        assert success is False
        assert "Invalid number" in message

    def test_is_complete_empty_grid(self):
        """Test completion check with empty grid."""
        game = KillerSudokuGame("easy")
        game.generate_puzzle()

        assert game.is_complete() is False

    def test_is_complete_filled_correct(self):
        """Test completion check with correctly filled grid."""
        game = KillerSudokuGame("easy")
        # Create a simple valid grid
        game.grid = [[0 for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                game.grid[row][col] = (row * 3 + row // 3 + col) % 9 + 1

        # Create cages that match this grid (no duplicates within cages)
        game.cages = [
            ([(0, 0), (0, 1)], game.grid[0][0] + game.grid[0][1]),
            ([(1, 0), (1, 1)], game.grid[1][0] + game.grid[1][1]),
            ([(2, 0), (2, 1)], game.grid[2][0] + game.grid[2][1]),
        ]
        # Add more cages to cover all cells
        for row in range(9):
            for col in range(2, 9):
                game.cages.append(([(row, col)], game.grid[row][col]))

        assert game.is_complete() is True

    def test_is_complete_cage_wrong_sum(self):
        """Test completion check with wrong cage sum."""
        game = KillerSudokuGame("easy")
        game.cages = [
            ([(0, 0), (0, 1)], 5),
        ]
        game.grid = [[1, 2, 3, 4, 5, 6, 7, 8, 9] for _ in range(9)]

        # This grid has 1+2=3, but cage expects 5
        assert game.is_complete() is False

    def test_get_hint(self):
        """Test hint generation."""
        game = KillerSudokuGame("easy")
        game.generate_puzzle()

        hint_data, hint_message = game.get_hint()
        assert hint_data is not None
        assert len(hint_data) == 3  # (row, col, num)
        assert "placing" in hint_message.lower()

    def test_get_hint_solved(self):
        """Test hint when puzzle is solved."""
        game = KillerSudokuGame("easy")
        game.generate_puzzle()
        game.grid = [row[:] for row in game.solution]

        result = game.get_hint()
        assert result is None

    def test_render_grid(self):
        """Test grid rendering."""
        game = KillerSudokuGame("easy")
        game.generate_puzzle()

        grid_str = game.render_grid()
        assert "|" in grid_str
        assert "+" in grid_str
        assert "Cages" in grid_str

    def test_get_rules(self):
        """Test rules retrieval."""
        game = KillerSudokuGame("easy")
        rules = game.get_rules()

        assert "KILLER SUDOKU" in rules
        assert "9×9" in rules
        assert "cage" in rules.lower()

    def test_get_commands(self):
        """Test commands retrieval."""
        game = KillerSudokuGame("easy")
        commands = game.get_commands()

        assert "place" in commands.lower()
        assert "clear" in commands.lower()
        assert "hint" in commands.lower()

    def test_get_stats(self):
        """Test statistics retrieval."""
        game = KillerSudokuGame("easy")
        game.generate_puzzle()

        stats = game.get_stats()
        assert "Moves made:" in stats
        assert "Empty cells:" in stats
        assert "Total cages:" in stats

    def test_solve(self):
        """Test puzzle solving."""
        game = KillerSudokuGame("easy")
        game.grid = [[0 for _ in range(9)] for _ in range(9)]

        # Simple valid grid
        for row in range(9):
            for col in range(9):
                game.grid[row][col] = (row * 3 + row // 3 + col) % 9 + 1

        # Create simple cages that match
        game.cages = [
            ([(0, 0), (0, 1)], game.grid[0][0] + game.grid[0][1]),
        ]

        # Grid should already be a valid solution
        test_grid = [row[:] for row in game.grid]
        assert game.solve(test_grid) is True

    def test_moves_counter(self):
        """Test that moves are counted correctly."""
        game = KillerSudokuGame("easy")
        game.generate_puzzle()

        initial_moves = game.moves_made
        game.validate_move(1, 1, 5)
        assert game.moves_made == initial_moves + 1

    def test_all_cells_covered_by_cages(self):
        """Test that all cells are covered by exactly one cage."""
        game = KillerSudokuGame("easy")
        game.generate_puzzle()

        # Count cells in cages
        covered_cells = set()
        for cells, _target_sum in game.cages:
            for cell in cells:
                assert cell not in covered_cells, "Cell covered by multiple cages"
                covered_cells.add(cell)

        # All cells should be covered
        assert len(covered_cells) == 81

    def test_cage_sizes(self):
        """Test that cages are reasonable sizes."""
        game = KillerSudokuGame("easy")
        game.generate_puzzle()

        for cells, _target_sum in game.cages:
            assert 1 <= len(cells), "Cage must have at least 1 cell"
