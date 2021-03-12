""""
Different classes of nodes
"""
import copy
import numpy as np

class DSNode():

    def call_forward(self):
        pass

    def call_backward(self):
        pass
    
    # def mod_ast(self):
    #     """some function for changing the ast -> todo?"""
    #     pass


#whether we need this or not depends on the data pertubation step -> ignore for now   
class BijectNode(DSNode):
    def __init__(self, node):
        self.node = node

    def call_forward(self, inputs):
        # assuming that we have an input we don't need to do anything -> can make more efficient later
        return inputs

    def call_backward(self, inputs):
        # assuming that we have an input we don't need to do anything -> can make more efficient later
        return inputs

class AggregateNode(DSNode):
    def __init__(self, node):
        self.node = node
    
    def call_forward(self, inputs):
        # assuming that we have an input we don't need to do anything -> can make more efficient later
        output = []
        for input in inputs:
            output.append(np.max(input))
        return inputs

    def call_backward(self, inputs):
        raise NotImplemented()

class SelectionNode(DSNode):
    def __init__(self, node):
        self.node = node

class JoinNode(DSNode):
    def __init__(self, node):
        self.node = node

    def call_forward(self, inputs):
        # assuming that we have an input we don't need to do anything -> can make more efficient later
        return inputs

GRAPH_TO_DSNODE = {'_reduce': }