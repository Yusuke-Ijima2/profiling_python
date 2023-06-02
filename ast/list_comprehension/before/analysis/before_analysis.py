import os
import ast


# ast.NodeVisitorを継承したクラスを作成します。このクラスは、抽象構文木を訪れるためのツールとなります。
class ListComprehensionPotentialFinder(ast.NodeVisitor):
    def __init__(self):
        # potentialフラグは、リスト内包表記に変換可能なforループを見つけた場合にTrueとなります。
        self.potential = False

    def visit_For(self, node):
        # forループノードを訪れるたびに呼び出されます。
        # forループ内に一つのステートメントだけがある場合を確認します。
        if len(node.body) == 1:
            statement = node.body[0]
            # ステートメントがif文だった場合を確認します。
            if isinstance(statement, ast.If):
                # if文内に一つのステートメントだけがある場合を確認します。
                if len(statement.body) == 1:
                    if_body_statement = statement.body[0]
                    # ステートメントがappendメソッドの呼び出しだった場合、potentialフラグをTrueにします。
                    if self.is_append_call(if_body_statement):
                        self.potential = True
            # ステートメントがif文でなく、appendメソッドの呼び出しだった場合、potentialフラグをTrueにします。
            elif self.is_append_call(statement):
                self.potential = True
        # forループ内にさらにforループやif文があるかもしれないため、それをチェックするためにgeneric_visitを呼び出します。
        self.generic_visit(node)

    def is_append_call(self, statement):
        # ステートメントが式で、かつその式が関数呼び出しだった場合をチェックします。
        if isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call):
            call_node = statement.value
            # 関数呼び出しがappendメソッドのものだった場合をチェックします。
            if isinstance(call_node.func, ast.Attribute) and call_node.func.attr == 'append':
                # リストに追加される値がforループの変数に依存しているかをチェックします。
                if isinstance(call_node.args[0], ast.Name):
                    return True
        return False

    def is_append_call(self, statement):
        # ステートメントが式（Expr）で、その式が関数呼び出し（Call）であるかを確認します。
        if isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call):
            call_node = statement.value
            # 関数呼び出しが実際にリストのappendメソッドであるかを確認します。
            return isinstance(call_node.func, ast.Attribute) and call_node.func.attr == 'append'
        # 上記の条件に一致しない場合はFalseを返します。
        return False


def has_potential_for_list_comprehension(filepath):
    with open(filepath, 'r') as file:
        code = file.read()

    tree = ast.parse(code)

    finder = ListComprehensionPotentialFinder()
    finder.visit(tree)

    return finder.potential


# ディレクトリを指定します。
directory = '/Users/iijimayuusuke/Profile_yusuke_ijima/ast/list_comprehension/before/analysis/test_code'

# ディレクトリ内の全てのPythonファイルを検出します。
filepaths = [os.path.join(directory, f)
             for f in os.listdir(directory) if f.endswith('.py')]

# 各ファイルについてリスト内包表記に変換可能なforループが存在するかをチェックします。
for filepath in filepaths:
    filename = os.path.basename(filepath)
    print(f"{filename}: {has_potential_for_list_comprehension(filepath)}")
