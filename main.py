import utils
from game import game

array_length = utils.get_number_from_user("Enter array length from 15 to 25 (default 15): ", min_value=15, max_value=25, default=15)
is_player_starts = utils.get_choice_from_user("Does the player start first? (Y/n): ", choices=['y', 'n'], default='y') == 'y'

g = game(array_length, player_starts=is_player_starts)

g.start_game()