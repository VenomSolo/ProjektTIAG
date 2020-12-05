import pydot
import os

input_folder = 'input/'

class Pair:
    def __init__(self, production, transformation):
        self.production = production
        self.transformation = transformation

class Transform:
    def __init__(self, entry, name):
        self.entry = entry
        self.name = name
        self.bindings = {}

    def __str__(self):
        ret = self.entry + " --> " + self.name + "\n"
        for key, value in self.bindings.items():
            ret += key + " |"
            for s in value:
                ret += " " + s
            ret += "\n"
        return ret

    def addBinding(self, bind):
        self.bindings[bind[0]] = bind[1]

def get_productions(filename):
    productParentGraph = pydot.graph_from_dot_file(filename)[0]
    subgraphs = productParentGraph.get_subgraphs()
    os.remove(filename)
    return subgraphs

def get_transforms(filename):
    transformFile = open(filename, 'r') 
    Lines = []

    for line in transformFile:
        newLine = line.strip()
        if newLine != "":
            Lines.append(newLine)

    lineCtr = len(Lines)
    lineTrc = 0
    transforms = []

    while lineTrc < lineCtr:
        if Lines[lineTrc][0] == '!':
            newTransform = Transform(Lines[lineTrc][1], Lines[lineTrc][2:])
            lineTrc += 1
            while lineTrc < lineCtr:
                if Lines[lineTrc][0] == '@':
                    transforms.append(newTransform)
                    break
                else:
                    splitLine = Lines[lineTrc].split(":")
                    vertexLabel = splitLine[0]
                    connectionList = splitLine[1]
                    labelsList = connectionList.split(",")
                    newTransform.addBinding((vertexLabel, labelsList))
                lineTrc += 1
        lineTrc += 1
    transformFile.close()
    os.remove(filename)
    return transforms

def pair(prodGraphs, transforms):
    ret = {}
    for i in range(0, max(len(prodGraphs), len(transforms))):
        p = prodGraphs[i]
        name = p.get_name()
        for t in transforms:
            if t.name == name:
                ret[name] = Pair(p, t)
        if ret[name] is None: ret[name] = Pair(p, None)
    return ret

def splitInputIntoTempFiles(filename):
    input_file = open(filename, 'r')
    grahp_file = open(input_folder + "tempGraph.dot", 'w')
    prod_file = open(input_folder + "tempProd.dot", 'w')
    trans_file = open(input_folder + "tempTrans.trsf", 'w')
    files = [grahp_file, prod_file, trans_file]
    Lines = []
    
    p = 0

    for line in input_file:
        p += 1
        newLine = line.strip()
        if newLine != "":
            Lines.append(newLine)

    lineCtr = len(Lines)
    
    separators = []

    for i in range(lineCtr):
        if Lines[i][0] == '#':
            separators.append(i)

    def overwrite(file, start, end):
        nonlocal Lines
        for i in range(start+1, end):
            file.write(Lines[i] + "\n")

    for i in range(3):
        overwrite(files[i], separators[i], separators[i+1])

    for file in files:
        file.close()
       
