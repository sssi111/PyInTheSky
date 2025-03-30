import pytest
from src.matrix import Matrix

@pytest.fixture
def sample_matrix_2x2():
    return Matrix([[1, 2], [3, 4]])

@pytest.fixture
def sample_matrix_2x3():
    return Matrix([[1, 2, 3], [4, 5, 6]])

@pytest.fixture
def sample_matrix_3x2():
    return Matrix([[1, 2], [3, 4], [5, 6]])

def test_matrix_initialization_valid():
    data = [[1, 2], [3, 4]]
    matrix = Matrix(data)
    assert matrix.data == data
    assert matrix.rows == 2
    assert matrix.cols == 2

def test_matrix_initialization_invalid():
    with pytest.raises(ValueError):
        Matrix([[1, 2], [3]])

def test_matrix_addition_valid(sample_matrix_2x2):
    m1 = sample_matrix_2x2
    m2 = Matrix([[5, 6], [7, 8]])
    result = m1 + m2
    assert result.data == [[6, 8], [10, 12]]

def test_matrix_addition_invalid(sample_matrix_2x2):
    m1 = sample_matrix_2x2
    m2 = Matrix([[1, 2, 3], [4, 5, 6]])
    with pytest.raises(ValueError):
        m1 + m2

def test_componentwise_multiplication_valid(sample_matrix_2x2):
    m1 = sample_matrix_2x2
    m2 = Matrix([[2, 3], [4, 5]])
    result = m1 * m2
    assert result.data == [[2, 6], [12, 20]]

def test_componentwise_multiplication_invalid(sample_matrix_2x2):
    m1 = sample_matrix_2x2
    m2 = Matrix([[1, 2, 3], [4, 5, 6]])
    with pytest.raises(ValueError):
        m1 * m2

def test_matrix_multiplication_valid(sample_matrix_2x3, sample_matrix_3x2):
    m1 = sample_matrix_2x3
    m2 = sample_matrix_3x2
    result = m1 @ m2
    assert result.data == [[22, 28], [49, 64]]

def test_matrix_multiplication_invalid(sample_matrix_2x2):
    m1 = sample_matrix_2x2
    m2 = Matrix([[1, 2], [3, 4], [5, 6]])
    with pytest.raises(ValueError):
        m1 @ m2

def test_to_file(tmp_path, sample_matrix_2x2):
    file_path = tmp_path / "test_matrix.txt"
    sample_matrix_2x2.to_file(file_path)
    with open(file_path) as f:
        content = f.read()
    assert content == "1 2\n3 4\n"
