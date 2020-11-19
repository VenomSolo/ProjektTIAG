from pydot import *
from enum import Enum
from random import Random
import parser

class Mode(Enum):
    RANDOM = 0
    MANUAL = 1

def get_neighbours(dot, node):
    edges = dot.get_edges()
    name = node.get('name')
    ret = []
    for e in edges:
        if e.get_source() is name or e.get_destination() is name:
            ret.append(dot.get_node(name))
    return ret

def get_node_label(dot, label):
    return [n for n in dot.get_nodes if n.get("label") is label]

def delete_node(dot, node):
    neighbours = get_neighbours(dot, node)
    edges = []
    v1_name = node.get("name")
    for n in neighbours:
        v2_name = n.get("name")
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
    if len(candidates) == 0: return -1
    rnd = Random()
    index = rnd.randint(0, len(candidates)-1)
    return _apply_production(dot, pair, candidates[index])

def apply_production(dot, pair, counter, index):
    if dot.get_node(index)[0].get("label") is not pair.transformation.entry:
        return -1
    else: return _apply_production(dot, pair, index)
    

def _apply_production(dot, pair, counter, index):
    node = dot.get_node(index)
    neighbours = get_neighbours(dot, node)
    vertexes = pair.production.get_node_list()
    edges = pair.production.get_edge_list()
    transform = pair.transformation
    dictMap = {vertexes[c-counter].get("name") : c for c in range(counter, counter + len(vertexes))}
    for v in vertexes:
        v.set_name(dictMap[v.get("name")])
        dot.add_node(v)
    for e in edges:
        dot.add_edge(Edge(dictMap[e.get_source()], dictMap[e.get_source()]))
    for n in neighbours:
        for bind in transform.bindings[n.get("label")]:
            for v in vertexes:
                if v.get("label") is bind:
                    dot.add_edge(Edge(n.get("name"), v.get("name")))
    return counter + len(vertexes)

    pass

