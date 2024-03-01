"""
Игровой процесс
"""
from itertools import islice 
from shutil import get_terminal_size
import data
import players
import utils
import help
import bot
import files

def set_mode() -> None:
    """Управляет ветвлением запросов к игроку при настройке игрового процесса в начале новой партии."""
    input_mode = input(data.MESSAGES['ввод режима'])
    if input_mode == '1':
        input_level = input(data.MESSAGES['ввод уровня'])
        if input_level == '1':
            data.active_players_names += ['%1']
        elif input_level == '2':
            data.active_players_names += ['%2']
    elif input_mode == '2':
        players.get_player_name()
    input_tokens = input(data.MESSAGES['ввод токена'])
    if input_tokens == '2':
        data.active_players_names.reverse() 

def load() -> bool:
    """Управляет загрузкой партии. Выводит два последних хода сохранённой партии."""
    save = players.player_load()
    if save is None:
        print(data.MESSAGES['нет сохранений'])
        return False
    p, save = save
    data.active_player_names = list(p)
    utils.change_dimension(save['dim'])
    
    draw = len(save['turns']) % 2
    try:    
        turn_last = save['turns'].popitem()
    except:
        print_board()
        return True
    data.turns = save['turns']
    print_board(draw)
    save['turns'] |= (last_turn,)
    data.turns = save['turns']
    return True


def game() -> data.GameStats:
    """Управляет игровым процессом партии."""
    data.field = utils.generate_field_template()
    data.wins = utils.generate_win_combinations(3)   
    for p in range(len(data.turns), data.all_cells):
        pointer = p % 2
        
        if data.active_players_names[pointer] == '%1':
            turn = bot.easy_mode(pointer)       
        elif data.active_players_names[pointer] == '%2':
            turn = bot.hard_mode(pointer) 
        else:    
            turn = players.get_human_turn()
        
        if turn is None:
            save()
            data.active_players_names = [data.authorized]
            data.turns = {}
            return None
        data.turns |= {turn: data.TOKENS[pointer]}
        print_board()
        if is_won(pointer):
            winner = print(data.MESSAGES['победитель'].format(data.active_players_names[pointer]))
            break
        

    

def save() -> None:
    """Добавляет данные текущей партии в словарь сохранений и обновляет файлы данных."""
    data.saves_db |= {
        frozenset((data.active_players_names)): {
            'X': data.active_players_names[0],
            'dim': data.dim,
            'turns': data.turns
        }
    }
    files.write_saves()


def print_board() -> None:
    """
    Отправляет в stdout игровое поле с токенами сделанных ходов.        
    """
      
    board = data.field.format(*(data.empty | data.turns).values())
    return print(board)
    

def is_won(pointer: data.Pointer) -> bool:
    """Проверяет наличие победной комбинации для текущего игрока.
    
    :param pointer: индекс-указатель на текущий токен
    """
    players_turns = set(islice(data.turns, pointer, None, 2))
    for win_comb in data.wins:
        if win_comb <= players_turns:
            return True
        