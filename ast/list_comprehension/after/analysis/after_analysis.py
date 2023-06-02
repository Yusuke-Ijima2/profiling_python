import os
import ast


class ListComprehensionFinder(ast.NodeVisitor):
    def __init__(self):
        self.found = False  # リスト内包表記の検出フラグを初期化します。

    def visit_ListComp(self, node):
        # ListCompノードが見つかるたびに呼び出されます。
        self.found = True  # リスト内包表記を見つけたので、検出フラグを立てます。


def has_list_comprehension(filepath):
    with open(filepath, 'r') as file:
        code = file.read()

    tree = ast.parse(code)

    finder = ListComprehensionFinder()
    finder.visit(tree)

    return finder.found


# ディレクトリを指定します。
directory = '/Users/iijimayuusuke/Profile_yusuke_ijima/ast/list_comprehension/after/analysis/test_code'

# ディレクトリ内の全てのPythonファイルを検出します。
filepaths = [os.path.join(directory, f)
             for f in os.listdir(directory) if f.endswith('.py')]

# 各ファイルについてリスト内包表記に変換可能なforループが存在するかをチェックします。
for filepath in filepaths:
    filename = os.path.basename(filepath)
    print(f"{filename}: {has_list_comprehension(filepath)}")
