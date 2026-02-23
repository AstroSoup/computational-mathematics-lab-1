from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt
import command_helper

from pathlib import Path

import sys

import gaussian_linear_system

app = command_helper.App()

def parse_matrix(args: list[str]):
    if ("--from-file" in args and args.index("--from-file") + 1 < len(args)):
        path_to_file = Path(args[args.index("--from-file") + 1])
        if (path_to_file.is_file()):
            input = path_to_file.read_text()

        else:
            print("файл не найден.")
            return
    else: 
        print("Введите матрицу построчно, каждый новый элемент должен быть отделен от предыдущего пробелом. Для выхода из режима ввода нажмите esc, а затем enter.\nПример ввода:\n1 2 3\n4 5 6\n7 8 9\n")
        input = prompt("", multiline=True)
    
    if not input.strip():
        print("Матрица не была введена. Пожалуйста, попробуйте еще раз указав матрицу.")
        return

    matrix = []
    for line in input.splitlines():
        matrix.append([])
        for char in line.split():
            try:
                matrix[-1].append(float(char))
            except ValueError:
                print(f"В матрице найден недопустимый элемент {char} матрица должна состоять только из чисел.")
                return
    return matrix


@app.command()
def determinant(args: list[str]):
    """
    Команда для подсчета определителя матрицы определенной СЛАУ. По умолчанию значения считываются с консоли.
    использование: determinant [--from-file <filepath> --numpy]
    --from-file <filepath> - считать данные из файла расположенного по пути <filepath>.
    --numpy - использовать numpy для решения.
    """
    matrix = parse_matrix(args)
    if (matrix):
        if any(len(row) != len(matrix) + 1 for row in matrix):
            print("СЛАУ должна быть определенной.")
        else:
            if ("--numpy" in args):
                print(gaussian_linear_system.np_find_determinant(matrix))
            else:
                print(gaussian_linear_system.find_determinant(matrix))        

@app.command()
def triangle_matrix(args: list[str]):
    """
    Команда для приведения матрицы определенной СЛАУ к треугольному виду. По умолчанию значения считываются с консоли.
    использование: triangle_matrix [--from-file <filepath> --numpy]
    --from-file <filepath> - считать данные из файла расположенного по пути <filepath>.
    --numpy - использовать numpy для решения.
    """
    matrix = parse_matrix(args)
    if (matrix):
        if any(len(row) != len(matrix) + 1 for row in matrix):
            print("СЛАУ должна быть определенной.")
        else:
            if ("--numpy" in args):
                matrix = gaussian_linear_system.np_find_triangle_matrix(matrix)
            else:
                matrix = gaussian_linear_system.find_triangle_matrix(matrix)
            for row in matrix:
                for elem in row:
                    print(elem, end=" ")
                print("\n")

@app.command()
def variable_vector(args: list[str]):
    """
    Команда для решения определенной СЛАУ. По умолчанию значения считываются с консоли.
    использование: variable_vector [--from-file <filepath> --numpy]
    --from-file <filepath> - считать данные из файла расположенного по пути <filepath>.
    --numpy - использовать numpy для решения.
    """
    matrix = parse_matrix(args)
    if (matrix):
        if any(len(row) != len(matrix) + 1 for row in matrix):
            print("СЛАУ должна быть определенной.")
        else:
            if ("--numpy" in args):
                vector = gaussian_linear_system.np_find_variable_vector(matrix)
            else:
                vector = gaussian_linear_system.find_variable_vector(matrix)
            for i in range(len(vector)):
                print(f"x[{i + 1}] = {vector[i]}")


@app.command()
def residual_vector(args: list[str]):
    """
    Команда для подсчета вектора невязок определенной СЛАУ. По умолчанию значения считываются с консоли.
    использование: variable_vector [--from-file <filepath> --numpy]
    --from-file <filepath> - считать данные из файла расположенного по пути <filepath>.
    --numpy - использовать numpy для решения.
    """
    matrix = parse_matrix(args)
    if (matrix):
        if any(len(row) != len(matrix) + 1 for row in matrix):
            print("СЛАУ должна быть определенной.")
        else:
            if ("--numpy" in args):
                vector = gaussian_linear_system.np_find_vector_of_residuals(matrix)
            else:
                vector = gaussian_linear_system.find_vector_of_residuals(matrix)
            for i in range(len(vector)):
                print(f"r[{i + 1}] = {vector[i]}")

@app.command()
def all_info(args: list[str]):
    """
    Вызывает все команды по работе с матрицей и выводит их.
    использование: all_info [--from-file <filepath>]
    --from-file <filepath> - считать данные из файла расположенного по пути <filepath>.
    --numpy - использовать numpy для решения.
    """
    matrix = parse_matrix(args)
    if (matrix):
        if any(len(row) != len(matrix) + 1 for row in matrix):
            print("СЛАУ должна быть определенной.")
        else:
            if ("--numpy" in args):
                print("Определитель:")
                print(gaussian_linear_system.np_find_determinant(matrix))
                
                print("Преобразованнная матрица:")
                tmatrix = gaussian_linear_system.np_find_triangle_matrix(matrix)
                for row in tmatrix:
                    for elem in row:
                        print(elem, end=" ")
                    print("\n")

                print("Решение методом Гаусса:")
                vector = gaussian_linear_system.np_find_variable_vector(matrix)
                for i in range(len(vector)):
                    print(f"x[{i + 1}] = {vector[i]}")
                print("Вектор невязки:")
                vector = gaussian_linear_system.np_find_vector_of_residuals(matrix)
                for i in range(len(vector)):
                    print(f"r[{i + 1}] = {vector[i]}")
            else:
                print("Определитель:")
                print(gaussian_linear_system.find_determinant(matrix))
                
                print("Преобразованнная матрица:")
                tmatrix = gaussian_linear_system.find_triangle_matrix(matrix)
                for row in tmatrix:
                    for elem in row:
                        print(elem, end=" ")
                    print("\n")

                print("Решение методом Гаусса:")
                vector = gaussian_linear_system.find_variable_vector(matrix)
                for i in range(len(vector)):
                    print(f"x[{i + 1}] = {vector[i]}")
                print("Вектор невязки:")
                vector = gaussian_linear_system.find_vector_of_residuals(matrix)
                for i in range(len(vector)):
                    print(f"r[{i + 1}] = {vector[i]}")


@app.command()
def exit(args: list[str]):
    """
    Завершить программу.
    использование: exit
    """
    sys.exit()

completer = WordCompleter(app.commands.keys(), sentence=True)

def main():
    session = PromptSession(completer=completer)
    while True:
        try:
            text = session.prompt('> ')
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            text = text.split()
            if (text[0] in app.commands.keys()):
                app.commands[text[0]](text[1:])
            else:
                print("Вы ввели недействительную команду. Возможные команды: \n")
                app.commands["help"]()


if __name__ == '__main__':
    main()