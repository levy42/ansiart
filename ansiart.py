import argparse
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
    return text


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Tool for generating ANSI pictures.')
    parser.add_argument('path', help='path to image (.png, .jpg or .jpeg)')
    parser.add_argument('--size', type=int, nargs='?',
                        help='size of picture to be generated, default: 60',
                        default=60)
    parser.add_argument('--palette', nargs='?',
                        help='palette name, default : "Default", '
                             'palettes are taken from "palette.json" file',
                        default='Default')
    parser.add_argument('-inverse', default=True, action='store_true',
                        help='inverse picture')

    args = parser.parse_args().__dict__
    if args.get('palette'):
        args['palette'] = PALETTE_MAP[args['palette']]
    print get_art(**args)
