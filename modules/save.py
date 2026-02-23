# {
#   "name": "NAND",
#   "colour": "175,10,175",
#   "width": 0.10,
#   "height": 0.08,
#   "inputs": 2,
#   "outputs": 1,
#   "src": "NAND.csv"
# }

# import modules.menus

def checkValidDetails(menu):
    try:
        for widget in menu.widgets:
            if widget.text == "Save":
                continue
            elif widget.text == "Name":
                temp = str(widget.value)
            elif widget.text == "Colour":
                for colourBox in widget.boxes:
                    temp = int(colourBox.value)
            else:
                temp = int(widget.value)

            print(temp)

        print("it works")
        return True

    except Exception as e:
        print(e)
        return False


def getSaveDetails(menu):
    details = [-1] * 6

    assignDict = {"Name": 0, "Colour": 1, "No. of Inputs": 2, "No. of Outputs": 3, "Width": 4, "Height": 5}

    widgets = menu.widgets

    details[assignDict[widgets[0].text]] = str(widgets[0].value)

    colourBoxes = widgets[1].boxes
    colour = colourBoxes[0].value + "," + colourBoxes[2].value + "," + colourBoxes[1].value
    details[assignDict[widgets[1].text]] = colour

    details[assignDict[widgets[2].text]] = int(widgets[2].value)
    details[assignDict[widgets[3].text]] = int(widgets[3].value)
    details[assignDict[widgets[4].text[:-5]]] = int(widgets[4].value)
    details[assignDict[widgets[5].text[:-5]]] = int(widgets[5].value)

    return details

def saveLogic(nodes, inPlugs, outPlugs, lines, saveMenu):
    if not checkValidDetails(saveMenu):
        print("Error saving!")
        return None

    name, colour, width, height, inputs, outputs = getSaveDetails(saveMenu)
    src = name + ".csv"
    print(name, colour, width, height, inputs, outputs, src)

    return None