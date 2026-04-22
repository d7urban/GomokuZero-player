## GomokuZero Player

Interactive Gomoku front ends for playing against a trained AlphaZero-style
network, plus the shared game logic and MCTS implementation used by both UIs.

This repository is focused on play, not training. The included model loading
path expects pre-trained `.weights.h5` files, with
`gomoku_best.weights.h5` used by default when present.

### What Is Included

- `play_qt.py`: Qt desktop UI for human-vs-AI and human-vs-human play
- `play.py`: terminal curses UI for human-vs-AI play
- `gomoku.py`: board logic, state encoding, model definition, and MCTS
- `entrypoint_shared.py`: shared model-loading and AI configuration helpers

### Requirements

- Python 3.13+
- TensorFlow 2.20
- NumPy 2.4.2
- PyQt6 6.10.2

The project metadata is in `pyproject.toml`, and the pinned dependencies are
also listed in `requirements.txt`.

### Setup

Using `uv`:

```bash
uv sync
```

Using `pip`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Model Weights

The player expects a Keras weights file ending in `.h5`.

Weight selection behavior:

- `play.py` defaults to `gomoku_best.weights.h5`, then falls back to the newest
  `gomoku_*.weights.h5` checkpoint in the repository root
- `play_qt.py` auto-loads the newest `*.weights.h5` file in the current working
  directory at startup, and otherwise falls back to `gomoku_best.weights.h5`
- both UIs allow choosing a specific weights file

### Run

Qt GUI:

```bash
uv run play_qt.py
```

Terminal UI:

```bash
uv run play.py
```

With plain Python:

```bash
python play_qt.py
python play.py
```

### Curses UI

`play.py` is a keyboard-driven terminal interface.

Controls:

- Arrow keys: move cursor
- `Space`: place a stone
- `U`: undo the last two moves
- `Q`: quit

Options:

```bash
uv run play.py --difficulty medium
uv run play.py --difficulty 2500
uv run play.py --weight_file ./my_model.weights.h5
```

Difficulty accepts:

- `easy`
- `medium`
- `hard`
- any positive integer simulation count

### Qt UI

`play_qt.py` provides the richer desktop interface.

Features:

- human-vs-AI play
- human-vs-human mode
- model auto-load on startup
- selectable weight source
- difficulty controls, including custom simulation counts
- game save/load as JSON
- background position analysis / pondering support

### Notes

- `main.py` is currently only a minimal placeholder and is not the main way to
  run the project.
- TensorFlow startup logging is intentionally suppressed in the entrypoints to
  reduce native backend noise during launch.
- This repository does not include a training pipeline; it assumes you already
  have compatible weights.
