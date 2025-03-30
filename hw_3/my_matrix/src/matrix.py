from src.matrix_hash import MatrixHash
from functools import lru_cache

class Matrix(MatrixHash):
    def __init__(self, data):
        self.rows = len(data)
        if self.rows == 0:
            self.cols = 0
        else:
            self.cols = len(data[0])
            for row in data:
                if len(row) != self.cols:
                    raise ValueError(
                        "All rows must have the same number of columns")
        self.data = data

    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices dimensions do not match for addition")
        result = [
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def __mul__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(
                "Matrices dimensions do not match for component-wise multiplication")
        result = [
            [self.data[i][j] * other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    @lru_cache(maxsize=None)
    def __matmul__(self, other):
        if self.cols != other.rows:
            raise ValueError("Matrices cannot be multiplied: columns of first != rows of second")
        result = []
        for i in range(self.rows):
            row = []
            for j in range(other.cols):
                sum_val = 0
                for k in range(self.cols):
                    sum_val += self.data[i][k] * other.data[k][j]
                row.append(sum_val)
            result.append(row)
        return Matrix(result)

    def to_file(self, filename):
        with open(filename, 'w') as f:
            for row in self.data:
                f.write(' '.join(map(str, row)) + '\n')
