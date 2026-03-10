import random

def get_number_from_user(text, min_value=None, max_value=None, default=None):
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
            if default is not None:
                return default
            print("Invalid input. Please enter a valid number.")
            
def get_string_from_user(text, allow_empty=False):
    while True:
        string = input(text)
        if string.strip() == "":
            if allow_empty:
                return string
            print("Input cannot be empty. Please enter a valid string.")
            continue
        return string
    
def get_choice_from_user(text, choices, default=None):
    while True:
        choice = input(text).strip().lower()
        if choice in choices:
            return choice
        elif default is not None and choice == "":
            return default
        print(f"Invalid choice. Please choose from: {', '.join(choices)}.")

def num_array(diapason):
    num_array=[]
    for _ in range(diapason):
        random_num = random.randint(1, 6)
        num_array.append(random_num)
    return num_array