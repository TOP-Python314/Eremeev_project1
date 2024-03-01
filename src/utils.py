"""
Вспомогательные модули
"""
from configparser import ConfigParser
from shutil import get_terminal_size
from typing import Literal
import bot
import data



def change_dimension(new_dimension: int = 3) -> None:
    """Переопределяет все глобальные переменные, связанные с размером игрового поля."""
    data.dim = new_dimension
    data.all_cells = new_dimension**2
    data.dim_range = range(new_dimension)
    data.all_cells_range = range(data.all_cells)
    data.empty = dict.fromkeys(data.all_cells_range, ' ')
    data.field = generate_field_template(new_dimension)
    data.wins = generate_win_combinations(new_dimension)
    data.start_matrices = (
        bot.calc_sm_cross(),
        bot.calc_sm_zero()
    )
    data.MESSAGES['ход не в диапазоне'].format(data.all_cells-1)


def get_new_dimension() -> int:
    """Получает от пользователя новый размер игрового поля."""
    while True:
        dim = input(data.MESSAGES['ввод размерности'])
        if data.DIM_PATTERN.fullmatch(dim):
            return int(dim)
        print(data.MESSAGES['некорректная размерность'])


def generate_field_template(dimension: int = None) -> str:
    """Возвращает строковый шаблон игрового поля требуемого размера."""
    if dimension is None:
        field_w = data.dim * (3 + max(len(t) for t in data.TOKENS)) - 1
    else:        
        field_w = data.dim * (3 + dimension) - 1
    line_w, line_h = '|', '—'
    
    line_w = line_w.join([' {} ']* data.dim)
    line_h = f'\n{line_h*field_w}\n'
    return line_h.join([line_w] * data.dim)
        

def generate_win_combinations(dimension: int) -> data.WinCombinations:
    """Возвращает список победных комбинаций номеров клеток игрового поля требуемого размера."""
    wins = [
        set(data.all_cells_range[::data.dim+1]),
        set(data.all_cells_range[data.dim-1:data.all_cells-data.dim+1:data.dim-1]),
    ]
    wins += [
        set(data.all_cells_range[i:i+data.dim])
        for i in range(0, data.all_cells, data.dim)
    ]
    wins += [
        set(data.all_cells_range[i::data.dim])
        for i in data.dim_range
    ]
    return wins


def clear(delete_save: bool = False) -> None:
    """Перезаписывает начальными значениями глобальные переменные, связанные с игровым процессом."""
    if delete_save:
        data.saves_db.pop(frozenset((data.active_players_names)),None)
    data.players = [data.authorized]    
    data.turns = {} 
    



def columnize(text: str, column_width: int) -> list[str]:
    """Разбивает переданную строку на отдельные слова и формирует из слов строки, длины которых не превышают заданное значение (текст-колонка). Возвращает список строк, к которым впоследствии может быть применено любое выравнивание.
    
    :param text: текст для обработки
    :param column_width: ширина колонки в символах
    """
    multiline, line_len, i = [[]], 0, 0
    for word in text.split():
        word_len = len(word)
        if line_len + word_len + len(multiline[i]) <= column_width:
            multiline[i] += [word]
            line_len += word_len
        else:
            multiline += [[word]]
            line_len = word_len
            i += 1
    return [' '.join(line) for line in multiline]


def concatenate_rows(
        multiline1: str,
        multiline2: str,
        *multilines: str,
        padding: int = 8
) -> str:
    """Объединяет произвольное количество строк текстов-колонок в одну строку с несколькими колонками и отступом между ними.

    :param padding: ширина отступа между колонками в пробелах
    """
    multilines = multiline1, multiline2, *multilines
    multilines = [m.split('\n') for m in multilines]
    padding = ' '*padding
    return '\n'.join(
        padding.join(row)
        for row in zip(*multilines)
    )

