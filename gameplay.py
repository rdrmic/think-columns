# ALL STATES TICKS: start, (levelstart), fall, sd   --> ticks

import random

import pygame
from pygame.constants import *

import game
import grid
import screen
import hud
import blocks
import scoring


class GamePlay:
    def __init__(self, prevhandler):
        self.prevhandler = prevhandler
        self.hud = hud.Hud()
        self.scoring = scoring.Scoring()
        self.transporter = blocks.Transporter()
        self.blocksdown = blocks.BlocksDown()
        self.objects = [self.transporter, self.blocksdown] # self.(all)blocks
        #self.frame = 0
        self.events = [] ######
        #self.level = 1
        self.state = ''
        self.state_tick = self.dummyfunc
        self.prevscore = 0
        self.prevrank = 0
        self.prevhscore = game.highscore
        self.message = hud.Message('')

    def start(self): ###
        game.grid = grid.Grid() # garbage collecting?
        screen.surface.fill(game.colors['black'])
        self.hud.new() #
        self.transporter.new() #
        pygame.key.set_repeat(200, 25) #
        pygame.display.update()

        self.change_state('gamestart')

    def handle(self, event): ###
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.change_state('gameover')
##            if event.key == K_RETURN or event.key == K_KP_ENTER or event.key == K_PAUSE:
##                self.events.append('pause')
            if event.key == K_SPACE:
                self.events.append('drop')
            elif event.key == K_LEFT:
                self.events.append('left')
            elif event.key == K_RIGHT:
                self.events.append('right')
            elif event.key == K_UP:
                self.events.append('up')
            elif event.key == K_DOWN:
                self.events.append('down')

    def dummyfunc(self): pass

    def change_state(self, state):
        getattr(self, self.state+'_end', self.dummyfunc)() ###
        self.state = state
        getattr(self, state+'_start', self.dummyfunc)()
        self.state_tick = getattr(self, state+'_tick')

    def run(self):
        #self.frame += 1
        self.state_tick()
        for o in self.objects:
            if o.changed:
                o.erase()
                o.paint()
        if self.message.timer:
            self.message.tick()
        if self.events:
            del self.events[:]


#GAME START:
    def gamestart_start(self):
        self.start_ticks = 0

    def gamestart_tick(self):
        self.start_ticks += 1
        if self.events:
            if self.start_ticks > 20:
                self.message.erase()
            self.change_state('falling')
        elif self.start_ticks == 20:
            self.message = hud.Message('start!')

#LEVEL START: ###
    def levelstart_start(self):
        self.levelstart_ticks = 0

    def levelstart_tick(self):
        self.levelstart_ticks += 1
#----------------

###PAUSE:
##    def pause_start(self):
##        pass
##
##    def pause_tick(self):
##        pass

#FALLING:
    def falling_start(self):
        self.fall_ticks = 0
        self.transporter.new()

    def falling_tick(self):
        self.fall_ticks += 1
        if self.fall_ticks == 20: #
            self.fall_ticks = 0
            self.events.insert(1, 'fall') #after 'drop', but before others
            hscore = self.scoring.hscore
            if hscore != self.prevhscore:
                self.prevhscore = hscore
                self.hud.show_hscore(hscore)
        if self.events:
            for event in self.events:
                if event == 'drop':
                    self.transporter.drop()
                    self.fall_ticks = 0
                    break
                elif event == 'fall':
                    self.transporter.fall()
                    break #
                elif event == 'left':
                    self.transporter.move_left()
                elif event == 'right':
                    self.transporter.move_right()
                elif event == 'up':
                    self.transporter.shuffle('up')
                elif event == 'down':
                    self.transporter.shuffle('down')

            if self.transporter.arrived: ### gameover is not ok !!!
                self.blocksdown.take(self.transporter)
                if game.grid.take(self.transporter):
                    self.change_state('searchdestroy')
                else:
                    self.change_state('gameover')

#SEARCH AND DESTROY:
    def searchdestroy_start(self):
        self.sd_ticks = 0

    def searchdestroy_tick(self):
        self.sd_ticks += 1 
        if not game.grid.to_kill and not game.grid.to_drop:
            #print game.grid
            matches = game.grid.search()
            if matches:
                self.scoring.process(matches)
                self.hud.show_hit(self.scoring.hit)
            else:
                score = self.scoring.score
                if score != self.prevscore:
                    self.prevscore = score
                    self.hud.show_score(score)
                    #updating rank:
                    rank = self.scoring.rank
                    if rank != self.prevrank:
                        self.prevrank = rank
                        self.hud.show_rank(rank)
                    #-------------
                    self.scoring.reset()
                    hud.flash_hscore() ###
                self.change_state('falling')
                self.hud.erase_hit()
                return
        elif game.grid.to_kill:
            if self.sd_ticks == 20:
                self.blocksdown.kill_matches()
                if self.scoring.multi and self.scoring.chain:
                    self.message = hud.Message('multi: +%d' % self.scoring.multi, 20)
                    self.message = hud.Message('chain: +%d' % self.scoring.chain, 40, 20)
                elif self.scoring.multi:
                    self.message = hud.Message('multi: +%d' % self.scoring.multi, 40)
                elif self.scoring.chain:
                    self.message = hud.Message('chain: +%d' % self.scoring.chain, 40)
        elif self.sd_ticks == 40:
            if game.grid.to_drop:
                self.blocksdown.drop_hanging()
            self.sd_ticks = 0

#GAME OVER:
    def gameover_start(self):
        self.message = hud.Message('game over')
        game.highscore = self.scoring.hscore #
        self.allblocks = filter(lambda b: game.arena.contains(b.rect), self.transporter.sprites())
        self.allblocks.extend(self.blocksdown.sprites())
        self.clear_blocks = 0

    def gameover_tick(self):
        if self.events:
            self.clear_blocks = 1
        if self.clear_blocks:
            for i in range(6): #number of blocks that disappear in one tick
                if not self.allblocks:
                    game.handler = self.prevhandler
                    pygame.display.update()
                    pygame.time.wait(500)
                    return
                b = random.choice(self.allblocks)
                self.allblocks.remove(b)
                screen.erase(b.rect)
                b.kill()
                del b
        pygame.key.set_repeat() #
