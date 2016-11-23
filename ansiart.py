import sys
import json
from PIL import Image

SIZE = 30
DEFAULT = ['  ', '. ', '..', '.-', '--', '-+', '++', '**', 'HH', 'H#', '##']
PALETTE_MAP = {'Default': DEFAULT}
try:
    PALETTE_MAP.update(json.loads(file("palette.json").read()))
except:
    pass


def get_art(path, size=SIZE, inverse=True, palette=DEFAULT):
    im = Image.open(path)
    if not inverse:
        palette = list(reversed(palette))
        palette.append(palette[-1])
    shadow_step = 255 * 3 / (len(palette) - 1)
    w_h = float(im.height) / im.width
    im = im.resize((size, int(size * w_h)))
    text = ""
    for i in range(im.height):
        for j in range(im.width):
            p = im.getpixel((j, i))
            text += palette[sum(p) / shadow_step]
        text += "\n"
    return text


if __name__ == '__main__':
    path = sys.argv[1]
    size = int(sys.argv[2]) if len(sys.argv) > 2 else SIZE
    pal = sys.argv[3] if len(sys.argv) > 3 else 'Default'
    inv = bool(sys.argv[4]) if len(sys.argv) > 4 else True
    print get_art(path, size=size, inverse=inv, palette=PALETTE_MAP[pal])
