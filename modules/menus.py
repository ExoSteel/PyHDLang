import pygame as pg
from pygame.locals import *
from fonts.fontManager import *
from modules.constants import *
from modules.objects import *
# Save logic diagram/truth table menu WIP

class Widget:
    def __init__(self, text, colour, width, height, relX, relY):
        self.text = text
        self.colour = colour
        self.width = width
        self.height = height
        self.relX = relX
        self.relY = relY
        self.x = None
        self.y = None

    def textJustifyLeft(self, menuWidth, menuHeight, textX, textY):
        return self.x + menuWidth * self.relX - textX - 5, self.y + menuHeight * self.relY + (self.height / 2 - textY / 2)

class InputBox(Widget):
    def __init__(self, text, colour, width, height, relX, relY):
        super().__init__(text, colour, width, height, relX, relY)
        self.value = ""
    
    def draw(self, menuX, menuY, menuWidth, menuHeight):
        if menuX == None and menuY == None:
            self.x, self.y = None, None
        
        self.x, self.y = menuX, menuY

        pg.draw.rect(win, self.colour, (self.x + menuWidth * self.relX, self.y + menuHeight * self.relY, self.width, self.height))

        text = p.render(self.text, True, (255, 255, 255))
        textX, textY = text.get_size()

        centerX, centerY = self.textJustifyLeft(menuWidth, menuHeight, textX, textY)
        
        win.blit(text, (centerX, centerY))

class Slider(Widget):
    pass

class Radio(Widget):
    pass

class ColourPicker(Widget):
    def __init__(self, text, colour, width, height, relX, relY):
        super().__init__(text, colour, width, height, relX, relY)

        self.boxes = self.initInputBoxes(3)

    def initInputBoxes(self, numBoxes):
        boxes = []
        for box in range(numBoxes):
            boxes.append(InputBox("", BACKGROUND3, self.width / 3, self.height, 1.0, 1.0))
        
        return boxes
    
    def draw(self, menuX, menuY, menuWidth, menuHeight):
        if menuX == None and menuY == None:
            self.x, self.y = None, None
        
        self.x, self.y = menuX, menuY

        RGB = (RED, GREEN, BLUE)
        for i, box in enumerate(self.boxes):
            pg.draw.rect(win, RGB[i], (self.x + (menuWidth * self.relX) * (i+1), self.y + menuHeight * self.relY, self.width/3 - 15, self.height))

        text = p.render(self.text, True, (255, 255, 255))
        textX, textY = text.get_size()

        centerX, centerY = self.textJustifyLeft(menuWidth, menuHeight, textX, textY)
        
        win.blit(text, (centerX, centerY))

class SaveMenu(Block):
    def __init__(self, text:str="", colour:tuple[int,int,int]=(0,0,0), width:float=0.0, height:float=0.0):
        super().__init__(text, colour, width, height, None, None)
        self.isVisible = False
        self.widgets = self.initWidgets()
        self.x = None
        self.y = None
    
    def initWidgets(self):
        nameInput = InputBox("Name", BACKGROUND3, worldWidth*0.2, worldHeight*0.07, 0.12, 0.22)
        colourInput = ColourPicker("Colour", BACKGROUND3, worldWidth*0.2, worldHeight*0.07, 0.17, 0.42)
        numInputsInput = InputBox("No. of Inputs", BACKGROUND3, worldWidth*0.06, worldHeight*0.07, 0.34, 0.62)
        numOutputsInput = InputBox("No. of Outputs", BACKGROUND3, worldWidth*0.05, worldHeight*0.07, 0.36, 0.82)
        return [nameInput, colourInput, numInputsInput, numOutputsInput]

    def draw(self, menuX, menuY):
        if menuX == None and menuY == None:
            self.x, self.y = None, None

        self.x, self.y = menuX, menuY
        pg.draw.rect(win, BACKGROUND4, (menuX, menuY, self.width, self.height))

        text = h2.render(self.text, True, (255, 255, 255))
        textX, textY = text.get_size()

        centerX, centerY = self.textJustifyCenter(textX, textY)
        
        win.blit(text, (centerX, centerY))
        
        for widget in self.widgets:
            widget.draw(menuX, menuY, self.width, self.height)
        
    def textJustifyCenter(self, textX, textY):
        return self.x + (self.width - textX) / 2, self.y + self.height * 0.01


if __name__ == "__main__":
    pg.init()
    clock = pg.time.Clock()
    worldWidth, worldHeight = 1000, 1000
    running = True
    userText = ""
    win = pg.display.set_mode((worldWidth,worldHeight))
    onMenu = False
    saveMenu = SaveMenu(WHITE, 100, 100, [])
    button = SaveButton(RED, 150, 150, 800, 800, saveMenu)
    menuX, menuY = None, None

    while running:
        win.fill(BLACK)
        button.draw()
        cursorCoords = pg.mouse.get_pos()
        cursorCoordsRel = pg.mouse.get_rel()
        cursorClicks = pg.mouse.get_pressed(num_buttons=3)
        keyState = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button.checkCursor(cursorCoords) or saveMenu.checkCursor(cursorCoords):
                        onMenu = True
                        menuX, menuY = cursorCoords[0]-saveMenu.width, cursorCoords[1]-saveMenu.height
                    else:
                        onMenu = False
        
        if onMenu:
            saveMenu.draw(menuX, menuY)
            print("burh")

        if keyState[pg.K_ESCAPE]:
            print("exit")
            running = False
        if keyState[pg.K_w]: #debug
            print("gay", cursorCoords, cursorClicks, cursorCoordsRel, f"{clock.get_fps():.0f}")

        
        clock.tick(500)
        pg.display.update()
    
    pg.quit()