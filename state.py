class game_state:
    def __init__(self):
        self.first_player_score = 0
        self.second_player_score = 0
        self.num_array = []
        self.is_player_move = True
        
    def set_num_array(self, num_array):
        self.num_array = num_array