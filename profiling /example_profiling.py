import cProfile
import pstats


def example_function1(n):
    sum = 0
    for i in range(n):
        sum += i
    return sum


def example_function2(n):
    sum = 0
    for i in range(n):
        sum += i
    return sum


# cProfileを使って関数を実行
# cProfile.Profile インスタンスを作成
profiler = cProfile.Profile()

# runcall を使って example_function をプロファイリング
# 関数を引数nで実行する
# profiler.runcall(関数, n)
profiler.runcall(example_function1, 10000)
profiler.runcall(example_function2, 10000)

# pstatsで結果を解析
# Stats オブジェクトを作成し、データを解析
stats = pstats.Stats(profiler)

# ディレクトリ名を削除し、結果を "cumulative" 順にソート
stats.strip_dirs().sort_stats("cumulative")

# 結果をプログラム上で扱う
for func_tuple, (cc, nc, tt, ct, callers) in stats.stats.items():
    func_name = func_tuple[2]

    # disableメソッドを除外
    # プロファイリング結果から disable メソッドを除外するための条件
    if func_name == "<method 'disable' of '_lsprof.Profiler' objects>":
        continue

    # 関数名、呼び出し回数、実行時間を出力
    print(f"関数名: {func_name}")
    print(f"呼び出し回数: {cc}")
    print(f"実行時間: {ct}秒")
    print()
