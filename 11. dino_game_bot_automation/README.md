# Dino Game Bot Automation

Automates Chrome Dino gameplay using screenshot-based obstacle detection and keyboard control.

## Features
- Screen-region calibration mode
- Obstacle detection for cactus and birds
- Adaptive jump timing and follow-up jumps
- Optional debug frame capture (`v`) and stop hotkey (`z`)

## Requirements
- Python 3.10+
- Chrome Dino game running in a visible browser window
- Windows/macOS/Linux desktop session (not headless)

## Install
```bash
pip install -r requirements.txt
```

## Run
```bash
python main.py
```

## Usage
1. Start the script.
2. Type `c` + Enter to calibrate (recommended) or press Enter for default region.
3. Focus the Dino game during countdown.
4. Press `z` to stop.

## Notes
- Detection depends on game region and display scaling.
- Use `v` during runtime to save `debug_frame.png` for tuning.
