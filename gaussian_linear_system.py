

def find_determinant(matrix: list[list[float]]) -> float:
    """Определитель матрицы"""
    n = len(matrix)
    matrix = find_triangle_matrix(matrix)
    ac = 1
    for i in range(n):
        ac *= matrix[i][i]
    return ac

def find_triangle_matrix(matrix: list[list[float]]) -> list[list[float]]:
    """Приведение квадратной матрицы или СЛАУ того же ранга к треугольному виду"""
    matrix = [row[:] for row in matrix] # Копируем матрицу 
    n = len(matrix)

    for i in range(n):
        
        pivot_row = None
        for j in range(i, n): # проходимся по строке и ищем по какому из элементов можно приводить матрицу
            if (abs(matrix[j][i]) > 1e-12):
                pivot_row = j
                break
        
        if (pivot_row != None):
            if (pivot_row != i): # если строка стоит не на своем месте меняем местами
                matrix[pivot_row], matrix[i] = matrix[i], matrix[pivot_row]

            for j in range(i + 1, n): # проходимся по всем строкам ниже и вычитаем из каждой строку по которой приводим
                factor = matrix[j][i] / matrix[i][i] # множитель для конкретной строки
                for k in range(i, len(matrix[j])):
                    matrix[j][k] -= factor * matrix[i][k]
        else:
            raise ValueError("Матрицу невозможно привести к треугольному виду.")
            
    return matrix
        

def find_variable_vector(matrix: list[list[float]]) -> list[float]:
    """Нахождение вектора решений"""
    n = len(matrix)

    matrix = [row[:] for row in matrix] # Копируем матрицу 
    matrix = find_triangle_matrix(matrix)
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