from line_profiler import LineProfiler
import importlib.util


# profile_code関数を定義します。
# この関数は、指定されたファイルパスのPythonソースコードをプロファイリングします。
def profile_code(file_path: str) -> None:
    # importlibを使って、指定されたファイルパスのソースコードをインポートします。
    spec = importlib.util.spec_from_file_location("source_code", file_path)
    source_code = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source_code)

    # インポートされたソースコードの関数名を取得します。
    function_names = [
        obj.__name__ for obj in source_code.__dict__.values() if hasattr(obj, '__call__')]

    # line_profilerオブジェクトを作成し、インポートされた関数を追加します。
    profiler = LineProfiler()
    for name in function_names:
        profiler.add_function(getattr(source_code, name))

    # line_profilerを有効にして、インポートされたソースコードのmain関数を実行します。
    profiler.enable_by_count()
    source_code.main()
    profiler.disable_by_count()

    # プロファイリング結果を表示します。
    profiler.print_stats()


# ソースコードファイルのパスを指定します。
source_code_file = "source_code.py"

# profile_code関数を呼び出して、指定されたソースコードファイルをプロファイリングします。
profile_code(source_code_file)
