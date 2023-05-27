def slow_code(N=10000):
    numbers = list(range(1, N+1))
    even_numbers = []
    for num in numbers:
        if num % 2 == 0:
            even_numbers.append(num)
    return even_numbers


def fast_code(N=10000):
    numbers = list(range(1, N+1))
    even_numbers = [num for num in numbers if num % 2 == 0]
    return even_numbers
