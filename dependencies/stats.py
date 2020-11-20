import pydot
from .utilities import get_neighbours
def Nodes_number(nodes):
    return len(nodes)
def Edges_number(Graph):
    return len(Graph.get_edges())
def Mean_vertice_rank(Graph,nodes):
    sum=0
    for node in nodes:
        sum+=len(get_neighbours(Graph,node))
    return round(sum/len(nodes),2)

def Mean_vertice_by_label(Graph,nodes):
    count=[['a',0],['b',0],['c',0],['d',0]]#Moze zmienic zeby sie dostosowywaly  ¯\_(ツ)_/¯
    for i in range(len(count)):
        number_of_labels=0
        for node in nodes:
            if(node.get('label')==count[i][0]):
                count[i][1]+=len(get_neighbours(Graph,node))
                number_of_labels+=1
                #same_label.append(node)
        count[i][1]=round(count[i][1]/number_of_labels,2)
    return count
def Component_number(Graph,nodes):
    components=[]
    while nodes:
        count=1
        queue=get_neighbours(Graph,nodes.pop())
        while queue:
            tmp=queue.pop()
            x=is_in_list(tmp,nodes)
            if x !=-1:
                del nodes[x]
                count+=1
                queue.extend(get_neighbours(Graph,tmp))
        components.append(count)
    return components
def is_in_list(node,nodelist):
    for i in range(len(nodelist)):
        if node.get_name()==nodelist[i].get_name():
            return i
    return -1
def print_stats(Graph):
    print("Liczba węzłów" + str(Nodes_number(Graph)))
    print("Liczba krawedzi"+str(Edges_number(Graph)))
    print("Sredni stopien wierzcholka"+str(Mean_vertice_rank(Graph)))
    print("Sredni stopien wierzcholka o labelu"+str(Mean_vertice_by_label(Graph)))
    print("Liczba nodow w grafach spojnych"+str(Component_number(Graph)))
def get_stats(Graph):
    nodes=Graph.get_nodes()[2:]
    return Nodes_number(nodes),Edges_number(Graph),Mean_vertice_rank(Graph,nodes),Mean_vertice_by_label(Graph,nodes),Component_number(Graph,nodes)