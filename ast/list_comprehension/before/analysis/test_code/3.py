# forループ内で複合的な計算を行う
result = []
for i in range(5):
    # print(i, j)
    for j in range(5):
        result.append((i, j))
        # print(i, j)
