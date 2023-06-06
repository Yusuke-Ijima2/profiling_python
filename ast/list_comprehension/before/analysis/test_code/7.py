# そして、 switch の代わりに if-elif-else 構文を使用したコード例を示します。これもリスト内包表記に直接変換することはできません。
nums = []
for i in range(10):
    if i % 3 == 0:
        nums.append(i)
    else:
        nums.append(i * 3)
