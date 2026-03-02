import random

diapason = int(input("Enter length from 15 to 25: "))
first_player_score = 0
second_player_score = 0

if diapason < 15 or diapason > 25:
    print("Invalid input. Please enter a number between 15 and 25.")

def num_array(diapason):
    num_array=[];
    for i in range(diapason):
        random_num = random.randint(1, 6)
        num_array.append(random_num)
    return num_array

# ? For testing
print(num_array(diapason))

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

