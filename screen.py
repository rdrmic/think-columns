import os

import pygame

import game


SIZE = 240, 400
rect = pygame.rect.Rect((0, 0), SIZE)
bgcolor = game.colors['black']

surface = None
dirtyrects = []

def initialize():
    global surface
    os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
    surface = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Think Columns")

def blit(img, rect):
    dirty(surface.blit(img, rect))

def erase(rect=rect):
    dirty(surface.fill(bgcolor, rect))

def dirty(rect):
    dirtyrects.append(rect)

def dirty2(rect1, rect2):
    if not rect2:
        dirtyrects.append(rect1)
    elif rect1.colliderect(rect2):
        dirtyrects.append(rect1.union(rect2))
    else:
        dirtyrects.append(rect1)
        dirtyrects.append(rect2)

def update():
    if dirtyrects:
        pygame.display.update(dirtyrects)
        del dirtyrects[:]
