from PIL import Image
from flask import Flask, render_template, request

app = Flask(__name__)

def rgb_to_hex(color):
    return '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])

@app.route('/', methods=['GET', 'POST'])
def index():
    colors = []

    if request.method == 'POST':
        file = request.files.get('image')

        if file and file.filename:
            image = Image.open(file).convert("RGB")

            # Shrink large images first so color analysis stays fast.
            image.thumbnail((250, 250))

            quantized = image.quantize(colors=10, method=Image.Quantize.MEDIANCUT)
            color_counts = quantized.getcolors()

            if color_counts:
                palette = quantized.getpalette()
                top_colors = []

                for count, color_index in sorted(color_counts, reverse=True)[:10]:
                    start = color_index * 3
                    rgb = tuple(palette[start:start + 3])
                    top_colors.append(rgb)

                colors = [rgb_to_hex(color) for color in top_colors]


    return render_template('index.html', colors=colors)


if __name__ == '__main__':
    app.run(debug=True)
