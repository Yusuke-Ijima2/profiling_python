# 関数呼び出しを含むループ
def square(x):
    return x ** 2


nums = []
for i in range(10):
    nums.append(square(i))
