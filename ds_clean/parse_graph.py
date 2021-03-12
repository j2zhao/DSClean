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
        if graph[node]['function'] in node_conv:
            graph[node]['lineage'] = node_conv[node['function']]
        elif graph[node]['function'] == 'new':
            graph[node]['lineage'] = None
        else:
            graph[node]['lineage'] =  BijectNode()
    return graph

# def check_graph_backwards(graph):

def check_graph_forwards(graph):
    check_errors = []
    for node in graph.nodes:
        func = graph[node]['function']
        if func != 'new':
            prevs = graph.predecessors(node)
            inputs = []
            if 'error' in graph[node]:
                graph[node]['error'].array(graph, node, prevs)
                check_errors.append(graph[node]['error'])

            for prev in prevs:
                if 'lineage' in graph[prev]:
                    inputs.append(graph[prev]['lineage'])
                else:
                    inputs.append(None)
            
            outputs = graph[node].call_forward(inputs)
            
            sucs = graph.successors[node]
            for i, output in enumerate(outputs):
                graph[sucs[i]]['lineage'] = output
                
            for check_error in check_errors:
                error = check_error(outputs)
                if error:
                    print(graph[node])
                    return error
    return False

def find_errors(graph):
    for node in graph.nodes:
        func = graph[node]['function']
        if func in errors_conv:
            graph[node]['error'] = errors_conv[func]
    
    check_graph_forwards(graph)

if __name__ == '__main__':
    graph_name = sys.argv[1]
    with open(graph_name, 'rb') as f:
        graph = pickle.load(f)
    
    graph = parse_graph(graph)
    find_errors(graph)