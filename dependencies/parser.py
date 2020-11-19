import pydot

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

    return transforms

def pair(prodGraphs, transforms):
    ret = {}
    for i in range(0, max(len(prodGraphs), len(transforms))):
        p = prodGraphs[i]
        name = p.get_name()
        for t in transforms:
            print(t.name, name)
            if t.name == name:
                ret[name] = Pair(p, t)
                print("ok")
        if ret[name] is None: ret[name] = Pair(p, None)
    return ret