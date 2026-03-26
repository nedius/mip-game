import moves
import random

def heuristic(state):
    value = sum(state.get_num_array()) * 0.05
    return (state.second_player_score - state.first_player_score) + (state.second_player_score * 0.1) + value 

# ── Minimax ────────────────────────────────────────────────────────────────────

def minimax(state, depth=3): 
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

def get_best_move(state, depth=3):
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

# ── Alpha-Beta ─────────────────────────────────────────────────────────────────

def alphabeta(state, depth=3, alpha=float("-inf"), beta=float("inf")):
    """
    Minimax with Alpha-Beta pruning.
    alpha – best value the maximiser (computer) can guarantee so far.
    beta  – best value the minimiser (player)   can guarantee so far.
    """
    if depth == 0 or moves.is_terminal(state):
        return heuristic(state)

    legal_moves = moves.get_legal_moves(state)
    if not legal_moves:
        return heuristic(state)

    if state.is_player_move:          # minimiser  (human)
        value = float("inf")
        for move in legal_moves:
            next_state = moves.apply_move(state, move)
            value = min(value, alphabeta(next_state, depth - 1, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:         # alpha cut-off
                break
        return value

    else:                             # maximiser  (computer)
        value = float("-inf")
        for move in legal_moves:
            next_state = moves.apply_move(state, move)
            value = max(value, alphabeta(next_state, depth - 1, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:         # beta cut-off
                break
        return value

def get_best_move_alphabeta(state, depth=3):
    legal_moves = moves.get_legal_moves(state)
    if not legal_moves:
        return None

    best_moves = []
    best_value = float("-inf")
    alpha = float("-inf")
    beta  = float("inf")

    for move in legal_moves:
        next_state = moves.apply_move(state, move)
        value = alphabeta(next_state, depth - 1, alpha, beta)
        if value > best_value:
            best_value = value
            best_moves = [move]
        elif value == best_value:
            best_moves.append(move)
        alpha = max(alpha, best_value)

    return random.choice(best_moves)
