""" 
Точка входа. Управляющий код верхнего уровня
"""
import data
import files
import help
import players
import utils
import game

data.saves_db = files.read_saves()
help.print_full_help()
data.authorized = players.get_player_name()
data.players_db = files.read_players()
utils.change_dimension()

    
while True:        
    command = input(data.MESSAGES['ввод команды']) 
        
    if command in data.COMMANDS['начать новую партию']:
        game.set_mode()
        game_result = game.game()
        if game_result is not None:
            players.update_stats(game_result)
        utils.clear()
        
    elif command in data.COMMANDS['загрузить существующую партию']:
        if game.load():
            game_result = game.game()
            if game_result is not None:
                players.update_stats(game_result)
                utils.clear()
            else:
                utils.clear()
            
    elif command in data.COMMANDS['изменить размер поля']:
        utils.change_dimension(get_new_dimension()) 
        
    elif command in data.COMMANDS['выйти']:
        break                    
       
    else:
         data.MESSAGES['некорректная команда']

files.write_players()
files.write_saves()
utils.clear()
