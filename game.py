import utils
import moves
from state import game_state


class game:
    def __init__(self, diapason, player_starts=True):
        self.__state = game_state()
        
        self.__state.is_player_move = player_starts
        self.__state.set_num_array(utils.num_array(diapason))

    def start_game(self):
        self.turn()
        return 
    
    def turn(self):
        print("\n" + "="*20)
        
        if moves.is_terminal(self.__state):
            self.end_game()
            return
        
        print(f"{'Player' if self.__state.is_player_move else 'Computer'}'s turn.")
        print(f'Current scores - Player: {self.__state.first_player_score}, Computer: {self.__state.second_player_score}')
        print("Current array: ")
        self.print_state()
        
        if self.__state.is_player_move:
            max_pair_number = len(self.__state.get_num_array()) // 2 + (1 if len(self.__state.get_num_array()) % 2 != 0 else 0)
            pair_number = utils.get_number_from_user(f"Enter the number of the pair to remove (1 - {max_pair_number}): ", min_value=1, max_value=max_pair_number)
            
            num_array = self.__state.get_num_array()
            
            if len(num_array) % 2 != 0 and pair_number == max_pair_number:
                move = (moves.MoveType.REMOVE_LAST, None)
            else:
                move = (moves.MoveType.SUM_PAIR, pair_number)
            
            if moves.is_allowed_move(self.__state, move):
                self.__state = moves.apply_move(self.__state, move)

        else:
            # TODO: implement computer's ai logic here
            
            # Computer's move logic here
            # For simplicity, let's just remove the last element of the array for the computer's move if possible
            # else sum first pair
            if len(self.__state.get_num_array()) % 2 != 0:
                # if the last pair has only one number, remove it and decrease player score by 1
                self.__state.remove_last()
                self.__state.first_player_score -= 1
                print("Computer removed the last number and decreased player's score by 1.")
            else:
                # sum the first pair and increase computer score by 1
                self.__state.sum_pair(1)
                self.__state.second_player_score += 1
                print(f"Computer summed the {1} pair and increased its score by 1.")
                
        self.__state.is_player_move = not self.__state.is_player_move
        self.turn()
        return
    
    def print_state(self):
        # print current array state in format: pair index: |num1, num2|, ... 
        # if last par has only one number, print it as: pair index: |num1
        num_array = self.__state.get_num_array()
        pairs = []
        for i in range(0, len(num_array), 2):
            if i + 1 < len(num_array):
                pairs.append(f"{i//2 + 1}: |{num_array[i]}, {num_array[i+1]}|")
            else:
                pairs.append(f"{i//2 + 1}: |{num_array[i]}")
        print(" ".join(pairs))
        return
    
    def end_game(self):
        print("Game ended!")
        print(f'Final scores - Player: {self.__state.first_player_score}, Computer: {self.__state.second_player_score}')
        print(f"Final array: {self.__state.get_num_array()}")
        print()
        
        if self.__state.first_player_score > self.__state.second_player_score:
            print("Player wins!")
        elif self.__state.first_player_score < self.__state.second_player_score:
            print("Computer wins!")
        else:
            print("It's a tie!")
        return
    