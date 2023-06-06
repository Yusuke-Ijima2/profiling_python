def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total


def main():
    # ユーザーから数値のリストを入力
    input_str = input("数値のリストをカンマ区切りで入力してください: ")
    # numbers = [int(num) for num in input_str.split(",")]
    numbers = []
    input_list = input_str.split(",")
    for num in input_list:
        numbers.append(int(num))

    # 合計を計算
    total = calculate_sum(numbers)

    # 結果を表示
    print("入力された数値の合計: ", total)


if __name__ == "__main__":
    main()
