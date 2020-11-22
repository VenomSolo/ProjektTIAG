from pydot import *
from enum import Enum
from random import Random
import parser

class Mode(Enum):
    RANDOM = 0
    MANUAL = 1

def get_neighbours(dot, node):
    edges = dot.get_edges()
    name = node.get_name()
    ret = []
    for e in edges:
        if e.get_source() == name:
            ret.append(dot.get_node(e.get_destination())[0])
        elif e.get_destination() == name:
            ret.append(dot.get_node(e.get_source())[0])
    return ret

def get_node_label(dot, label):
    return [n for n in dot.get_nodes() if n.get("label") is label]

def delete_node(dot, node):
    neighbours = get_neighbours(dot, node)
    edges = []
    v1_name = node.get_name()
    for n in neighbours:
        v2_name = n.get_name()
        if len(dot.get_edge(v1_name, v2_name)) != 0:
            edges += dot.get_edge(v1_name, v2_name)
        if len(dot.get_edge(v2_name, v1_name)) != 0:
            edges += dot.get_edge(v2_name, v1_name)
    for e in edges:
        dot.del_edge(e.get_source(), e.get_destination())
    dot.del_node(v1_name)

def apply_production_random(dot, pair, counter):
    leftSide = pair.transformation.entry
    candidates = get_node_label(dot, leftSide)
    if len(candidates) == 0: return counter
    rnd = Random()
    index = rnd.randint(0, len(candidates)-1)
    return _apply_production(dot, pair, counter, candidates[index].get_name())

def apply_production(dot, pair, counter, index):
    if dot.get_node(index)[0].get("label") is not pair.transformation.entry:
        return counter
    else: return _apply_production(dot, pair, counter, index)
    

def _apply_production(dot, pair, counter, index):
    #print(index)
    node = dot.get_node(index)[0]
    neighbours = get_neighbours(dot, node)
    delete_node(dot, node)
    vertexes = pair.production.get_node_list()
    #print("Vertexes in sub: ", len(vertexes))
    edges = pair.production.get_edge_list()
    transform = pair.transformation
    dictMap = {vertexes[c-counter].get_name() : str(c) for c in range(counter, counter + len(vertexes))}
    newVertexes = []
    for v in vertexes:
        newVertexes.append(Node(dictMap[v.get_name()]))
        n = newVertexes[len(newVertexes)-1]
        n.set("label", v.get("label"))
        dot.add_node(n)
    for e in edges:
        #print(dictMap[e.get_source()], dictMap[e.get_destination()])
        dot.add_edge(Edge(dictMap[e.get_source()], dictMap[e.get_destination()]))
    for n in neighbours:
        if n.get("label") not in transform.bindings: continue
        for bind in transform.bindings[n.get("label")]:
            for v in newVertexes:
                if v.get("label") is bind:
                    dot.add_edge(Edge(n.get_name(), v.get_name()))
    return counter + len(vertexes)

