import functools
import sys
from graphviz import Digraph

def add_nodes(graph, nodes):
    for n in nodes:
        if isinstance(n, tuple):
            graph.node(n[0], **n[1])
        else:
            graph.node(n)
    return graph

def add_edges(graph, edges):
    for e in edges:
        if isinstance(e[0], tuple):
            graph.edge(*e[0], **e[1])
        else:
            graph.edge(*e)
    return graph
    
def main(argv=None):
    if argv == None:
        argv = sys.argv
    
    states = []
    edges = []
    dot = Digraph()
    
    with open(argv[1]) as inFile:
        data = inFile.read()
        segments = data.split('\n\n')
        dot.graph_attr["label"] = segments[0].split('\n')[0].split(' ')[1]
        for transition in segments[1:-1]:
            lines = transition.split('\n')
            state = lines[0].split(',')[0]
            character = lines[0].split(',')[1]
            nstate = lines[1].split(',')[0]
            ncharacter = lines[1].split(',')[1]
            nmove = lines[1].split(',')[2]
            if state not in states:
                states.append(state)
            edges.append(((state,nstate), {'label': character+", "+ncharacter+", "+nmove},))
            
        dot = add_edges(add_nodes(dot,states),edges)
        dot.render(view=True)
            
if __name__ == "__main__":
    main()