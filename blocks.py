import random

import pygame
from pygame.rect import Rect

import game
import screen


surfaces = None

def load_game_resources():
    create_block_surfaces()


def create_block_surfaces():
    global surfaces
    surfaces = {
        'R': make_surface(game.blockcolors['red']),
        'G': make_surface(game.blockcolors['green']),
        'B': make_surface(game.blockcolors['blue']),
        'O': make_surface(game.blockcolors['orange']),
        'Y': make_surface(game.blockcolors['yellow']),
        'V': make_surface(game.blockcolors['violet']),
        'W': make_surface(game.blockcolors['white'])
    }
    surfaces = surfaces.items()

def make_surface(color):
        surface = pygame.Surface((game.blocksize, game.blocksize)).convert()
        surface.fill(color)
        return surface


def create_startpositions(startpoint, nr_fields):
    return [startpoint + game.blocksize * field for field in range(nr_fields)]

def erase_block(surface, rect):
    surface.fill(game.colors['black'], rect)


class Block(pygame.sprite.Sprite):
    def __init__(self, left, top):
        pygame.sprite.Sprite.__init__(self)
        self.colorkey, self.image = random.choice(surfaces)
        self.rect = Rect((left, top), (game.blocksize, game.blocksize))


class Transporter(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.nr_blocks = 3 # game.nr_blocks
        self.width = game.blocksize
        self.height = game.blocksize * self.nr_blocks
        self.startingtop = game.arena.top - self.height
        self.leftstartpositions = create_startpositions(game.arena.left, game.nr_columns)
        self.topstartpositions = create_startpositions(self.startingtop, self.nr_blocks)
        self.rect = None
        self.lastrect = None
        self.changed = False
        self.arrived = False

    def new(self):
        startingleft = random.choice(self.leftstartpositions)
        self.rect = Rect((startingleft, self.startingtop), (self.width, self.height))
        self.empty()
        for block_top in self.topstartpositions:
            self.add(Block(startingleft, block_top)) #creation of boxes
        self.changed = False
        self.arrived = False

    def fall(self):
        columntop = game.grid.columntop(self.rect.left)
        self.rect.top += game.blocksize
        for b in self.sprites():
            b.rect.top += game.blocksize
        if not self.rect.bottom < columntop:
            self.arrived = True
        self.changed = True

    def drop(self):
        columntop = game.grid.columntop(self.rect.left)
        dist = columntop - self.rect.bottom
        self.rect.top += dist
        for b in self.sprites():
            b.rect.top += dist
        self.changed = True
        self.arrived = True

    def move_left(self):
        if self.rect.left > game.arena.left:
            column_left = self.rect.left - game.blocksize
            columntop = game.grid.columntop(column_left)
            if not self.rect.bottom > columntop:
                self.rect.left -= game.blocksize
                for b in self.sprites():
                    b.rect.left -= game.blocksize
                if self.rect.bottom == columntop:
                    self.arrived = True
                self.changed = True

    def move_right(self):
        if self.rect.right < game.arena.right:
            column_right = self.rect.left + game.blocksize
            columntop = game.grid.columntop(column_right)
            if not self.rect.bottom > columntop:
                self.rect.left += game.blocksize
                for b in self.sprites():
                    b.rect.left += game.blocksize
                if self.rect.bottom == columntop:
                    self.arrived = True
                self.changed = True

    def shuffle(self, direct):
        bottompos = self.rect.bottom - game.blocksize
        if direct == 'up':
            for b in self.sprites():
                if b.rect.top != self.rect.top:
                    b.rect.top -= game.blocksize
                else:
                    b.rect.top = bottompos
        if direct == 'down':
            for b in self.sprites():
                if b.rect.top != bottompos:
                    b.rect.top += game.blocksize
                else:
                    b.rect.top = self.rect.top
        self.changed = True

    def erase(self):
        self.clear(screen.surface, erase_block)
        if self.arrived:
            if self.lastrect:
                screen.dirty(self.lastrect)
            self.lastrect = None

    def paint(self):
        if self.rect.bottom > game.arena.top:
            if game.arena.contains(self.rect):
                for b in self.sprites():
                    r = screen.surface.blit(b.image, b.rect)
                    self.spritedict[b] = r
                screen.dirty2(self.rect, self.lastrect)
                self.lastrect = Rect(self.rect)
            else:
                b_rects = 0
                for b in self.sprites():
                    if game.arena.contains(b.rect):
                        r = screen.surface.blit(b.image, b.rect)
                        self.spritedict[b] = r
                        b_rects += 1
                new_height = game.blocksize * b_rects
                short_rect = Rect((self.rect.left, self.rect.bottom - new_height), (self.width, new_height))
                screen.dirty2(short_rect, self.lastrect)
                self.lastrect = Rect(short_rect)
        self.changed = False


class BlocksDown(pygame.sprite.RenderUpdates):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.changed = False

    def take(self, transporter):
        for b in transporter.sprites():
            if b.rect.bottom > game.arena.top:
                self.add(b)
        self.changed = True

    def kill_matches(self):
        for pos in game.grid.to_kill:
            for b in self.sprites():
                if pos == b.rect.topleft:
                    b.kill()
                    del b
        del game.grid.to_kill[:]
        self.changed = True

    def drop_hanging(self):
        for drop in game.grid.to_drop:
            for b in self.sprites():
                if drop[0] == b.rect.topleft:
                    b.rect.top += drop[1]
        del game.grid.to_drop[:]
        self.changed = True

    def erase(self):
        self.clear(screen.surface, erase_block)

    def paint(self):
        dirty_blocks = self.draw(screen.surface)
        if dirty_blocks:
            dirty_area = dirty_blocks[0].unionall(dirty_blocks[1:])
            screen.dirty(dirty_area)
