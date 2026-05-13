# BBC US & Canada News Scraper

Simple Python scraper that collects BBC News cards tagged **US & Canada** and exports them to CSV.

## Requirements
- Python 3.10+
- `requests`
- `beautifulsoup4`

## Install
```bash
pip install -r requirements.txt
```

## Run
```bash
python main.py
```

Output file:
- `bbc_us_canada_news.csv` (created only when articles are found)

## Notes
- The script includes request timeout and network error handling.
- If BBC changes page structure, selector updates may be needed.
