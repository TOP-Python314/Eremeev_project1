"""
Раздел помощи.
"""

import data


def print_full_help() -> None:
    """Отправляет в stdout полную справку."""
    print(
        render_game_info(),
        render_interface_help(),
        render_commands(),
        sep='\n\n'
    )


def render_game_info() -> str:
    """Возвращает строку с информацией об игре."""
    return data.RULES


def render_interface_help() -> str:
    """Возвращает строку с описанием интерфейса командной строки."""
    return data.INTERFACE
       

def render_commands() -> str:
    """Возвращает строку со списком команд и вариантов ввода."""
    return data.COMMANDS