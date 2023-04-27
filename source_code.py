# source_code.py
def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def main():
    print(fibonacci(20))


if __name__ == "__main__":
    main()
