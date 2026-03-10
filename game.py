import utils
from state import game_state
class game:
    def __init__(self, diapason, player_starts=True):
        self.__state = game_state()
        
        self.__state.is_player_move = player_starts
        self.__state.set_num_array(utils.num_array(diapason))
        print(self.__state.get_num_array())

    def start_game(self):
        self.turn()
        return 
    
    def turn(self):
        
        return
    