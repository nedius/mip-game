from copy import deepcopy

SUM_PAIR = "sum_pair"
REMOVE_LAST = "remove_last"

def is_terminal(state):
    return len(state.get_num_array()) <= 1

def get_legal_moves(state):
    num_array = state.get_num_array()
    moves = []
    
    full_pairs = len(num_array) // 2 
    for pair_number in range(1, full_pairs + 1):
        moves.append((SUM_PAIR, pair_number))
        
    if len(num_array) % 2 != 0:
        moves.append((REMOVE_LAST, None))
        
def is_allowed_move(state, move):
    if is_terminal(state):
        return False
    
    if not isinstance(move, tuple) or len(move) != 2:
        return False
    
    move_type, value = move
    num_array = state.get_num_array()
    full_pairs = len(num_array) // 2
    
    if move_type == SUM_PAIR:
        return isinstance(value, int) and 1 <= value <= full_pairs
    
    if move_type == REMOVE_LAST:
        return value is None and len(num_array) % 2 != 0
    
    return False

def apply_move(state, move):
    if not is_allowed_move(state, move):
        raise ValueError(f"Ileegal move : {move}")
    
    new_state = deepcopy(state)
    move_type, value = move
    
    if move_type == SUM_PAIR:
        new_state.sum_pair(value)
        
        if state.is_player_move:
            new_state.first_player_score += 1
        else:
            new_state.second_player_score +=1
            
    elif move_type == REMOVE_LAST:
        new_state.remove_last(value)
        
        if state.is_player_move:
            new_state.second_player_score -=1
        else:
            new_state.first_player_score -= 1
            
    new_state.is_player_move = not state.is_player_move
    return new_state

def generate_next_states(state):
    return [apply_move(state, move) for move in get_legal_moves(state)]

def generate_next_state_with_moves(state):
    return [(move, apply_move(state, move)) for move in get_legal_moves(state)]