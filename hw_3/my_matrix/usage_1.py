import numpy as np

from src.matrix import Matrix


def main():
    np.random.seed(0)
    matrix_a = np.random.randint(0, 10, (10, 10))
    matrix_b = np.random.randint(0, 10, (10, 10))

    matrix1 = Matrix(matrix_a.tolist())
    matrix2 = Matrix(matrix_b.tolist())

    try:
        result_add = matrix1 + matrix2
        result_add.to_file('matrix+.txt')
    except ValueError as e:
        print(f"Addition error: {e}")

    try:
        result_mul = matrix1 * matrix2
        result_mul.to_file('matrix*.txt')
    except ValueError as e:
        print(f"Component-wise multiplication error: {e}")

    try:
        result_matmul = matrix1 @ matrix2
        result_matmul.to_file('matrix@.txt')
    except ValueError as e:
        print(f"Matrix multiplication error: {e}")


if __name__ == '__main__':
    main()
