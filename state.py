class game_state:
    def __init__(self):
        self.first_player_score = 0
        self.second_player_score = 0
        self.num_array = []
        self.is_player_move = True
        
    def set_num_array(self, num_array):
        self.num_array = num_array
        
    def get_num_array(self):
        return self.num_array
    
    def sum_pair(self, index):
        if index < 1 or index >= len(self.num_array):
            raise IndexError("Index out of bounds for summing pair.")
        pair_sum = self.num_array[index - 1] + self.num_array[index]
        if pair_sum > 6:
            pair_sum = pair_sum - 6
        del self.num_array[index - 1:index + 1]
        self.num_array.insert(index - 1, pair_sum)
        return pair_sum
    
    def remove_last(self):
        if not self.num_array:
            raise IndexError("No elements to remove.")
        return self.num_array.pop()