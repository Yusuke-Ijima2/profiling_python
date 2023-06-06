# breakやcontinueを含むループ
nums = []
for i in range(10):
    if i == 5:
        continue
    nums.append(i)
