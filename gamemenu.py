import pygame
from pygame.constants import *

import game
import screen
import gameplay


menu_img = None

def load_game_resources():
    global menu_img
    menu_img = game.load_image('menu.png')


class GameMenu:
    def __init__(self):
        pass

    def start(self):
        screen.surface.blit(menu_img, (0,0))
        pygame.display.update()

    def handle(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                game.handler = None
            elif not event.key == K_LALT:
                game.handler = gameplay.GamePlay(self)
                pygame.time.wait(200)

    def run(self):
        pass
