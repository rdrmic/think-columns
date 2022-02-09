import pygame

import game
import screen


hit_img = None
score_img = None
rank_img = None
hscore_img = None
valuefont = None
messagefont = None


# LOADINGS----------------------------------------------------------------------
def load_game_resources():
    global hit_img, score_img, rank_img, hscore_img
    hit_img = game.load_image('hit.png')
    score_img = game.load_image('score.png')
    rank_img = game.load_image('rank.png')
    hscore_img = game.load_image('hscore.png')

    global valuefont, messagefont
    valuefont = pygame.font.Font('data/slkscr.ttf', 15)
    valuefont.set_bold(1)
    valuefont.set_italic(1)
    messagefont = pygame.font.Font('data/slkscr.ttf', 38)
    messagefont.set_bold(1)
    messagefont.set_italic(0)
# ------------------------------------------------------------------------------


# STATS POSITIONS----------------------------------------------------------TO DO
#titles:
titles_left = game.arena.right + game.blocksize + 8
titles_startingtop = 175
dist = game.blocksize * 3
titles_tops = range(
    titles_startingtop, titles_startingtop + dist*4, dist
)
#values:
values_left = game.arena.right + game.blocksize
values_tops = [9 + top for top in titles_tops]
# -----------------------------------------------------------------------------/


# DRAW ARENA BORDER & STATS TITLES----------------------------------------------
def draw_arena_border():
    borderrect = game.arena.inflate(2, 2) #one pixel on every side
    pygame.draw.rect(screen.surface, game.colors['gray'], borderrect, 1)


hscore_rect = None ###

def draw_titles(): #
    hit_rect = hit_img.get_rect(topleft=(titles_left, titles_tops[0]))
    score_rect = score_img.get_rect(topleft=(titles_left, titles_tops[1]))
    rank_rect = rank_img.get_rect(topleft=(titles_left, titles_tops[2]))
    global hscore_rect ###
    hscore_rect = hscore_img.get_rect(topleft=(titles_left, titles_tops[3]))

    screen.blit(hit_img, hit_rect)
    screen.blit(score_img, score_rect)
    screen.blit(rank_img, rank_rect)
    screen.blit(hscore_img, hscore_rect)

def flash_hscore(): ###
##    screen.erase(hscore_rect)
    pass
# ------------------------------------------------------------------------------


# HUD----------------------------------------------------------------------TO DO
class Hud:
    def __init__(self):
        self.hitpos = values_left, values_tops[0]
        self.hitrect = pygame.Rect(self.hitpos, (0,0))
        self.scorepos = values_left, values_tops[1]
        self.rankpos = values_left, values_tops[2]
        self.hscorepos = values_left, values_tops[3]

        self.bgcolor = game.colors['black']

    def new(self):
        draw_arena_border()
        draw_titles()
        self.show_score(0)
        self.show_rank('-')
        self.show_hscore(game.highscore)

    def show_hit(self, hit):
        img = valuefont.render(str(hit), 1, game.blockcolors['blue'], self.bgcolor)
        self.hitrect.size = img.get_size()
        screen.blit(img, self.hitrect)

    def erase_hit(self):
        screen.erase(self.hitrect)

    def show_score(self, score):
        img = valuefont.render(str(score), 1, game.blockcolors['orange'], self.bgcolor)
        rect = img.get_rect(topleft=self.scorepos)
        screen.blit(img, rect)

    def show_rank(self, rank):
        img = valuefont.render(str(rank), 1, game.blockcolors['green'], self.bgcolor)
        rect = img.get_rect(topleft=self.rankpos)
        screen.blit(img, rect)

    def show_hscore(self, hscore):
        img = valuefont.render(str(hscore), 1, game.blockcolors['red'], self.bgcolor)
        rect = img.get_rect(topleft=self.hscorepos)
        screen.blit(img, rect)
# -----------------------------------------------------------------------------/


# MESSAGES-----------------------------------------------------------------TO DO
class Message:
    def __init__(self, text, timer=0, start=0):
        self.img = messagefont.render(text, 1, game.blockcolors['green'], game.colors['black'])
        width = 220
        height = self.img.get_height()
        if self.img.get_width() > width:
            self.img = pygame.transform.scale(self.img, (width, height))
        self.rect = self.img.get_rect(topleft=(10, 345))

        self.timer = timer
        self.start = start
        self.ticks = 0
        if not self.start:
            self.paint()

    def tick(self):
        self.ticks += 1
        if self.ticks == self.start:
            self.paint()
            self.start = 0
        if self.ticks == self.timer:
            self.ticks = 0
            self.erase()

    def paint(self):
        #self.erase() #
        screen.blit(self.img, self.rect)

    def erase(self):
        screen.erase(self.rect)
# -----------------------------------------------------------------------------/
