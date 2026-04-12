import moves
import random
from tree import build_tree


def heuristic(state):
    value = sum(state.get_num_array()) * 0.05
    return (state.second_player_score - state.first_player_score) + \
           (state.second_player_score * 0.1) + value


# ── Minimax ────────────────────────────────────────────────────────────────────

def _minimax(node, counters):
    """
    Internal recursive minimax.
    counters = {"generated": int, "evaluated": int}
      generated – every node visited
      evaluated – leaf nodes scored by heuristic
    """
    if not node.children:
        counters["evaluated"] += 1
        return heuristic(node.state)

    if node.state.is_player_move:          # minimiser (human)
        best_value = float("inf")
        for child in node.children:
            counters["generated"] += 1
            value = _minimax(child, counters)
            if value < best_value:
                best_value = value
        return best_value
    else:                                  # maximiser (computer)
        best_value = float("-inf")
        for child in node.children:
            counters["generated"] += 1
            value = _minimax(child, counters)
            if value > best_value:
                best_value = value
        return best_value


def get_best_move(state, depth=3):
    if not moves.get_legal_moves(state):
        return None, {"generated": 0, "evaluated": 0}

    counters   = {"generated": 0, "evaluated": 0}
    root       = build_tree(state, depth) 
    best_moves = []
    best_value = float("-inf")

    for child in root.children:
        counters["generated"] += 1
        value = _minimax(child, counters)
        if value > best_value:
            best_value = value
            best_moves = [child.move]
        elif value == best_value:
            best_moves.append(child.move)

    return random.choice(best_moves), counters

 
# ── Alpha-Beta ─────────────────────────────────────────────────────────────────

def _alphabeta(node, alpha, beta, counters):
    """
    Internal recursive alpha-beta.
    counters = {"generated": int, "evaluated": int, "pruned": int}
      pruned – number of times a branch was cut off
    """
    if not node.children:
        counters["evaluated"] += 1
        return heuristic(node.state)

    if node.state.is_player_move:          # minimiser (human)
        value = float("inf")
        for child in node.children:
            counters["generated"] += 1
            value = min(value, _alphabeta(child, alpha, beta, counters))
            beta = min(beta, value)
            if alpha >= beta:
                counters["pruned"] += 1
                break
        return value
    else:                                  # maximiser (computer)
        value = float("-inf")
        for child in node.children:
            counters["generated"] += 1
            value = max(value, _alphabeta(child, alpha, beta, counters))
            alpha = max(alpha, value)
            if alpha >= beta:
                counters["pruned"] += 1
                break
        return value


def get_best_move_alphabeta(state, depth=3):
    if not moves.get_legal_moves(state):
        return None, {"generated": 0, "evaluated": 0, "pruned": 0}

    counters   = {"generated": 0, "evaluated": 0, "pruned": 0}
    root       = build_tree(state, depth)   
    best_moves = []
    best_value = float("-inf")
    alpha      = float("-inf")
    beta       = float("inf")

    for child in root.children:
        counters["generated"] += 1
        value = _alphabeta(child, alpha, beta, counters)
        if value > best_value:
            best_value = value
            best_moves = [child.move]
        elif value == best_value:
            best_moves.append(child.move)
        alpha = max(alpha, best_value)

    return random.choice(best_moves), counters