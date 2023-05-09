# 多重ループ（行列の積）

import random


def matrix_multiply(A, B):
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result


def generate_matrix(m, n):
    return [[random.randint(0, 10) for _ in range(n)] for _ in range(m)]


def main():
    A = generate_matrix(100, 100)
    B = generate_matrix(100, 100)
    result = matrix_multiply(A, B)


if __name__ == "__main__":
    main()
