"""
Solution trace generation for puzzle games.

Generates machine-verifiable step-by-step solutions using
the Trace schema from chuk-gym-core.
"""

from puzzle_arcade_server.trace.generator import TraceGenerator, generate_trace

__all__ = ["TraceGenerator", "generate_trace"]
