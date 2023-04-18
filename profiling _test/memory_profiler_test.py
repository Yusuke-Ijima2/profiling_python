from memory_profiler import profile


@profile
def example_function(n):
    sum = 0
    for i in range(n):
        sum += i
    return sum


# memory_profilerを使って関数を実行
example_function(10000)
