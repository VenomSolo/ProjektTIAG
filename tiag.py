from tkinter import *
from tkinter import filedialog as fd
import pydot
import os


#Initialization
output_folder="output/"
max_index=0#Uzywane w 'historii' grafu
index=0#id aktualnie wyswietlanego grafu
root =Tk()

def Action_button_clicked(Graph_label):
    global max_index,index
    data=pydot.graph_from_dot_file(output_folder+str(index)+".gv")[0]
    index+=1
    max_index=index
    data.add_node(pydot.Node(str(index),label="TEST"))#Placeholder na produkcje
    Generate_files(data)
    img=PhotoImage(file = output_folder+str(index)+".png")
    Graph_label.image = img
    Graph_label.configure(image = img)
def Backward_button_clicked(Graph_label):
    global index
    if index-1<0:
        return
    index-=1
    img=PhotoImage(file = output_folder+str(index)+".png")
    Graph_label.image = img
    Graph_label.configure(image = img)
def Forward_button_clicked(Graph_label):
    global max_index,index
    if not index<max_index:
        return
    index+=1
    img=PhotoImage(file = output_folder+str(index)+".png")
    Graph_label.image = img
    Graph_label.configure(image = img)
def Generate_files(graph):
    graph.write_dot(output_folder+str(index)+".gv")
    graph.write_png(output_folder+str(index)+".png")
if __name__ == "__main__":
    graph_source = fd.askopenfilename(parent=root,title='Wybierz początkowy plik DOT')
    data = pydot.graph_from_dot_file(graph_source)[0]
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    Generate_files(data)
    #Graph label
    Graph_label =Label(root, text = "")
    img=PhotoImage(file = output_folder+str(index)+".png")
    Graph_label.image =img
    Graph_label.configure(image = img)
    Graph_label.pack()
    #Action Button
    Action_button =Button(root, text = "Wykonaj", command = lambda: Action_button_clicked(Graph_label))
    Action_button.pack()
    #Backward Button
    Backward_button =Button(root, text = "Poprzedni", command = lambda: Backward_button_clicked(Graph_label))
    Backward_button.pack()
    #Forward Button
    Forward_button =Button(root, text = "Następny", command = lambda: Forward_button_clicked(Graph_label))
    Forward_button.pack()

    root.mainloop()