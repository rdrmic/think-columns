import sys
import os

import pygame


__version__ = '0.4.1'


blocksize = 14
nr_columns = 6
nr_rows = 18
arena = pygame.rect.Rect((32, 75), (nr_columns * blocksize, nr_rows * blocksize))

colors = {
    'black': (0, 0, 0),
    'gray': (128, 128, 128) #(128, 255, 128) - neon green
}
blockcolors = {
    'white': (198, 216, 216),
    'red': (255, 0, 0),
    'green': (2, 192, 2),
    'blue': (0, 48, 255),
    'orange': (255, 114, 0),
    'yellow': (234, 228, 2),
    'violet': (153, 21, 153)
}

grid = None
handler = None
highscore = None


def load_resources():
    target_attr = 'load_game_resources'
    for module in sys.modules.values():
        if hasattr(module, target_attr):
            getattr(module, target_attr)()

def load_image(filename, colorkey=None):
    path = os.path.join('data', filename)
    try:
        image = pygame.image.load(path)
    except pygame.error, message:
        print 'Cannot load image:', path #
        raise SystemExit, message
    image = image.convert()
    if colorkey != None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image



if __name__ == '__main__': print 'version', __version__,; raw_input()
