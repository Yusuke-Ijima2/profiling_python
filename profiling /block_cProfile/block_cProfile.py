import linecache
import line_profiler


# 指定されたファイル名と行番号からソースコードを取得する関数
def get_source_code(filename, lineno):
    return linecache.getline(filename, lineno).strip()


# 与えられたソースコードとターゲット関数を用いて、行ごとの実行時間を計測する関数
def line_profiling(source_code, target_functions):
    # line_profilerオブジェクトを作成
    lp = line_profiler.LineProfiler()

    # ターゲット関数をプロファイラに追加
    for func in target_functions:
        lp.add_function(func)

    # プロファイリングを開始
    lp.enable_by_count()
    lp.run(source_code)
    lp.disable_by_count()

    # プロファイリング結果を取得
    profile_data = lp.get_stats()

    results = {}
    # プロファイリング結果から関数ごとの実行時間を取得
    for (function_tuple, timings) in profile_data.timings.items():
        # 各行の実行時間を取得
        for (line, nhits, time) in timings:
            source_line = get_source_code(function_tuple[0], line)
            results.setdefault(
                line, {"source_line": source_line, "nhits": 0, "time": 0})
            results[line]["nhits"] += nhits
            results[line]["time"] += time

    return results


# 実行時間プロファイリングの対象となるサンプル関数1
def example_function():
    total = 0
    for i in range(10):
        total += i
    return total


# 実行時間プロファイリングの対象となるサンプル関数2
def another_function():
    total = 0
    for i in range(20):
        total += i
    return total


if __name__ == "__main__":
    # プロファイリング対象のソースコード
    sample_code = "example_function()\nanother_function()"

    # 行ごとの実行時間プロファイリングを実行
    profiling_results = line_profiling(
        sample_code, [example_function, another_function])

    # プロファイリング結果を出力
    for line, result in profiling_results.items():
        # Convert to microseconds
        avg_time_per_hit = (result['time'] / result['nhits'])
        print(
            f"{result['source_line']}: nhits={result['nhits']}, time={avg_time_per_hit:.2f}マイクロ秒")
