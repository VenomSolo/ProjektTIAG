#from pydot import * 
#from tkinter import *
#from graphviz import *
#index=0
#dot = Graph(comment='The Round Table',format='png')
#dot.node('A', 'King Arthur')
#dot.node('B', 'Sir Bedevere the Wise')
#dot.node('L', 'Sir Lancelot the Brave')

#dot = graph_from_dot_file("graph1.dot")[0]

##dot.edges(['AB', 'AL'])
##dot.edge('B', 'L', constraint='false')
##print(dot.source)
##dot.render('test-output/round-table.gv')  
#dot.write('test-output.gv')

#root = Tk()

#def clicked(label1):
#    global index

#    img = PhotoImage(file = "test-output.gv.png")
#    label1.image = img # bez referencji garbage collector wyebie
#    label1.configure(image = img)
#    dot.add_node(Node(str(index), 'King Arthur'))
#    index+=1
#    dot.write('test-output.gv') 


#label1 =Label(root, text = "")
#label1.pack()
#b1 =Button(root, text = "Display", command = lambda: clicked(label1))
#b1.pack()
#root.mainloop()

from pydot import * 
from graphviz import Digraph
from graphviz import Source
from tkinter import *

index=0
output_folder="output/"
dot = graph_from_dot_file("graph.gv")[0]
dot2 = graph_from_dot_file("subgraph.gv")[0]
subg = dot2.get_subgraph("subTEST")[0]
neighbours = []


dot.write_png(output_folder+str(index)+".png")

root =Tk()

def clicked(label1):
    global index
    img = PhotoImage(file = output_folder+str(index)+".png")
    label1.image = img # bez referencji garbage collector wyebie
    label1.configure(image = img)
    dot.add_node(Node(str(index), label = 'a'))
    dot.add_node(Node(str(index), label = 'a'))
    index+=1
    dot.write_dot(output_folder+str(index)+".gv")
    dot.write_png(output_folder+str(index)+".png")

def getNeighbours(node):
    edges = dot.get_edges()
    name = node.get('name')
    ret = []
    for e in edges:
        if e.get_source() is name or e.get_destination() is name:
            ret.append(dot.get_node(name))

def applyTo(label1):
    global index
    nodes = dot.get_node_list()
    for n in nodes:
        print(n.get("name"))
        if n.get('label').rstrip() == "\"d\"":
            neighbours = getNeighbours(n)
            dot.del_node("\"d\"")
            dot.add_subgraph(subg)
            break
        else: print(n.get('label'), n)
    index+=1
    dot.write_dot(output_folder+str(index)+".gv")
    dot.write_png(output_folder+str(index)+".png")
    img = PhotoImage(file = output_folder+str(index)+".png")
    label1.image = img # bez referencji garbage collector wyebie
    label1.configure(image = img)




label1 =Label(root, text = "")
label1.pack()
b1 =Button(root, text = "Display", command = lambda: clicked(label1))
b1.pack()
b2 =Button(root, text = "Apply", command = lambda: applyTo(label1))
b2.pack()
root.mainloop()