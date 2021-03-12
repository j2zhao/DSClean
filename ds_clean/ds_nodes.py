""""
Different classes of nodes
"""
import copy
import numpy as np

class DSNode():

    def call_forward(self):
        raise NotImplemented()

    def call_backward(self):
        raise NotImplemented()
    
    # def mod_ast(self):
    #     """some function for changing the ast -> todo?"""
    #     pass


#whether we need this or not depends on the data pertubation step -> ignore for now   
class BijectNode(DSNode):

    def call_forward(self, inputs):
        # assuming that we have an input we don't need to do anything -> can make more efficient later
        return inputs

    def call_backward(self, inputs):
        # assuming that we have an input we don't need to do anything -> can make more efficient later
        return inputs

class AddNode(DSNode):

    def call_forward(self, inputs):
        # assuming that we have an input we don't need to do anything -> can make more efficient later
        if inputs[0] is not None and inputs[1] is not None:
            return [np.maximum(inputs[0], inputs[1])]
        else:
            return [None]
    def call_backward(self, inputs):
        # assuming that we have an input we don't need to do anything -> can make more efficient later
        raise NotImplemented()

class AggregateNode(DSNode):

    def call_forward(self, inputs):
        # assuming that we have an input we don't need to do anything -> can make more efficient later
        output = []
        for input in inputs:
            output.append(np.ones(input.shape)*np.max(input))
        return output

    def call_backward(self, inputs):
        raise NotImplemented()

class SelectionNode(DSNode):
    def call_forward(self):
        raise NotImplemented()

    def call_backward(self):
        raise NotImplemented()

class JoinNode(DSNode):
    def call_forward(self):
        raise NotImplemented()

    def call_backward(self):
        raise NotImplemented()

GRAPH_TO_DSNODE = {'add,__call__': AddNode(), 'add,reduce': AggregateNode()}