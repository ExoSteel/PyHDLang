import pygame as pg
from pygame.locals import *
import os, csv
from modules.finder import jsonReader, getLogicDetails
from fonts.fontManager import h1, h2, h3, p

pg.init()
pg.display.set_caption("Pygame Hardware Description Language")

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
    def __init__(self, colour, radius, x=None, y=None) -> None:
        self.colour = colour
        self.radius = radius
        self.x = x
        self.y = y
        self.isActivated = False

    def getCoords(self) -> tuple[int,int]:
        return self.x, self.y
    
    def checkCursor(self, cursorCoords:tuple[int,int]) -> bool:
        cursorX, cursorY = cursorCoords
        # (x-x0)^2 + (y-y0)^2 = r^2
        if (cursorX - self.x)**2 + (cursorY - self.y)**2 <= self.radius ** 2:
            return True

    def draw(self) -> None:
        pg.draw.circle(win, self.colour, (self.x, self.y), self.radius)
    
    def checkCurrent(self):
        if self.isActivated:
            self.colour = RED

class InputPlug(Plug):
    def __init__(self, colour, radius, x=None, y=None):
        super().__init__(colour, radius, x, y)
        self.switchRadius = self.radius * 2
        self.switchX = self.x * 0.65
        self.switchY = self.y
        self.switchColour = BLACK

    def draw(self):
        pg.draw.circle(win, self.colour, (self.x, self.y), self.radius)
        pg.draw.circle(win, self.switchColour, (self.switchX, self.switchY), self.switchRadius)
    
    def checkCursorOnSwitch(self, cursorCoords):
        cursorX, cursorY = cursorCoords
        # (x-x0)^2 + (y-y0)^2 = r^2
        if (cursorX - self.switchX)**2 + (cursorY - self.switchY)**2 <= self.switchRadius ** 2:
            return True

class OutputPlug(Plug):
    def __init__(self, colour, radius, x=None, y=None):
        super().__init__(colour, radius, x, y)
        self.lampRadius = self.radius * 2
        self.lampX = self.x * 1.04
        self.lampY = self.y 
        
    def draw(self):
        pg.draw.circle(win, self.colour, (self.x, self.y), self.radius)
        pg.draw.circle(win, self.colour, (self.lampX, self.lampY), self.lampRadius)

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
    
    def setOrigin(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def draw(self) -> None:
        pg.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))

    def moveTo(self, x, y) -> None:
        pg.draw.rect(win, self.colour, (x, y, self.width, self.height))
        self.x = x
        self.y = y
    
    def checkCursor(self, cursorCoords) -> bool:
        cursorX, cursorY = cursorCoords

        if cursorX >= self.x and cursorX <= self.x + self.width and cursorY >= self.y and cursorY <= self.y + self.height:
            # print("cursor inside")
            return True

class Button(Block):
    def __init__(self, colour, width, height, x, y, nodeData):
        super().__init__(colour, width, height, x, y)
        
        self.name = nodeData[0]
        self.nodeWidth = WIDTH * float(nodeData[2])
        self.nodeHeight = WIDTH * float(nodeData[3])
        self.inputs = nodeData[4]
        self.outputs = nodeData[5]
        self.truthTable = nodeData[6]

    def isClicked(self):
        pass

    def createNode(self) -> "Node":
        newNode = Node(self.colour, self.nodeWidth, self.nodeHeight, WIDTH * 0.1, HEIGHT * 0.1, self.inputs, self.outputs, self.name, self.truthTable)
        return newNode

class PlugButton(Block):
    def __init__(self, colour, width, height, x, y, plugType):
        super().__init__(colour, width, height, x, y)
        self.plugType = plugType
    
    def createPlug(self, plugs) -> "Node":
        colour = self.colour
        topPadding = HEIGHT * 0.08
        
        if self.plugType == "input":
            inPlugs = []
            for plug in plugs:
                inPlugs.append(plug) if type(plug) == InputPlug else 0
            spacing = (HEIGHT * 0.7) / (len(inPlugs) + 1)

            for ind, plug in enumerate(inPlugs):
                plug.y = topPadding + (spacing * (ind+2))
                plug.switchY = plug.y
            newPlug = InputPlug(colour, WIDTH * 0.01, WIDTH * 0.1, topPadding + spacing)

        elif self.plugType == "output":
            outPlugs = []
            for plug in plugs:
                outPlugs.append(plug) if type(plug) == OutputPlug else 0
            spacing = (HEIGHT * 0.7) / (len(outPlugs) + 1)

            for ind, plug in enumerate(outPlugs):
                plug.y = topPadding + (spacing * (ind+2))
                plug.lampY = plug.y
            newPlug = OutputPlug(colour, WIDTH * 0.01, WIDTH * 0.9, topPadding + spacing)

        plugs.insert(0, newPlug)
        return plugs

class Node(Block):
    def __init__(self, colour, width, height, x, y, inputs, outputs, name, truthTable):
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
        
        self.name = name
        self.truthTable = truthTable

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

    def readInputs(self):
        for i, inp in enumerate(self.inputs):
            pass

def drawBackground():
    win.fill(BACKGROUND)
    pg.draw.rect(win, BACKGROUND2, ((0, HEIGHT * 0.82), (WIDTH, HEIGHT)))
    pg.draw.rect(win, BACKGROUND3, ((0,0), (WIDTH * 0.1, HEIGHT * 0.82)))
    pg.draw.rect(win, BACKGROUND3, ((WIDTH * 0.9,0), (WIDTH, HEIGHT * 0.82)))

def calcBoxCenter(x, y, width, height, textX, textY):
    centerX, centerY = x+(width//2), y+(height//2)
    return centerX-textX/2, centerY-textY/2

def drawObjects(buttons=[], inPlugs=[], outPlugs=[], nodes=[], lines=[]) -> None:
    for button in buttons:
        button.draw()
        if type(button) == PlugButton:
            text = p.render("+", True, (255, 255, 255))
        elif type(button) == Button:
            text = p.render(button.name, True, (255, 255, 255))

        textX, textY = text.get_size()
        centerX, centerY = calcBoxCenter(button.x, button.y, button.width, button.height, textX, textY)
        win.blit(text, (centerX, centerY))
        
    for inPlug in inPlugs:
        inPlug.draw()

    for outPlug in outPlugs:
        outPlug.draw()

    for node in nodes:
        node.draw()
        text = p.render(node.name, True, (255, 255, 255))
        textX, textY = text.get_size()
        centerX, centerY = calcBoxCenter(node.x, node.y, node.width, node.height, textX, textY)
        
        win.blit(text, (centerX, centerY))
    
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

def isValidWiring(selectedPlug:[Plug,InputPlug,OutputPlug], newWire:Wire) -> Wire:
    if type(selectedPlug) == InputPlug:
        newWire.start = selectedPlug
    elif type(selectedPlug) == OutputPlug:
        newWire.end = selectedPlug
    else:
        if type(newWire.start) == tuple:
            newWire.start = selectedPlug
        else:
            newWire.end = selectedPlug

    return newWire

def initialise(data) -> tuple[list,list,list,list,list]:
    nodes, inPlugs, outPlugs, buttons, lines = [], [], [], [], []
    # node1 = Node(RED, WIDTH * 0.1, WIDTH * 0.075, WIDTH * 0.25, HEIGHT * 0.01, 2, 1, "AND", "")
    # node2 = Node(BLUE, WIDTH * 0.1, WIDTH * 0.075, WIDTH * 0.12, HEIGHT * 0.1, 1, 1, "OR", "")
    # nodes.insert(0, node1)
    # nodes.insert(1, node2)
    
    inputPlug = InputPlug(BLACK, WIDTH * 0.01, WIDTH * 0.1, HEIGHT * 0.33)
    inputPlug2 = InputPlug(BLACK, WIDTH * 0.01, WIDTH * 0.1, HEIGHT * 0.66)
    inPlugs.append(inputPlug)
    inPlugs.append(inputPlug2)
    
    outputPlug = OutputPlug(BLACK, WIDTH * 0.01, WIDTH * 0.9, HEIGHT * 0.33)
    outputPlug2 = OutputPlug(BLACK, WIDTH * 0.01, WIDTH * 0.9, HEIGHT * 0.66)
    outPlugs.append(outputPlug)

    for ind, logic in enumerate(data):
        colour = tuple([int(i) for i in logic[1].split(",")])
        button = Button(colour=colour, width=(WIDTH * 0.06), height=(WIDTH * 0.04), x=(WIDTH * 0.01 + WIDTH * 0.07 * (ind)), y=(HEIGHT * 0.845), nodeData=logic)
        buttons.insert(0, button)
    buttonInput = PlugButton((100,100,100), WIDTH * 0.05, WIDTH * 0.05, WIDTH * 0.02, HEIGHT * 0.01, "input")
    buttonOutput = PlugButton((100,100,100), WIDTH * 0.05, WIDTH * 0.05, WIDTH * 0.92, HEIGHT * 0.01, "output")
    
    buttons.insert(0, buttonInput)
    buttons.insert(0, buttonOutput)

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

    data = []
    collectionJSON = jsonReader("./collection.json")
    for logic in collectionJSON["logics"]:
        data.append(getLogicDetails(logic))
        
    nodes, inPlugs, outPlugs, buttons, lines = initialise(data)

    while running:
        drawBackground()
        keyState, cursorClicks, cursorCoords, cursorCoordsRel = detectInput()
        
        for event in pg.event.get():
            if event.type == QUIT:
                running = False

            elif event.type == MOUSEBUTTONDOWN:
                # Find Selected
                selected = findSelected(cursorCoords, buttons, nodes, inPlugs, outPlugs, lines)

                # Actions (Left Click)
                if event.button == 1:
                    if type(selected) == Button:
                        node = selected.createNode()
                        nodes.append(node)
                        for inp in node.inputs:
                            inPlugs.append(inp)
                        for out in node.outputs:
                            outPlugs.append(out)
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
                # Actions (Middle Click)
                elif event.button == 2:
                    # dk what to do with this WIP
                    pass 
                # Actions (Right Click)
                elif event.button == 3:
                    if type(selected) == PlugButton:
                        # Delete an input/output plug WIP
                        pass
                    elif type(selected) == Node:
                        # Delete selected node WIP
                        pass

            elif event.type == MOUSEBUTTONUP:
                prevSelected = selected
                
                if isWiring:
                    selected = findSelected(cursorCoords, inPlugs=inPlugs, outPlugs=outPlugs)

                    if selected and selected != newWire.start and selected != newWire.end:
                        newWire = isValidWiring(selected, newWire)

                        lines[-1] = newWire
                        newWire = None
                    else:
                        lines.pop(-1)

                    isWiring = False
                    # print(lines)
        
                selected = None

        if keyState[pg.K_ESCAPE]:
            print("exit")
            running = False
        if keyState[pg.K_w]: #debug
            print("gay", cursorCoords, cursorClicks, cursorCoordsRel, f"{clock.get_fps():.0f}")

        # Moving nodes
        if type(selected) == Node:
            selected.setOrigin(cursorCoordsRel[0] + selected.x, cursorCoordsRel[1] + selected.y)

        # Check if hovering over plugs or activated
        for plug in inPlugs + outPlugs:
            if plug.checkCurrent():
                plug.colour = RED
            elif type(plug) == InputPlug and plug.checkCursorOnSwitch(cursorCoords):
                plug.switchColour = GREEN
                break
            elif plug.checkCursor(cursorCoords):
                plug.colour = GREEN
                break
            else:
                plug.colour = BLACK
                if type(plug) == InputPlug:
                    plug.switchColour = BLACK

        # Check lines
        for line in lines:
            if isinstance(line.start, Plug) and type(line.end) == tuple:
                line.end = cursorCoords
            elif isinstance(line.end, Plug) and type(line.start) == tuple:
                line.start = cursorCoords

        drawObjects(buttons=buttons, inPlugs=inPlugs, outPlugs=outPlugs, nodes=nodes, lines=lines)
        clock.tick(500)
        pg.display.update()


    
    pg.quit()

if __name__ == "__main__":
    main()