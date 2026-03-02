import utils
from state import game_state
class game:
    def __init__(self, diapason):
        self.__state = game_state()
        
        self.__state.set_num_array(utils.num_array(diapason))

    def start(self, player_starts=True):
        return