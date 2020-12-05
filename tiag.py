import tkinter as tk
from tkinter import filedialog as fd
import pydot
import os
import dependencies.parser as parser
import dependencies.utilities as utilities
import subprocess
import dependencies.stats as stats
import random

class MainApplication(tk.Tk):
    output_folder="output/"
    input_folder="input/"
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
        #self.Index_text.configure(state="disabled")
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
        input=parser.splitInputIntoTempFiles(fd.askopenfilename(parent=self,title='Wybierz początkowy plik Input'))
        data=pydot.graph_from_dot_file(self.input_folder + "tempGraph.dot")[0]
        os.remove("input/tempGraph.dot")
        self.Generate_files(data)
        self.vertex_counter = len(data.get_nodes())+1
        img=tk.PhotoImage(file = self.output_folder+str(self.index)+".png")
        self.Graph_label.image =img
        self.Graph_label.configure(image = img)
        self.Update_stats_label()
        transforms = parser.get_transforms(self.input_folder + "tempTrans.trsf")
        productions = parser.get_productions(self.input_folder + "tempProd.dot")
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
        Action_button.pack(padx=5, pady=20,side=tk.LEFT)
        #Random text
        self.Random_text=tk.Text(frame3,height=1,width=5,font = ("Helvetica", 20))
        self.Random_text.pack(side=tk.LEFT,padx=(20,0))
        #Random Button
        Random_button =tk.Button(frame3, text = "<- Losowych",font = ("Helvetica", 20),command = lambda: self.Random_Actions(names[0][:-1],len(names)))
        Random_button.pack(padx=5, pady=20,side=tk.LEFT)
        #Check Button
        self.var1 =tk.IntVar()
        Check_Button=tk.Checkbutton(frame3, text="Wymuś", variable=self.var1,font = ("Helvetica", 20))
        Check_Button.pack(padx=5, pady=20,side=tk.LEFT)

    def Update_stats_label(self):
        #self.Index_text.configure(state="normal")
        self.Index_text.delete(1.0,tk.END)
        self.Index_text.insert(1.0,str(self.index))
        #self.Index_text.configure(state="disabled")
        stats_ret=stats.get_stats(pydot.graph_from_dot_file(self.output_folder+str(self.index)+".gv")[0])
        str3=""
        for i in stats_ret[2]:
            str3+=i[0]+': '+str(i[1])+'\n'
        stats_text=("Liczba węzłów\n "+str(stats_ret[0])+'\n\n'+
                    "Liczba krawędzi\n"+str(stats_ret[1])+'\n\n'+
                    "Średni stopień wierzchołka w Gk\n"+str(round(stats_ret[1]*2/stats_ret[0],2))+"\n\n"+
                    "Liczba składowych spójnych\n"+str(len(stats_ret[3]))+"\n\n"+
                    "Średni stopień wierzchołka dla etykiet\n"+str3+"\n\n"+
                    "Liczba węzłów w spójnych składowych\n"+str(stats_ret[3])+
                    "\n\n Średnia liczba węzłów w składowej spójnej\n"+str(stats_ret[0]/len(stats_ret[3])))
        self.Stats_label.configure(text=stats_text)
    def Action_button_clicked(self,variable):
        data=pydot.graph_from_dot_file(self.output_folder+str(self.index)+".gv")[0]       
        tempCount = self.vertex_counter
        self.vertex_counter=utilities.apply_production_random(data,self.pairs[variable.get()],self.vertex_counter)
        if tempCount == self.vertex_counter:
            return
        self.index+=1
        self.max_index=self.index
        self.Generate_files(data)
        img=tk.PhotoImage(file = self.output_folder+str(self.index)+".png")
        self.Graph_label.image = img
        self.Graph_label.configure(image = img)
        self.Update_stats_label()
    def Random_Actions(self,name,lenght):
        if(self.var1.get()):
            self.Random_Actions2(name,lenght)
        else:
            self.Random_Actions1(name,lenght)
    def Random_Actions1(self,name,lenght):
        how_much=int(self.Random_text.get(1.0,tk.END))
        data=pydot.graph_from_dot_file(self.output_folder+str(self.index)+".gv")[0]
        tempCount = self.vertex_counter
        for i in range(how_much+1):
            tmp_rand=random.randint(1,lenght)
            self.vertex_counter=utilities.apply_production_random(data,self.pairs[name+str(tmp_rand)],self.vertex_counter)
            if tempCount == self.vertex_counter:
                print("Nie można wykonać "+name+str(tmp_rand)+", przerywam serię transformacji")
                self.Update_stats_label()
                return
            tempCount=self.vertex_counter
            self.index+=1
            self.max_index=self.index
            self.Generate_files(data)
            img=tk.PhotoImage(file = self.output_folder+str(self.index)+".png")
            self.Graph_label.image = img
            self.Graph_label.configure(image = img)
        self.Update_stats_label()
    def Random_Actions2(self,name,lenght):
        i=0
        index_before=self.index
        how_much=int(self.Random_text.get(1.0,tk.END))
        error_count2=0
        while i<how_much:
            self.index=index_before
            data=pydot.graph_from_dot_file(self.output_folder+str(self.index)+".gv")[0]
            tempCount = self.vertex_counter
            for i in range(how_much+1):
                flag=0
                error_count=0
                while not flag:
                    self.vertex_counter=utilities.apply_production_random(data,self.pairs[name+str(random.randint(1,lenght))],self.vertex_counter)
                    if tempCount == self.vertex_counter:
                        error_count+=1
                        if (error_count==lenght):
                            flag=-1
                    else:
                        self.index+=1
                        self.Generate_files(data)
                        tempCount=self.vertex_counter
                        flag=1
                if flag==-1:
                    break
            print("Dotarto do:"+str(i))
            if (error_count2==how_much):
                self.index=index_before
                print("Pomimo "+str(how_much)+" prób nie udało się wykonać serii "+str(how_much)+" transformacji.\nTIMEOUT")
                return
            error_count2+=1
        #self.index+=1
        #self.max_index=self.index
        #self.Generate_files(data)
        self.max_index=self.index
        img=tk.PhotoImage(file = self.output_folder+str(self.index)+".png")
        self.Graph_label.image = img
        self.Graph_label.configure(image = img)
        self.Update_stats_label()
    def Generate_files(self,graph):
        graph.write_dot(self.output_folder+str(self.index)+".gv")
        os.system("dot -Kneato -Tpng -o "+self.output_folder+str(self.index)+".png "+ self.output_folder+str(self.index)+".gv")
    def Backward_button_clicked(self):
        tmp=int(self.Index_text.get("1.0",tk.END))
        if tmp!=self.index:
            if tmp-1>=0:
                if tmp-1<=self.max_index:
                    self.index=tmp
                else:
                    self.index=self.max_index
            else:
                self.index=1
        if self.index-1<0:
            return
        self.index-=1
        img=tk.PhotoImage(file = self.output_folder+str(self.index)+".png")
        self.Graph_label.image = img
        self.Graph_label.configure(image = img)
        self.Update_stats_label()
    def Forward_button_clicked(self):
        tmp=int(self.Index_text.get("1.0",tk.END))
        if tmp!=self.index:
            if tmp+1>=0:
                if tmp+1<self.max_index:
                    self.index=tmp
                else:
                    self.index=self.max_index-1
            else:
                self.index=0
        if not self.index<self.max_index:
            return
        self.index+=1
        img=tk.PhotoImage(file = self.output_folder+str(self.index)+".png")
        self.Graph_label.image = img
        self.Graph_label.configure(image = img)
        self.Update_stats_label()
    def Show_full_size_clicked(self):
        data=pydot.graph_from_dot_file(self.output_folder+str(self.index)+".gv")[0]       
        os.system("dot -Kneato -Tpng -Gsize=40,40\! -o "+self.output_folder+"FULL.png "+ self.output_folder+str(self.index)+".gv")
        subprocess.run(["explorer","output\\"+"FULL.png"])


def main(): 
    Window=MainApplication()
    Window.mainloop()
if __name__=="__main__": 
    main() 


