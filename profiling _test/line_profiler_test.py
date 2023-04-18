from line_profiler import LineProfiler


def example_function(n):
    sum = 0
    for i in range(n):
        sum += i
    return sum


# line_profilerを使って関数を実行
lp = LineProfiler()
lp_wrapper = lp(example_function)
lp_wrapper(10000)

# 結果を表示
lp.print_stats()
