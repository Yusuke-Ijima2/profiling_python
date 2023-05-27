import ast


class CallCollector(ast.NodeVisitor):
    def __init__(self):
        self.calls = []

    def visit_Call(self, node):
        self.calls.append(ast.dump(node))
        self.generic_visit(node)


source_code = """
def foo(x):
    return x * 2

y = foo(10)
"""

tree = ast.parse(source_code)
collector = CallCollector()
collector.visit(tree)

for call in collector.calls:
    print(call)
