import ast


class ListCompFinder(ast.NodeVisitor):
    def __init__(self):
        self.found = False

    def visit_ListComp(self, node):
        self.found = True


def contains_list_comprehension(code):
    tree = ast.parse(code)
    finder = ListCompFinder()
    finder.visit(tree)
    return finder.found


# 使用例
code = """
x = [i for i in range(10)]
"""
print(contains_list_comprehension(code))  # Trueを返す

code = """
x = []
for i in range(10):
    x.append(i)
"""
print(contains_list_comprehension(code))  # Falseを返す
