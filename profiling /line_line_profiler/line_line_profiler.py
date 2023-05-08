from line_profiler import LineProfiler
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


def import_source_code(file_path):
    spec = importlib.util.spec_from_file_location("source_code", file_path)
    source_code = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source_code)
    return source_code


def profile_line_code(source_code):
    function_names = [
        obj.__name__ for obj in source_code.__dict__.values() if hasattr(obj, '__call__')]

    profiler = LineProfiler()
    for name in function_names:
        profiler.add_function(getattr(source_code, name))

    profiler.enable_by_count()
    source_code.main()
    profiler.disable_by_count()

    total_time = 0
    timer_unit = profiler.timer_unit
    stats = profiler.get_stats()
    for func, timings in stats.timings.items():
        total_time += sum([time * timer_unit for _, _, time in timings])

    profiler.print_stats()

    formatted_total_time = format_time(total_time)
    print(f"\nTotal time: {formatted_total_time}")


source_code_file = "source_code.py"
source_code = import_source_code(source_code_file)

if __name__ == "__main__":
    profile_line_code(source_code)
