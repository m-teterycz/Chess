[README-python-main.md](https://github.com/user-attachments/files/35221919/README-python-main.md)
# Chess Engine — Python Version

A chess project built in Python with a Pygame interface. This is the original implementation of the project, where the game logic and board representation are written in Python.

The project is also a way for me to explore chess programming: representing a position, generating moves, enforcing chess rules, and connecting an engine to an interactive board.
It also acts as a way for me to learn algorithims such as negamax and minimax with alpha beta pruning.

> **Branch:** `main` — original Python implementation. The C++ rewrite is on [`cpp-engine`](../../tree/cpp-engine) (if viewing the repository on GitHub, switch branches using the branch selector).

## Features

- Interactive chessboard rendered using Pygame.
- Click a piece to select it and see available destinations.
- Move handling and turn management.
- Chess-rule logic, including special moves and game-ending conditions, developed as part of the Python implementation.
- A starting point for experimenting with chess-engine search and evaluation.

This is a personal learning project, **not** a finished chess engine. Some features may still be experimental or incomplete.

## Getting started

**Requirements:** Python 3 and Pygame.

```bash
python -m pip install pygame
python -m pip install torch
python -m pip install numpy
python -m pip install pandas
python main.py
```

The app opens a Pygame window. Select a piece with the mouse, then click one of its highlighted destinations to move it.

## Project layout

The original Python version is organised around these modules:

| File | Role |
| --- | --- |
| `main.py` | Application entry point and event loop |
| `board.py` | Board state and chess-rule logic |
| `piece.py` | Piece-related logic |
| `game.py` | Player interaction and turn handling |
| `renderer.py` | Drawing the board and interface |
| `engine.py` | Chess-engine experiments and logic |

## Why a C++ rewrite?

Chess search can explore millions of positions, making performance and memory management interesting challenges. I started a separate C++ implementation to learn systems programming and experiment with faster move generation and search, while keeping Python and Pygame for the interface.

The rewrite uses a **0x88 board representation**, C++20, and a lightweight text protocol between Python and a native C++ executable. See the `cpp-engine` branch for that version.

## Future ideas

- Compare the performance of Python and C++ implementations.
- Improve chess evaluation and move search.
- Explore neural-network-based position evaluation.
- Expand automated rule and move-generation testing.

## Status

This branch is kept as the original Python version for comparison and project history. Current C++ engine work lives on `cpp-engine`.
