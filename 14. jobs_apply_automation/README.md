# Jobs Apply Automation

A Selenium automation script that searches Python jobs on Working Nomads, filters to "Today", opens the first result, and attempts to click apply.

## Requirements
- Python 3.10+
- Google Chrome installed

## Install
```bash
pip install -r requirements.txt
```

## Run
```bash
python main.py
```

## What It Does
1. Opens Working Nomads jobs page.
2. Searches for `Python` roles.
3. Applies `Today` filter.
4. Opens first available job.
5. Clicks the apply button and waits for your manual verification/login.

## Notes
- This is a learning automation script.
- Website selectors can change over time and may require updates.
- The script closes the browser safely on exit/errors.
