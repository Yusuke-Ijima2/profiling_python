import ast


code = """
x = []
for i in range(10):
    x.append(i)
"""

print(ast.dump(ast.parse(code), indent=4))
