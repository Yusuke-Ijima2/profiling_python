import cProfile
import pstats
from io import StringIO
import importlib.util


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
    format_str = "{:<10} {:<10} {:<10} {:<10} {:<10} {}"
    print(format_str.format("ncalls", "tottime", "percall",
          "cumtime", "percall", "filename:lineno(function)"))
    print("-" * 80)

    for func in ps.fcn_list:
        cc, nc, tt, ct, callers = ps.stats[func]
        ncalls = f"{nc} ({cc})" if nc != cc else str(nc)
        tottime = f"{tt:0.6f}"
        percall = f"{tt/nc:0.6f}"
        cumtime = f"{ct:0.6f}"
        percall2 = f"{ct/cc:0.6f}"
        file, lineno, func_name = func

        print(format_str.format(ncalls, tottime, percall,
              cumtime, percall2, f"{file}:{lineno}({func_name})"))


source_code_file = "source_code.py"
source_code = import_source_code(source_code_file)

if __name__ == "__main__":
    profile_code(source_code)
