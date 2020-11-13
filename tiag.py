from tkinter import *
from tkinter import filedialog as fd
import pydot
import os

#Initialization
index=0
root =Tk()
output_folder='output/'
graph_source = fd.askopenfilename(parent=root,title='Wybierz początkowy plik DOT')
data = pydot.graph_from_dot_file(graph_source)[0]
if not os.path.exists('output'):
    os.makedirs('output')
data.write_png(output_folder+str(index)+".png")
#Graph label
Graph_label =Label(root, text = "")
img=PhotoImage(file = output_folder+str(index)+".png")
Graph_label.image =img
Graph_label.configure(image = img)
Graph_label.pack()
def clicked(Graph_label):
    global index
    index+=1
    data.add_node(pydot.Node(str(index),label="TEST"))
    data.write_png(output_folder+str(index)+".png")
    img=PhotoImage(file = output_folder+str(index)+".png")
    Graph_label.image = img
    Graph_label.configure(image = img)

#Action Button
Action_button =Button(root, text = "Wykonaj", command = lambda: clicked(Graph_label))
Action_button.pack()
root.mainloop()