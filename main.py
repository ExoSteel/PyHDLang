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
BACKGROUND3 = (50,50,50)

class Plug:
    def __init__(self, colour, radius, x=None, y=None):
        self.colour = colour
        self.radius = radius
        self.x = x
        self.y = y

    def getCoords(self):
        return self.x, self.y
    
    def checkCursor(self, cursorCoords:tuple[int,int]) -> bool:
        cursorX, cursorY = cursorCoords
        # (x-x0)^2 + (y-y0)^2 = r^2
        if (cursorX - self.x)**2 + (cursorY - self.y)**2 <= self.radius ** 2:
            return True

    def draw(self):
        pg.draw.circle(win, self.colour, (self.x, self.y), self.radius)

class InputPlug(Plug):
    def __init__(self, colour, radius, x=None, y=None):
        super().__init__(colour, radius, x, y)
        self.isActivated = False

    def drawAt(self, x, y):
        pg.draw.circle(win, self.colour, (x, y), self.radius)

    def checkCurrent(self):
        if self.isActivated:
            self.colour = RED

class OutputPlug(Plug):
    def __init__(self, colour, radius, x=None, y=None):
        super().__init__(colour, radius, x, y)

    def drawAt(self, x, y):
        pg.draw.circle(win, self.colour, (x, y), self.radius)

class Wire:
    def __init__(self, deactColour, actColour, start:Plug | tuple[int,int], end:Plug | tuple[int,int]):
        self.deactColour = deactColour
        self.actColour = actColour
        self.start = start
        self.end = end
        self.isActivated = False

    def draw(self):
        if type(self.start) in [Plug, InputPlug]:
            startX, startY = self.start.getCoords()
        else:
            startX, startY = self.start[0], self.start[1]

        if type(self.end) in [Plug, OutputPlug]:
            endX, endY = self.end.getCoords()
        else:
            endX, endY = self.end[0], self.end[1]
        pg.draw.line(win, self.actColour if self.isActivated else self.deactColour, (startX, startY), (endX, endY), 4)

    def checkCurrent(self):
        if self.start.activated:
            self.isActivated = True
            self.end.activated = True

    def checkCursor(self, currentCoords):
        return False

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
        inputs = len(self.node.inputs)
        outputs = len(self.node.outputs)

        newNode = Node(colour, width, height, WIDTH * 0.01, HEIGHT * 0.01, inputs, outputs)
        return newNode

class PlugButton(Block):
    def __init__(self, colour, width, height, x, y, plugType):
        super().__init__(colour, width, height, x, y)
        self.plugType = plugType
    
    def createPlug(self, plugs) -> Node:
        colour = self.colour

        topPadding = HEIGHT * 0.08
        spacing = (HEIGHT * 0.8) / (len(plugs) + 1)

        if self.plugType == "input":
            for ind, plug in enumerate(plugs):
                plug.y = topPadding + (spacing * (ind+1))
            newPlug = InputPlug(colour, WIDTH * 0.01, WIDTH * 0.1, topPadding + spacing)

        elif self.plugType == "output":
            for ind, plug in enumerate(plugs):
                plug.y = topPadding + (spacing * (ind+1))
            newPlug = InputPlug(colour, WIDTH * 0.01, WIDTH * 0.9, topPadding + spacing)

        plugs.insert(0, newPlug)
        return plugs

class Node(Block):
    def __init__(self, colour, width, height, x, y, inputs, outputs):
        super().__init__(colour, width, height, x, y)
        self.inputs = []
        for i in range(1, inputs+1):
            plugY = self.y + self.height / (inputs+1) * i
            inPlug = Plug(BLACK, WIDTH * 0.01, self.x, plugY)
            self.inputs.append(inPlug)

        self.outputs = []
        for o in range(1, outputs+1):
            plugY = self.y + self.height / (outputs+1) * o
            outPlug = Plug(BLACK, WIDTH * 0.01, self.x + self.width, plugY)
            self.outputs.append(outPlug)

    def draw(self):
        super().draw()
        for i, inp in enumerate(self.inputs):
            inp.x = self.x
            inp.y = self.y + self.height / (len(self.inputs)+1) * (i+1)
            inp.draw()

        
        for o, out in enumerate(self.outputs):
            out.x = self.x + self.width
            out.y = self.y + self.height / (len(self.outputs)+1) * (o+1)
            out.draw()
    
    def checkCursorOnPlug(self, cursorCoords):
        for inp in self.inputs:
            if inp.checkCursor(cursorCoords):
                inp.colour = GREEN
            else:
                inp.colour = BLACK
            
        for out in self.outputs:
            if out.checkCursor(cursorCoords):
                out.colour = GREEN
            else:
                out.colour = BLACK

def drawBackground():
    win.fill(BACKGROUND)
    pg.draw.rect(win, BACKGROUND2, ((0, HEIGHT * 0.82), (WIDTH, HEIGHT)))
    pg.draw.rect(win, BACKGROUND3, ((0,0), (WIDTH * 0.1, HEIGHT * 0.82)))
    pg.draw.rect(win, BACKGROUND3, ((WIDTH * 0.9,0), (WIDTH, HEIGHT * 0.82)))

def drawObjects(buttons=[], inPlugs=[], outPlugs=[], nodes=[], lines=[]) -> void:
    for button in buttons:
        button.draw()
    
    for inPlug in inPlugs:
        inPlug.draw()

    for outPlug in outPlugs:
        outPlug.draw()

    for node in nodes:
        node.draw()
    
    for line in lines:
        line.draw()

def detectInput():
    keyState = pg.key.get_pressed()
    cursorClicks = pg.mouse.get_pressed(num_buttons=3) # Left, Center, Right
    cursorCoords = pg.mouse.get_pos() # (x, y)
    cursorCoordsRel = pg.mouse.get_rel() # (x, y)

    return keyState, cursorClicks, cursorCoords, cursorCoordsRel

def findSelected(cursorCoords, buttons=[], nodes=[], inPlugs=[], outPlugs=[], lines=[]):
    objects = buttons + nodes + inPlugs + outPlugs + lines

    for obj in objects:
        if not obj.checkCursor(cursorCoords):
            continue

        if type(obj) == Node:
            for plug in obj.inputs + obj.outputs:
                if plug.checkCursor(cursorCoords):
                    return plug

        return obj
    
    return None

def isValidWiring(selectedPlug, newWire):
    if type(selectedPlug) == InputPlug:
        newWire.start = selectedPlug
    elif type(selectedPlug) == OutputPlug:
        print("what", newWire.start, newWire.end)
        newWire.end = selectedPlug
    else:
        if type(newWire.start) == tuple:
            print("reis")
            newWire.start = selectedPlug
        else:
            print('fale')
            newWire.end = selectedPlug

    return newWire

def initialise():
    nodes, inPlugs, outPlugs, buttons, lines = [], [], [], [], []
    node1 = Node(RED, WIDTH * 0.1, WIDTH * 0.1, WIDTH * 0.25, HEIGHT * 0.01, 2, 1)
    node2 = Node(BLUE, WIDTH * 0.1, WIDTH * 0.1, WIDTH * 0.12, HEIGHT * 0.1, 2, 2)
    nodes.insert(0, node1)
    nodes.insert(1, node2)
    
    inputPlug = InputPlug(BLACK, WIDTH * 0.01, WIDTH * 0.1, HEIGHT * 0.33)
    inputPlug2 = InputPlug(BLACK, WIDTH * 0.01, WIDTH * 0.1, HEIGHT * 0.66)
    inPlugs.insert(0, inputPlug)
    inPlugs.insert(0, inputPlug2)

    
    outputPlug = OutputPlug(BLACK, WIDTH * 0.01, WIDTH * 0.9, HEIGHT * 0.33)
    outputPlug2 = OutputPlug(BLACK, WIDTH * 0.01, WIDTH * 0.9, HEIGHT * 0.66)
    outPlugs.insert(0, outputPlug)
    outPlugs.insert(0, outputPlug2)

    
    button1 = Button((50,10,20), WIDTH * 0.07, WIDTH * 0.07, WIDTH * 0.01, HEIGHT * 0.845, node1)
    button2 = Button((50,20,200), WIDTH * 0.07, WIDTH * 0.07, WIDTH * 0.09, HEIGHT * 0.845, node2)
    button3 = PlugButton((100,100,100), WIDTH * 0.05, WIDTH * 0.05, WIDTH * 0.02, HEIGHT * 0.01, "input")
    button4 = PlugButton((100,100,100), WIDTH * 0.05, WIDTH * 0.05, WIDTH * 0.92, HEIGHT * 0.01, "output")
    buttons.insert(0, button1)
    buttons.insert(0, button2)
    buttons.insert(0, button3)
    buttons.insert(0, button4)

    for node in nodes:
        for inp in node.inputs:
            inPlugs.append(inp)
        for out in node.outputs:
            outPlugs.append(out)

    return nodes, inPlugs, outPlugs, buttons, lines

def main():
    clock = pg.time.Clock()
    selected = None
    prevSelected = None
    isWiring = False
    newWire = None
    running = True
    nodes, inPlugs, outPlugs, buttons, lines = initialise()

    while running:
        drawBackground()
        keyState, cursorClicks, cursorCoords, cursorCoordsRel = detectInput()
        
        for event in pg.event.get():
            if event.type == QUIT:
                running = False

            elif event.type == MOUSEBUTTONDOWN:
                # Find Selected
                selected = findSelected(cursorCoords, buttons, nodes, inPlugs, outPlugs, lines)

                # Actions
                if type(selected) == Button:
                    nodes.append(selected.createNode())
                elif type(selected) == PlugButton:
                    selected.createPlug(inPlugs if selected.plugType == "input" else outPlugs)
                elif type(selected) == InputPlug:
                    newWire = Wire(BLACK, GREEN, selected, cursorCoords)
                    lines.append(newWire)
                    isWiring = True
                elif type(selected) == OutputPlug:
                    newWire = Wire(BLACK, GREEN, cursorCoords, selected)
                    lines.append(newWire)
                    isWiring = True
                elif type(selected) == Plug and selected in inPlugs:
                    newWire = Wire(BLACK, GREEN, cursorCoords, selected)
                    lines.append(newWire)
                    isWiring = True
                elif type(selected) == Plug and selected in outPlugs:
                    newWire = Wire(BLACK, GREEN, selected, cursorCoords)
                    lines.append(newWire)
                    isWiring = True

            elif event.type == MOUSEBUTTONUP:
                prevSelected = selected
                
                if isWiring:
                    selected = findSelected(cursorCoords, inPlugs=inPlugs, outPlugs=outPlugs)

                    if selected and selected != newWire.start and selected != newWire.end:
                        print("cursed")
                        newWire = isValidWiring(selected, newWire)

                        lines[-1] = newWire
                        newWire = None
                    else:
                        lines.pop(-1)


                    isWiring = False
                    print(lines)
        
                selected = None    

        if keyState[pg.K_ESCAPE]:
            print("exit")
            running = False
        if keyState[pg.K_w]: #debug
            print("gay", cursorCoords, cursorClicks, cursorCoordsRel)

        # Moving nodes
        if type(selected) == Node:
            selected.setOrigin(cursorCoordsRel[0] + selected.x, cursorCoordsRel[1] + selected.y)

        # Check if hovering over plugs
        for plug in inPlugs + outPlugs:
            if plug.checkCursor(cursorCoords):
                plug.colour = GREEN
                break
            else:
                plug.colour = BLACK

        # Check lines
        for line in lines:
            if isinstance(line.start, Plug) and type(line.end) == tuple:
                line.end = cursorCoords
            elif isinstance(line.end, Plug) and type(line.start) == tuple:
                line.start = cursorCoords

        drawObjects(buttons=buttons, inPlugs=inPlugs, outPlugs=outPlugs, nodes=nodes, lines=lines)

        clock.tick(480)
        pg.display.update()
    
    pg.quit()

if __name__ == "__main__":
    main()