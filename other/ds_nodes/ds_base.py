"""
Graph representation of the data science lineage
"""
import networkx as nx

class DSNode():
    def __init__(self, node):
        self.node = node

    def call(self):
        """will need some type of function which can be called from the program"""
        pass
    
    def mod_ast(self):
        """some function for changing the ast -> todo?"""
        pass

class DSTree():
    def __init__(self):
        self.root = []
        self.tree = nx.MultiDiGraph()

    def _add_leaf(self, parent, node):
        self.tree.add_node(node)
        self.tree.add_edge(parent, node)

# have a dictionary of lineages?
class Lineage():
    def __init__(self):
        self.array = None
    
    def set_array(self, array):
        # need to link arrays
        pass

class WrapperTree():
    def __init__(self):
        pass