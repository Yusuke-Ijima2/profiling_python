import ast


# ノード訪問者クラスを作成します。このクラスは特定のASTノードを訪問する機能を持ちます。
class ListComprehensionPotentialFinder(ast.NodeVisitor):
    # 初期化メソッドでは、リスト内包表記の可能性を示すフラグをFalse（つまり、可能性はまだ見つかっていない）に設定します。
    def __init__(self):
        self.potential = False

    # forループノードを訪問するためのメソッドを定義します。
    # このメソッドは、AST内の各forループノードで呼び出されます。
    def visit_For(self, node):
        # ループ内のステートメントが1つだけで、そのステートメントが関数呼び出しであり、
        # それが 'append' メソッドの呼び出しである場合、リスト内包表記の可能性があると判断します。
        if len(node.body) == 1 and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Call):
            call_node = node.body[0].value
            if isinstance(call_node.func, ast.Attribute) and call_node.func.attr == 'append':
                self.potential = True
        # generic_visitメソッドは、現在のノードのすべての子ノードを訪問するために使用されます。
        # これは、forループノードの中に他のノード（例えば、別のforループやifステートメント）がある場合に必要です。
        self.generic_visit(node)


# この関数は、与えられたコードにリスト内包表記の可能性があるかどうかを確認します。
def has_potential_for_list_comprehension(code):
    # まず、コードをASTに解析します。
    tree = ast.parse(code)
    # 次に、作成したノード訪問者クラスのインスタンスを作ります。
    finder = ListComprehensionPotentialFinder()
    # そして、ASTを訪問します。これにより、上記で定義したvisit_Forメソッドが適切に呼び出されます。
    finder.visit(tree)
    # 最後に、リスト内包表記の可能性が見つかったかどうかを返します。
    return finder.potential


# # 使用例
# code = """
# x = []
# for i in range(10):
#     x.append(i)
# """
# print(has_potential_for_list_comprehension(code))  # Trueを返す

code = """
x = []
for i in range(10):
    x.append(i)
    print(i)
"""
print(has_potential_for_list_comprehension(code))  # Falseを返す
