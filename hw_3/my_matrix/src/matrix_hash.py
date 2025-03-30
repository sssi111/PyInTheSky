class MatrixHash:
    def __hash__(self):
        if self.rows == 0 or self.cols == 0:
            return 0
        total = 0
        for i in range(self.rows):
            for j in range(self.cols):
                total += self.data[i][j] * (i+1) * (j+1)
        return total % (10**9)

    def __eq__(self, other):
        return self.data == other.data
