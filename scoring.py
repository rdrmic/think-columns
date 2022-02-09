import pickle

import game


highscores = None

def load_game_resources():
    global highscores
    try:
        f = file('data\hs', 'rb')
        highscores = pickle.load(f)
        game.highscore = highscores[1]
    except:
        game.highscore = 0


def save_highscores(): ###
    if game.highscore == 0: # and 'different from old highsore':
        return
    f = file('data\hs', 'wb')
    pickle.dump({1: game.highscore}, f, 1)


class Scoring:
    def __init__(self):
        self.hit = 0
        self.score = 0
        self.rank = 0
        self.hscore = game.highscore #

        self.multi = 0
        self.chain = -1

    def process(self, matches):
        points = 0
        for match in matches:
            points += match / 3 + match % 3
        self.multi = len(matches) - 1
        self.chain += 1

        self.hit += points + self.multi + self.chain
        self.score += self.hit
        self.check_rank()
        if self.score > self.hscore:
            self.hscore = self.score

    def check_rank(self):
        pass

    def reset(self):
        self.hit = 0
        self.multi = 0
        self.chain = -1
        
