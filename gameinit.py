#no threads are harmed during creation of this module...

import pygame
from pygame.constants import * #

import game
import screen
import gamemenu


title_img = None

def load_game_resources():
    global title_img
    title_img = game.load_image('splash_title.png', game.colors['black'])


def get_input(): # reuse?
    for event in pygame.event.get():
        if event.type == QUIT:
            return -1
        if event.type == KEYDOWN:
            if event.mod & KMOD_LALT and event.key == K_F4:
                return -1
            elif not event.key == K_LALT:
                return 1


class GameInit:
    def __init__(self):
        self.titleimg = title_img
        self.titlerect = self.titleimg.get_rect(topleft=(20,138))
        self.nexthandler = gamemenu.GameMenu()

    def start(self):
        pass

    def user_quit(self):
        input = get_input()
        if input:
            if input == -1:
                self.nexthandler = None
            return 1

    def intro_animation(self):
        wait = pygame.time.wait
        wait(100)
        for i in range(0, 256, 3):
            self.titleimg.set_alpha(i, RLEACCEL)
            screen.blit(self.titleimg, self.titlerect)
            screen.update()
            screen.erase(self.titlerect)
            wait(15)
            if self.user_quit(): return
        for i in range(14):
            wait(100)
            if self.user_quit(): return

    def handle(self, event):
        pass

    def run(self):
        self.intro_animation()
        if self.nexthandler:
            screen.update() #already erased...
            for i in range(4):
                pygame.time.wait(100)
                if self.user_quit(): break
        game.handler = self.nexthandler
