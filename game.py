import aiLogic
import utils
import moves
from state import game_state

ALGO_MINIMAX   = "minimax"
ALGO_ALPHABETA = "alphabeta"

class game:
    def __init__(self, diapason, player_starts=True, algorithm=ALGO_MINIMAX):
        self.__state = game_state()
        self.__state.is_player_move = player_starts
        self.__state.set_num_array(utils.num_array(diapason))
        self.__algorithm = algorithm

    def get_algorithm(self):
        return self.__algorithm

    def start_game(self):
        self.turn()

    def turn(self):
        print("\n" + "="*20)

        if moves.is_terminal(self.__state):
            self.end_game()
            return

        print(f"{'Player' if self.__state.is_player_move else 'Computer'}'s turn.")
        print(f'Current scores - Player: {self.__state.first_player_score}, '
              f'Computer: {self.__state.second_player_score}')
        print("Current array: ")
        self.print_state()

        if self.__state.is_player_move:
            max_pair_number = (len(self.__state.get_num_array()) // 2 +
                               (1 if len(self.__state.get_num_array()) % 2 != 0 else 0))
            pair_number = utils.get_number_from_user(
                f"Enter the number of the pair to remove (1 - {max_pair_number}): ",
                min_value=1, max_value=max_pair_number)

            num_array = self.__state.get_num_array()
            if len(num_array) % 2 != 0 and pair_number == max_pair_number:
                move = (moves.REMOVE_LAST, None)
            else:
                move = (moves.SUM_PAIR, pair_number)

            self.__state = moves.apply_move(self.__state, move)

        else:
            # ── choose algorithm ───────────────────────────────────────────
            if self.__algorithm == ALGO_ALPHABETA:
                best_move = aiLogic.get_best_move_alphabeta(self.__state, depth=3)
            else:
                best_move = aiLogic.get_best_move(self.__state, depth=3)

            if best_move is None:
                print("Computer has no legal moves.")
                self.end_game()
                return

            self.__state = moves.apply_move(self.__state, best_move)
            algo_label = "Alpha-Beta" if self.__algorithm == ALGO_ALPHABETA else "Minimax"
            print(f"Computer chose ({algo_label}): {best_move}")

        self.turn()

    def print_state(self):
        num_array = self.__state.get_num_array()
        pairs = []
        for i in range(0, len(num_array), 2):
            if i + 1 < len(num_array):
                pairs.append(f"{i//2 + 1}: |{num_array[i]}, {num_array[i+1]}|")
            else:
                pairs.append(f"{i//2 + 1}: |{num_array[i]}")
        print(" ".join(pairs))

    def end_game(self):
        print("Game ended!")
        print(f'Final scores - Player: {self.__state.first_player_score}, '
              f'Computer: {self.__state.second_player_score}')
        print(f"Final array: {self.__state.get_num_array()}")
        print()
        if self.__state.first_player_score > self.__state.second_player_score:
            print("Player wins!")
        elif self.__state.first_player_score < self.__state.second_player_score:
            print("Computer wins!")
        else:
            print("It's a tie!")
