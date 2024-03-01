"""
Взаимодействие с игроками
"""
import data
import files

def input_name() -> str:
    while True:
        name = input(data.MESSAGES['ввод имени'])        
        if data.NAME_PATTERN.fullmatch(name):
            return name
        else:
            print(data.MESSAGES['некорректное имя'])

        
def get_player_name(flag = True) -> str:
    """Запрашивает имя игрока до соответствия с шаблоном. Добавляет в словарь игроков имя и начальную статистику, если имя является новым.""" 
    name = input_name()
    if name not in data.players_db:
        data.players_db[name] = {'побед': 0, 'поражений': 0, 'ничьих': 0}
        files.write_players() 
    if flag:
        data.authorized = name
        data.active_players_names += [name]
    else:
        data.active_players_names += [name]
        


def update_stats(result: data.GameStats) -> None:
    """Обновляет статистику активных игроков по результатам партии."""
    if result:
        win,lose = result
        data.players_db[win]['побед'] += 1
        data.player_db[lose]['поражений'] += 1
    else:
        for name in data.active_players_names:
            data.players_db[name]['ничьих'] += 1
    files.write_players()

def get_human_turn() -> data.SquareIndex | None:
    """Запрашивает пользовательский ввод для хода во время партии до получения корректного ввода."""
    while True:
        turn = input(data.MESSAGES['ввод хода'])
        if not turn:
            return None
        try:        
            turn = int(turn)    
        except ValueError:
            print(data.MESSAGES['ход не число'])        
        else:
            if 0 <= turn <= data.all_cells:
                if turn not in data.turns:
                    return turn
                else:
                    print({data.MESSAGES['ход в занятую']})
            else:
                print(data.MESSAGES['ход не в диапазоне'])

                
def player_load():
    slots = []
    for i, players in enumerate(data.saves_db, 1):
        if data.authorized in players:
            players = ', '.join(
                f'{t}: {p}'
                for t, p in zip(data.TOKENS, players)
            )
            slots += [f'    {i} - {players}']
    if not slots:
        return None
    print(data.MESSAGES['ввод сохранения'].format('\n'.join(slots)))
    while True:
        choice = input()
        try:
            choice = int(choice)
            return frozenset(data.saves_db.items())[choice-1]
        except (ValueError, IndexError):
            print(data.MESSAGES['некорректное сохранение'].format(i))


  
    
   
    

        