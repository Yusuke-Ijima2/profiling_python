import cProfile
import pstats


def example_function(n):
    sum = 0
    for i in range(n):
        sum += i
    return sum


# cProfileを使って関数を実行
profiler = cProfile.Profile()
profiler.runcall(example_function, 10000)

# pstatsで結果を解析
stats = pstats.Stats(profiler)
stats.strip_dirs().sort_stats("cumulative").print_stats()
