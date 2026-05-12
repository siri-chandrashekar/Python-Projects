# Color Palette Generator

A Flask app that extracts dominant colors from an uploaded image and shows them as a palette with HEX values.

## Features

- Upload any image file
- Extract up to 10 dominant colors
- Display clean swatches with HEX codes
- Responsive UI with separated static CSS

## Tech Stack

- Python
- Flask
- Pillow (PIL)

## Project Structure

```text
color_palette_generator/
|-- main.py
|-- requirements.txt
|-- .gitignore
|-- README.md
|-- templates/
|   `-- index.html
`-- static/
    `-- style.css
```

## Setup

1. Open terminal in this folder.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

Open the app at `http://127.0.0.1:5000`.

## Notes

- Best results come from clear, well-lit images.
- Very large images are automatically resized before analysis for speed.
