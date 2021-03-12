""""
Different classes of nodes
"""

from ds_nodes.ds_base import DSNode
import copy
import numpy as np

class SplitNode(DSNode):
    def __init__(self, node):
        self.node = node

    def call(self, input, func, output):
        # we want to run the same splitting function on the lineage array as well.
        # so we do want to reduce randomness? -> at the same time, it should work for any randomness
        """copy the data groups split from the program"""
        outputs = func(input)
        self.data_split = copy.deepcopy(outputs) # we don't want to do this for every function or we would save too many copies?
        return outputs

class TimeNode(DSNode):
    # currently assuming users give a sorting function
    def __init__(self, node, function):
        self.node = node
        self.order_func = function # problem is that this might not take care of different files?

    def call(self, input, func, output):
        """
        Input: is original array because we start our graph here
        """
        return self.order_func(output)

#whether we need this or not depends on the data pertubation step -> ignore for now   
class BijectNode(DSNode):
    def __init__(self, node):
        self.node = node

    def call(self, input, func, output):
        # assuming that we have an input we don't need to do anything -> can make more efficient later
        return input

class SelectionNode(DSNode):
    def __init__(self, node):
        self.node = node


class AggregateNode(DSNode):
    def __init__(self, node):
        self.node = node
    
    def call(self, input, func, output):
        pass