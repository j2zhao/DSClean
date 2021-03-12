"""
parse data graph to convert to lineage
"""
from ds_nodes import *
from ds_errors import *
import networkx as nx
import pickle
import sys

node_conv = GRAPH_TO_DSNODE
errors_conv = FUNC_TO_ERRORS

def parse_graph(graph):
    for node in graph.nodes:
        name = graph.nodes[node]['function_name']
        if name in node_conv:
            graph.nodes[node]['lineage'] = node_conv[name]
        elif name == 'new':
            graph.nodes[node]['lineage'] = None
        else:
            graph.nodes[node]['lineage'] =  BijectNode()
    return graph

# def check_graph_backwards(graph):

def check_graph_forwards(graph):
    check_errors = []
    for node in graph.nodes:
        func = graph.nodes[node]['function_name']
        
        prevs = graph.predecessors(node)
        
        if 'error' in graph.nodes[node]:
            graph.nodes[node]['error'].array(graph, node, prevs)
            check_errors.append(graph.nodes[node]['error'])

        if func != 'new':
            inputs = []
            for prev in prevs:
                if 'lineage' in graph.nodes[prev]:
                    inputs.append(graph.nodes[prev]['lineage'])
                else:
                    inputs.append(None)
            outputs = graph.nodes[node]['lineage'].call_forward(inputs)
            sucs = list(graph.successors(node))
            for check_error in check_errors:
                error = check_error.check_forwards(outputs)
                if error:
                    print('ERROR AT:')
                    print(graph.nodes[node])
                    return error
            if len(sucs) == len(outputs):
                for i, output in enumerate(outputs):
                    graph.nodes[sucs[i]]['lineage'] = output
    return False

def find_errors(graph):
    for node in graph.nodes:
        func = graph.nodes[node]['function_name']
        if func in errors_conv:
            graph.nodes[node]['error'] = errors_conv[func]
    
    check_graph_forwards(graph)

if __name__ == '__main__':
    graph_name = sys.argv[1]
    with open(graph_name, 'rb') as f:
        graph = pickle.load(f)
    
    graph = parse_graph(graph)
    find_errors(graph)