﻿import tkinter as tk
from tkinter import filedialog as fd
import pydot
import os
import dependencies.parser as parser
import dependencies.utilities as utilities
import subprocess
import dependencies.stats as stats

class MainApplication(tk.Tk):
    output_folder="output/"
    max_index=0#Uzywane w 'historii' grafu
    index=0#id aktualnie wyswietlanego grafu
    def __init__(self):
        super().__init__()
        self.state('zoomed')
        self.title("TIAG Project")
        #Frames
        frame1 = tk.Frame(self,bg="white")
        frame2 = tk.Frame(self,bg="grey80")
        frame3 = tk.Frame(self,bg="grey50")
        frame4 = tk.Frame(self,bg="grey50")
        frame5 = tk.Frame(self,bg="grey50")
        #Positions
        frame1.grid(row=0, columnspan=2, sticky="nsew")
        frame2.grid(row=0, column=2, sticky="nsew")
        frame3.grid(row=1, column=0, sticky="nsew")
        frame4.grid(row=1, column=1, sticky="nsew")
        frame5.grid(row=1, column=2, sticky="nsew")

        self.grid_columnconfigure(0, weight=4, uniform="group1")
        self.grid_columnconfigure(1, weight=4, uniform="group1")
        self.grid_columnconfigure(2, weight=1, uniform="group1")
        self.grid_rowconfigure(0, weight=12)
        self.grid_rowconfigure(1, weight=1)
        #Graph label
        self.Graph_label =tk.Label(frame1, text = "",bg ="white",padx=100,pady=100)
        self.Graph_label.pack(fill=tk.BOTH)
        #Backward Button
        Backward_button =tk.Button(frame4, text = "Poprzedni",font = ("Helvetica", 20), command = lambda: self.Backward_button_clicked())
        Backward_button.pack(padx=50, pady=20,side=tk.LEFT)
        #Index Text
        self.Index_text=tk.Text(frame4,height=1,width=5,font = ("Helvetica", 20))
        self.Index_text.insert(tk.END,"0")
        self.Index_text.configure(state="disabled")
        self.Index_text.pack(side=tk.LEFT)
        #Forward Button
        Forward_button =tk.Button(frame4, text = "Następny",font = ("Helvetica", 20), command = lambda: self.Forward_button_clicked())
        Forward_button.pack(padx=50, pady=20,side=tk.LEFT)
        #Full_Size
        Show_full_size_button=tk.Button(frame5, text = "Jeżeli za małe",font = ("Helvetica", 15), command = lambda: self.Show_full_size_clicked())
        Show_full_size_button.pack(padx=(0,25), pady=20,side=tk.RIGHT)
        #Stats Label
        self.update()
        self.Stats_label = tk.Label(frame2,bg="grey80",font = ("Helvetica", 15),wraplength=frame2.winfo_width(), justify="center")
        self.Stats_label.pack(fill=tk.BOTH)
        #Load Data
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        data=pydot.graph_from_dot_file(fd.askopenfilename(parent=self,title='Wybierz początkowy plik DOT'))[0]
        self.Generate_files(data)
        self.vertex_counter = len(data.get_nodes())+1
        img=tk.PhotoImage(file = self.output_folder+str(self.index)+".png")
        self.Graph_label.image =img
        self.Graph_label.configure(image = img)
        self.Update_stats_label()
        transforms = parser.get_transforms(fd.askopenfilename(parent=self,title='Wybierz plik z transformacjami'))
        productions = parser.get_productions(fd.askopenfilename(parent=self,title='Wybierz plik z produkcjami'))
        self.pairs = parser.pair(productions, transforms);

        #Drop list
        names=[]
        for obj in transforms:
            names.append(obj.name)
        self.variable = tk.StringVar(frame3)
        self.variable.set(names[0])
        Drop_list = tk.OptionMenu(frame3, self.variable,*names)
        Drop_list.pack(padx=(100, 5), pady=20,side=tk.LEFT)
        Drop_list.config(font = ("Helvetica", 20))
        #Action Button
        Action_button =tk.Button(frame3, text = "Wykonaj",font = ("Helvetica", 20),command = lambda: self.Action_button_clicked(self.variable))
        Action_button.pack(padx=5, pady=20,side=tk.LEFT,)

    def Update_stats_label(self):
        self.Index_text.configure(state="normal")
        self.Index_text.delete(1.0,tk.END)
        self.Index_text.insert(1.0,str(self.index))
        self.Index_text.configure(state="disabled")
        stats_ret=stats.get_stats(pydot.graph_from_dot_file(self.output_folder+str(self.index)+".gv")[0])
        str3=""
        for i in stats_ret[3]:
            str3+=i[0]+': '+str(i[1])+'\n'
        stats_text=("Liczba węzłów\n "+str(stats_ret[0])+'\n\n'+
                    "Liczba krawędzi\n"+str(stats_ret[1])+'\n\n'+
                    "Średni stopień wierzchołka w Gk\n"+str(stats_ret[2])+"\n\n"+
                    "Liczba składowych spójnych\n"+str(len(stats_ret[4]))+"\n\n"+
                    "Średni stopień wierzchołka dla labelów\n"+str3+"\n\n"+
                    "Średnia liczba węzłów w składowej spójnej\n"+str(stats_ret[4]))
        self.Stats_label.configure(text=stats_text)
    def Action_button_clicked(self,variable):
        data=pydot.graph_from_dot_file(self.output_folder+str(self.index)+".gv")[0]       
        tempCount = self.vertex_counter
        self.vertex_counter=utilities.apply_production_random(data,self.pairs[variable.get()],self.vertex_counter)#Placeholder na produkcje
        if tempCount == self.vertex_counter:
            return
        self.index+=1
        self.max_index=self.index
        self.Generate_files(data)
        img=tk.PhotoImage(file = self.output_folder+str(self.index)+".png")
        self.Graph_label.image = img
        self.Graph_label.configure(image = img)
        self.Update_stats_label()
    def Generate_files(self,graph):
        graph.write_dot(self.output_folder+str(self.index)+".gv")
        graph.write_png(self.output_folder+str(self.index)+".png")
    def Backward_button_clicked(self):
        if self.index-1<0:
            return
        self.index-=1
        img=tk.PhotoImage(file = self.output_folder+str(self.index)+".png")
        self.Graph_label.image = img
        self.Graph_label.configure(image = img)
        self.Update_stats_label()
    def Forward_button_clicked(self):
        if not self.index<self.max_index:
            return
        self.index+=1
        img=tk.PhotoImage(file = self.output_folder+str(self.index)+".png")
        self.Graph_label.image = img
        self.Graph_label.configure(image = img)
        self.Update_stats_label()
    def Show_full_size_clicked(self):subprocess.run(["explorer","output\\"+str(self.index)+".png"])

if __name__ == "__main__":
    Window=MainApplication()
    Window.mainloop()