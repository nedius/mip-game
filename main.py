import utils
from game import game

diapason = utils.get_number_from_user("Enter array length from 15 to 25: ", min_value=15, max_value=25)

# # ? For testing
# print(utils.num_array(diapason))

g = game(diapason)

# for i in range(diapason):
#     if i % 2 == 0:
#         first_player_score += action_sum(num_array(diapason))
#     else:
#         second_player_score += action_sum(num_array(diapason))

# for (int i = diapason; i >=1; i--):


# def action_sum(num_array):
#     sum = 0
#     for i in num_array:
#         sum += i
#     return sum

