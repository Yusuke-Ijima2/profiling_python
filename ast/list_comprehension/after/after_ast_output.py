import ast


code = """
x = [i for i in range(10)]
"""

print(ast.dump(ast.parse(code), indent=4))
