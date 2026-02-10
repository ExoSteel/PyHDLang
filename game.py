import pygame as pg
from pygame.locals import *

pg.init()

info = pg.display.Info()

WIDTH = info.current_w / 4
HEIGHT = info.current_h / 4
win = pg.display.set_mode((WIDTH,HEIGHT), pg.RESIZABLE | pg.SCALED)

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0, 125)

BACKGROUND = (25,25,25)
BACKGROUND2 = (12,12,12)

class Block:
    def __init__(self, colour, width, height, x, y):
        self.colour = colour
        self.width = width
        self.height = height
        self.x = x
        self.y = y
    
    def setOrigin(self, x, y) -> void:
        self.x = x
        self.y = y
    
    def draw(self) -> void:
        pg.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))

    def moveTo(self, x, y) -> void:
        pg.draw.rect(win, self.colour, (x, y, self.width, self.height))
        self.x = x
        self.y = y
    
    def checkCursor(self, cursorCoords) -> bool:
        cursorX, cursorY = cursorCoords

        if cursorX >= self.x and cursorX <= self.x + self.width and cursorY >= self.y and cursorY <= self.y + self.height:
            # print("cursor inside")
            return True

class Button(Block):
    def __init__(self, colour, width, height, x, y):
        super().__init__(colour, width, height, x, y)

    def isClicked(self):
        pass
    

class Node(Block):
    def __init__(self, colour, width, height, x, y):
        super().__init__(colour, width, height, x, y)


def drawObjects(buttons, nodes=[], lines=[]) -> void:
    for button in buttons:
        button.draw()
    
    for node in nodes:
        node.draw()
    
    for line in lines:
        line.draw()

def main():
    clock = pg.time.Clock()

    blocks = []
    block1 = Block(RED, 50, 50, 10, 10)
    blocks.append(block1)

    running = True
    while running:
        win.fill(BACKGROUND)
        pg.draw.rect(win, BACKGROUND2, ((0, 700), (800, 800)))
        
        
        # block.move(block.x + 5, block.y + 5)

        for event in pg.event.get():
            if event.type == QUIT:
                running = False

        keyState = pg.key.get_pressed()
        cursorCoords = pg.mouse.get_pos() # (x, y)
        cursorClicks = pg.mouse.get_pressed(num_buttons=3) # Left, Center, Right
        cursorCoordsRel = pg.mouse.get_rel()

        if keyState[pg.K_ESCAPE]:
            print("exit")
            running = False
        if keyState[pg.K_w]:
            print("gay", cursorCoords, cursorClicks)
        
        
        # Render all blocks
        for block in blocks:
            block.draw()
            
            if block.checkCursor(cursorCoords) and cursorClicks[0]:
                print("Moving:", block)
                
                print(cursorCoordsRel)
                block.setOrigin(cursorCoordsRel[0] + block.x, cursorCoordsRel[1] + block.y)

        clock.tick(480)
        pg.display.update()

    
    pg.quit()


if __name__ == "__main__":
    main()