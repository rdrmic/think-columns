import pygame
from pygame.constants import *

import init_modules
import game
import screen
import gameinit
import scoring


FPS = 40 #

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen.initialize()
    game.load_resources()

    game.handler = gameinit.GameInit()
    lasthandler = None
    while game.handler:
        handler = game.handler
        if handler != lasthandler:
            lasthandler = handler
            handler.start()

        for event in pygame.event.get():
            if event.type == QUIT:
                game.handler = None
                break
            if event.type == KEYDOWN: # and ...
                if event.mod & KMOD_LALT and event.key == K_F4:
                    game.handler = None
                    break
                handler.handle(event) # indent to the left? (only KEYDOWN events, or e.g. ACTIVEEVENT...)

        handler.run()
        screen.update()
        clock.tick(FPS)

    scoring.save_highscores()
    pygame.quit()



if __name__ == '__main__': main()

##    raw_input()
