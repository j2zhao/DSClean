"""
Parse Python AST graph and annotate functions
"""
import ast
#import networkx
from astmonkey import visitors, transformers
FUNCTIONS = {'train_test_split': None}

class ASTDecorator(ast.NodeTransformer):
    def visit_Call(self, node):
        pass
        #if 


# def annotate_ast(source_code):
#     node = ast.parse(source_code)
#     node = transformers.ParentChildNodeTransformer().visit(node)
#     visitor = visitors.GraphNodeVisitor()
#     visitor.visit(node)
#     for n in ast.walk(node):
#         if n.
#     #visitor.graph.write_png('graph_1.png')
#     #print(ast.dump(node))