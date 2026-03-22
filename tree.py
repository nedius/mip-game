from copy import deepcopy


class TreeNode:
    def __init__(self, state):
        self.state = state
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
    num_array = state.get_num_array()

    for pair_number in range(1, len(num_array) // 2 + 1):
        new_state = deepcopy(state)
        new_state.sum_pair(pair_number)

        if state.is_player_move:
            new_state.first_player_score += 1
        else:
            new_state.second_player_score += 1

        new_state.is_player_move = not state.is_player_move
        next_states.append(new_state)

    if len(num_array) % 2 != 0:
        new_state = deepcopy(state)
        new_state.remove_last()

        if state.is_player_move:
            new_state.second_player_score -= 1
        else:
            new_state.first_player_score -= 1

        new_state.is_player_move = not state.is_player_move
        next_states.append(new_state)

    return next_states


def build_tree(state, depth=3, visited=None):

    if visited is None:
        visited = set()

    key = state_key(state)

    if key in visited:
        return None

    visited.add(key)

    node = TreeNode(deepcopy(state))


    if depth == 0 or len(state.get_num_array()) == 1:
        return node

    next_states = generate_next_states(state)

    for next_state in next_states:
        child = build_tree(next_state, depth - 1, visited)

        if child is not None:
            node.children.append(child)

    return node