# 速いプログラム（二分探索を使ってリスト内の値が存在するかどうか調べる）


def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_value = arr[mid]

        if mid_value == target:
            return True
        elif mid_value < target:
            left = mid + 1
        else:
            right = mid - 1
    return False


def main():
    arr = list(range(100000))
    print(binary_search(arr, 99999))


if __name__ == "__main__":
    main()
