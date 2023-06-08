# forループ内で複合的な計算を行う
result = []
for i in range(5):
    print()
    for j in range(5):
        print()
        for k in range(5):
            result.append((i, j, k))
