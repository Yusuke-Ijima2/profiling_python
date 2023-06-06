# forループ内で複数の条件を使用
result = []
for i in range(10):
    if i % 2 == 0 and i % 3 == 0:
        result.append(i)
