from copy import deepcopy
import moves


class TreeNode:
    def __init__(self, state, move=None):
        self.state = state
        self.move = move
        self.children = []


def state_key(state):
    return (
        tuple(state.get_num_array()),
        state.first_player_score,
        state.second_player_score,
        state.is_player_move
    )


def generate_next_states(state):
    next_states = []

    for move in moves.get_legal_moves(state):
        new_state = moves.apply_move(state, move)
        next_states.append(new_state)

    return next_states


def generate_next_states_with_moves(state):
    next_states_with_moves = []

    for move in moves.get_legal_moves(state):
        new_state = moves.apply_move(state, move)
        next_states_with_moves.append((move, new_state))

    return next_states_with_moves


def build_tree(state, depth=3, visited=None):
    if visited is None:
        visited = set()

    key = state_key(state)
    if key in visited:
        return None

    node = TreeNode(deepcopy(state))

    if depth == 0 or moves.is_terminal(state):
        return node

    visited.add(key)

    for move, next_state in generate_next_states_with_moves(state):
        child = build_tree(next_state, depth - 1, visited.copy())

        if child is not None:
            child.move = move
            node.children.append(child)

    return node