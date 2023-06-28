import ast
import cProfile
import pstats

# サンプルソースコード
sample_code = """
def example_function():
    total = 0
    for i in range(10):
        total += i
    return total

def another_function():
    total = 0
    for i in range(20):
        total += i
    return total

example_function()
another_function()
"""


# ソースコードを解析して関数名を取得するためのクラス
class FunctionNameExtractor(ast.NodeVisitor):
    def __init__(self):
        self.function_names = []

    # 関数定義ノードに遭遇したときに呼び出されるメソッド
    def visit_FunctionDef(self, node):
        self.function_names.append(node.name)


# ソースコードを解析し、関数名を抽出
extractor = FunctionNameExtractor()
tree = ast.parse(sample_code)
extractor.visit(tree)

# 関数ごとにプロファイリングを行い、結果を格納する辞書
profiling_data = {}
for function_name in extractor.function_names:
    # cProfile.Profileオブジェクトを作成してプロファイリングを実行
    pr = cProfile.Profile()
    pr.runctx(sample_code, globals(), locals())

    # プロファイリング結果をpstats.Statsオブジェクトに変換
    ps = pstats.Stats(pr).strip_dirs().sort_stats("cumulative")
    profiling_data[function_name] = ps

# プロファイリングデータをプログラム上で利用
for function_name, ps in profiling_data.items():
    print(f"関数名: {function_name}")

    # ここで、psオブジェクトを利用して、プロファイリングデータを操作できます
    # 例: 各関数の統計情報を取得
    stats = ps.stats
    total_time = 0  # 関数の実行時間の合計を初期化
    total_calls = 0  # 関数の呼び出し回数の合計を初期化
    for func, (cc, nc, tt, ct, callers) in stats.items():
        # 関数名でフィルタリング
        if function_name in func[2]:
            total_time += ct  # 累積実行時間を合計に加算
            total_calls += cc  # 呼び出し回数を合計に加算

    # 関数の実行時間の合計と呼び出し回数の合計を表示
    print(f"呼び出し回数の合計: {total_calls}")
    print(f"実行時間の合計: {total_time}秒")
    print()
