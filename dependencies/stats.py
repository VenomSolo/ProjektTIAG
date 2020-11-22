import pydot
from .utilities import get_neighbours
def Nodes_number(nodes):
    return len(nodes)
def Edges_number(Graph):
    return len(Graph.get_edges())
def Mean_vertice_by_label(Graph,nodes):
    counts = dict()
    for node in nodes:
        tmp=node.get('label')
        counts[tmp] =counts.get(tmp, [0,0])
        counts[tmp][0]+=len(get_neighbours(Graph,node))
        counts[tmp][1]+=1
    ret=[]
    for item in counts.items():
        ret.append([item[0],round(item[1][0]/item[1][1],2)])
    return ret
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
def get_stats(Graph):
    nodes=Graph.get_nodes()[2:]
    return Nodes_number(nodes),Edges_number(Graph),Mean_vertice_by_label(Graph,nodes),Component_number(Graph,nodes)