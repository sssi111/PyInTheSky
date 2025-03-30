import pytest
import numpy as np
from src.arithmetic import Matrix

def test_addition():
    a = Matrix([[1, 2], [3, 4]])
    b = Matrix([[5, 6], [7, 8]])
    result = a + b
    expected = np.array([[6, 8], [10, 12]])
    assert np.array_equal(result.data, expected)

def test_elementwise_multiplication():
    a = Matrix([[1, 2], [3, 4]])
    b = Matrix([[5, 6], [7, 8]])
    result = a * b
    expected = np.array([[5, 12], [21, 32]])
    assert np.array_equal(result.data, expected)

def test_matrix_multiplication():
    a = Matrix([[1, 2], [3, 4]])
    b = Matrix([[5, 6], [7, 8]])
    result = a @ b
    expected = np.array([[19, 22], [43, 50]])
    assert np.array_equal(result.data, expected)

def test_addition_incompatible_shapes():
    a = Matrix([[1, 2]])
    b = Matrix([[3]])
    with pytest.raises(ValueError):
        a + b

def test_elementwise_mul_incompatible_shapes():
    a = Matrix([[1, 2]])
    b = Matrix([[3]])
    with pytest.raises(ValueError):
        a * b

def test_matmul_incompatible_shapes():
    a = Matrix([[1, 2, 3]])
    b = Matrix([[4], [5]])
    with pytest.raises(ValueError):
        a @ b

def test_setter_valid_data():
    a = Matrix([[1]])
    a.data = np.array([[2]])
    assert a.data[0, 0] == 2

def test_setter_invalid_data():
    a = Matrix([[1]])
    with pytest.raises(ValueError):
        a.data = np.array([1, 2, 3])
    with pytest.raises(ValueError):
        a.data = 'invalid'
