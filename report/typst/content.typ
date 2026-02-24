= Цель работы

Изучить численные методы решения систем линейных алгебраических уравнений и реализовать один из них программно.

= Описание метода
Метод Гаусса.

Основан на приведении матрицы системы к треугольному виду так, чтобы ниже ее главной диагонали находились только нулевые элементы. Состоит из 2 фаз: прямого и обратного хода.

Прямой ход метода Гаусса состоит в последовательном исключении неизвестных из
уравнений системы. Сначала с помощью первого уравнения исключается $x_1$ из всех
последующих уравнений системы. Затем с помощью второго уравнения исключается
$x_2$ из третьего и всех последующих уравнений и т.д.
Этот процесс продолжается до тех пор, пока в левой части последнего ($n$-го) уравнения
не останется лишь один член с неизвестным $x_n$, т. е. матрица системы будет
приведена к треугольному виду.

Обратный ход метода Гаусса состоит в последовательном вычислении искомых
неизвестных: решая последнее уравнение, находим неизвестное $x_n$. Далее, из
предыдущего уравнения вычисляем $x_(n-1)$ и т. д. Последним найдем $x_1$ из первого
уравнения.

#figure(
  caption: [Блок-схема метода Гаусса],
  image("assets/gauss.png"),
)

= Листинг
Далее приведен листинг функций используемых для нахождения определителя, треугольного представления матрицы коэффициентов, вектора решений и вектора невязок. Также приведены функции с использованием сторонних библиотек для нахождения всего вышеперечисленного.
```py


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
    """Приведение квадратной матрицы к треугольному виду."""
    matrix = [row[:] for row in matrix] # Копируем матрицу 
    n = len(matrix)
    swap_count = 0
    for i in range(n):
        
        pivot_row = None
        for j in range(i, n): # проходимся по строке и ищем по какому из элементов можно приводить матрицу
            if (abs(matrix[j][i]) > 1e-12):
                pivot_row = j
                break
        
        if (pivot_row != None):
            if (pivot_row != i): # если строка стоит не на своем месте меняем местами
                matrix[pivot_row], matrix[i] = matrix[i], matrix[pivot_row]
                swap_count += 1

            for j in range(i + 1, n): # проходимся по всем строкам ниже и вычитаем из каждой строку по которой приводим
                factor = matrix[j][i] / matrix[i][i] # множитель для конкретной строки
                for k in range(i, len(matrix[j])):
                    matrix[j][k] -= factor * matrix[i][k]
        else:
            raise ValueError("Матрицу невозможно привести к треугольному виду.")
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
```

= Примеры работы программы
На следующем листинге представлен пример работы программы с вводом данных из консоли и подсчетом всех параметров при помощи самописных функций:
```
> all_info
Введите матрицу построчно, каждый новый элемент должен быть отделен от предыдущего пробелом. Для выхода из режима ввода нажмите esc, а затем enter.
Пример ввода:
1 2 3
4 5 6
7 8 9

1 1
Определитель:
1.0
Преобразованнная матрица:
+-----+-----+
| 1.0 | 1.0 |
+-----+-----+
Решение методом Гаусса:
x[1] = 1.0
Вектор невязки:
r[1] = 0.0
```
На следующем листинге представлен пример работы программы с вводом данных из файла и подсчетом всех параметров при помощи библиотеки "numpy":
```
> all_info --from-file test.txt --numpy
Определитель:
1.0
Преобразованнная матрица:
+-----+-----+
| 1.0 | 1.0 |
+-----+-----+
Решение методом Гаусса:
x[1] = 1.0
Вектор невязки:
r[1] = 0.0
```

= Вывод
В результате выполнения лабораторной работы я познакомился с численными методами решения СЛАУ, и реализовал метод Гаусса на языке программирования Python. 

Сравнивая результат работы программы написанной мной и библиотеки "numpy" можно заметить, что при достаточно несбалансированных матрицах результат может отличаться. Это происходит из-за того что при вычислении необходимых параметров библиотекой "numpy" используется другой численный метод, из-за чего результат операций с числами с плавающей точкой может незначительно отличаться.