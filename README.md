""line_line_profiler.py""

# Line Profiler 出力結果

以下は、`line_line_profiler.py` を使用してプロファイリングされた `source_code.py` の結果です。

## Timer unit

Timer unit: 1e-09 s

タイマーの単位は 1 ナノ秒です。これは、プロファイリングされたコードの実行時間を測定する際に使用される単位です。

## 関数ごとの結果

Total time: 0.006648 s
File: source_code.py
Function: fibonacci at line 2

# Line # Hits Time Per Hit % Time Line Contents

     2                                           def fibonacci(n):
     3     17710    1963000.0    110.8     29.5      if n == 0:
     4      4181     541000.0    129.4      8.1          return 0
     5     10945    1452000.0    132.7     21.8      elif n == 1:
     6      6765     895000.0    132.3     13.5          return 1
     7                                               else:
     8     10945    1797000.0    164.2     27.0          return fibonacci(n - 1) + fibonacci(n - 2)

このセクションでは、fibonacci 関数のプロファイリング結果が表示されています。各行の結果は以下のとおりです。

Line #: ソースコードの行番号。
Hits: その行が実行された回数。
Time: その行の合計実行時間（ナノ秒）。
Per Hit: 1 回の実行にかかった平均時間（ナノ秒）。
% Time: 関数全体の実行時間に占めるその行の実行時間の割合。

Total time: 0.021268 s
File: source_code.py
Function: main at line 11

# Line # Hits Time Per Hit % Time Line Contents

    11                                           def main():
    12         1   21268000.0 21268000.0    100.0      print(fibonacci(20))

このセクションでは、main 関数のプロファイリング結果が表示されています。結果の意味は、fibonacci 関数のセクションと同様です。

## 合計実行時間

Total time: 27.92 ms

プロファイリングされたコード全体の実行にかかった時間は、約 27.92 ミリ秒です。
