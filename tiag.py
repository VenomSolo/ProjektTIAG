import tkinter as tk
from tkinter import filedialog as fd
import pydot
import os
import dependencies.parser as parser
import subprocess
#Initialization
output_folder="output/"
max_index=0#Uzywane w 'historii' grafu
index=0#id aktualnie wyswietlanego grafu
root =tk.Tk()

def Action_button_clicked(Graph_label,variable):
    global max_index,index
    data=pydot.graph_from_dot_file(output_folder+str(index)+".gv")[0]
    index+=1
    max_index=index
    data.add_node(pydot.Node(str(index),label=variable.get()))#Placeholder na produkcje
    Generate_files(data)
    img=tk.PhotoImage(file = output_folder+str(index)+".png")
    Graph_label.image = img
    Graph_label.configure(image = img)
def Backward_button_clicked(Graph_label):
    global index
    if index-1<0:
        return
    index-=1
    img=tk.PhotoImage(file = output_folder+str(index)+".png")
    Graph_label.image = img
    Graph_label.configure(image = img)
def Forward_button_clicked(Graph_label):
    global max_index,index
    if not index<max_index:
        return
    index+=1
    img=tk.PhotoImage(file = output_folder+str(index)+".png")
    Graph_label.image = img
    Graph_label.configure(image = img)
def Generate_files(graph):
    graph.write_dot(output_folder+str(index)+".gv")
    graph.write_png(output_folder+str(index)+".png")
def Show_full_size_clicked():subprocess.run(["explorer","output\\"+str(index)+".png"])
#def Load_graphs(file_list):    #TODO
if __name__ == "__main__":
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    Generate_files(pydot.graph_from_dot_file(fd.askopenfilename(parent=root,title='Wybierz początkowy plik DOT'))[0])
    transforms = parser.getTransforms(fd.askopenfilename(parent=root,title='Wybierz plik z transformacjami'))
    #Graph label
    Graph_label =tk.Label(root, text = "")
    img=tk.PhotoImage(file = output_folder+str(index)+".png")
    Graph_label.image =img
    Graph_label.configure(image = img)
    Graph_label.pack()
    #Drop list
    names=[]
    for obj in transforms:
        names.append(obj.name)
    variable = tk.StringVar(root)
    variable.set(names[0])
    Drop_list = tk.OptionMenu(root, variable,*names)
    Drop_list.pack()
    #Action Button
    Action_button =tk.Button(root, text = "Wykonaj", command = lambda: Action_button_clicked(Graph_label,variable))
    Action_button.pack()
    #Backward Button
    Backward_button =tk.Button(root, text = "Poprzedni", command = lambda: Backward_button_clicked(Graph_label))
    Backward_button.pack()
    #Forward Button
    Forward_button =tk.Button(root, text = "Następny", command = lambda: Forward_button_clicked(Graph_label))
    Forward_button.pack()
    #Full_Size
    Show_full_size_button=tk.Button(root, text = "Jezeli sie nie miesci...", command = lambda: Show_full_size_clicked())
    Show_full_size_button.pack()
    root.mainloop()