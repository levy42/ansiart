import os
import datetime
import uuid
import logging
from flask import Flask, render_template, request
from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy
import ansiart as art

LOG = logging.getLogger('ANSIArt')
hdlr = logging.FileHandler('ansiart.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
LOG.addHandler(hdlr)
LOG.setLevel(logging.INFO)

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
cache = Cache(app, config=app.config)


class Picture(db.Model):
    __tablename__ = 'pictures'
    id = db.Column(db.String, primary_key=True)
    text = db.Column(db.Text)
    inverse = db.Column(db.Boolean)
    created_at = db.Column(db.DATETIME, default=datetime.datetime.now)
    updated_at = db.Column(db.DATETIME, onupdate=datetime.datetime.now)

    def __init__(self, id, text, inverse=True):
        self.id = id
        self.text = text
        self.inverse = inverse
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()


PALETTES = sorted(art.PALETTE_MAP.keys())
SIZES = [('M', 70), ('XS', 30), ('S', 50), ('L', 90),
         ('XL', 120)]


@app.route("/<lang>/")
@app.route("/")
@cache.cached(timeout=3600)
def index(lang='en'):
    if lang not in ['en', 'ua', 'ru']:
        return "", 404
    return render_template("index_%s.html" % lang, sizes=SIZES,
                           palettes=PALETTES)


@app.route('/<lang>/upload', methods=['GET', 'POST'])
@app.route('/upload', methods=['GET', 'POST'])
def create_picture(lang='en'):
    if lang not in ['en', 'ua', 'ru']:
        return "", 404
    if request.method == 'POST':
        f = request.files.get('file')
        size = int(request.form['size'])
        inverse = True if request.form.get('inverse') else False
        palette = request.form['palette']
        LOG.info("New request. Params: %s" % [size, inverse, palette])
        filename = str(uuid.uuid4())
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(filepath)
        try:
            image = art.get_art(filepath, size=size,
                                inverse=inverse,
                                palette=art.PALETTE_MAP[palette])
            picture = Picture(filename, image, inverse)
            db.session.add(picture)
            db.session.commit()
        except Exception as e:
            LOG.error("Failed to create ANSI picture. Reason: %s" % e)
            error = "Failed to create ANSI picture. Check your image file"
            return render_template("index_en.html", sizes=SIZES,
                                   palettes=PALETTES, error=error)
        os.remove(filepath)
        link = filename
        return render_template("index_%s.html" % lang, image=image,
                               inverse=inverse,
                               sizes=SIZES,
                               palettes=PALETTES, link=link)


@app.route('/<lang>/view/<id>')
@app.route('/view/<id>')
@cache.cached(timeout=3600)
def get_picture(id, lang='en'):
    picture = Picture.query.get(id)
    if not picture:
        return "", 404
    db.session.add(picture)
    db.session.commit()
    return render_template("picture_view.html", image=picture.text,
                           inverse=picture.inverse)


if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.mkdir(app.config['UPLOAD_FOLDER'], 0o755)

LOG.info("ANSIART Started!!!")
app.run(port=4000, host='0.0.0.0')
