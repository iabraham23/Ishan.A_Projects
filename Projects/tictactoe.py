
INITIAL_STATE = '.........'

def successor(state, index, player):
    return state[:index] + player + state[index+1:]

def legal_moves(state):
    return [i for i in range(len(state)) if state[i] == '.']

def winner(state):
    lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
             [0, 3, 6], [1, 4, 7], [2, 5, 8],
             [0, 4, 8], [2, 4, 6]]
    for line in lines:
        if state[line[0]] == state[line[1]] == state[line[2]]:
            player = state[line[0]]
            if player == 'X':
                return 1
            if player == 'O':
                return -1
    return 0

def less(a, b):
    return a < b

def greater(a, b):
    return a > b

def value(state, player, better, bad):
    """
    Returns the value of state if it is player's turn.
    :param better takes two values and returns True if the first is better.
    :param bad a value worse than anything we will see.
    """
    if winner(state) != 0: #someone has won
        return winner(state)
    if not legal_moves(state): #game ended in tie
        return 0
    best_value = bad
    for m in legal_moves(state):
        s = successor(state, m, player)
        if player == 'X':
            v = value(s, 'O', less, 2)
        else:
            v = value(s, 'X', greater, -2)
        if better(v, best_value):
            best_value = v
    return best_value

def best_move_for_x(state):
    best_value = -2
    best_move = None
    for m in legal_moves(state):
        s = successor(state, m, 'X')
        v = value(s, 'O', less, 2)
        if v > best_value:
            best_value = v
            best_move = m
    return best_move

