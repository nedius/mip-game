

def heurustic(state):
    score_diff = state.first_player_score - state.second_player_score
    
    move_bonuss = 0.2 if not state.is_player_move else -0.2
    odd_bonus = 0.3 if len(state.get_num_array()) % 2 != 0 else 0
    return score_diff + move_bonuss + odd_bonus