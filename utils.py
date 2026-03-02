import random

def get_number_from_user(text, min_value=None, max_value=None):
    while True:
        try:
            number = int(input(text))
            if min_value is not None and number < min_value:
                print(f"Number must be at least {min_value}.")
                continue
            if max_value is not None and number > max_value:
                print(f"Number must be at most {max_value}.")
                continue
            return number
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            
def num_array(diapason):
    num_array=[]
    for _ in range(diapason):
        random_num = random.randint(1, 6)
        num_array.append(random_num)
    return num_array