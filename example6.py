import random

# 入力データ
numbers = [random.randint(1, 9) for _ in range(10000)]


# 重複要素の除去（速い方法）
def remove_duplicates_fast(numbers):
    return list(set(numbers))


def main():
    remove_duplicates_fast(numbers)


if __name__ == "__main__":
    main()
