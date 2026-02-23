import pygame as pg
import fonts.fontManager
import modules.constants
import modules.objects

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
    
    def checkCursor(self, cursorCoords, menuWidth, menuHeight):
        if self.x == None and self.y == None:
            return False

        cursorX, cursorY = cursorCoords[0], cursorCoords[1]

        if cursorX >= self.x + menuWidth * self.relX and cursorX <= self.x + menuWidth * self.relX + self.width and cursorY >= self.y + menuHeight * self.relY and cursorY <= self.y + menuHeight * self.relY + self.height:
            return True

        return False


class InputBox(Widget):
    def __init__(self, text, colour, width, height, relX, relY):
        super().__init__(text, colour, width, height, relX, relY)
        self.value = ""

    def draw(self, window, menuX, menuY, menuWidth, menuHeight):
        if menuX == None and menuY == None:
            self.x, self.y = None, None

        self.x, self.y = menuX, menuY

        pg.draw.rect(window, self.colour, (self.x + menuWidth * self.relX, self.y + menuHeight * self.relY, self.width, self.height))

        text = fonts.fontManager.p.render(self.text, True, (255, 255, 255))
        textX, textY = text.get_size()

        centerX, centerY = self.textJustifyLeft(menuWidth, menuHeight, textX, textY)

        window.blit(text, (centerX, centerY))

        inpText = fonts.fontManager.p.render(self.value, True, (255, 255, 255))
        inpTextX, inpTextY = inpText.get_size()

        centerX, centerY = self.x + menuWidth * self.relX + (self.width - inpTextX) / 2, self.y + menuHeight * self.relY + inpTextY / 2

        window.blit(inpText, (centerX, centerY))


class Slider(Widget):
    pass


class Radio(Widget):
    pass


class ColourPicker(Widget):
    def __init__(self, text, colour, width, height, relX, relY):
        super().__init__(text, colour, width, height, relX, relY)

        self.R = 0
        self.G = 0
        self.B = 0
        self.x = None
        self.y = None
        self.boxes = self.initInputBoxes(3)

    def initInputBoxes(self, numBoxes):
        boxes = []
        for box in range(numBoxes):
            boxes.append(InputBox("", modules.constants.BACKGROUND3, self.width / 3, self.height, self.relX, self.relY))

        return boxes

    def draw(self, window, menuX, menuY, menuWidth, menuHeight):
        if menuX == None and menuY == None:
            self.x, self.y = None, None

        self.x, self.y = menuX, menuY

        self.R = int(self.boxes[0].value) if self.boxes[0].value != "" else 0
        self.G = int(self.boxes[1].value) if self.boxes[1].value != "" else 0
        self.B = int(self.boxes[2].value) if self.boxes[2].value != "" else 0

        colour = (self.R, self.G, self.B)
        for i, box in enumerate(self.boxes):
            box.colour = colour
            box.draw(window, menuX + (box.width + 15) * i, menuY, menuWidth, menuHeight)
            # pg.draw.rect(window, colour, (self.x + (menuWidth * self.relX) * (i+1), self.y + menuHeight * self.relY, self.width/3 - 15, self.height))

        text = fonts.fontManager.p.render(self.text, True, (255, 255, 255))
        textX, textY = text.get_size()

        centerX, centerY = self.textJustifyLeft(menuWidth, menuHeight, textX, textY)

        window.blit(text, (centerX, centerY))

    def checkCursor(self, cursorCoords, menuWidth, menuHeight):
        if self.x == None and self.y == None:
            return None

        cursorX, cursorY = cursorCoords[0], cursorCoords[1]


class SaveButtonWidget(Widget):
    def __init__(self, text, colour, width, height, relX, relY):
        super().__init__(text, colour, width, height, relX, relY)

    def draw(self, window, menuX, menuY, menuWidth, menuHeight):
        if menuX == None and menuY == None:
            self.x, self.y = None, None

        self.x, self.y = menuX, menuY

        pg.draw.rect(window, self.colour, (self.x + menuWidth * self.relX, self.y + menuHeight * self.relY, self.width, self.height))

        text = fonts.fontManager.p.render(self.text, True, (255, 255, 255))
        textX, textY = text.get_size()

        centerX, centerY = self.x + menuWidth * self.relX + (self.width - textX) / 2, self.y + menuHeight * self.relY + textY / 2

        window.blit(text, (centerX, centerY))


class SaveMenu(modules.objects.Block):
    def __init__(self, worldWidth, worldHeight, text: str = "", colour: tuple[int, int, int] = (0, 0, 0), width: float = 0.0, height: float = 0.0):
        super().__init__(text, colour, width, height, None, None)
        self.isVisible = False
        self.widgets = self.initWidgets(worldWidth, worldHeight)
        self.x = None
        self.y = None

    def initWidgets(self, worldWidth, worldHeight):
        nameInput = InputBox("Name", modules.constants.BACKGROUND3, worldWidth * 0.2, worldHeight * 0.07, 0.12, 0.15)
        colourInput = ColourPicker("Colour", modules.constants.BACKGROUND3, worldWidth * 0.2, worldHeight * 0.07, 0.17, 0.28)
        numInputsInput = InputBox("No. of Inputs", modules.constants.BACKGROUND3, worldWidth * 0.06, worldHeight * 0.07, 0.34, 0.42)
        numOutputsInput = InputBox("No. of Outputs", modules.constants.BACKGROUND3, worldWidth * 0.05, worldHeight * 0.07, 0.36, 0.57)
        nodeWidthInput = InputBox("Width (px)", modules.constants.BACKGROUND3, worldWidth * 0.05, worldHeight * 0.07, 0.27, 0.72)
        nodeHeightInput = InputBox("Height (px)", modules.constants.BACKGROUND3, worldWidth * 0.05, worldHeight * 0.07, 0.29, 0.87)
        widgetSave = SaveButtonWidget("Save", modules.constants.GREEN, worldWidth * 0.07, worldHeight * 0.07, 0.8, 0.82)
        return [nameInput, colourInput, numInputsInput, numOutputsInput, nodeWidthInput, nodeHeightInput, widgetSave]

    def draw(self, window, menuX, menuY):
        if menuX == None and menuY == None:
            self.x, self.y = None, None

        self.x, self.y = menuX, menuY
        pg.draw.rect(window, modules.constants.BACKGROUND4, (menuX, menuY, self.width, self.height))

        text = fonts.fontManager.h2.render(self.text, True, (255, 255, 255))
        textX, textY = text.get_size()

        centerX, centerY = self.textJustifyCenter(textX, textY)

        window.blit(text, (centerX, centerY))

        for widget in self.widgets:
            widget.draw(window, menuX, menuY, self.width, self.height)

    def textJustifyCenter(self, textX, textY):
        return self.x + (self.width - textX) / 2, self.y


# if __name__ == "__main__":
#     pg.init()
#     clock = pg.time.Clock()
#     worldWidth, worldHeight = 1000, 1000
#     running = True
#     userText = ""
#     window = pg.display.set_mode((worldWidth,worldHeight))
#     onMenu = False
#     saveMenu = SaveMenu(modules.constants.WHITE, 100, 100, [])
#     button = modules.objects.SaveButton(modules.constants.RED, 150, 150, 800, 800, saveMenu)
#     menuX, menuY = None, None

#     while running:
#         window.fill(modules.constants.BLACK)
#         button.draw()
#         cursorCoords = pg.mouse.get_pos()
#         cursorCoordsRel = pg.mouse.get_rel()
#         cursorClicks = pg.mouse.get_pressed(num_buttons=3)
#         keyState = pg.key.get_pressed()

#         for event in pg.event.get():
#             if event.type == pg.QUIT:
#                 running = False
#             elif event.type == pg.MOUSEBUTTONDOWN:
#                 if event.button == 1:
#                     if button.checkCursor(cursorCoords) or saveMenu.checkCursor(cursorCoords):
#                         onMenu = True
#                         menuX, menuY = cursorCoords[0]-saveMenu.width, cursorCoords[1]-saveMenu.height
#                     else:
#                         onMenu = False

#         if onMenu:
#             saveMenu.draw(menuX, menuY)
#             print("burh")

#         if keyState[pg.K_ESCAPE]:
#             print("exit")
#             running = False
#         if keyState[pg.K_w]: #debug
#             print("gay", cursorCoords, cursorClicks, cursorCoordsRel, f"{clock.get_fps():.0f}")

#         clock.tick(500)
#         pg.display.update()

#     pg.quit()