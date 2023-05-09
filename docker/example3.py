#  メモリ使用量が高いデータ構造（リストの結合）


def join_lists(lists):
    result = []
    for l in lists:
        result.extend(l)
    return result


def main():
    lists = [list(range(1000)) for _ in range(1000)]
    result = join_lists(lists)


if __name__ == "__main__":
    main()
