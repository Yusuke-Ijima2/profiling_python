from line_profiler import LineProfiler
import importlib.util
import os


def profile_code(file_path: str) -> None:
    spec = importlib.util.spec_from_file_location("source_code", file_path)
    source_code = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source_code)

    function_names = [
        obj.__name__ for obj in source_code.__dict__.values() if hasattr(obj, '__call__')]

    profiler = LineProfiler()
    for name in function_names:
        profiler.add_function(getattr(source_code, name))

    profiler.enable_by_count()
    source_code.main()
    profiler.disable_by_count()

    profiler.print_stats()


source_code_file = "source_code.py"

profile_code(source_code_file)
