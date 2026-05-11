# Text to Speech App

This project now runs as a Flask web app and serves a browser-based text-to-speech interface.

## Features

- Upload PDF or DOCX files
- Extract text in browser
- Read text aloud using browser speech synthesis
- Stop reading anytime

## Project Structure

```text
text_to_speech/
|-- main.py
|-- templates/
|   `-- index.html
|-- static/
|   |-- styles.css
|   `-- script.js
|-- requirements.txt
|-- .gitignore
`-- README.md
```

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

Then open the local URL shown in terminal (usually `http://127.0.0.1:5000`).

## Notes

- Browser mode supports `.pdf` and `.docx` reading.
- `.doc` files are not reliably supported in browser parsing.
- `main.py` is now used to render the web app through Flask.
