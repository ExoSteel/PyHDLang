import pygame as pg
from pygame.locals import *

pg.init()

info = pg.display.Info()

WIDTH = info.current_w / 2
HEIGHT = info.current_h / 2
win = pg.display.set_mode((WIDTH,HEIGHT))

RED = (255,50,50)
GREEN = (50,255,50)
BLUE = (50,50,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

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
    def __init__(self, colour, width, height, x, y, node):
        super().__init__(colour, width, height, x, y)
        self.node = node

    def isClicked(self):
        pass

    def createNode(self) -> Node:
        colour = self.node.colour
        width = self.node.width
        height = self.node.height
        inputs = self.node.inputs
        outputs = self.node.outputs

        newNode = Node(colour, width, height, WIDTH * 0.01, HEIGHT * 0.01, inputs, outputs)
        return newNode

class Node(Block):
    def __init__(self, colour, width, height, x, y, inputs, outputs):
        super().__init__(colour, width, height, x, y)
        self.inputs = inputs
        self.outputs = outputs
    
    def draw(self):
        super().draw()
        for inp in range(1, self.inputs + 1):
            pg.draw.circle(win, BLACK, (self.x , self.y + self.height / (self.inputs+1) * inp), WIDTH * 0.01)
        
        for out in range(1, self.outputs + 1):
            pg.draw.circle(win, BLACK, (self.x + self.width , self.y + self.height / (self.outputs+1) * out), WIDTH * 0.01)


def drawObjects(buttons=[], nodes=[], lines=[]) -> void:
    for button in buttons:
        button.draw()
    
    for node in nodes:
        node.draw()
    
    for line in lines:
        line.draw()

def main():
    clock = pg.time.Clock()

    nodes = []
    node1 = Node(RED, WIDTH * 0.1, WIDTH * 0.1, WIDTH * 0.01, HEIGHT * 0.01, 2, 1)
    node2 = Node(BLUE, WIDTH * 0.1, WIDTH * 0.1, WIDTH * 0.1, HEIGHT * 0.1, 2, 2)
    nodes.append(node1)
    nodes.append(node2)

    buttons = []
    button1 = Button((50,10,20), WIDTH * 0.07, WIDTH * 0.07, WIDTH * 0.01, HEIGHT * 0.845, node1)
    button2 = Button((50,20,200), WIDTH * 0.07, WIDTH * 0.07, WIDTH * 0.09, HEIGHT * 0.845, node2)
    buttons.append(button1)
    buttons.append(button2)

    running = True
    while running:
        win.fill(BACKGROUND)
        pg.draw.rect(win, BACKGROUND2, ((0, HEIGHT * 0.82), (WIDTH, HEIGHT)))
        
        
        # block.move(block.x + 5, block.y + 5)
        keyState = pg.key.get_pressed()
        cursorCoords = pg.mouse.get_pos() # (x, y)
        cursorClicks = pg.mouse.get_pressed(num_buttons=3) # Left, Center, Right
        cursorCoordsRel = pg.mouse.get_rel()

        for event in pg.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                # print("click")
                for button in buttons:
                    if button.checkCursor(cursorCoords):
                        print(button, "clicked")
                        nodes.append(button.createNode())
        

        if keyState[pg.K_ESCAPE]:
            print("exit")
            running = False
        if keyState[pg.K_w]:
            print("gay", cursorCoords, cursorClicks, cursorCoordRel)
        
        drawObjects(buttons=buttons, nodes=nodes)

        # Moving nodes if needed
        for node in nodes:
            if node.checkCursor(cursorCoords) and cursorClicks[0]:
                # print("Moving:", node)
                
                # print(cursorCoordsRel)
                node.setOrigin(cursorCoordsRel[0] + node.x, cursorCoordsRel[1] + node.y)

        clock.tick(480)
        pg.display.update()

    
    pg.quit()


if __name__ == "__main__":
    main()