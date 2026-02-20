# Collection of objects WIP
from modules.constants import *

class Plug:
    def __init__(self, colour:tuple[int,int,int]=(0,0,0), radius:float=0.0, x:float=0.0, y:float=0.0) -> None:
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
        
        return False

    def draw(self) -> None:
        pg.draw.circle(win, self.colour, (self.x, self.y), self.radius)
    
    def checkCurrent(self) -> None:
        if self.isActivated:
            self.colour = RED
        else:
            self.colour = BLACK

class InputPlug(Plug):
    def __init__(self, colour:tuple[int,int,int]=(0,0,0), radius:float=0.0, x:float=0.0, y:float=0.0) -> None:
        super().__init__(colour, radius, x, y)
        self.switchRadius = self.radius * 2
        self.switchX = self.x * 0.65
        self.switchY = self.y
        self.switchColour = BLACK

    def draw(self) -> None:
        pg.draw.circle(win, self.colour, (self.x, self.y), self.radius)
        pg.draw.circle(win, self.switchColour, (self.switchX, self.switchY), self.switchRadius)
    
    def checkCursor(self, cursorCoords:tuple[int,int]=(0,0)) -> int:
        cursorX, cursorY = cursorCoords
        # (x-x0)^2 + (y-y0)^2 = r^2
        if (cursorX - self.x)**2 + (cursorY - self.y)**2 <= self.radius ** 2:
            return 1
        elif (cursorX - self.switchX)**2 + (cursorY - self.switchY)**2 <= self.switchRadius ** 2:
            return 2
        
        return 0

class OutputPlug(Plug):
    def __init__(self, colour:tuple[int,int,int]=(0,0,0), radius:float=0.0, x:float=0.0, y:float=0.0) -> None:
        super().__init__(colour, radius, x, y)
        self.lampRadius = self.radius * 2
        self.lampX = self.x * 1.04
        self.lampY = self.y 
        
    def draw(self) -> None:
        pg.draw.circle(win, self.colour, (self.x, self.y), self.radius)
        pg.draw.circle(win, self.colour, (self.lampX, self.lampY), self.lampRadius)

class Wire:
    def __init__(self, colour:tuple[int,int,int]=(0,0,0), start:Plug | tuple[int,int]=None, end:Plug | tuple[int,int]=None) -> None:
        self.colour = colour
        self.start = start
        self.end = end
        self.isActivated = False

    def draw(self) -> None:
        if type(self.start) in [Plug, InputPlug]:
            startX, startY = self.start.getCoords()
        else:
            startX, startY = self.start[0], self.start[1]

        if type(self.end) in [Plug, OutputPlug]:
            endX, endY = self.end.getCoords()
        else:
            endX, endY = self.end[0], self.end[1]
        pg.draw.line(win, self.colour, (startX, startY), (endX, endY), 4)

    def checkCurrent(self) -> bool:
        if self.start.isActivated:
            self.colour = RED
            self.isActivated = True
            self.end.isActivated = True
            return True

        self.colour = BLACK
        self.isActivated = False
        self.end.isActivated = False
        return False

    def checkCursor(self, currentCoords:tuple[int,int]=(0,0)) -> bool:
        # Need math equation WIP
        return False

class Block:
    def __init__(self, colour:tuple[int,int,int]=(0,0,0), width:float=0.0, height:float=0.0, x:float=0.0, y:float=0.0):
        self.colour = colour
        self.width = width
        self.height = height
        self.x = x
        self.y = y
    
    def setOrigin(self, x:float=0.0, y:float=0.0) -> None:
        self.x = x
        self.y = y
    
    def draw(self) -> None:
        pg.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))

    def moveTo(self, x:float=0.0, y:float=0.0) -> None:
        pg.draw.rect(win, self.colour, (x, y, self.width, self.height))
        self.x = x
        self.y = y
    
    def checkCursor(self, cursorCoords:tuple[int,int]=(0,0)) -> bool:
        cursorX, cursorY = cursorCoords

        if cursorX >= self.x and cursorX <= self.x + self.width and cursorY >= self.y and cursorY <= self.y + self.height:
            # print("cursor inside")
            return True

        return False

class Button(Block):
    def __init__(self, colour:tuple[int,int,int]=(0,0,0), width:float=0.0, height:float=0.0, x:float=0.0, y:float=0.0, nodeData:list[any, ...]=[]):
        super().__init__(colour, width, height, x, y)
        
        self.name = nodeData[0]
        self.nodeWidth = worldWidth * float(nodeData[2])
        self.nodeHeight = worldWidth * float(nodeData[3])
        self.inputs = nodeData[4]
        self.outputs = nodeData[5]
        self.truthTable = nodeData[6]

    def createNode(self) -> "Node":
        newNode = Node(self.colour, self.nodeWidth, self.nodeHeight, worldWidth * 0.1, worldHeight * 0.1, self.inputs, self.outputs, self.name, self.truthTable)
        return newNode

class PlugButton(Block):
    def __init__(self, colour:tuple[int,int,int]=(0,0,0), width:float=0.0, height:float=0.0, x:float=0.0, y:float=0.0, plugType:str=""):
        super().__init__(colour, width, height, x, y)
        self.plugType = plugType
    
    def createPlug(self, plugs:list[any, ...]=[]) -> "Node":
        colour = self.colour
        topPadding = worldHeight * 0.08
        
        if self.plugType == "input":
            inPlugs = []
            for plug in plugs:
                inPlugs.append(plug) if type(plug) == InputPlug else 0
            spacing = (worldHeight * 0.7) / (len(inPlugs) + 1)

            for ind, plug in enumerate(inPlugs):
                plug.y = topPadding + (spacing * (ind+2))
                plug.switchY = plug.y
            newPlug = InputPlug(colour, worldWidth * 0.01, worldWidth * 0.1, topPadding + spacing)

        elif self.plugType == "output":
            outPlugs = []
            for plug in plugs:
                outPlugs.append(plug) if type(plug) == OutputPlug else 0
            spacing = (worldHeight * 0.7) / (len(outPlugs) + 1)

            for ind, plug in enumerate(outPlugs):
                plug.y = topPadding + (spacing * (ind+2))
                plug.lampY = plug.y
            newPlug = OutputPlug(colour, worldWidth * 0.01, worldWidth * 0.9, topPadding + spacing)

        plugs.insert(0, newPlug)
        return plugs

class Node(Block):
    def __init__(self, colour:tuple[int,int,int]=(0,0,0), width:float=0.0, height:float=0.0, x:float=0.0, y:float=0.0, inputs:int=0, outputs:int=0, name:str="", truthTable:list[dict, ...]=[]):
        super().__init__(colour, width, height, x, y)

        self.inputs = []
        for i in range(1, inputs+1):
            plugY = self.y + self.height / (inputs+1) * i
            inPlug = Plug(BLACK, worldWidth * 0.01, self.x, plugY)
            self.inputs.append(inPlug)

        self.outputs = []
        for o in range(1, outputs+1):
            plugY = self.y + self.height / (outputs+1) * o
            outPlug = Plug(BLACK, worldWidth * 0.01, self.x + self.width, plugY)
            self.outputs.append(outPlug)
        
        self.name = name
        self.truthTable = truthTable
        # print(self.truthTable)

    def draw(self) -> None:
        super().draw()
        for i, inp in enumerate(self.inputs):
            inp.x = self.x
            inp.y = self.y + self.height / (len(self.inputs)+1) * (i+1)
            inp.draw()
        
        for o, out in enumerate(self.outputs):
            out.x = self.x + self.width
            out.y = self.y + self.height / (len(self.outputs)+1) * (o+1)
            out.draw()
    
    def checkCursorOnPlug(self, cursorCoords:tuple[int,int]=(0,0)) -> None:
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

    def calcOutput(self) -> None:
        inputs = []
        outputs = []
        for proposition in self.truthTable:
            binaryInp = ""
            binaryOut = ""

            for key, value in proposition.items():
                if key in ALPHABET:
                    binaryInp += value
                if "OUT" in key:
                    binaryOut += value
            
            inputs.append(binaryInp)
            outputs.append(binaryOut)

        # print(inputs)
        # print(outputs)
            
        binaryInput = ""
        for i, inp in enumerate(self.inputs):
            binaryInput += str(int(inp.isActivated))
        
        result = False
        binaryOutput = ""
        if binaryInput in inputs:
            index = inputs.index(binaryInput)
            binaryOutput = outputs[index]

        for i, out in enumerate(self.outputs):
            out.isActivated = True if binaryOutput[i] == "1" else False