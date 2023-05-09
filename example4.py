# 遅いプログラム（線形探索を使ってリスト内の値が存在するかどうか調べる）


def find_value_slow(arr, target):
    for value in arr:
        if value == target:
            return True
    return False


def main():
    arr = list(range(100000))
    print(find_value_slow(arr, 99999))


if __name__ == "__main__":
    main()
