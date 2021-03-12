"""
Capture data science errors in the program
"""
import ast
import numpy as np


class DataErrors():
    def array(self, node):
        raise NotImplemented()

    def check_backwards(self, node, inputs):
        raise NotImplemented()

    def check_forwards(self, node, inputs, outputs):
        raise NotImplemented()

class TimeErrors(DataErrors):
    def array(self, graph, node, prevs):
        n = graph.nodes[node]
        i = ast.literal_eval(node)
        graph.nodes[node]['lineage'] = np.arange(i[0][0])

    def check_backwards(self, node, inputs, outputs):
        raise NotImplemented()

    def check_forwards(self, outputs):
        for output in outputs:
            index = np.arange(output.shape[0])
            test = np.sum(output > index)
            if test > 0:
                return True

# class SplitErrors():
#     def array(self, node):
#         raise NotImplemented()

#     def walk_backwards(self, node, edge):
#         raise NotImplemented()

#     def walk_forwards(self, node, edge):
#         raise NotImplemented()

FUNC_TO_ERRORS = {'new': TimeErrors()}