# Breakout Game

A classic Breakout-style arcade game built with Python and Tkinter.

## Features

- Paddle movement with left and right arrow keys
- Ball collision with walls, paddle, and bricks
- Brick destruction and live score updates
- Ball speed increases as bricks are hit
- Game over screen when the ball falls below the paddle
- Win screen when all bricks are cleared
- Restart button to start a fresh round

## Requirements

- Python 3.x
- Tkinter (included with most Python installations)

No third-party packages are required.

## How to Run

1. Open a terminal in this folder:

```bash
python main.py
```

## Controls

- `Left Arrow`: Move paddle left
- `Right Arrow`: Move paddle right
- `Restart` button: Start a new game

## Project Structure

```text
breakout_game/
|-- main.py
|-- ball.py
|-- paddle.py
|-- bricks.py
|-- scores.py
|-- README.md
`-- .gitignore
```

## Gameplay Logic

- `main.py` creates the window, canvas, restart button, and game loop.
- `ball.py` handles movement, collisions, speed increase, win/loss states.
- `paddle.py` handles keyboard input and paddle movement boundaries.
- `bricks.py` generates the brick grid.
- `scores.py` tracks and renders score on screen.

## Future Improvements

- Add lives system and level progression
- Add start/pause menu
- Add sound effects and background music
- Track high score across sessions

## License

This project is for learning and personal use.
