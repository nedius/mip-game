import moves
import random


def heuristic(state):
    value = sum(state.get_num_array()) * 0.05
    return (state.second_player_score - state.first_player_score) + \
           (state.second_player_score * 0.1) + value


# ── Minimax ────────────────────────────────────────────────────────────────────

def _minimax(state, depth, counters):
    """
    Internal recursive minimax.
    counters = {"generated": int, "evaluated": int}
      generated – every node created (apply_move call)
      evaluated – leaf nodes scored by heuristic
    """
    if depth == 0 or moves.is_terminal(state):
        counters["evaluated"] += 1
        return heuristic(state)

    legal_moves = moves.get_legal_moves(state)
    if not legal_moves:
        counters["evaluated"] += 1
        return heuristic(state)

    if state.is_player_move:          # minimiser (human)
        best_value = float("inf")
        for move in legal_moves:
            counters["generated"] += 1
            next_state = moves.apply_move(state, move)
            value = _minimax(next_state, depth - 1, counters)
            if value < best_value:
                best_value = value
        return best_value
    else:                             # maximiser (computer)
        best_value = float("-inf")
        for move in legal_moves:
            counters["generated"] += 1
            next_state = moves.apply_move(state, move)
            value = _minimax(next_state, depth - 1, counters)
            if value > best_value:
                best_value = value
        return best_value


def get_best_move(state, depth=3):
    """
    Returns (best_move, stats_dict).
    stats_dict keys: generated, evaluated
    """
    legal_moves = moves.get_legal_moves(state)
    if not legal_moves:
        return None, {"generated": 0, "evaluated": 0}

    counters   = {"generated": 0, "evaluated": 0}
    best_moves = []
    best_value = float("-inf")

    for move in legal_moves:
        counters["generated"] += 1
        next_state = moves.apply_move(state, move)
        value = _minimax(next_state, depth - 1, counters)
        if value > best_value:
            best_value = value
            best_moves = [move]
        elif value == best_value:
            best_moves.append(move)

    return random.choice(best_moves), counters


# ── Alpha-Beta ─────────────────────────────────────────────────────────────────

def _alphabeta(state, depth, alpha, beta, counters):
    """
    Internal recursive alpha-beta.
    counters = {"generated": int, "evaluated": int, "pruned": int}
      pruned – number of times a branch was cut off
    """
    if depth == 0 or moves.is_terminal(state):
        counters["evaluated"] += 1
        return heuristic(state)

    legal_moves = moves.get_legal_moves(state)
    if not legal_moves:
        counters["evaluated"] += 1
        return heuristic(state)

    if state.is_player_move:          # minimiser (human)
        value = float("inf")
        for move in legal_moves:
            counters["generated"] += 1
            next_state = moves.apply_move(state, move)
            value = min(value, _alphabeta(next_state, depth - 1, alpha, beta, counters))
            beta = min(beta, value)
            if alpha >= beta:
                counters["pruned"] += 1
                break
        return value
    else:                             # maximiser (computer)
        value = float("-inf")
        for move in legal_moves:
            counters["generated"] += 1
            next_state = moves.apply_move(state, move)
            value = max(value, _alphabeta(next_state, depth - 1, alpha, beta, counters))
            alpha = max(alpha, value)
            if alpha >= beta:
                counters["pruned"] += 1
                break
        return value


def get_best_move_alphabeta(state, depth=3):
    """
    Returns (best_move, stats_dict).
    stats_dict keys: generated, evaluated, pruned
    """
    legal_moves = moves.get_legal_moves(state)
    if not legal_moves:
        return None, {"generated": 0, "evaluated": 0, "pruned": 0}

    counters   = {"generated": 0, "evaluated": 0, "pruned": 0}
    best_moves = []
    best_value = float("-inf")
    alpha      = float("-inf")
    beta       = float("inf")

    for move in legal_moves:
        counters["generated"] += 1
        next_state = moves.apply_move(state, move)
        value = _alphabeta(next_state, depth - 1, alpha, beta, counters)
        if value > best_value:
            best_value = value
            best_moves = [move]
        elif value == best_value:
            best_moves.append(move)
        alpha = max(alpha, best_value)

    return random.choice(best_moves), counters