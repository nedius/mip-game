import moves
import random

def heuristic(state):
    value = sum(state.get_num_array()) * 0.05
    return (state.second_player_score - state.first_player_score) + (state.second_player_score * 0.1) + value 

def minimax(state, depth = 3): 
    if depth == 0 or moves.is_terminal(state):
        return heuristic(state)

    legal_moves = moves.get_legal_moves(state)

    if not legal_moves:
        return heuristic(state)

    if state.is_player_move:
        best_value = float("inf")

        for move in legal_moves:
            next_state = moves.apply_move(state, move)
            value = minimax(next_state, depth - 1)

            if value < best_value:
                best_value = value

        return best_value

    else:
        best_value = float("-inf")

        for move in legal_moves:
            next_state = moves.apply_move(state, move)
            value = minimax(next_state, depth - 1)

            if value > best_value:
                best_value = value

        return best_value
    
def get_best_move(state, depth):
    legal_moves = moves.get_legal_moves(state)

    if not legal_moves:
        return None

    best_moves = []
    best_value = float("-inf")

    for move in legal_moves:
        next_state = moves.apply_move(state, move)
        value = minimax(next_state, depth - 1)

        if value > best_value:
            best_value = value
            best_moves = [move]
        elif value == best_value:
            best_moves.append(move)

    return random.choice(best_moves)