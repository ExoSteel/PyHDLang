import pygame as pg
from pygame.locals import *
from fonts.fontManager import *
from constants import *
# Save logic diagram/truth table menu WIP

class Widget:
    pass

class InputBox(Widget):
    pass

class Slider(Widget):
    pass

class Menu:
    def __init_(self):
        pass

class SaveMenu(Menu):
    pass

if __name__ == "__main__":
    pg.init()
    clock = pg.time.Clock()
    WIDTH, HEIGHT = 1000, 750
    running = True
    userText = ""
    win = pg.display.set_mode((WIDTH,HEIGHT))

    while running:
        cursorCoords = pg.mouse.get_pos()
        cursorCoordsRel = pg.mouse.get_rel()
        cursorClicks = pg.mouse.get_pressed(num_buttons=3)
        keyState = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 3:
                    pg.draw.rect(win, WHITE, (cursorCoords[0], cursorCoords[1], WIDTH*0.2, WIDTH*0.2))

                pass

        if keyState[pg.K_ESCAPE]:
            print("exit")
            running = False
        if keyState[pg.K_w]: #debug
            print("gay", cursorCoords, cursorClicks, cursorCoordsRel, f"{clock.get_fps():.0f}")

        clock.tick(500)
        pg.display.update()
    
    pg.quit()