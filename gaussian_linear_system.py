

def find_determinant(matrix: list[list[float]]) -> float:
    """Определитель матрицы"""
    n = len(matrix)

    triangle_matrix, swap_count = find_triangle_matrix(matrix)

    det = 1.0
    for i in range(n):
        det *= triangle_matrix[i][i]

    if swap_count % 2 != 0:
        det = -det

    return det


def find_triangle_matrix(matrix: list[list[float]]) -> tuple[list[list[float]], int]:
    """
    Приведение квадратной матрицы к треугольному виду.
    """
    matrix = [row[:] for row in matrix]  # Копируем матрицу
    n = len(matrix)
    swap_count = 0

    for i in range(n):

        pivot_row = None
        for j in range(i, n):
            if abs(matrix[j][i]) > 1e-12:
                pivot_row = j
                break

        if pivot_row is None:
            return matrix, swap_count

        if pivot_row != i:
            matrix[pivot_row], matrix[i] = matrix[i], matrix[pivot_row]
            swap_count += 1

        for j in range(i + 1, n):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(i, n):
                matrix[j][k] -= factor * matrix[i][k]

    return matrix, swap_count
        

def find_variable_vector(matrix: list[list[float]]) -> list[float]:
    """Нахождение вектора решений"""
    n = len(matrix)

    matrix = [row[:] for row in matrix] # Копируем матрицу 
    matrix, _ = find_triangle_matrix(matrix)
    ans = []
    for i in range(n - 1, -1, -1):
        matrix[i][n] /= matrix[i][i]
        for j in range(i - 1, -1, -1):
            matrix[j][n] -= matrix[j][i] * matrix[i][n]
        ans.append(matrix[i][n])
    return ans[::-1]

def find_vector_of_residuals(matrix: list[list[float]]) -> list[float]:
    """Нахождение вектора невязок"""
    n = len(matrix)
    matrix = [row[:] for row in matrix] # Копируем матрицу 
    variables = find_variable_vector(matrix)
    residuals = [0] * n
    for i in range(n):
        for j in range(n):
               residuals[i] += matrix[i][j] * variables[j]
        residuals[i] -= matrix[i][n]
    return residuals

import numpy as np

def np_find_determinant(matrix: list[list[float]]) -> float:
    A = np.array(matrix, dtype=float)
    A = A[:, : -1]
    return float(np.linalg.det(A))

def np_find_triangle_matrix(matrix: list[list[float]]) -> list[list[float]]:
    A = np.array(matrix, dtype=float)
    
    Q, R = np.linalg.qr(A)
    
    return R.tolist()

def np_find_variable_vector(matrix: list[list[float]]) -> list[float]:
    A = np.array([row[:-1] for row in matrix], dtype=float)
    b = np.array([row[-1] for row in matrix], dtype=float)

    x = np.linalg.solve(A, b)
    return x.tolist()

def np_find_vector_of_residuals(matrix: list[list[float]]) -> list[float]:
    A = np.array([row[:-1] for row in matrix], dtype=float)
    b = np.array([row[-1] for row in matrix], dtype=float)

    x = np.linalg.solve(A, b)

    residuals = A @ x - b
    return residuals.tolist()