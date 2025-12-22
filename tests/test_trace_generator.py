"""Tests for trace generation."""

import pytest

from puzzle_arcade_server.games import AVAILABLE_GAMES
from puzzle_arcade_server.models import SolverConfig
from puzzle_arcade_server.trace import TraceGenerator, generate_trace


class TestTraceGenerator:
    """Tests for TraceGenerator class."""

    @pytest.fixture
    def generator(self):
        """Create a trace generator."""
        return TraceGenerator()

    async def test_generate_sudoku_trace(self, generator):
        """Test trace generation for Sudoku."""
        game = AVAILABLE_GAMES["sudoku"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generator.generate(game)

        assert trace.problem_id == "sudoku_easy_42"
        assert len(trace.steps) > 0
        assert trace.checkpoints

        # Check step structure
        step = trace.steps[0]
        assert step.index == 0
        assert step.operation.value == "place"
        assert "cell" in step.before_state
        assert "cell" in step.after_state
        assert step.explanation

    async def test_generate_binary_trace(self, generator):
        """Test trace generation for Binary puzzle."""
        game = AVAILABLE_GAMES["binary"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generator.generate(game)

        assert trace.problem_id == "binary_puzzle_easy_42"
        assert len(trace.steps) > 0

        # Check binary-specific content
        step = trace.steps[0]
        assert step.rule_applied == "balance_constraint"
        assert "balance" in step.explanation.lower() or "consecutive" in step.explanation.lower()

    async def test_generate_einstein_trace(self, generator):
        """Test trace generation for Einstein's Puzzle."""
        game = AVAILABLE_GAMES["einstein"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generator.generate(game)

        assert "einstein" in trace.problem_id
        assert len(trace.steps) > 0

        # Check Einstein-specific content
        step = trace.steps[0]
        assert step.operation.value == "deduce"
        assert "house" in step.before_state

    async def test_generate_mastermind_trace(self, generator):
        """Test trace generation for Mastermind."""
        game = AVAILABLE_GAMES["mastermind"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generator.generate(game)

        assert trace.problem_id == "mastermind_easy_42"
        assert len(trace.steps) == 1

        step = trace.steps[0]
        assert step.operation.value == "deduce"
        assert "secret_code" in step.before_state

    async def test_generate_hitori_trace(self, generator):
        """Test trace generation for Hitori."""
        game = AVAILABLE_GAMES["hitori"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generator.generate(game)

        assert trace.problem_id == "hitori_easy_42"
        assert len(trace.steps) > 0

        step = trace.steps[0]
        assert step.operation.value == "eliminate"
        assert "shaded" in step.after_state

    async def test_generate_bridges_trace(self, generator):
        """Test trace generation for Bridges."""
        game = AVAILABLE_GAMES["bridges"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generator.generate(game)

        assert trace.problem_id == "bridges_easy_42"
        assert len(trace.steps) > 0

        step = trace.steps[0]
        assert step.operation.value == "place"
        assert "bridge" in step.before_state

    async def test_generate_knapsack_trace(self, generator):
        """Test trace generation for Knapsack."""
        game = AVAILABLE_GAMES["knapsack"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generator.generate(game)

        assert trace.problem_id == "knapsack_easy_42"
        assert len(trace.steps) > 0

        step = trace.steps[0]
        assert step.operation.value == "place"
        assert "item" in step.before_state

    async def test_generate_lights_trace(self, generator):
        """Test trace generation for Lights Out."""
        game = AVAILABLE_GAMES["lights"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generator.generate(game)

        assert trace.problem_id == "lights_out_easy_42"
        assert len(trace.steps) > 0

        step = trace.steps[0]
        assert step.operation.value == "place"
        assert "pressed" in step.after_state

    async def test_generate_minesweeper_trace(self, generator):
        """Test trace generation for Minesweeper."""
        game = AVAILABLE_GAMES["minesweeper"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generator.generate(game)

        assert trace.problem_id == "minesweeper_easy_42"
        assert len(trace.steps) > 0

    async def test_generate_scheduler_trace(self, generator):
        """Test trace generation for Scheduler."""
        game = AVAILABLE_GAMES["scheduler"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generator.generate(game)

        assert "scheduler" in trace.problem_id
        assert len(trace.steps) > 0

        step = trace.steps[0]
        assert step.operation.value == "place"
        assert "task" in step.before_state

    async def test_generate_slither_trace(self, generator):
        """Test trace generation for Slitherlink."""
        game = AVAILABLE_GAMES["slither"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generator.generate(game)

        assert trace.problem_id == "slitherlink_easy_42"
        assert len(trace.steps) > 0

        step = trace.steps[0]
        assert step.operation.value == "place"
        assert "edge" in step.before_state

    async def test_generate_sokoban_trace(self, generator):
        """Test trace generation for Sokoban."""
        game = AVAILABLE_GAMES["sokoban"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generator.generate(game)

        assert trace.problem_id == "sokoban_easy_42"
        assert len(trace.steps) > 0

        step = trace.steps[0]
        assert step.operation.value == "place"
        assert "box" in step.before_state

    async def test_generate_logic_trace(self, generator):
        """Test trace generation for Logic Grid."""
        game = AVAILABLE_GAMES["logic"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generator.generate(game)

        assert "logic" in trace.problem_id
        assert len(trace.steps) > 0

        step = trace.steps[0]
        assert step.operation.value == "deduce"

    async def test_generate_nonogram_trace(self, generator):
        """Test trace generation for Nonogram."""
        game = AVAILABLE_GAMES["nonogram"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generator.generate(game)

        assert trace.problem_id == "nonogram_easy_42"
        assert len(trace.steps) > 0

    async def test_generate_futoshiki_trace(self, generator):
        """Test trace generation for Futoshiki."""
        game = AVAILABLE_GAMES["futoshiki"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generator.generate(game)

        assert trace.problem_id == "futoshiki_easy_42"
        assert len(trace.steps) > 0

    async def test_generate_kenken_trace(self, generator):
        """Test trace generation for KenKen."""
        game = AVAILABLE_GAMES["kenken"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generator.generate(game)

        assert trace.problem_id == "kenken_easy_42"
        assert len(trace.steps) > 0

    async def test_generate_kakuro_trace(self, generator):
        """Test trace generation for Kakuro."""
        game = AVAILABLE_GAMES["kakuro"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generator.generate(game)

        assert trace.problem_id == "kakuro_easy_42"
        assert len(trace.steps) > 0

    async def test_all_games_generate_traces(self, generator):
        """Test that all games generate non-empty traces."""
        for game_name in AVAILABLE_GAMES:
            game_class = AVAILABLE_GAMES[game_name]
            game = game_class(difficulty="easy", seed=42, solver_config=SolverConfig())
            await game.generate_puzzle()

            trace = generator.generate(game)

            assert len(trace.steps) > 0, f"{game_name} should generate trace steps"
            assert trace.problem_id, f"{game_name} should have problem_id"

    async def test_checkpoints_generated(self, generator):
        """Test that checkpoints are generated for traces with enough steps."""
        game = AVAILABLE_GAMES["sudoku"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generator.generate(game)

        # Sudoku should have enough steps for checkpoints
        assert len(trace.checkpoints) > 0
        assert all(isinstance(cp, int) for cp in trace.checkpoints)
        assert all(0 <= cp < len(trace.steps) for cp in trace.checkpoints)

    async def test_trace_to_jsonl_steps(self, generator):
        """Test trace conversion to JSONL format."""
        game = AVAILABLE_GAMES["sudoku"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generator.generate(game)
        jsonl_steps = trace.to_jsonl_steps()

        assert len(jsonl_steps) == len(trace.steps)
        step = jsonl_steps[0]
        assert "index" in step
        assert "operation" in step
        assert "before" in step
        assert "after" in step
        assert "value" in step
        assert "rule" in step
        assert "explanation" in step

    async def test_trace_to_natural_language(self, generator):
        """Test trace conversion to natural language."""
        game = AVAILABLE_GAMES["sudoku"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generator.generate(game)
        nl = trace.to_natural_language()

        assert isinstance(nl, str)
        assert len(nl) > 0
        assert "Step 1:" in nl


class TestGenerateTraceFunction:
    """Tests for the generate_trace convenience function."""

    async def test_generate_trace_function(self):
        """Test the convenience function."""
        game = AVAILABLE_GAMES["sudoku"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generate_trace(game)

        assert trace.problem_id == "sudoku_easy_42"
        assert len(trace.steps) > 0


class TestTraceGeneratorEdgeCases:
    """Tests for edge cases in trace generation."""

    @pytest.fixture
    def generator(self):
        """Create a trace generator."""
        return TraceGenerator()

    async def test_grid_puzzle_fallback(self, generator):
        """Test fallback to grid puzzle generator."""
        # Fillomino uses the generic grid puzzle generator
        game = AVAILABLE_GAMES["fillomino"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generator.generate(game)

        assert len(trace.steps) > 0

    async def test_step_explanations_vary_by_game(self, generator):
        """Test that explanations are game-specific."""
        sudoku = AVAILABLE_GAMES["sudoku"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await sudoku.generate_puzzle()
        sudoku_trace = generator.generate(sudoku)

        binary = AVAILABLE_GAMES["binary"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await binary.generate_puzzle()
        binary_trace = generator.generate(binary)

        # Explanations should be different
        sudoku_expl = sudoku_trace.steps[0].explanation
        binary_expl = binary_trace.steps[0].explanation

        assert sudoku_expl != binary_expl
        assert "box" in sudoku_expl.lower() or "row" in sudoku_expl.lower()
        assert "balance" in binary_expl.lower() or "consecutive" in binary_expl.lower()

    async def test_infer_sudoku_rule(self, generator):
        """Test Sudoku rule inference."""
        game = AVAILABLE_GAMES["sudoku"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generator.generate(game)

        # Check that rules are inferred
        rules = {step.rule_applied for step in trace.steps}
        assert len(rules) > 0
        # Should have some Sudoku-specific rules
        valid_rules = {"naked_single_row", "naked_single_column", "naked_single_box", "elimination"}
        assert rules.intersection(valid_rules)

    async def test_empty_trace_fallback(self, generator):
        """Test empty trace when no generator or solution available (lines 57-61)."""
        from puzzle_arcade_server.games._base import PuzzleGame
        from puzzle_arcade_server.models import DifficultyLevel

        # Create a minimal mock game with no generator and no grid/solution
        class MockGame(PuzzleGame):
            def __init__(self):
                self._name = "MockGame"
                self._difficulty = DifficultyLevel.EASY
                self._seed = 123
                self._canonical_solution = None

            @property
            def name(self) -> str:
                return self._name

            @property
            def description(self) -> str:
                return "Mock game"

            @property
            def difficulty(self):
                return self._difficulty

            @property
            def seed(self):
                return self._seed

            @property
            def canonical_solution(self):
                return self._canonical_solution

            async def generate_puzzle(self):
                pass

            async def validate_move(self, move):
                pass

            def is_complete(self):
                return True

            def render_grid(self):
                return ""

            def get_rules(self):
                return ""

            def get_commands(self):
                return ""

            async def get_hint(self):
                return None

        game = MockGame()
        trace = generator.generate(game)

        # Should return empty trace
        assert trace.problem_id == "mockgame_easy_123"
        assert len(trace.steps) == 0

    async def test_grid_puzzle_no_solution(self, generator):
        """Test grid puzzle generator with no solution (line 76)."""
        from puzzle_arcade_server.games._base import PuzzleGame
        from puzzle_arcade_server.models import DifficultyLevel

        class MockGridGame(PuzzleGame):
            def __init__(self):
                self._name = "GridMock"
                self._difficulty = DifficultyLevel.EASY
                self._seed = 456
                self.grid = [[0, 1], [2, 0]]
                self.solution = None  # No solution

            @property
            def name(self) -> str:
                return self._name

            @property
            def description(self) -> str:
                return "Mock grid game"

            @property
            def difficulty(self):
                return self._difficulty

            @property
            def seed(self):
                return self._seed

            @property
            def canonical_solution(self):
                return None

            async def generate_puzzle(self):
                pass

            async def validate_move(self, move):
                pass

            def is_complete(self):
                return True

            def render_grid(self):
                return ""

            def get_rules(self):
                return ""

            def get_commands(self):
                return ""

            async def get_hint(self):
                return None

        game = MockGridGame()
        trace = generator.generate(game)

        # Should return empty trace when no solution
        assert trace.problem_id == "gridmock_easy_456"
        assert len(trace.steps) == 0

    async def test_generate_from_canonical_tuple(self, generator):
        """Test generating trace from canonical solution with tuples (lines 113-131)."""
        from puzzle_arcade_server.games._base import PuzzleGame
        from puzzle_arcade_server.models import DifficultyLevel

        class MockCanonicalGame(PuzzleGame):
            def __init__(self):
                self._name = "CanonicalMock"
                self._difficulty = DifficultyLevel.MEDIUM
                self._seed = 789
                self._canonical_solution = [(0, 0, 5), (1, 2, 3), (2, 1, 7)]

            @property
            def name(self) -> str:
                return self._name

            @property
            def description(self) -> str:
                return "Mock canonical game"

            @property
            def difficulty(self):
                return self._difficulty

            @property
            def seed(self):
                return self._seed

            @property
            def canonical_solution(self):
                return self._canonical_solution

            async def generate_puzzle(self):
                pass

            async def validate_move(self, move):
                pass

            def is_complete(self):
                return True

            def render_grid(self):
                return ""

            def get_rules(self):
                return ""

            def get_commands(self):
                return ""

            async def get_hint(self):
                return None

        game = MockCanonicalGame()
        trace = generator.generate(game)

        assert trace.problem_id == "canonicalmock_medium_789"
        assert len(trace.steps) == 3
        assert trace.steps[0].operation.value == "place"
        assert "cell(0,0)=5" in trace.steps[0].after_state

    async def test_generate_from_canonical_non_tuple(self, generator):
        """Test generating trace from canonical solution with non-tuple moves (lines 133-139)."""
        from puzzle_arcade_server.games._base import PuzzleGame
        from puzzle_arcade_server.models import DifficultyLevel

        class MockCanonicalNonTupleGame(PuzzleGame):
            def __init__(self):
                self._name = "CanonicalNonTuple"
                self._difficulty = DifficultyLevel.HARD
                self._seed = 101
                self._canonical_solution = ["move_up", "push_left", "move_down"]

            @property
            def name(self) -> str:
                return self._name

            @property
            def description(self) -> str:
                return "Mock canonical non-tuple game"

            @property
            def difficulty(self):
                return self._difficulty

            @property
            def seed(self):
                return self._seed

            @property
            def canonical_solution(self):
                return self._canonical_solution

            async def generate_puzzle(self):
                pass

            async def validate_move(self, move):
                pass

            def is_complete(self):
                return True

            def render_grid(self):
                return ""

            def get_rules(self):
                return ""

            def get_commands(self):
                return ""

            async def get_hint(self):
                return None

        game = MockCanonicalNonTupleGame()
        trace = generator.generate(game)

        assert trace.problem_id == "canonicalnontuple_hard_101"
        assert len(trace.steps) == 3
        assert trace.steps[0].operation.value == "deduce"
        assert "Move 1:" in trace.steps[0].explanation

    async def test_generate_from_canonical_empty(self, generator):
        """Test generating trace from empty canonical solution (line 118)."""
        from puzzle_arcade_server.games._base import PuzzleGame
        from puzzle_arcade_server.models import DifficultyLevel

        class MockEmptyCanonicalGame(PuzzleGame):
            def __init__(self):
                self._name = "EmptyCanonical"
                self._difficulty = DifficultyLevel.EASY
                self._seed = 202
                self._canonical_solution = []

            @property
            def name(self) -> str:
                return self._name

            @property
            def description(self) -> str:
                return "Mock empty canonical game"

            @property
            def difficulty(self):
                return self._difficulty

            @property
            def seed(self):
                return self._seed

            @property
            def canonical_solution(self):
                return self._canonical_solution

            async def generate_puzzle(self):
                pass

            async def validate_move(self, move):
                pass

            def is_complete(self):
                return True

            def render_grid(self):
                return ""

            def get_rules(self):
                return ""

            def get_commands(self):
                return ""

            async def get_hint(self):
                return None

        game = MockEmptyCanonicalGame()
        trace = generator.generate(game)

        assert len(trace.steps) == 0

    async def test_infer_rule_nonogram(self, generator):
        """Test rule inference for nonogram returns line_constraint (line 160)."""
        # The _infer_rule method is called during grid puzzle generation
        # We need a game that triggers this path
        game = AVAILABLE_GAMES["nonogram"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        # Check the rule directly
        rule = generator._infer_rule(game, 0, 0, 1)
        assert rule == "line_constraint"

    async def test_infer_sudoku_rule_column(self, generator):
        """Test Sudoku rule inference for column (lines 174-176)."""
        game = AVAILABLE_GAMES["sudoku"](difficulty="medium", seed=123, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generator.generate(game)

        # Check if naked_single_column is detected for any step
        rules = {step.rule_applied for step in trace.steps}
        # The test verifies the method runs - column detection depends on puzzle state
        assert len(rules) > 0

    async def test_infer_sudoku_rule_box(self, generator):
        """Test Sudoku rule inference for box (lines 179-188)."""
        game = AVAILABLE_GAMES["sudoku"](difficulty="hard", seed=456, solver_config=SolverConfig())
        await game.generate_puzzle()

        trace = generator.generate(game)

        # Check that box-related rules are inferred for some steps
        rules = {step.rule_applied for step in trace.steps}
        # At minimum, elimination should be detected
        assert (
            "elimination" in rules
            or "naked_single_box" in rules
            or "naked_single_column" in rules
            or "naked_single_row" in rules
        )

    async def test_identify_checkpoints_empty(self, generator):
        """Test checkpoint identification with empty steps (line 217)."""
        checkpoints = generator._identify_checkpoints([])
        assert checkpoints == []

    async def test_binary_trace_delegation(self, generator):
        """Test Binary puzzle trace generation delegates to grid puzzle (line 238)."""
        game = AVAILABLE_GAMES["binary"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        # Direct call to _generate_binary
        trace = generator._generate_binary(game)

        assert len(trace.steps) > 0
        # Binary should use balance_constraint rule
        assert any(step.rule_applied == "balance_constraint" for step in trace.steps)

    async def test_einstein_puzzle_name_aliases(self, generator):
        """Test Einstein puzzle name aliases (lines 698, 702)."""
        game = AVAILABLE_GAMES["einstein"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        # Test _generate_einstein_s_puzzle alias
        trace1 = generator._generate_einstein_s_puzzle(game)
        assert "einstein" in trace1.problem_id
        assert len(trace1.steps) > 0

        # Test _generate_einstein_puzzle alias
        trace2 = generator._generate_einstein_puzzle(game)
        assert "einstein" in trace2.problem_id
        assert len(trace2.steps) > 0

    async def test_generate_explanation_default(self, generator):
        """Test default explanation generation (line 212)."""
        # Create a game that isn't sudoku, binary, futoshiki, or kenken
        game = AVAILABLE_GAMES["fillomino"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        # Call _generate_explanation directly for a game not in special cases
        explanation = generator._generate_explanation(game, 0, 0, 5)
        assert "Place 5 at row 1, column 1" in explanation

    async def test_infer_rule_kenken_kakuro(self, generator):
        """Test rule inference for kenken/kakuro returns arithmetic_constraint (line 158)."""
        game = AVAILABLE_GAMES["kenken"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        rule = generator._infer_rule(game, 0, 0, 1)
        assert rule == "arithmetic_constraint"

        game2 = AVAILABLE_GAMES["kakuro"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game2.generate_puzzle()

        rule2 = generator._infer_rule(game2, 0, 0, 1)
        assert rule2 == "arithmetic_constraint"

    async def test_infer_rule_default(self, generator):
        """Test rule inference default returns constraint_propagation (line 164)."""
        # Use a game that doesn't match any special case
        game = AVAILABLE_GAMES["fillomino"](difficulty="easy", seed=42, solver_config=SolverConfig())
        await game.generate_puzzle()

        rule = generator._infer_rule(game, 0, 0, 1)
        assert rule == "constraint_propagation"

    async def test_format_cell_state_variations(self, generator):
        """Test cell state formatting variations (lines 144-148)."""
        # Empty cell
        state1 = generator._format_cell_state(0, 0, None, is_empty=True)
        assert state1 == "cell(r1,c1)=empty"

        # Non-empty cell
        state2 = generator._format_cell_state(1, 2, 5, is_empty=False)
        assert state2 == "cell(r2,c3)=5"

        # Value of -1 should be treated as empty
        state3 = generator._format_cell_state(0, 0, -1, is_empty=False)
        assert state3 == "cell(r1,c1)=empty"
