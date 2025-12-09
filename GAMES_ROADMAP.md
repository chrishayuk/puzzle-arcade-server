# Puzzle Arcade Server - Games Roadmap

This document outlines the current and planned puzzle games for the Puzzle Arcade Server, organized by the constraint solving features they demonstrate.

## Currently Implemented ✅

### Classic Logic Puzzles

| Game | Grid Size | Constraint Types | Status |
|------|-----------|------------------|--------|
| **Sudoku** | 9×9 | AllDifferent (rows, cols, boxes) | ✅ Complete |
| **KenKen** | 4×4 to 6×6 | Arithmetic cages + AllDifferent | ✅ Complete |
| **Kakuro** | 5×5 to 8×8 | Sum constraints + AllDifferent | ✅ Complete |
| **Binary Puzzle** | 6×6 to 10×10 | Adjacency limits + Equal counts | ✅ Complete |
| **Futoshiki** | 4×4 to 6×6 | Inequalities + AllDifferent | ✅ Complete |
| **Nonogram** | 5×5 to 10×10 | Line sum constraints + Blocks | ✅ Complete |
| **Logic Grid** | Variable | Category associations + Logic | ✅ Complete |

**Total Implemented: 7 games**

---

## Planned Games - Phase 1: Core CP-SAT Demonstrations

### 🔥 High Priority (Best Solver Showcases)

#### 1. **Slitherlink** 🎯
- **Constraint Type**: Edge loops, global connectivity
- **Grid Size**: 5×5 to 10×10
- **Demonstrates**:
  - Binary edge variables (on/off)
  - Exactly 2 edges active per clue number
  - Single continuous closed loop (global constraint)
  - No branches or disconnected segments
- **Solver Value**: ⭐⭐⭐⭐⭐ (Shows global loop constraints)
- **Implementation Complexity**: Medium-High

#### 2. **Lights Out** 🎯
- **Constraint Type**: Boolean XOR-style SAT
- **Grid Size**: 5×5 to 7×7
- **Demonstrates**:
  - Boolean variables (light on/off)
  - XOR constraints (toggle affects neighbors)
  - SAT-style problem solving
  - Parity constraints
- **Solver Value**: ⭐⭐⭐⭐⭐ (Perfect SAT showcase)
- **Implementation Complexity**: Medium

#### 3. **Mastermind** 🎯
- **Constraint Type**: Deduction, implication, combination space
- **Setup**: 4-6 pegs, 6-8 colors
- **Demonstrates**:
  - Integer variables (colors)
  - Feedback consistency constraints
  - Black/white peg counting
  - Deductive reasoning
- **Solver Value**: ⭐⭐⭐⭐⭐ (Shows deduction power)
- **Implementation Complexity**: Medium

#### 4. **Killer Sudoku** 🎯
- **Grid Size**: 9×9
- **Constraint Type**: Linear constraints + AllDifferent
- **Demonstrates**:
  - Sum constraints (like Kakuro)
  - AllDifferent per cage
  - AllDifferent per row/col/box
  - Hybrid arithmetic + logic
- **Solver Value**: ⭐⭐⭐⭐ (Combines multiple constraint types)
- **Implementation Complexity**: Low (similar to existing games)

---

## Planned Games - Phase 2: Advanced Constraint Types

### Advanced CP-SAT Puzzles

#### 5. **Nurikabe**
- **Constraint Type**: Region connectivity, adjacency rules
- **Grid Size**: 8×8 to 12×12
- **Demonstrates**:
  - Black/white cell variables
  - Connected region constraints
  - "No 2×2 black block" rule
  - All white regions touch specific numbers
- **Solver Value**: ⭐⭐⭐⭐ (Region constraints)
- **Implementation Complexity**: High

#### 6. **Masyu**
- **Constraint Type**: Loop paths, directional constraints
- **Grid Size**: 6×6 to 10×10
- **Demonstrates**:
  - Edge-based loop constraints
  - Forced turns through white circles
  - Forced straight through black circles
  - Similar to Slitherlink with different rules
- **Solver Value**: ⭐⭐⭐⭐ (Directional constraints)
- **Implementation Complexity**: Medium-High

#### 7. **Hitori**
- **Constraint Type**: Elimination + adjacency
- **Grid Size**: 6×6 to 10×10
- **Demonstrates**:
  - Cell elimination (shaded/visible)
  - AllDifferent on visible cells per row/col
  - No adjacent shaded cells
  - All visible cells connected
- **Solver Value**: ⭐⭐⭐ (Hybrid constraints)
- **Implementation Complexity**: Medium

---

## Planned Games - Phase 3: Optimization Showcase

### 🚀 Real-World Optimization Demonstrations

These games demonstrate **objective optimization** - a key feature that distinguishes CP-SAT from pure logic puzzles!

#### 8. **Mini Scheduler** 🎯
- **Type**: Task scheduling optimization
- **Demonstrates**:
  - Task variables with start times
  - Duration constraints
  - Dependency constraints (task A before B)
  - Resource constraints
  - **Objective**: Minimize total time (makespan)
- **Solver Value**: ⭐⭐⭐⭐⭐ (Real-world application!)
- **Implementation Complexity**: Medium
- **Example**:
  ```
  Tasks: A(3hrs), B(2hrs), C(4hrs)
  Dependencies: A→C, B→C
  Workers: 2
  Goal: Minimize completion time
  ```

#### 9. **Knapsack Puzzle**
- **Type**: Value optimization under capacity
- **Demonstrates**:
  - Binary selection variables
  - Linear capacity constraint
  - **Objective**: Maximize total value
- **Solver Value**: ⭐⭐⭐⭐⭐ (Classic optimization)
- **Implementation Complexity**: Low
- **Example**:
  ```
  Items: Gold(5kg,$100), Silver(3kg,$50), Bronze(2kg,$20)
  Capacity: 8kg
  Goal: Maximize value
  ```

#### 10. **Bin Packing**
- **Type**: Assignment optimization
- **Demonstrates**:
  - Item-to-bin assignment
  - Capacity constraints per bin
  - **Objective**: Minimize number of bins
- **Solver Value**: ⭐⭐⭐⭐ (Resource allocation)
- **Implementation Complexity**: Medium
- **Example**:
  ```
  Items: 6, 5, 4, 3, 3, 2, 2
  Bin capacity: 10
  Goal: Use minimum bins
  ```

---

## Planned Games - Phase 4: Extended Variants

### Larger/Harder Variants of Existing Games

- **Latin Squares** (generalized Sudoku, N×N)
- **Magic Squares** (sum constraints everywhere)
- **Futoshiki XL** (9×9 or 12×12 versions)
- **Nonogram XL** (15×15+ grids)
- **Calcudoku** (KenKen variant with more operators)
- **Kakurasu** (weighted row/col sums, binary grid)

---

## Planned Games - Phase 5: Logic/Detective Puzzles

### Extended Logic Grid Variants

- **Murder Mystery** (who, where, weapon, time)
- **Logic Detective** (solve crimes with clues)
- **Einstein's Puzzle** (houses, colors, pets, drinks)
- **Office Assignment** (people, desks, departments, floors)

These demonstrate **business rule reasoning** - showing how the solver can handle real-world logical deduction problems.

---

## Menu Reorganization Plan

The game menu will be reorganized into three categories to showcase different solver capabilities:

```
==================================================
       WELCOME TO THE PUZZLE ARCADE!
       Powered by chuk-mcp-solver
==================================================

CLASSIC LOGIC PUZZLES (7 games)
  1) Sudoku          - 9×9 AllDifferent constraints
  2) KenKen          - Arithmetic cages + logic
  3) Kakuro          - Crossword math sums
  4) Binary Puzzle   - Adjacency + parity rules
  5) Futoshiki       - Inequality constraints
  6) Nonogram        - Line clue deduction
  7) Logic Grid      - Category associations

ADVANCED CP-SAT PUZZLES (4 games)
  8) Slitherlink     - Global loop constraints ⭐
  9) Mastermind      - Deductive reasoning ⭐
 10) Lights Out      - Boolean SAT solving ⭐
 11) Killer Sudoku   - Hybrid constraints ⭐

OPTIMIZATION CHALLENGES (3 games)
 12) Task Scheduler  - Minimize completion time ⭐
 13) Knapsack        - Maximize value ⭐
 14) Bin Packing     - Minimize resources ⭐
==================================================
```

---

## Implementation Priority

### Phase 1: Next 4 Games (Immediate)
1. **Lights Out** - Quick to implement, perfect SAT demo
2. **Killer Sudoku** - Reuses existing Sudoku code
3. **Mastermind** - Unique gameplay, great deduction showcase
4. **Slitherlink** - More complex, but amazing constraint demo

### Phase 2: Optimization Games (High Impact)
5. **Knapsack** - Simple optimization, big impact
6. **Task Scheduler** - Real-world application showcase
7. **Bin Packing** - Resource allocation demo

### Phase 3: Advanced Puzzles
8. **Nurikabe** - Advanced connectivity
9. **Masyu** - Loop variations
10. **Hitori** - Elimination logic

### Phase 4: Variants & Extensions
- Larger versions of existing games
- More logic grid scenarios
- Additional optimization problems

---

## Constraint Mapping Reference

For each game type, here's how they map to CP-SAT JSON models:

### Binary/Boolean Games
- **Variables**: Boolean (0/1) or Binary choices
- **Constraints**: Boolean logic, XOR, adjacency
- **Examples**: Lights Out, Binary Puzzle, Nonogram

### AllDifferent + Arithmetic
- **Variables**: Integer domains (1-N)
- **Constraints**: AllDifferent, Sum, Product, Division
- **Examples**: Sudoku, KenKen, Kakuro, Killer Sudoku

### Graph/Loop Constraints
- **Variables**: Edge states (on/off)
- **Constraints**: Connectivity, degree constraints, loops
- **Examples**: Slitherlink, Masyu

### Optimization Problems
- **Variables**: Integer choices or assignments
- **Constraints**: Capacity, time, dependencies
- **Objective**: Minimize or maximize a function
- **Examples**: Scheduler, Knapsack, Bin Packing

### Deduction/Logic
- **Variables**: Categorical assignments
- **Constraints**: Implication, exclusion, association
- **Examples**: Mastermind, Logic Grid, Murder Mystery

---

## Success Metrics

By completing this roadmap, the Puzzle Arcade Server will:

✅ Demonstrate **all major CP-SAT constraint types**
✅ Show **optimization** capabilities (not just satisfaction)
✅ Provide **real-world application** examples (scheduling, packing)
✅ Cover **SAT**, **CSP**, and **MIP** problem classes
✅ Serve as a comprehensive **constraint solver showcase**

---

## Contributing

Want to add a new game? Follow this process:

1. Choose from the roadmap or propose a new puzzle
2. Identify the constraint types it demonstrates
3. Implement the game extending `PuzzleGame` base class
4. Add comprehensive tests (>90% coverage)
5. Document the constraint mapping
6. Submit a PR!

See [README.md](README.md) for implementation details.

---

**Last Updated**: December 2025
**Current Games**: 7 implemented, 10+ planned
**Target**: 17+ games covering all major constraint types
