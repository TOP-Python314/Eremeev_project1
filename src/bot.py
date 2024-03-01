"""
Функционал бота
"""
from random import choice
import data


def easy_mode(pointer=None) -> data.SquareIndex:
    """Возвращает номер случайной свободной клетки игрового поля."""
    return choice(list(set(data.empty) - set(data.turns)))


def hard_mode(pointer: int) -> data.SquareIndex:
    """Вычисляет наиболее выигрышный ход и возвращает номер соответствующей клетки игрового поля."""
    tw = weights_tokens(pointer)
    ew = weights_empty(tw)
    if len(data.turns) < 2*data.dim:
        ew = matrices_sum(ew, data.start_matrices[pointer])
        weights_clear(tw, ew)
    ew = vectorization(ew)
    if any(ew):
        return index_of_rand_max(ew) + 1
    else:
        return easy_mode()


def weights_tokens(pointer: int) -> data.Matrix:
    """Конструирует и возвращает матрицу весов занятых ячеек игрового поля."""
    board = tuple((data.empty | data.turns).values())
    board = matricization(board)
    tokensweights = [[0]*data.dim for _ in data.dim_range]
    for i in data.dim_range:
        for j in data.dim_range:
            if board[i][j] == data.TOKENS[pointer]:
                tokensweights[i][j] = data.WEIGHT_OWN
            elif board[i][j] == data.TOKENS[pointer-1]:
                tokensweights[i][j] = data.WEIGHT_FOE
    return tokensweights


def weights_empty(tokensweights: data.Matrix) -> data.Matrix:
    """Вычисляет и возвращает матрицу весов свободных ячеек игрового поля."""
    emptyweights = [[0]*data.dim for _ in data.dim_range]
    for i in data.dim_range:
        for j in data.dim_range:
            if not tokensweights[i][j]:
                for seq in [
                        get_row(tokensweights, i),
                        get_column(tokensweights, j),
                        get_maindiag(tokensweights, i, j),
                        get_antidiag(tokensweights, i, j)
                ]:
                    if not data.WEIGHTS <= set(seq):
                        emptyweights[i][j] += sum(seq)**2
                emptyweights[i][j] = int(emptyweights[i][j])
    return emptyweights


def weights_clear(
        tokensweights: data.Matrix,
        solvingweights: data.Matrix
) -> None:
    """Обрабатывает матрицу принятия решения, приравнивая к нолю элементы, соответствующие занятым на поле клеткам."""
    for i in data.dim_range:
        for j in data.dim_range:
            if tokensweights[i][j]:
                solvingweights[i][j] = 0


def vectorization(matrix: data.Matrix) -> data.Series:
    """Возвращает плоскую последовательность, полученную в результате преобразования переданной матрицы."""
    return [cell for row in matrix for cell in row]


def matricization(sequence: data.Series) -> data.Matrix:
    """Возвращает квадратную матрицу, полученную в результате преобразования переданной плоской последовательности."""
    return [sequence[i*data.dim:(i+1)*data.dim] for i in data.dim_range]


def get_row(
        matrix: data.Matrix,
        row_index: int
) -> data.Series:
    """Возвращает ряд матрицы по переданному индексу."""
    return matrix[row_index]


def get_column(
        matrix: data.Matrix,
        column_index: int
) -> data.Series:
    """Возвращает столбец матрицы по переданному индексу."""
    return [row[column_index] for row in matrix]


def get_maindiag(
        matrix: data.Matrix,
        row_index: int,
        column_index: int
) -> data.Series:
    """Возвращает главную диагональ матрицы, если элемент по переданным индексам ей принадлежит."""
    if row_index == column_index:
        return [matrix[i][i] for i in data.dim_range]
    return []


def get_antidiag(
        matrix: data.Matrix,
        row_index: int,
        column_index: int
) -> data.Series:
    """Возвращает побочную диагональ матрицы, если элемент по переданным индексам ей принадлежит."""
    if row_index == data.dim - column_index - 1:
        return [matrix[i][-i-1] for i in data.dim_range]
    return []


def matrices_sum(
        matrix1: data.Matrix,
        matrix2: data.Matrix,
        *matrices: data.Matrix
) -> data.Matrix:
    """Возвращает результат математического сложения двух и более матриц."""
    matrices = matrix1, matrix2, *matrices
    result = [[0]*data.dim for _ in data.dim_range]
    for i in data.dim_range:
        for j in data.dim_range:
            result[i][j] = sum(m[i][j] for m in matrices)
    return result


def index_of_rand_max(series: data.Series) -> int:
    """Возвращает индекс случайного среди равных максимальных значений в последовательности."""
    m = max(series)
    return choice([i for i, v in enumerate(series) if v == m])


def calc_sm_cross() -> data.Matrix:
    """Вычисляет и возвращает начальную матрицу стратегии крестика."""
    sm_cross = [[0]*data.dim for _ in data.dim_range]
    half, rem = divmod(data.dim, 2)
    diag = list(range(1, half+1)) + list(range(half+rem, 0, -1))
    for i in data.dim_range:
        sm_cross[i][i] = diag[i]
        sm_cross[i][-i-1] = diag[i]
    return sm_cross


def calc_sm_zero() -> data.Matrix:
    """Вычисляет и возвращает начальную матрицу стратегии нолика."""

    def triangle_desc(n: int, start: int) -> data.Matrix:
        """Генерирует и возвращает верхне-треугольную по побочной диагонали матрицу, заполняемую параллельно побочной диагонали значениями по убыванию."""
        flat = []
        indexes = range(n)
        for i in indexes:
            flat += [m if m > 0 else 0 for m in range(start-i, -start, -1)][:n]
        matrix = [flat[i*n:(i+1)*n] for i in indexes]
        if n > 2:
            for i in indexes:
                for j in indexes:
                    if i > n-j-1:
                        matrix[i][j] = 0
        return matrix

    def rot90(matrix: data.Matrix) -> data.Matrix:
        """Возвращает "повёрнутую" на 90° матрицу."""
        indexes = range(len(matrix))
        matrix = [[matrix[j][i] for j in indexes] for i in indexes]
        for i in indexes:
            matrix[i] = matrix[i][::-1]
        return matrix

    half, rem = divmod(data.dim, 2)
    quarter = triangle_desc(half, half+rem)
    if data.dim > 6:
        for i in range(half):
            for j in range(half):
                if i == half-j-1:
                    if i != j:
                        quarter[i][j] -= 1
                if i > half-j:
                    quarter[i][i] = half - i - (rem+1)%2
    m1 = quarter
    m2 = rot90(m1)
    m3 = rot90(m2)
    m4 = rot90(m3)
    top, bot = [], []
    for i in range(half):
        top += [m1[i] + [0]*rem + m2[i]]
        bot += [m4[i] + [0]*rem + m3[i]]
    return top + [[0]*data.dim]*rem + bot