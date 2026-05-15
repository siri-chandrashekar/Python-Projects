# Space Invaders (Turtle)

A simple Space Invaders-style game built with Python `turtle`.

## Features
- Move cannon left/right with arrow keys
- Shoot lasers with spacebar
- Increasing alien speed as score grows
- Game over state
- Restart support: click `RESTART` button or press `r`

## Requirements
- Python 3.10+
- No third-party dependencies

## Run
```bash
python main.py
```

## Controls
- `Left Arrow`: move left
- `Right Arrow`: move right
- `Space`: fire laser
- `r`: restart after game over
- `q`: quit

## Notes
- Uses screen timers (`ontimer`) for the game loop and alien spawning.
- If restart button click is missed, use keyboard `r`.
