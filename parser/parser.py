class Transform:
    def __init__(self, entry, name):
        self.entry = entry
        self.name = name
        self.bindings = []

    def __str__(self):
        ret = self.entry + " --> " + self.name + "\n"
        for b in self.bindings:
            ret += b[0] + " |"
            for s in b[1]:
                ret += " " + s
            ret += "\n"
        return ret

    def addBinding(self, bind):
        self.bindings.append(bind)


def getTransforms(filename):
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

def main():
    transforms = getTransforms('myfile.trsf')
    for t in transforms:
        print(t)

if __name__ == "__main__":
    main()
