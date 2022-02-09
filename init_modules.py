allmodules = """
main
game
screen
grid
scoring
hud
blocks
gameinit
gamemenu
gameplay
"""

def multi_import(modules):
    for m in modules.split('\n'):
        if m:
            __import__(m)



multi_import(allmodules)
