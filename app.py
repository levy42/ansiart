import datetime
import json
import logging
import uuid
from flask import Flask, Blueprint
from flask import render_template, request, redirect, abort, g
from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel, _
from PIL import Image

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
    share_image = db.Column(db.String)
    created_at = db.Column(db.DATETIME, default=datetime.datetime.now)
    updated_at = db.Column(db.DATETIME, onupdate=datetime.datetime.now)

    def __init__(self, id, text, inverse=True):
        self.id = id
        self.text = text
        self.inverse = inverse
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()


SIZE = 30
DEFAULT = ['  ', '. ', '..', '.-', '--', '-+', '++', '**', 'HH', 'H#', '##']
PALETTES = {'Default': DEFAULT}
PALETTES.update(json.loads(file("palette.json").read()))
SIZES = [('M', 70), ('XS', 30), ('S', 50), ('L', 90),
         ('XL', 120)]


@babel.localeselector
def get_locale():
    return g.get('lang_code', app.config['BABEL_DEFAULT_LOCALE'])


@main.url_value_preprocessor
def get_lang_code(endpoint, values):
    if values is not None:
        g.lang_code = values.pop('lang_code', None)


@main.before_request
def ensure_lang_support():
    lang_code = g.get('lang_code', None)
    if lang_code and lang_code not in app.config['SUPPORTED_LANGUAGES'].keys():
        return abort(404)


@main.url_defaults
def set_language_code(endpoint, values):
    if g.get('lang_code') in values or not g.get('lang_code',
                                                             None):
        return
    if app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
        values['lang_code'] = g.get('lang_code')


# @main.url_value_preprocessor
# def get_lang_code(endpoint, values):
#     if values is not None:
#         lang_code = values.get('lang_code', None)
#         session['redirected'] = lang_code is not None
#         if lang_code in app.config['SUPPORTED_LANGUAGES'].keys():
#             session['lang_code'] = lang_code
#             values.pop('lang_code')
#         elif lang_code:
#             abort(404)
#
#
# @main.before_request
# def locale_redirect():
#     if not session.get('redirected') and session.get('lang_code'):
#         session['redirected'] = True
#         return redirect(
#                 "/%s%s" % (session.get('lang_code') or "",
#                            request.path if request.path != "/" else ""))


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        f = request.files.get('file')
        size = int(request.form['size'])
        inverse = True if request.form.get('inverse') else False
        palette = PALETTES.get(request.form['palette'], DEFAULT)
        LOG.info(_("New request. Params: %s") % [size, inverse, palette])
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
            id = str(uuid.uuid4())
            picture = Picture(id, text, inverse)
            db.session.add(picture)
            db.session.commit()
            return redirect("/%s/%s" % (get_locale(), id))
        except Exception as e:
            LOG.error(
                    _("Failed to create ANSI picture. Reason: %(error)s",
                      error=e))
            error = _("Failed to create ANSI picture. Check your image file")
            return render_template("index.html", sizes=SIZES,
                                   palettes=PALETTES, error=error)
    else:
        return render_template("index.html", sizes=SIZES,
                               palettes=PALETTES)


@main.route('/<id>/')
@cache.cached(timeout=3600)
def get_picture(id):
    picture = Picture.query.get(id)
    if not picture:
        return "", 404
    db.session.add(picture)
    db.session.commit()
    return render_template("index.html", image=picture.text,
                           inverse=picture.inverse, sizes=SIZES,
                           palettes=PALETTES, id=id)


@main.route('/<id>/share/', methods=['POST'])
def share(id):
    picture = Picture.query.get(id)
    if not picture:
        return "", 404
    if picture.share_image:
        return picture.share_image
    size = app.config.get('SHARE_IMAGE_SIZE', 562)
    f = request.files.get('file')
    im = Image.open(f)
    w_h = float(im.height) / im.width
    im = im.resize((size, int(size * w_h)), resample=Image.LANCZOS)
    path = "static/share_images/" + id + ".jpg"
    im.save(path)
    picture.share_image = path
    db.session.add(picture)
    db.session.commit()
    return "/" + path


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html")


if __name__ == '__main__':
    LOG.info(_("ANSIART Started!!!"))
    app.register_blueprint(main, url_prefix="/<lang_code>")
    app.register_blueprint(main)
    app.run(port=app.config.get('PORT') or 4000,
            host=app.config.get('HOST') or '0.0.0.0')
