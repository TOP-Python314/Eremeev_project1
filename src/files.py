"""
Вспомогательный модуль — чтение/запись файлов данных.
"""

import data



def read_players() -> data.Players:
    """Читает из файла данные об игроках и их статистике и возвращает словарь игроков с требуемой структурой данных."""
    with open(data.players_path, 'r') as file:
        player_data = file.readlines()
    players_db = {}
    for player_entry in player_data:
        player_info = player_entry.strip().split(':')
        if len(player_info) == 3:
            name, wins, losses = player_info
            players_db[name] = {'побед': int(win), 'поражений': int(lose), 'ничьих': 0}
    return players_db    
    
    


def read_saves() -> data.Saves:
    """Читает из файла данные о сохранённых партиях и возвращает словарь сохранений с требуемой структурой данных."""
    saves_data = data.saves_path.read_text(encoding='utf-8').split('\n')  # Split by newline character
    for save in saves_data:
        save_elements = save.split('!')
        if len(save_elements) == 3:
            players, turns, dim = save_elements
            players = players.split(',')
            data.saves_db[frozenset((players))] = {
                'X': players,
                'turns': [int(t) for t in turns.split(',') if t],
                'dim': int(dim)
            }
    return data.saves_db
    
def write_players() -> None:
    """Записывает в файл данные об игроках и их статистике."""
    with open(data.players_path, 'w', encoding='utf-8') as fileout:
        fileout.write(str(data.players_path))
    

def write_saves() -> None:
    """Записывает в файл данные о сохранённых партиях."""
    saves_str = []
    for players, save in data.saves_db.items():
        players = ','.join((
            str(save['X']),
            str([p for p in players if p != save['X']][0])
        ))
        turns = ','.join(map(str, save['turns']))
        saves_str.append(f'{players}!{turns}!{save["dim"]}')
    saves = '\n'.join(saves_str)
    with open(str(data.saves_path), 'w', encoding='utf-8') as file:
        file.write(saves)