import json
from flask import Flask
from flask import render_template, request
from PIL import Image

app = Flask(__name__, template_folder="./")

SIZES = [('M', 70), ('XS', 30), ('S', 50), ('L', 90), ('XL', 120)]
DEFAULT = ['  ', '. ', '..', '.-', '--', '-+', '++', '**', 'HH', 'H#', '##']
PALETTES = {'Default': DEFAULT}
PALETTES.update(json.loads(file("palette.json").read()))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        f = request.files.get('file')
        size = int(request.form['size'])
        inverse = True if request.form.get('inverse') else False
        palette = PALETTES[request.form['palette']]
        try:
            im = Image.open(f)
            if not inverse:
                palette = list(reversed(palette))
                palette.append(palette[-1])
            shadow_step = 255 / (len(palette) - 1)
            w_h = float(im.height) / im.width
            im = im.resize((size, int(size * w_h)))
            im = im.convert(mode="L")
            text = ""
            for i in range(im.height):
                for j in range(im.width):
                    p = im.getpixel((j, i))
                    text += palette[p / shadow_step]
                text += "\n"
        except Exception as e:
            error = "Failed to create ANSI picture. Check your image file"
            return render_template("index.html", sizes=SIZES,
                                   palettes=PALETTES, error=error)
        return render_template("index.html", image=text, inverse=inverse,
                               sizes=SIZES, palettes=PALETTES)
    else:
        return render_template("index.html", sizes=SIZES, palettes=PALETTES)


app.run(port=4000, host='0.0.0.0')
