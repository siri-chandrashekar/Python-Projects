# WaterMarkly.photos

A simple and polished desktop app built with Python Tkinter and Pillow for adding text watermarks to images.

## Features

- Upload PNG, JPG, or JPEG images.
- Add a custom text watermark.
- Save the watermarked image as a PNG file.
- Clear/reset the form with one click.
- Clean, modern Tkinter UI.

## Screenshots

Add screenshots here if you want to show the interface.

## Requirements

- Python 3.9+
- Pillow

> Tkinter is included with most Python installs, but on some Linux systems you may need to install it separately through your package manager.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/watermarkly.photos.git
cd watermarkly.photos
```

2. Install dependencies:

```bash
pip install pillow
```

## Run the app

```bash
python main.py
```

## Usage

1. Click **Upload Image** and choose a photo.
2. Type your watermark text.
3. Click **Add Watermark**.
4. Choose where to save the output file.
5. Use **Clear** to reset the form.

## Project structure

```text
watermarkly.photos/
├── app.py
├── README.md
```

## Notes

- The app saves watermarked images as PNG.
- If `arial.ttf` is not available, the app falls back to the default Pillow font.
- For best results, use a large, high-quality image.

## License

Add your preferred license here.