import numpy as np

class ArithmeticMixin:
    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Can only add Matrix to Matrix")
        if self.data.shape != other.data.shape:
            raise ValueError("Matrices must have the same dimensions for addition")
        return Matrix(self.data + other.data)
    
    def __mul__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Can only multiply Matrix with Matrix")
        if self.data.shape != other.data.shape:
            raise ValueError("Matrices must have the same dimensions for element-wise multiplication")
        return Matrix(self.data * other.data)
    
    def __matmul__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Can only perform matrix multiplication with Matrix")
        if self.data.shape[1] != other.data.shape[0]:
            raise ValueError("Incompatible dimensions for matrix multiplication")
        return Matrix(self.data @ other.data)

class IOMixin:
    def to_file(self, filename):
        np.savetxt(filename, self.data, fmt='%d')

class PrettyPrintMixin:
    def __str__(self):
        return np.array_str(self.data)

class PropertyMixin:
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        if not isinstance(value, np.ndarray) or value.ndim != 2:
            raise ValueError("Data must be a 2D numpy array")
        self._data = value

class Matrix(ArithmeticMixin, IOMixin, PrettyPrintMixin, PropertyMixin):
    def __init__(self, data):
        self._data = np.array(data)
        if self._data.ndim != 2:
            raise ValueError("Matrix must be 2-dimensional")
