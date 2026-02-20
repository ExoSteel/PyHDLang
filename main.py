import pygame as pg
from pygame.locals import *
import os, csv
from fonts.fontManager import h1, h2, h3, p
from modules.objects import *
from modules.finder import jsonReader, getLogicDetails
from modules.constants import *

pg.init()
pg.display.set_caption("Pygame Hardware Description Language")

def drawBackground() -> None:
    win.fill(BACKGROUND)
    pg.draw.rect(win, BACKGROUND2, ((0, HEIGHT * 0.82), (WIDTH, HEIGHT)))
    pg.draw.rect(win, BACKGROUND3, ((0,0), (WIDTH * 0.1, HEIGHT * 0.82)))
    pg.draw.rect(win, BACKGROUND3, ((WIDTH * 0.9,0), (WIDTH, HEIGHT * 0.82)))

def calcBoxCenter(x:float=0.0, y:float=0.0, width:float=0.0, height:float=0.0, textX:float=0.0, textY:float=0.0) -> tuple[float, float]:
    centerX, centerY = x+(width//2), y+(height//2)
    return centerX-textX/2, centerY-textY/2

def drawObjects(buttons:list[any, ...]=[], inPlugs:list[any, ...]=[], outPlugs:list[any, ...]=[], nodes:list[any, ...]=[], lines:list[any, ...]=[]) -> None:
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

def detectInput() -> tuple[tuple[any, ...],tuple[any, ...],tuple[any, ...],tuple[any, ...]]:
    keyState = pg.key.get_pressed()
    cursorClicks = pg.mouse.get_pressed(num_buttons=3) # Left, Center, Right
    cursorCoords = pg.mouse.get_pos() # (x, y)
    cursorCoordsRel = pg.mouse.get_rel() # (x, y)

    return keyState, cursorClicks, cursorCoords, cursorCoordsRel

def findSelected(cursorCoords:tuple[int, int]=(0,0), buttons:list[any, ...]=[], nodes:list[any, ...]=[], inPlugs:list[any, ...]=[], outPlugs:list[any, ...]=[], lines:list[any, ...]=[]) -> any:
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

def isValidWiring(selectedPlug:[Plug,InputPlug,OutputPlug]=None, newWire:Wire=None) -> Wire:
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

def deleteConnections(lines:list[any, ...]=[], inPlugs:list[any, ...]=[], outPlugs:list[any, ...]=[], selected:any=None) -> None:
    toDelete = []
    for line in lines:
        # print(line.start, selected.inputs, line.end, selected.outputs)
        if line.end in selected.inputs or line.start in selected.outputs:
            toDelete.append(line)

    [lines.pop(lines.index(i)) for i in toDelete]

    toDelete = []
    for inPlug in inPlugs:
        if inPlug in selected.inputs:
            toDelete.append(inPlug)

    [inPlugs.pop(inPlugs.index(i)) for i in toDelete]

    toDelete = []
    for outPlug in outPlugs:
        if outPlug in selected.outputs:
            toDelete.append(outPlug)

    [outPlugs.pop(outPlugs.index(i)) for i in toDelete]

def initialise(data=list[any, ...]) -> tuple[list,list,list,list,list]:
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

def main() -> None:
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
                # print(selected)

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
                        if selected.checkCursor(cursorCoords) == 2:
                            selected.isActivated = False if selected.isActivated else True
                            # print("Activated:", selected.isActivated)
                        else:
                            newWire = Wire(BLACK, selected, cursorCoords)
                            lines.append(newWire)
                            isWiring = True
                    elif type(selected) == OutputPlug:
                        newWire = Wire(BLACK, cursorCoords, selected)
                        lines.append(newWire)
                        isWiring = True
                    elif type(selected) == Plug and selected in inPlugs:
                        newWire = Wire(BLACK, cursorCoords, selected)
                        lines.append(newWire)
                        isWiring = True
                    elif type(selected) == Plug and selected in outPlugs:
                        newWire = Wire(BLACK, selected, cursorCoords)
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
                        nodeIndex = nodes.index(selected)
                        print(lines)
                        deleteConnections(lines, inPlugs, outPlugs, selected)
                        print(lines)
                        nodes.pop(nodes.index(selected))

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
            print("hay", cursorCoords, cursorClicks, cursorCoordsRel, f"{clock.get_fps():.0f}")

        # Moving nodes
        if type(selected) == Node:
            selected.setOrigin(cursorCoordsRel[0] + selected.x, cursorCoordsRel[1] + selected.y)

        # Check if hovering over plugs or activated
        for plug in inPlugs + outPlugs:
            if not plug.checkCursor(cursorCoords):
                if type(plug) == InputPlug:
                    plug.switchColour = BLACK
                
                plug.colour = RED if plug.isActivated else BLACK
            if plug.checkCursor(cursorCoords):
                if plug.checkCursor(cursorCoords) == 2:
                    plug.switchColour = GREEN
                plug.colour = GREEN

        # Check lines
        for line in lines:
            # print(line.start, line.end)
            if type(line.start) in [Plug, InputPlug] and type(line.end) == tuple:
                line.end = cursorCoords
            elif type(line.end) in [Plug, InputPlug] and type(line.start) == tuple:
                line.start = cursorCoords
            else:
                line.checkCurrent()

        # Calculate node logic
        for node in nodes:
            node.calcOutput()

        drawObjects(buttons=buttons, inPlugs=inPlugs, outPlugs=outPlugs, nodes=nodes, lines=lines)
        clock.tick(500)
        pg.display.update()
    
    pg.quit()

if __name__ == "__main__":
    main()