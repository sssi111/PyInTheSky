import numpy as np
from src.arithmetic import Matrix


def main():
    np.random.seed(0)
    matrix1 = Matrix(np.random.randint(0, 10, (10, 10)))
    matrix2 = Matrix(np.random.randint(0, 10, (10, 10)))

    sum_matrix = matrix1 + matrix2
    mul_matrix = matrix1 * matrix2
    matmul_matrix = matrix1 @ matrix2

    sum_matrix.to_file('matrix+.txt')
    mul_matrix.to_file('matrix*.txt')
    matmul_matrix.to_file('matrix@.txt')


if __name__ == '__main__':
    main()
