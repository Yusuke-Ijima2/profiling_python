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
        self.has_map_lambda = False
        self.has_break = False
        self.has_continue = False
        self.has_mismatched_continue = False
        self.has_non_append_call = False

    def visit_Call(self, node):
        # lambda,mapの検出
        if isinstance(node.func, ast.Name) and node.func.id == 'map':
            if len(node.args) > 0 and isinstance(node.args[0], ast.Lambda):
                self.has_map_lambda = True
        self.generic_visit(node)

    def visit_Break(self, node):
        self.has_break = True

    def visit_Continue(self, node):
        self.has_continue = True
        # if len(self.parent_tracker) >= 2:
        #     parent = self.parent_tracker[-1]
        #     grandparent = self.parent_tracker[-2]
        #     if isinstance(parent, ast.If) and isinstance(grandparent, ast.For):
        #         self.potential = True
        #     else:
        #         self.potential = False
        #         self.has_mismatched_continue = True
        # else:
        #     self.potential = True
        # self.generic_visit(node)

    def visit_For(self, node):
        all_statements_valid = True

        for statement in node.body:
            if isinstance(statement, ast.If):
                if len(statement.body) == 1:
                    if_body_statement = statement.body[0]
                    if self.is_append_call(if_body_statement):
                        self.potential = True
                    else:
                        all_statements_valid = False
            elif isinstance(statement, ast.Assign):
                continue
            elif self.is_append_call(statement):
                self.potential = True
            elif isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call):
                self.has_non_append_call = True
                all_statements_valid = False
            else:
                all_statements_valid = False

        if not all_statements_valid:
            self.potential = False

        self.generic_visit(node)

    def visit_If(self, node):
        if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
            self.has_elif = True
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
                # ステートメントが副作用を持つ可能性のある関数やメソッドの呼び出し（例：print）である場合、potentialフラグをFalseにします。
                elif isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call):
                    self.potential = False
        # whileループ内にさらにforループやif文があるかもしれないため、それをチェックするためにgeneric_visitを呼び出します。
        self.generic_visit(node)

    def is_append_call(self, statement):
        if isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call):
            call_node = statement.value
            return isinstance(call_node.func, ast.Attribute) and call_node.func.attr == 'append'
        return False


def has_potential_for_list_comprehension(filepath):
    with open(filepath, 'r') as file:
        code = file.read()

    tree = ast.parse(code)

    finder = ListComprehensionPotentialFinder()
    finder.visit(tree)

    return finder.potential and not finder.has_elif and not finder.has_break and not finder.has_continue and not finder.has_mismatched_continue and not finder.has_non_append_call or finder.has_map_lambda


directory = '/Users/iijimayuusuke/Profile_yusuke_ijima/ast/list_comprehension/before/analysis/test_code'

filepaths = [os.path.join(directory, f)
             for f in os.listdir(directory) if f.endswith('.py')]

for filepath in filepaths:
    filename = os.path.basename(filepath)
    print(f"{filename}: {has_potential_for_list_comprehension(filepath)}")
