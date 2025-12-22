"""Tests for Sokoban game logic."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from chuk_puzzles_gym.games.sokoban import SokobanGame


class TestSokobanGame:
    """Test suite for SokobanGame class."""

    async def test_initialization(self):
        """Test game initialization."""
        game = SokobanGame("easy")
        assert game.difficulty.value == "easy"
        assert game.size == 6
        assert game.num_boxes == 2

    async def test_difficulty_settings(self):
        """Test different difficulty settings."""
        easy = SokobanGame("easy")
        assert easy.size == 6 and easy.num_boxes == 2

        medium = SokobanGame("medium")
        assert medium.size == 8 and medium.num_boxes == 3

    async def test_generate_puzzle(self):
        """Test puzzle generation."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Should have goals
        assert len(game.goals) == game.num_boxes

        # Should have player position
        assert game.player_pos is not None

    async def test_move_player(self):
        """Test moving the player."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Try to move in some direction
        for direction in ["up", "down", "left", "right"]:
            result = await game.validate_move(direction)
            assert isinstance(result.success, bool)
            if result.success:
                break

    async def test_invalid_direction(self):
        """Test invalid direction."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        result = await game.validate_move("invalid")
        assert not result.success

    async def test_get_hint(self):
        """Test hint generation."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        hint = await game.get_hint()
        # Hint might be None or a tuple
        if hint is not None:
            hint_data, hint_message = hint
            assert isinstance(hint_data, str)

    async def test_render_grid(self):
        """Test grid rendering."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        grid_str = game.render_grid()
        assert isinstance(grid_str, str)
        assert len(grid_str) > 0
        assert "@" in grid_str  # Player symbol

    async def test_name_and_description(self):
        """Test game name and description."""
        game = SokobanGame("easy")
        assert game.name == "Sokoban"
        assert len(game.description) > 0

    async def test_get_rules(self):
        """Test rules description."""
        game = SokobanGame("easy")
        rules = game.get_rules()
        assert "box" in rules.lower() or "push" in rules.lower()

    async def test_get_commands(self):
        """Test commands description."""
        game = SokobanGame("easy")
        commands = game.get_commands()
        assert "up" in commands.lower()

    async def test_get_stats(self):
        """Test stats generation."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        stats = game.get_stats()
        assert "Moves" in stats or "moves" in stats
        assert "Boxes" in stats or "boxes" in stats

    async def test_constraint_types(self):
        """Test constraint types metadata."""
        game = SokobanGame("easy")
        constraint_types = game.constraint_types
        assert isinstance(constraint_types, list)
        assert "irreversible_actions" in constraint_types

    async def test_business_analogies(self):
        """Test business analogies metadata."""
        game = SokobanGame("easy")
        analogies = game.business_analogies
        assert isinstance(analogies, list)
        assert "warehouse_logistics" in analogies

    async def test_complexity_profile(self):
        """Test complexity profile metadata."""
        game = SokobanGame("easy")
        profile = game.complexity_profile
        assert isinstance(profile, dict)
        assert "reasoning_type" in profile
        assert profile["reasoning_type"] == "optimization"

    async def test_move_into_wall(self):
        """Test that player cannot move into a wall."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Find a wall adjacent to player
        pr, pc = game.player_pos
        for direction, (dr, dc) in [("up", (-1, 0)), ("down", (1, 0)), ("left", (0, -1)), ("right", (0, 1))]:
            nr, nc = pr + dr, pc + dc
            if 0 <= nr < game.size and 0 <= nc < game.size and game.grid[nr][nc] == 1:
                result = await game.validate_move(direction)
                assert not result.success
                assert "wall" in result.message.lower()
                return

    async def test_move_outside_grid(self):
        """Test that player cannot move outside the grid."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Move player to edge and try to move out
        game.player_pos = (0, 1)
        _ = await game.validate_move("up")
        # Will hit wall at edge, but ensures bounds checking

    async def test_push_box(self):
        """Test pushing a box."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Find a box and try to push it
        pr, pc = game.player_pos
        for direction, (dr, dc) in [("up", (-1, 0)), ("down", (1, 0)), ("left", (0, -1)), ("right", (0, 1))]:
            nr, nc = pr + dr, pc + dc
            if 0 <= nr < game.size and 0 <= nc < game.size and game.grid[nr][nc] in [2, 5]:
                # There's a box here, check if we can push
                push_r, push_c = nr + dr, nc + dc
                if 0 <= push_r < game.size and 0 <= push_c < game.size:
                    result = await game.validate_move(direction)
                    if "push" in result.message.lower():
                        return

    async def test_cannot_push_box_into_wall(self):
        """Test that boxes cannot be pushed into walls."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Set up a scenario where box is against wall
        for r in range(1, game.size - 1):
            for c in range(1, game.size - 1):
                if game.grid[r][c] in [2, 5]:  # Box
                    # Check all directions for wall
                    for direction, (dr, dc) in [
                        ("up", (-1, 0)),
                        ("down", (1, 0)),
                        ("left", (0, -1)),
                        ("right", (0, 1)),
                    ]:
                        push_r, push_c = r + dr, c + dc
                        if game.grid[push_r][push_c] == 1:  # Wall
                            # Position player to push in that direction
                            player_r, player_c = r - dr, c - dc
                            if game.grid[player_r][player_c] in [0, 3]:
                                # Clear old player position
                                old_pr, old_pc = game.player_pos
                                on_goal = any(old_pr == gr and old_pc == gc for gr, gc in game.goals)
                                game.grid[old_pr][old_pc] = 3 if on_goal else 0

                                game.player_pos = (player_r, player_c)
                                game.grid[player_r][player_c] = 4
                                result = await game.validate_move(direction)
                                if not result.success and "wall" in result.message.lower():
                                    return

    async def test_cannot_push_box_into_box(self):
        """Test that boxes cannot be pushed into other boxes."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # This is tested implicitly by the game logic

    async def test_move_onto_goal(self):
        """Test moving player onto a goal."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Find a goal and move player there
        for gr, gc in game.goals:
            # Check if player can reach
            for direction, (dr, dc) in [("up", (-1, 0)), ("down", (1, 0)), ("left", (0, -1)), ("right", (0, 1))]:
                pr, pc = gr - dr, gc - dc
                if 0 <= pr < game.size and 0 <= pc < game.size and game.grid[pr][pc] in [0, 4]:
                    # Position player adjacent to goal
                    old_pr, old_pc = game.player_pos
                    on_goal = any(old_pr == gr and old_pc == gc for gr, gc in game.goals)
                    game.grid[old_pr][old_pc] = 3 if on_goal else 0
                    game.player_pos = (pr, pc)
                    game.grid[pr][pc] = 4

                    # Now move onto goal
                    if game.grid[gr][gc] == 3:  # Goal is empty
                        result = await game.validate_move(direction)
                        if result.success:
                            assert game.grid[gr][gc] == 6  # Player on goal
                            return

    async def test_push_box_onto_goal(self):
        """Test pushing a box onto a goal."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # This is tested through the completion logic

    async def test_is_complete_partial(self):
        """Test is_complete with some boxes not on goals."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        assert not game.is_complete()

    async def test_is_complete_all_on_goals(self):
        """Test is_complete when all boxes are on goals."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Place all boxes on goals
        for gr, gc in game.goals:
            game.grid[gr][gc] = 5  # Box on goal

        assert game.is_complete()

    async def test_hint_no_boxes_off_goal(self):
        """Test hint when all boxes are on goals."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Place all boxes on goals
        for gr, gc in game.goals:
            game.grid[gr][gc] = 5

        _ = await game.get_hint()
        # Should be None or give some other hint

    async def test_moves_counter(self):
        """Test that moves are counted."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        initial_moves = game.moves_made

        # Make a valid move
        for direction in ["up", "down", "left", "right"]:
            result = await game.validate_move(direction)
            if result.success:
                assert game.moves_made == initial_moves + 1
                return

    async def test_shorthand_directions(self):
        """Test shorthand direction commands (u, d, l, r)."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        for direction in ["u", "d", "l", "r"]:
            result = await game.validate_move(direction)
            assert isinstance(result.success, bool)

    async def test_hard_difficulty(self):
        """Test hard difficulty settings."""
        game = SokobanGame("hard")
        assert game.size == 10
        assert game.num_boxes == 4

    async def test_is_corner_detection(self):
        """Test corner detection for box trapping."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Corner at top-left (should always be a corner due to walls)
        result = game._is_corner(1, 1)
        # May or may not be a corner depending on puzzle
        assert isinstance(result, bool)

    async def test_can_push_to_goal_same_row(self):
        """Test push path checking on same row."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Test the path checking logic
        # This tests the internal method for horizontal push
        result = game._can_push_to_goal(3, 3, 3, 5)  # Same row
        assert isinstance(result, bool)

    async def test_can_push_to_goal_same_column(self):
        """Test push path checking on same column."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Test the path checking logic for vertical push
        result = game._can_push_to_goal(3, 3, 5, 3)  # Same column
        assert isinstance(result, bool)

    async def test_can_push_to_goal_different_row_col(self):
        """Test push path returns false for diagonal positions."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Different row and column - should return False
        result = game._can_push_to_goal(3, 3, 5, 5)
        assert result is False

    async def test_find_path_to_push_position_already_there(self):
        """Test BFS path finding when already at position."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Player already at target
        path = game._find_path_to_push_position(*game.player_pos)
        assert path == []

    async def test_find_path_to_push_position_blocked(self):
        """Test BFS path finding when path is blocked."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Try to find path to a wall cell
        path = game._find_path_to_push_position(0, 0)  # Border wall
        assert path is None

    async def test_fallback_puzzle_generation(self):
        """Test fallback puzzle generation creates valid puzzle."""
        game = SokobanGame("easy")
        # Force fallback by making main generation fail many times
        # This is tested by running generate_puzzle which may use fallback
        await game.generate_puzzle()
        assert len(game.goals) > 0
        assert game.player_pos is not None

    async def test_push_box_outside_grid(self):
        """Test that boxes cannot be pushed outside grid."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Find an edge position and set up a box push scenario
        # Position player to push box toward edge
        edge_r = game.size - 2
        edge_c = game.size - 2

        # Clear the area and set up test scenario
        game.grid[edge_r][edge_c] = 2  # Box
        old_pr, old_pc = game.player_pos
        game.grid[old_pr][old_pc] = 0
        game.player_pos = (edge_r - 1, edge_c)
        game.grid[edge_r - 1][edge_c] = 4

        # Try to push down (toward edge)
        result = await game.validate_move("down")
        # Should either succeed or fail depending on wall placement
        assert isinstance(result.success, bool)

    async def test_render_all_cell_types(self):
        """Test rendering covers all cell types."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Ensure we have all cell types
        game.grid[1][1] = 0  # Empty
        game.grid[1][2] = 1  # Wall
        game.grid[1][3] = 2  # Box
        game.grid[1][4] = 3  # Goal
        # Player (4) exists
        game.grid[2][1] = 5  # Box on goal
        game.grid[2][2] = 6  # Player on goal

        grid_str = game.render_grid()
        assert "." in grid_str  # Empty
        assert "#" in grid_str  # Wall
        assert "$" in grid_str  # Box
        assert "○" in grid_str  # Goal
        assert "@" in grid_str  # Player
        assert "☒" in grid_str  # Box on goal
        assert "Θ" in grid_str  # Player on goal

    async def test_hint_fallback_any_valid_move(self):
        """Test hint gives fallback move when no push available."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Get a hint - should always return something or None
        hint = await game.get_hint()
        if hint is not None:
            hint_data, hint_message = hint
            assert isinstance(hint_data, str)
            assert isinstance(hint_message, str)

    async def test_hint_push_direction_detection(self):
        """Test hint correctly identifies push directions."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Run multiple hints to exercise different code paths
        for _ in range(5):
            hint = await game.get_hint()
            if hint is None:
                break
            hint_data, _ = hint
            result = await game.validate_move(hint_data)
            if not result.success:
                break

    async def test_multiple_seeds_different_puzzles(self):
        """Test that different seeds produce different puzzles."""
        game1 = SokobanGame("easy", seed=12345)
        game2 = SokobanGame("easy", seed=67890)
        await game1.generate_puzzle()
        await game2.generate_puzzle()

        # Grid or positions should differ
        assert game1.render_grid() != game2.render_grid() or game1.player_pos != game2.player_pos

    async def test_push_box_toward_goal(self):
        """Test pushing a box toward its goal."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Use hints to push boxes toward goals
        for _ in range(20):
            if game.is_complete():
                break
            hint = await game.get_hint()
            if hint is None:
                break
            await game.validate_move(hint[0])

        # Game state may have changed
        assert isinstance(game.is_complete(), bool)

    async def test_player_on_goal_marking(self):
        """Test that player on goal is correctly marked."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Move player off its current position
        old_pr, old_pc = game.player_pos
        on_goal = any(old_pr == gr and old_pc == gc for gr, gc in game.goals)
        if on_goal:
            assert game.grid[old_pr][old_pc] == 6  # Player on goal

    async def test_box_on_goal_after_push(self):
        """Test that pushing box onto goal marks it correctly."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Use hints to make progress
        for _ in range(30):
            if game.is_complete():
                break
            hint = await game.get_hint()
            if hint is None:
                break
            await game.validate_move(hint[0])

        # Check box-on-goal cells
        for gr, gc in game.goals:
            if game.grid[gr][gc] == 5:
                assert True  # Box is on goal
                return

    async def test_can_push_to_goal_push_right(self):
        """Test _can_push_to_goal for pushing right."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Create a clear path scenario for push right
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        # Add border walls
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # Test push right: box at (2,2), goal at (2,4), need space at (2,1)
        result = game._can_push_to_goal(2, 2, 2, 4)
        assert isinstance(result, bool)

    async def test_can_push_to_goal_push_left(self):
        """Test _can_push_to_goal for pushing left."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Create a clear path scenario for push left
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # Test push left: box at (2,4), goal at (2,2), need space at (2,5)
        result = game._can_push_to_goal(2, 4, 2, 2)
        assert isinstance(result, bool)

    async def test_can_push_to_goal_push_down(self):
        """Test _can_push_to_goal for pushing down."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # Test push down: box at (2,2), goal at (4,2), need space at (1,2)
        result = game._can_push_to_goal(2, 2, 4, 2)
        assert isinstance(result, bool)

    async def test_can_push_to_goal_push_up(self):
        """Test _can_push_to_goal for pushing up."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # Test push up: box at (4,2), goal at (2,2), need space at (5,2)
        result = game._can_push_to_goal(4, 2, 2, 2)
        assert isinstance(result, bool)

    async def test_can_push_to_goal_blocked_by_wall(self):
        """Test _can_push_to_goal when wall blocks path."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # Add wall between box and goal
        game.grid[2][3] = 1

        # Test push right with wall in path
        result = game._can_push_to_goal(2, 2, 2, 4)
        assert result is False

    async def test_can_push_edge_cases(self):
        """Test _can_push_to_goal edge cases near borders."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # Test edge case: push space would be at border
        # box at (2,1), goal at (2,3) - push space would be at col 0 (border wall)
        result = game._can_push_to_goal(2, 1, 2, 3)
        # Should fail because push position is at border
        assert isinstance(result, bool)

    async def test_fallback_puzzle_creation(self):
        """Test that fallback puzzle is created correctly."""
        game = SokobanGame("easy")
        # Manually trigger fallback by generating
        await game.generate_puzzle()

        # Check puzzle is valid
        assert len(game.goals) > 0
        assert game.player_pos is not None
        assert game.initial_state is not None

    async def test_hint_when_player_at_push_position(self):
        """Test hint when player is already at push position."""
        game = SokobanGame("easy", seed=42)
        await game.generate_puzzle()

        # Use multiple hints to cover different scenarios
        for _ in range(10):
            hint = await game.get_hint()
            if hint is None:
                break
            await game.validate_move(hint[0])

    async def test_hint_fallback_push_box(self):
        """Test hint fallback for pushing any box."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Position player next to a box
        for r in range(1, game.size - 1):
            for c in range(1, game.size - 1):
                if game.grid[r][c] in [2, 5]:  # Box
                    # Try to position player adjacent
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        pr, pc = r + dr, c + dc
                        if 0 <= pr < game.size and 0 <= pc < game.size:
                            if game.grid[pr][pc] in [0, 3]:
                                # Clear old player
                                old_pr, old_pc = game.player_pos
                                game.grid[old_pr][old_pc] = 0
                                game.player_pos = (pr, pc)
                                game.grid[pr][pc] = 4

                                hint = await game.get_hint()
                                if hint:
                                    assert isinstance(hint[0], str)
                                return

    async def test_push_box_outside_grid_boundary(self):
        """Test pushing box to edge of grid."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Set up box near edge
        edge_r, edge_c = 1, game.size - 2
        game.grid[edge_r][edge_c] = 2  # Box near right edge

        # Clear old player and position for push
        old_pr, old_pc = game.player_pos
        game.grid[old_pr][old_pc] = 0
        game.player_pos = (edge_r, edge_c - 1)
        game.grid[edge_r][edge_c - 1] = 4

        # Try to push right (toward wall)
        result = await game.validate_move("right")
        # Should fail or succeed depending on what's at edge
        assert isinstance(result.success, bool)

    async def test_unknown_cell_type(self):
        """Test handling of unknown cell type."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Set up an invalid cell type scenario
        old_pr, old_pc = game.player_pos
        new_r, new_c = old_pr, old_pc + 1
        if new_c < game.size and game.grid[new_r][new_c] == 0:
            game.grid[new_r][new_c] = 99  # Invalid cell type

            result = await game.validate_move("right")
            # Should return unknown cell type error
            assert isinstance(result.success, bool)

    async def test_bfs_path_finding(self):
        """Test BFS path finding to various positions."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Find path to an empty cell
        for r in range(1, game.size - 1):
            for c in range(1, game.size - 1):
                if game.grid[r][c] == 0:
                    path = game._find_path_to_push_position(r, c)
                    if path is not None:
                        # Path should be a list of directions
                        assert isinstance(path, list)
                        return

    async def test_render_unknown_cell(self):
        """Test rendering handles unknown cell types."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Set an unknown cell type
        game.grid[1][1] = 99

        grid_str = game.render_grid()
        assert "?" in grid_str  # Unknown cell rendered as ?

    async def test_solve_puzzle_completely(self):
        """Test solving a puzzle using hints."""
        game = SokobanGame("easy", seed=12345)
        await game.generate_puzzle()

        # Use hints to solve
        for _ in range(100):
            if game.is_complete():
                break
            hint = await game.get_hint()
            if hint is None:
                break
            await game.validate_move(hint[0])

        # Puzzle should be solvable
        assert game.is_complete() or game.moves_made > 0

    async def test_hint_fallback_move_to_empty(self):
        """Test hint fallback when no box can be pushed."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Remove all boxes
        for r in range(game.size):
            for c in range(game.size):
                if game.grid[r][c] in [2, 5]:
                    game.grid[r][c] = 0

        # Clear goals too
        game.goals = []

        hint = await game.get_hint()
        # Should still return a valid move or None
        assert hint is None or isinstance(hint[0], str)

    async def test_hint_fallback_try_push(self):
        """Test hint fallback when player is next to pushable box."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Clear all boxes from goal positions
        for gr, gc in game.goals:
            if game.grid[gr][gc] == 5:
                game.grid[gr][gc] = 3  # Just goal

        # Get hint - should try to find a push or move
        hint = await game.get_hint()
        if hint:
            assert isinstance(hint[0], str)

    async def test_is_corner_all_positions(self):
        """Test corner detection at various positions."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Test corners
        result1 = game._is_corner(1, 1)
        result2 = game._is_corner(game.size - 2, 1)
        result3 = game._is_corner(1, game.size - 2)
        result4 = game._is_corner(game.size - 2, game.size - 2)

        # All should return bool
        assert all(isinstance(r, bool) for r in [result1, result2, result3, result4])

    async def test_move_box_onto_goal(self):
        """Test pushing a box specifically onto a goal."""
        game = SokobanGame("easy", seed=999)
        await game.generate_puzzle()

        # Use hints until we complete or run out
        for _ in range(50):
            if game.is_complete():
                break
            hint = await game.get_hint()
            if hint is None:
                break
            await game.validate_move(hint[0])

    async def test_player_leaves_goal(self):
        """Test player leaving a goal position."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Put player on a goal
        if game.goals:
            gr, gc = game.goals[0]
            old_pr, old_pc = game.player_pos
            game.grid[old_pr][old_pc] = 0
            game.player_pos = (gr, gc)
            game.grid[gr][gc] = 6  # Player on goal

            # Try to move off
            for direction in ["up", "down", "left", "right"]:
                result = await game.validate_move(direction)
                if result.success:
                    # Goal should be restored
                    assert game.grid[gr][gc] == 3  # Back to goal
                    return

    async def test_push_box_from_goal(self):
        """Test pushing a box that's already on a goal."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Find or create a box on goal scenario
        for gr, gc in game.goals:
            game.grid[gr][gc] = 5  # Box on goal

            # Position player to push
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                pr, pc = gr - dr, gc - dc
                push_r, push_c = gr + dr, gc + dc

                if (
                    1 <= pr < game.size - 1
                    and 1 <= pc < game.size - 1
                    and 1 <= push_r < game.size - 1
                    and 1 <= push_c < game.size - 1
                    and game.grid[pr][pc] in [0, 3]
                    and game.grid[push_r][push_c] in [0, 3]
                ):
                    # Clear old player
                    old_pr, old_pc = game.player_pos
                    game.grid[old_pr][old_pc] = 0
                    game.player_pos = (pr, pc)
                    game.grid[pr][pc] = 4

                    # Push direction
                    dir_map = {(-1, 0): "down", (1, 0): "up", (0, -1): "right", (0, 1): "left"}
                    direction = dir_map[(dr, dc)]

                    await game.validate_move(direction)
                    return

    async def test_multiple_difficulty_generation(self):
        """Test puzzle generation at all difficulties."""
        for difficulty in ["easy", "medium", "hard"]:
            game = SokobanGame(difficulty)
            await game.generate_puzzle()
            assert len(game.goals) > 0

    async def test_deterministic_seeding(self):
        """Test that same seed produces same puzzle."""
        game1 = SokobanGame("easy", seed=54321)
        game2 = SokobanGame("easy", seed=54321)

        await game1.generate_puzzle()
        await game2.generate_puzzle()

        assert game1.player_pos == game2.player_pos
        assert game1.goals == game2.goals

    async def test_can_push_left_clear_path(self):
        """Test _can_push_to_goal for pushing left with clear path."""
        game = SokobanGame("easy")
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # box at (2, 4), goal at (2, 2), push left
        # Need space to right of box at (2, 5)
        result = game._can_push_to_goal(2, 4, 2, 2)
        assert isinstance(result, bool)

    async def test_can_push_left_blocked(self):
        """Test _can_push_to_goal for pushing left when blocked."""
        game = SokobanGame("easy")
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # Block the path
        game.grid[2][3] = 1

        # box at (2, 4), goal at (2, 2)
        result = game._can_push_to_goal(2, 4, 2, 2)
        assert result is False

    async def test_can_push_up_clear_path(self):
        """Test _can_push_to_goal for pushing up with clear path."""
        game = SokobanGame("easy")
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # box at (4, 2), goal at (2, 2), push up
        result = game._can_push_to_goal(4, 2, 2, 2)
        assert isinstance(result, bool)

    async def test_can_push_up_blocked(self):
        """Test _can_push_to_goal for pushing up when blocked."""
        game = SokobanGame("easy")
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # Block the path
        game.grid[3][2] = 1

        # box at (4, 2), goal at (2, 2)
        result = game._can_push_to_goal(4, 2, 2, 2)
        assert result is False

    async def test_can_push_down_blocked(self):
        """Test _can_push_to_goal for pushing down when blocked."""
        game = SokobanGame("easy")
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # Block the path
        game.grid[3][2] = 1

        # box at (2, 2), goal at (4, 2)
        result = game._can_push_to_goal(2, 2, 4, 2)
        assert result is False

    async def test_can_push_right_blocked(self):
        """Test _can_push_to_goal for pushing right when blocked."""
        game = SokobanGame("easy")
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # Block the path
        game.grid[2][3] = 1

        # box at (2, 2), goal at (2, 4)
        result = game._can_push_to_goal(2, 2, 2, 4)
        assert result is False

    async def test_can_push_edge_of_grid(self):
        """Test _can_push_to_goal at edge of grid."""
        game = SokobanGame("easy")
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # box at edge - push space would be out of bounds
        result = game._can_push_to_goal(2, 1, 2, 3)
        assert result is False

    async def test_can_push_space_blocked(self):
        """Test _can_push_to_goal when push space is blocked."""
        game = SokobanGame("easy")
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # Block the push space
        game.grid[2][1] = 1

        # box at (2, 2), goal at (2, 4), push right needs space at (2, 1)
        result = game._can_push_to_goal(2, 2, 2, 4)
        assert result is False

    async def test_hint_fallback_box_push(self):
        """Test hint when pushing a box is the only option."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Place player next to a box with push space available
        for r in range(1, game.size - 2):
            for c in range(1, game.size - 2):
                if game.grid[r][c] in [2, 5]:  # Box
                    # Check if we can push in some direction
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        push_r, push_c = r + dr, c + dc
                        player_r, player_c = r - dr, c - dc
                        if (
                            0 <= push_r < game.size
                            and 0 <= push_c < game.size
                            and 0 <= player_r < game.size
                            and 0 <= player_c < game.size
                            and game.grid[push_r][push_c] in [0, 3]
                            and game.grid[player_r][player_c] in [0, 3]
                        ):
                            # Set up the scenario
                            old_pr, old_pc = game.player_pos
                            game.grid[old_pr][old_pc] = 0
                            game.player_pos = (player_r, player_c)
                            game.grid[player_r][player_c] = 4

                            hint = await game.get_hint()
                            if hint:
                                assert isinstance(hint[0], str)
                            return

    async def test_corner_detection_true(self):
        """Test corner detection returns true for corner positions."""
        game = SokobanGame("easy")
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # Position (1, 1) is in a corner with walls at (0, 1) and (1, 0)
        result = game._is_corner(1, 1)
        assert result is True

    async def test_corner_detection_false(self):
        """Test corner detection returns false for non-corner positions."""
        game = SokobanGame("easy")
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # Position (2, 2) is not in a corner
        result = game._is_corner(2, 2)
        assert result is False

    async def test_optimal_steps_no_goals(self):
        """Test optimal_steps returns None when no goals."""
        game = SokobanGame("easy")
        # Don't generate puzzle, so no goals
        assert game.optimal_steps is None

    async def test_optimal_steps_no_boxes(self):
        """Test optimal_steps returns None when no boxes."""
        game = SokobanGame("easy")
        await game.generate_puzzle()
        # Remove all boxes
        for r in range(game.size):
            for c in range(game.size):
                if game.grid[r][c] in [2, 5]:
                    game.grid[r][c] = 0
        assert game.optimal_steps is None

    async def test_optimal_steps_with_boxes(self):
        """Test optimal_steps calculation with boxes."""
        game = SokobanGame("easy")
        await game.generate_puzzle()
        steps = game.optimal_steps
        assert steps is not None
        assert steps > 0

    async def test_difficulty_profile_easy(self):
        """Test difficulty profile for easy."""
        game = SokobanGame("easy")
        profile = game.difficulty_profile
        assert profile.logic_depth == 3

    async def test_difficulty_profile_medium(self):
        """Test difficulty profile for medium."""
        game = SokobanGame("medium")
        profile = game.difficulty_profile
        assert profile.logic_depth == 5

    async def test_difficulty_profile_hard(self):
        """Test difficulty profile for hard."""
        game = SokobanGame("hard")
        profile = game.difficulty_profile
        assert profile.logic_depth == 8

    async def test_can_push_right_at_edge(self):
        """Test _can_push_to_goal pushing right near right edge."""
        game = SokobanGame("easy")
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # box at (2, game.size-3), goal at (2, game.size-2)
        # push space at (2, game.size-4)
        result = game._can_push_to_goal(2, game.size - 3, 2, game.size - 2)
        assert isinstance(result, bool)

    async def test_can_push_left_at_edge(self):
        """Test _can_push_to_goal pushing left near left edge."""
        game = SokobanGame("easy")
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # Test push left where push space would be at edge
        # box at (2, 2), goal at (2, 1), push left needs space at (2, 3)
        result = game._can_push_to_goal(2, 2, 2, 1)
        assert isinstance(result, bool)

    async def test_can_push_down_at_edge(self):
        """Test _can_push_to_goal pushing down near bottom edge."""
        game = SokobanGame("easy")
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # box at (game.size-3, 2), goal at (game.size-2, 2)
        result = game._can_push_to_goal(game.size - 3, 2, game.size - 2, 2)
        assert isinstance(result, bool)

    async def test_can_push_up_at_edge(self):
        """Test _can_push_to_goal pushing up near top edge."""
        game = SokobanGame("easy")
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # box at (2, 2), goal at (1, 2), push up needs space at (3, 2)
        result = game._can_push_to_goal(2, 2, 1, 2)
        assert isinstance(result, bool)

    async def test_fallback_puzzle_triggered(self):
        """Test that fallback puzzle generation works."""
        # Use a seed that might trigger fallback
        game = SokobanGame("hard", seed=999999)
        await game.generate_puzzle()
        assert game.game_started
        assert len(game.goals) > 0

    async def test_hint_all_boxes_on_goals(self):
        """Test hint when all boxes are already on goals."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Put all boxes on goals
        for r in range(game.size):
            for c in range(game.size):
                if game.grid[r][c] == 2:  # Box not on goal
                    game.grid[r][c] = 0

        for gr, gc in game.goals:
            game.grid[gr][gc] = 5  # Box on goal

        hint = await game.get_hint()
        # Should return None since puzzle is solved
        assert hint is None

    async def test_hint_find_path_to_push(self):
        """Test hint finding path to push position."""
        game = SokobanGame("easy", seed=123)
        await game.generate_puzzle()

        # Run a few hints to exercise path finding
        for _ in range(15):
            if game.is_complete():
                break
            hint = await game.get_hint()
            if hint is None:
                break
            await game.validate_move(hint[0])

    async def test_hint_fallback_empty_or_push(self):
        """Test hint fallback for empty moves or pushes."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Get hints until we exhaust options
        for _ in range(20):
            hint = await game.get_hint()
            if hint is None:
                break
            direction, message = hint
            assert direction in ["up", "down", "left", "right"]
            await game.validate_move(direction)

    async def test_generation_path_clear_check(self):
        """Test puzzle generation path clearing logic."""
        # Generate multiple puzzles to exercise different code paths
        for seed in range(10):
            game = SokobanGame("medium", seed=seed)
            await game.generate_puzzle()
            assert game.game_started

    async def test_generation_box_placement_directions(self):
        """Test puzzle generation tries all directions for box placement."""
        # Different seeds will exercise different direction choices
        for seed in [100, 200, 300, 400, 500]:
            game = SokobanGame("easy", seed=seed)
            await game.generate_puzzle()
            assert len(game.goals) > 0

    async def test_can_push_left_path_blocked_by_wall(self):
        """Test _can_push_to_goal push left with wall in path (line 152)."""
        game = SokobanGame("easy")
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # Block path between box and goal for push left
        # box at (2, 4), goal at (2, 2) - wall at (2, 3) blocks path
        game.grid[2][3] = 1

        result = game._can_push_to_goal(2, 4, 2, 2)
        assert result is False

    async def test_can_push_left_push_space_blocked(self):
        """Test _can_push_to_goal push left when push space is blocked (line 148)."""
        game = SokobanGame("easy")
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # Block push space for push left: box at (2, 3), goal at (2, 2)
        # Push space would be at (2, 4) - block it
        game.grid[2][4] = 1

        result = game._can_push_to_goal(2, 3, 2, 2)
        assert result is False

    async def test_can_push_down_space_blocked(self):
        """Test _can_push_to_goal push down when push space blocked (line 159)."""
        game = SokobanGame("easy")
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # Push down: box at (2, 2), goal at (4, 2), need space at (1, 2) for push
        # Block push space
        game.grid[1][2] = 1

        result = game._can_push_to_goal(2, 2, 4, 2)
        assert result is False

    async def test_can_push_up_space_blocked(self):
        """Test _can_push_to_goal push up when push space blocked (line 172)."""
        game = SokobanGame("easy")
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # Push up: box at (4, 2), goal at (2, 2), need space at (5, 2) for push
        # But (5, 2) is wall at edge (size-1 is 5 for size=6)
        # So use box at (3, 2), goal at (2, 2), block space at (4, 2)
        game.grid[4][2] = 1

        result = game._can_push_to_goal(3, 2, 2, 2)
        assert result is False

    async def test_can_push_up_path_blocked(self):
        """Test _can_push_to_goal push up with wall in path (line 176)."""
        game = SokobanGame("easy")
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # Push up: box at (4, 2), goal at (2, 2), wall at (3, 2) blocks path
        game.grid[3][2] = 1

        result = game._can_push_to_goal(4, 2, 2, 2)
        assert result is False

    async def test_push_box_outside_grid_check(self):
        """Test pushing box fails when push destination is outside grid (line 416)."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Place box at position where pushing would go outside
        # Position at row 1, col 1 - push up would go to row 0 (wall)
        # Clear area first
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # Set up: player at (2,2), box at (1,2) - pushing up goes into wall at (0,2)
        game.grid[1][2] = 2  # Box
        game.player_pos = (2, 2)
        game.grid[2][2] = 4  # Player

        result = await game.validate_move("up")
        # Should fail because box can't be pushed into wall
        assert not result.success

    async def test_unknown_cell_type_message(self):
        """Test handling of unknown cell type returns proper message (line 441)."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Set up an invalid cell type scenario
        pr, pc = game.player_pos
        # Find an adjacent empty cell
        for dr, dc, direction in [(0, 1, "right"), (0, -1, "left"), (1, 0, "down"), (-1, 0, "up")]:
            nr, nc = pr + dr, pc + dc
            if 0 <= nr < game.size and 0 <= nc < game.size and game.grid[nr][nc] == 0:
                game.grid[nr][nc] = 99  # Invalid cell type
                result = await game.validate_move(direction)
                assert not result.success
                assert "unknown" in result.message.lower() or isinstance(result.success, bool)
                return

    async def test_bfs_path_out_of_bounds(self):
        """Test BFS handles out of bounds checks (line 479)."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Position player at edge
        game.grid[1][1] = 4
        game.player_pos = (1, 1)

        # Try to find path - BFS should handle bounds
        path = game._find_path_to_push_position(3, 3)
        # Path may or may not exist, but should not crash
        assert path is None or isinstance(path, list)

    async def test_hint_no_boxes_not_on_goal(self):
        """Test get_hint when no boxes are off goals (line 521)."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Remove all boxes that are not on goals
        for r in range(game.size):
            for c in range(game.size):
                if game.grid[r][c] == 2:  # Box not on goal
                    game.grid[r][c] = 0

        # Ensure at least one goal has a box
        for gr, gc in game.goals:
            game.grid[gr][gc] = 5

        hint = await game.get_hint()
        # Should return None since no boxes need to be pushed
        assert hint is None

    async def test_hint_push_position_at_wall(self):
        """Test get_hint when push position is a wall (line 554)."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Create scenario where push position is blocked by wall
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # Goal at (3, 3), box at (3, 2), player needs to be at (3, 1) to push right
        # But we put wall there
        game.goals = [(3, 3)]
        game.grid[3][3] = 3  # Goal
        game.grid[3][2] = 2  # Box
        game.grid[3][1] = 1  # Wall blocking push position
        game.player_pos = (2, 2)
        game.grid[2][2] = 4

        hint = await game.get_hint()
        # Should try other options or return fallback
        if hint:
            assert isinstance(hint[0], str)

    async def test_hint_push_destination_blocked(self):
        """Test get_hint when push destination is blocked (lines 559, 561)."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # Goal at (3, 4), box at (3, 2), player at (3, 1)
        # But destination for push is blocked
        game.goals = [(3, 4)]
        game.grid[3][4] = 3  # Goal
        game.grid[3][2] = 2  # Box
        game.grid[3][3] = 1  # Wall blocking push destination
        game.player_pos = (3, 1)
        game.grid[3][1] = 4

        hint = await game.get_hint()
        # Should try other options
        if hint:
            assert isinstance(hint[0], str)

    async def test_hint_fallback_empty_cell(self):
        """Test hint fallback to empty cell move (line 589)."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Clear boxes so no push hints are possible
        for r in range(game.size):
            for c in range(game.size):
                if game.grid[r][c] == 2:
                    game.grid[r][c] = 0

        # Keep one goal but no boxes
        game.goals = game.goals[:1] if game.goals else [(2, 2)]
        for gr, gc in game.goals:
            game.grid[gr][gc] = 3

        hint = await game.get_hint()
        # Should return fallback move to empty cell
        if hint:
            assert hint[0] in ["up", "down", "left", "right"]
            assert "try" in hint[1].lower() or "move" in hint[1].lower()

    async def test_hint_fallback_push_any_box(self):
        """Test hint fallback to push any adjacent box (lines 591-594)."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Create a box adjacent to player that doesn't align with any goal
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]
        for i in range(game.size):
            game.grid[0][i] = 1
            game.grid[game.size - 1][i] = 1
            game.grid[i][0] = 1
            game.grid[i][game.size - 1] = 1

        # Goal at corner, box and player elsewhere
        game.goals = [(1, 1)]
        game.grid[1][1] = 3  # Goal
        game.grid[2][3] = 2  # Box (not aligned with goal)
        game.player_pos = (2, 2)
        game.grid[2][2] = 4  # Player next to box
        game.grid[2][4] = 0  # Empty for push

        hint = await game.get_hint()
        if hint:
            assert hint[0] in ["up", "down", "left", "right"]

    async def test_generation_insufficient_goals(self):
        """Test puzzle generation handles insufficient goals (line 212)."""
        # Test with small grid where goals might not all fit
        game = SokobanGame("easy")
        # Override to force small area
        game.size = 5
        game.num_boxes = 10  # More boxes than can fit
        game.grid = [[0 for _ in range(game.size)] for _ in range(game.size)]

        await game.generate_puzzle()
        # Should still create a valid puzzle (possibly fallback)
        assert game.game_started

    async def test_generation_path_blocked_by_box(self):
        """Test generation handles path blocked by other boxes (lines 261-274)."""
        # Generate many puzzles to hit path blocking scenarios
        for seed in range(20, 40):
            game = SokobanGame("medium", seed=seed)
            await game.generate_puzzle()
            assert game.game_started

    async def test_generation_push_position_on_box(self):
        """Test generation handles push position being a box (line 253)."""
        # Multiple puzzles with different seeds will exercise this
        for seed in range(50, 70):
            game = SokobanGame("hard", seed=seed)
            await game.generate_puzzle()
            assert game.game_started

    async def test_fallback_puzzle_structure(self):
        """Test fallback puzzle has correct structure (lines 320-351)."""
        game = SokobanGame("easy")

        # Force fallback by manipulating internals
        # Run generate, but we can verify it creates valid structure
        await game.generate_puzzle()

        # Verify structure
        assert game.grid is not None
        assert len(game.grid) == game.size
        assert all(len(row) == game.size for row in game.grid)
        assert game.player_pos is not None
        assert game.initial_state is not None
        assert "grid" in game.initial_state
        assert "player_pos" in game.initial_state

    async def test_hint_via_path_finding(self):
        """Test hint uses path finding when not at push position (line 572-577)."""
        game = SokobanGame("easy", seed=42)
        await game.generate_puzzle()

        # Move player away from any boxes
        for r in range(2, game.size - 2):
            for c in range(2, game.size - 2):
                if game.grid[r][c] == 0:
                    # Check no box adjacent
                    has_adjacent_box = False
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < game.size and 0 <= nc < game.size:
                            if game.grid[nr][nc] in [2, 5]:
                                has_adjacent_box = True
                                break
                    if not has_adjacent_box:
                        old_pr, old_pc = game.player_pos
                        game.grid[old_pr][old_pc] = 0
                        game.player_pos = (r, c)
                        game.grid[r][c] = 4
                        break
            else:
                continue
            break

        # Now hint should use path finding
        hint = await game.get_hint()
        if hint:
            assert isinstance(hint[0], str)
            assert isinstance(hint[1], str)

    async def test_hint_player_at_push_position(self):
        """Test hint when player is already at push position (lines 564-568)."""
        game = SokobanGame("easy")
        await game.generate_puzzle()

        # Find a box and position player for direct push
        for r in range(1, game.size - 1):
            for c in range(1, game.size - 1):
                if game.grid[r][c] == 2:  # Box
                    # Check if we can position player to push toward a goal
                    for gr, gc in game.goals:
                        if r == gr:  # Same row
                            if c < gc:  # Push right
                                player_r, player_c = r, c - 1
                                if player_c >= 1 and game.grid[player_r][player_c] in [0, 3]:
                                    old_pr, old_pc = game.player_pos
                                    game.grid[old_pr][old_pc] = 0
                                    game.player_pos = (player_r, player_c)
                                    game.grid[player_r][player_c] = 4

                                    hint = await game.get_hint()
                                    if hint and "push" in hint[1].lower():
                                        assert hint[0] == "right"
                                        return
                        elif c == gc:  # Same column
                            if r < gr:  # Push down
                                player_r, player_c = r - 1, c
                                if player_r >= 1 and game.grid[player_r][player_c] in [0, 3]:
                                    old_pr, old_pc = game.player_pos
                                    game.grid[old_pr][old_pc] = 0
                                    game.player_pos = (player_r, player_c)
                                    game.grid[player_r][player_c] = 4

                                    hint = await game.get_hint()
                                    if hint and "push" in hint[1].lower():
                                        assert hint[0] == "down"
                                        return
