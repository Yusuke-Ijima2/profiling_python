import os
import ast


class ParentNodeTrackingAstVisitor(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.parent_tracker = []  # 訪れたノードの親ノードを追跡するためのリスト

    def visit(self, node):
        super().visit(node)
        if self.parent_tracker and self.parent_tracker[-1] is node:
            self.parent_tracker.pop()

    def generic_visit(self, node):
        self.parent_tracker.append(node)
        super().generic_visit(node)
        if self.parent_tracker[-1] is node:
            self.parent_tracker.pop()


# ast.NodeVisitorを継承したクラスを作成します。このクラスは、抽象構文木を訪れるためのツールとなります。
class ListComprehensionPotentialFinder(ParentNodeTrackingAstVisitor):
    def __init__(self):
        super().__init__()
        self.parent = None
        # potentialフラグは、リスト内包表記に変換可能なforループを見つけた場合にTrueとなります。
        self.potential = False
        # if-elif構造の存在を検出するフラグを追加します。
        self.has_elif = False
        self.has_break = False
        self.has_mismatched_continue = False

    def visit_Break(self, node):
        self.has_break = True

    def visit_Continue(self, node):
        if len(self.parent_tracker) >= 2:
            parent = self.parent_tracker[-1]
            grandparent = self.parent_tracker[-2]
            if isinstance(parent, ast.If) and isinstance(grandparent, ast.For):
                # print("Continue文はForループ直下のIf文の中にあります")
                self.potential = True
            else:
                # print("Continue文はForループ直下のIf文の中にありません")
                self.potential = False  # continue文がForループ直下のIf文の中にない場合、potentialをFalseに設定します
        else:
            # print("Continue文が2つ以上の祖先ノードを持っていません")
            self.potential = True
        self.generic_visit(node)

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

    def visit_If(self, node):
        # Ifノードが見つかるたびに呼び出されます。
        # 'elif'が存在するかどうかをチェックします。
        # 'orelse'部分が1つのIfノードであれば、それは'elif'であると見なせます。
        if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
            self.has_elif = True
        # Ifノード内にさらにIfノードがあるかもしれないため、それをチェックするためにgeneric_visitを呼び出します。
        self.generic_visit(node)

    def visit_While(self, node):
        # whileループノードを訪れるたびに呼び出されます。
        # whileループ内に2つ以下のステートメントがある場合を確認します。
        if len(node.body) <= 2:
            for statement in node.body:
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
        # whileループ内にさらにforループやif文があるかもしれないため、それをチェックするためにgeneric_visitを呼び出します。
        self.generic_visit(node)

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

    # リスト内包表記に変換可能で、かつif-elif構造が存在しない場合に限りTrueを返します。
    return finder.potential and not finder.has_elif and not finder.has_break and not finder.has_mismatched_continue


# ディレクトリを指定します。
directory = '/Users/iijimayuusuke/Profile_yusuke_ijima/ast/list_comprehension/before/analysis/test_code'

# ディレクトリ内の全てのPythonファイルを検出します。
filepaths = [os.path.join(directory, f)
             for f in os.listdir(directory) if f.endswith('.py')]

# 各ファイルについてリスト内包表記に変換可能なforループが存在するかをチェックします。
for filepath in filepaths:
    filename = os.path.basename(filepath)
    print(f"{filename}: {has_potential_for_list_comprehension(filepath)}")
