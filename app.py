import os
import datetime
import uuid
import logging
from flask import Flask, render_template, request, abort, Blueprint, session, \
    redirect
from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel, _
import ansiart as art

LOG = logging.getLogger('ANSIArt')
hdlr = logging.FileHandler('ansiart.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
LOG.addHandler(hdlr)
LOG.setLevel(logging.INFO)

app = Flask(__name__)
app.config.from_pyfile('config.py')

main = Blueprint("main", __name__)

db = SQLAlchemy(app)
cache = Cache(app, config=app.config)
babel = Babel(app)


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


@babel.localeselector
def get_locale():
    return session.get('lang_code', app.config['BABEL_DEFAULT_LOCALE'])


@app.url_value_preprocessor
def get_lang_code(endpoint, values):
    if values is not None:
        lang_code = values.pop('lang_code', None)
        if not lang_code and session.get('lang_code'):
            return redirect("/%s/%s" % (session.get('lang_code'), endpoint))
        if lang_code and lang_code not in app.config[
            'SUPPORTED_LANGUAGES'].keys():
            return abort(404)
        session['lang_code'] = lang_code


@main.route('/')
@cache.cached(timeout=3600)
def index():
    return render_template("index.html", sizes=SIZES,
                           palettes=PALETTES)


@main.route('/upload', methods=['GET', 'POST'])
def create_picture():
    if request.method == 'POST':
        f = request.files.get('file')
        size = int(request.form['size'])
        inverse = True if request.form.get('inverse') else False
        palette = request.form['palette']
        LOG.info(_("New request. Params: %s") % [size, inverse, palette])
        filename = str(uuid.uuid4())
        filepath = os.path.join('/tmp', filename)
        f.save(filepath)
        try:
            image = art.get_art(filepath, size=size,
                                inverse=inverse,
                                palette=art.PALETTE_MAP[palette])
            picture = Picture(filename, image, inverse)
            db.session.add(picture)
            db.session.commit()
        except Exception as e:
            LOG.error(
                    _("Failed to create ANSI picture. Reason: %(error)s",
                      error=e))
            error = _("Failed to create ANSI picture. Check your image file")
            return render_template("index.html", sizes=SIZES,
                                   palettes=PALETTES, error=error)
        os.remove(filepath)
        link = filename
        return render_template("index.html", image=image,
                               inverse=inverse,
                               sizes=SIZES,
                               palettes=PALETTES, link=link)


@main.route('/view/<id>')
@cache.cached(timeout=3600)
def get_picture(id):
    raise Exception
    picture = Picture.query.get(id)
    if not picture:
        return "", 404
    db.session.add(picture)
    db.session.commit()
    return render_template("picture_view.html", image=picture.text,
                           inverse=picture.inverse)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html")


LOG.info(_("ANSIART Started!!!"))
app.register_blueprint(main, url_prefix="/<lang_code>")
app.register_blueprint(main)
app.run(port=4000, host='0.0.0.0')
