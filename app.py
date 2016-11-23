import os, sys
import uuid
from flask import Flask, render_template, request
import ansiart as art
import logging

UPLOAD_FOLDER = 'uploads'
PICTURE_FOLDER = 'pictures'

LOG = logging.getLogger('ANSIArt')
hdlr = logging.FileHandler('ansiart.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
LOG.addHandler(hdlr)
LOG.setLevel(logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

PALETTES = art.PALETTE_MAP.keys()
SIZES = [('x-small', 30), ('small', 50), ('medium', 70), ('large', 90),
         ('x-large', 120)]


@app.route("/")
def index():
    return render_template("index.html", sizes=SIZES,
                           palettes=PALETTES)


@app.route('/upload', methods=['GET', 'POST'])
def create_picture():
    if request.method == 'POST':
        f = request.files.get('file')
        size = int(request.form['size'])
        inverse = True if request.form.get('inverse') else False
        palette = request.form['palette']
        image = None
        error = None
        LOG.info("New request. Params: %s" % [size, inverse, palette])
        filename = str(uuid.uuid4())
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        f.save(filepath)
        try:
            image = art.get_art(filepath, size=size,
                                inverse=inverse,
                                palette=art.PALETTE_MAP[palette])
            file(os.path.join(PICTURE_FOLDER, filename), 'w').write(image)
        except Exception as e:
            LOG.error("Failed to create ANSI picture. Reason: %s" % e)
            error = "Failed to create ANSI picture. Check your image file"
        os.remove(filepath)
        return render_template("index.html", image=image, inverse=inverse,
                               sizes=SIZES,
                               palettes=PALETTES, link=filename,
                               error=error)


@app.route('/view/<uuid>')
def get_picture(uuid):
    image = file(os.path.join(PICTURE_FOLDER, uuid)).read()
    inverse = bool(request.args.get('i'))
    return render_template("picture_view.html", image=image, inverse=inverse)


if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER, 0755)
if not os.path.exists(PICTURE_FOLDER):
    os.mkdir(PICTURE_FOLDER, 0755)

LOG.info("ANSIART Started!!!")
app.run(port=4000, host='0.0.0.0')
