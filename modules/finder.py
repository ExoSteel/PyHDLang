import csv
import json
# import os

def jsonReader(path):
    with open(path, "r") as infile:
        return json.load(infile)

def getTruthTable(src):
    path = "./nodes/" + src

    # dirList = os.listdir(path)
    # print(dirList)

    with open(path, "r") as infile:
        table = csv.DictReader(infile, delimiter=",")

        return list(table)

def getLogicDetails(logic):
    name = logic["name"]
    colour = logic["colour"]
    width = logic["width"]
    height = logic["height"]
    inputs = logic["inputs"]
    outputs = logic["outputs"]
    src = logic["src"]
    
    tTable = getTruthTable(src)
    
    return name, colour, width, height, inputs, outputs, tTable

if __name__ == "__main__":
    collectionJSON = jsonReader("./collection.json")
    deets = []
    for logic in collectionJSON["logics"]:
        deets.append(getLogicDetails(logic))
        
    # logics = searchLogic()
    print(deets)