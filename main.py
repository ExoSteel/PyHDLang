# Fork test
import pygame as pg
from pygame.locals import *
import os, csv
from fonts.fontManager import h1, h2, h3, p
from modules.objects import *
from modules.finder import jsonReader, getLogicDetails
from modules.constants import *
from modules.menus import *
from modules.save import *

pg.init()
pg.display.set_caption("Pygame Hardware Description Language")

def drawBackground() -> None:
    # print(WIDTH, HEIGHT)
    win.fill(BACKGROUND)
    pg.draw.rect(win, BACKGROUND2, ((0, worldHeight - worldHeight*0.18), (worldWidth, worldHeight)))
    pg.draw.rect(win, BACKGROUND3, ((0,0), (worldWidth * 0.1, worldHeight - worldHeight*0.18)))
    pg.draw.rect(win, BACKGROUND3, ((worldWidth * 0.9,0), (worldWidth, worldHeight - worldHeight * 0.18)))

def drawObjects(buttons:list[any, ...]=[], inPlugs:list[any, ...]=[], outPlugs:list[any, ...]=[], nodes:list[any, ...]=[], lines:list[any, ...]=[], onMenu:any=None, menuCoords:tuple[int,int]=(0,0)) -> None:
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
    
    if onMenu:
        onMenu.draw(menuCoords[0], menuCoords[1])

def detectInput() -> tuple[tuple[any, ...],tuple[any, ...],tuple[any, ...],tuple[any, ...]]:
    keyState = pg.key.get_pressed()
    cursorClicks = pg.mouse.get_pressed(num_buttons=3) # Left, Center, Right
    cursorCoords = pg.mouse.get_pos() # (x, y)
    cursorCoordsRel = pg.mouse.get_rel() # (x, y)

    return keyState, cursorClicks, cursorCoords, cursorCoordsRel

def findSelected(cursorCoords:tuple[int, int]=(0,0), buttons:list[any, ...]=[], nodes:list[any, ...]=[], inPlugs:list[any, ...]=[], outPlugs:list[any, ...]=[], lines:list[any, ...]=[], menus:list[any, ...]=[]) -> any:
    # Slightly Complex Checks
    for node in nodes:
        for plug in node.inputs + node.outputs:
            if plug.checkCursor(cursorCoords):
                return plug

    for menu in menus:
        if menu.checkCursor(cursorCoords):
            for widget in menu.widgets:
                if type(widget) == ColourPicker:
                    for colourBox in widget.boxes:
                        # print(colourBox.checkCursor(cursorCoords, menu.width, menu.height))
                        if colourBox.checkCursor(cursorCoords, menu.width, menu.height):
                            return colourBox
                elif widget.checkCursor(cursorCoords, menu.width, menu.height):
                    return widget
            
            return menu
    
    objects = buttons + nodes + inPlugs + outPlugs + lines

    # Simple Checks
    for obj in objects:
        if not obj.checkCursor(cursorCoords):
            continue

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

def cleanReset():
    pass

def initialise(data=list[any, ...]) -> tuple[list,list,list,list,list]:
    nodes, inPlugs, outPlugs, buttons, lines, menus = [], [], [], [], [], []
    # node1 = Node(RED, WIDTH * 0.1, WIDTH * 0.075, WIDTH * 0.25, HEIGHT * 0.01, 2, 1, "AND", "")
    # node2 = Node(BLUE, WIDTH * 0.1, WIDTH * 0.075, WIDTH * 0.12, HEIGHT * 0.1, 1, 1, "OR", "")
    # nodes.insert(0, node1)
    # nodes.insert(1, node2)
    
    inputPlug = InputPlug(BLACK, worldWidth * 0.01, worldWidth * 0.1, worldHeight * 0.33)
    inputPlug2 = InputPlug(BLACK, worldWidth * 0.01, worldWidth * 0.1, worldHeight * 0.66)
    inPlugs.append(inputPlug)
    inPlugs.append(inputPlug2)
    
    outputPlug = OutputPlug(BLACK, worldWidth * 0.01, worldWidth * 0.9, worldHeight * 0.33)
    outputPlug2 = OutputPlug(BLACK, worldWidth * 0.01, worldWidth * 0.9, worldHeight * 0.66)
    outPlugs.append(outputPlug)

    saveMenu = SaveMenu("Save", WHITE, worldWidth * 0.4, worldHeight * 0.7)
    menus.insert(0, saveMenu)

    for ind, logic in enumerate(data):
        colour = tuple([int(i) for i in logic[1].split(",")])
        button = NodeButton(text=logic[0], colour=colour, width=(worldWidth * 0.06), height=(worldWidth * 0.04), x=(worldWidth * 0.01 + worldWidth * 0.07 * (ind)), y=(worldHeight * 0.845), data=logic)
        buttons.insert(0, button)
    buttonInput = PlugButton("+", (100,100,100), worldWidth * 0.05, worldWidth * 0.05, worldWidth * 0.02, worldHeight * 0.01, "input")
    buttonOutput = PlugButton("+", (100,100,100), worldWidth * 0.05, worldWidth * 0.05, worldWidth * 0.92, worldHeight * 0.01, "output")
    buttonSave = SaveButton("Save", RED, worldWidth * 0.10, worldHeight * 0.10, worldWidth * 0.85, worldHeight * 0.85, saveMenu)
    
    buttons.insert(0, buttonInput)
    buttons.insert(0, buttonOutput)
    buttons.insert(0, buttonSave)

    for node in nodes:
        for inp in node.inputs:
            inPlugs.append(inp)
        for out in node.outputs:
            outPlugs.append(out)

    return nodes, inPlugs, outPlugs, buttons, lines, menus

def resizeGUI(info:any, objects:list[any, ...]) -> None:
    global worldWidth, worldHeight
    percentDiffWidth = info.current_w / worldWidth
    percentDiffHeight = info.current_h / worldHeight
    worldWidth, worldHeight = info.current_w, info.current_h
    # print(info)

    for obj in objects:
        obj.x *= percentDiffWidth
        obj.y *= percentDiffHeight
        if type(obj) == InputPlug:
            obj.radius *= ((percentDiffWidth + percentDiffHeight) / 2)
            obj.switchRadius *= ((percentDiffWidth + percentDiffHeight) / 2)
            obj.switchX *= percentDiffWidth
            obj.switchY *= percentDiffHeight
        elif type(obj) == OutputPlug:
            obj.radius *= ((percentDiffWidth + percentDiffHeight) / 2)
            obj.lampRadius *= ((percentDiffWidth + percentDiffHeight) / 2)
            obj.lampX *= percentDiffWidth
            obj.lampY *= percentDiffHeight
        elif type(obj) in [Plug, InputPlug, OutputPlug]:
            obj.radius *= ((percentDiffWidth + percentDiffHeight) / 2)
        else:
            obj.width *= percentDiffWidth
            obj.height *= percentDiffHeight

def main() -> None:
    global worldWidth, worldHeight
    clock = pg.time.Clock()
    selected = None
    prevSelected = None
    isWiring = False
    newWire = None
    running = True
    onMenu = None
    menuCoords = (0,0)
    isTyping = None
    userInput = ""

    data = []
    collectionJSON = jsonReader("./collection.json")
    for logic in collectionJSON["logics"]:
        data.append(getLogicDetails(logic))
        
    nodes, inPlugs, outPlugs, buttons, lines, menus = initialise(data)

    while running:
        info = pg.display.Info()
        
        # print(info, info.current_w)
        if info.current_w != worldWidth or info.current_h != worldHeight:
            objects = nodes + inPlugs + outPlugs + buttons
            resizeGUI(info, objects)
        drawBackground()
        keyState, cursorClicks, cursorCoords, cursorCoordsRel = detectInput()
        
        for event in pg.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                print("hay", cursorCoords, cursorClicks, cursorCoordsRel, f"{clock.get_fps():.0f}") if event.key == K_w else None
                if event.key == K_ESCAPE:
                    print("exit")
                    running = False
                elif isTyping:
                    # print(event.unicode)
                    if event.key == K_BACKSPACE:
                        userInput = userInput[:-1]
                        isTyping.value = isTyping.value[:-1]
                    else:    
                        userInput += event.unicode
                        isTyping.value += event.unicode

            elif event.type == MOUSEBUTTONDOWN:
                # Find Selected
                selected = findSelected(cursorCoords, buttons, nodes, inPlugs, outPlugs, lines, menus)
                # print(selected)

                # Actions (Left Click)
                if event.button == 1:
                    if type(selected) == SaveMenu:
                        onMenu = selected
                    elif isinstance(selected, Widget):
                        pass
                    elif type(selected) == SaveButton:
                        menuCoords = (cursorCoords[0]-selected.menu.width, cursorCoords[1]-selected.menu.height)
                        onMenu = selected.menu
                    else:
                        if type(prevSelected) == SaveMenu:
                            prevSelected.x = None
                            prevSelected.y = None

                        onMenu = None

                    if type(selected) == NodeButton:
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
                    elif type(selected) == InputBox:
                        userInput = selected.value
                        isTyping = selected
                        # print(userInput)
                    elif type(selected) == SaveButtonWidget:
                        newButton = saveLogic(nodes, inPlugs, outPlugs, lines, onMenu)
                        if newButton != None:
                            cleanReset(buttons, nodes, inPlugs, outPlugs, lines, menus)
                    else:
                        isTyping = None
                        isWiring = False

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
                        nodeIndex = nodes.index(selected)
                        deleteConnections(lines, inPlugs, outPlugs, selected)
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

        # Moving nodes
        if type(selected) == Node:
            selected.x += cursorCoordsRel[0]
            selected.y += cursorCoordsRel[1]

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
            if type(line.start) in [Plug, InputPlug] and type(line.end) in [Plug, OutputPlug]:
                line.checkCurrent()
            elif type(line.start) in [Plug, InputPlug] and type(line.end) == tuple:
                line.end = cursorCoords
            elif type(line.end) in [Plug, OutputPlug] and type(line.start) == tuple:
                line.start = cursorCoords

        # Calculate node logic
        for node in nodes:
            node.calcOutput()

        drawObjects(buttons=buttons, inPlugs=inPlugs, outPlugs=outPlugs, nodes=nodes, lines=lines, onMenu=onMenu, menuCoords=menuCoords)
        clock.tick(500)
        pg.display.update()
    
    pg.quit()

if __name__ == "__main__":
    main()