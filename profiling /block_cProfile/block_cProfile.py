import cProfile
import pstats
from io import StringIO
import importlib.util


def format_time(time_in_seconds):
    if time_in_seconds < 1e-6:
        return f"{time_in_seconds * 1e9:.2f} ns"
    elif time_in_seconds < 1e-3:
        return f"{time_in_seconds * 1e6:.2f} µs"
    elif time_in_seconds < 1:
        return f"{time_in_seconds * 1e3:.2f} ms"
    else:
        return f"{time_in_seconds:.2f} s"


# source_code.pyファイルをインポートする関数
def import_source_code(file_path):
    spec = importlib.util.spec_from_file_location("source_code", file_path)
    source_code = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source_code)
    return source_code


# ソースコードのプロファイリングを行い、結果を表示する関数
def profile_code(source_code):
    pr = cProfile.Profile()
    pr.enable()  # プロファイリングを開始
    source_code.main()
    pr.disable()  # プロファイリングを終了

    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")

    # カスタム書式で出力を整形
    format_str = "{:<10} {:<15} {}"
    print(format_str.format("ncalls", "tottime", "filename:lineno(function)"))
    print("-" * 80)

    for func in ps.fcn_list:
        cc, nc, tt, ct, callers = ps.stats[func]
        ncalls = f"{nc} ({cc})" if nc != cc else str(nc)
        tottime = format_time(tt)
        file, lineno, func_name = func

        print(format_str.format(ncalls, tottime,
              f"{file}:{lineno}({func_name})"))

        total_time = sum(tt for (_, _, tt, _, _) in ps.stats.values())
        formatted_total_time = format_time(total_time)
        print(f"\nTotal time: {formatted_total_time}")


source_code_file = "source_code.py"
source_code = import_source_code(source_code_file)

if __name__ == "__main__":
    profile_code(source_code)
