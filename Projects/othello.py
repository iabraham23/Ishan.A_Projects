# Team members who contributed to this project: Ishan and Braydon

INITIAL_STATE = ('........',) * 3 + ('...XO...', '...OX...') + ('........',) * 3

DIRECTIONS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))


def flips(board, player, location):
    """
    :param board: A sequence of strings
    :param player: 'X' or 'O'
    :param location: A pair (r, c) with 0 <= r < 8 and 0 <= c < 8
    :return: A collection of pairs of locations of opponent's pieces that would be flipped by this move
    """
    def f(r, c, dr, dc):  # Find flips starting at (r, c) and looking in direction (dr, dc)
        line = []
        while True:
            r, c = (r + dr, c + dc)
            if not (0 <= r < 8 and 0 <= c < 8):
                return []  # Edge of board -- no capture
            if board[r][c] == '.':
                return []  # Empty space -- no capture
            if board[r][c] == player:
                return line  # Friendly piece -- capture all opposing pieces seen so far
            line.append((r, c))
    result = []
    for d in DIRECTIONS:
        result.extend(f(*location, *d))
    return result


def successor(board, player, move):
    """
    :param board: A sequence of strings
    :param player: 'X' or 'O'
    :param move: Either 'pass' or a pair (r, c) with 0 <= r < 8 and 0 <= c < 8
    :return: The board that would result if player played move
    """
    if move == 'pass':
        return board
    mutable_board = [list(row) for row in board]  # Copy to a list of lists
    for r, c in flips(board, player, move):
        mutable_board[r][c] = player
    r, c = move
    mutable_board[r][c] = player
    return tuple(''.join(row) for row in mutable_board)


def legal_moves(board, player):
    """
    :param board: A sequence of strings
    :param player: 'X' or 'O'
    :return: A collection of legal moves for player from board; each is (r, c). Returns an empty collection if neither
    player has a legal move or ['pass'] if player cannot make a capturing move.
    """
    result = []
    game_over = True
    for r in range(8):
        for c in range(8):
            if board[r][c] == '.':
                here = (r, c)
                if flips(board, player, here):
                    game_over = False
                    result.append(here)
                # The inclusion of game_over in the condition below is for efficiency:
                # If it has already been determined that the game is not over, there's not need to check
                # for opposing legal moves
                elif game_over and flips(board, opposite(player), here):
                    game_over = False
    if result or game_over:
        return result
    return ['pass']


def score(board):
    """
    :param board: A sequence of strings
    :return: The difference between the number of pieces 'X' has and the number 'O' has. This is therefore positive if
    'X' is winning, negative if 'O' is winning, and 0 if the score is tied.
    """
    res = 0
    for row in board:
        for piece in row:
            if piece == 'X':
                res+=1
            elif piece == 'O':
                res-=1
    return res


def opposite(player):
    if player == 'X':
        return 'O'
    return 'X'


def value(board, player, depth):
    """
    :param board: A string
    :param player: 'X' or 'O'
    :param depth: At least 1; greater depth is slower but smarter
    :return: The value of board if it is player's turn
    """
    def find_value(b, p, d, compare, worst):
        if not legal_moves(b, p):
            return 0
        best_val = worst
        if d == 1:  # handles case of depth being one = target depth, where we return best possible move
            for move in legal_moves(b, p):
                s = successor(b, p, move)
                if compare(score(s), best_val):
                    best_val = score(s)
            return best_val
        for move in legal_moves(b, p):
            s = successor(b, p, move)
            if player == 'X':  # turn for 'O'
                v = find_value(s, 'O', d - 1, less, float('inf'))
            else:  # turn for 'X'
                v = find_value(s, 'X', d - 1, greater, -float('inf'))
            if compare(v, best_val):
                best_val = v
        return best_val

    if player == 'X':
        return find_value(board, 'X', depth, greater, -float('inf'))
    else:
        return find_value(board, 'O', depth, less, float('inf'))

def less(x, y):
    return x < y


def greater(x, y):
    return x > y


def best_move(board, player, depth):
    """
    :param board: A string
    :param player: 'X' or 'O'
    :param depth: At least 1; greater depth is slower but smarter
    :return: The best move (index) for player
    """
    def find_move(b, p, d, compare, worst):
        if not legal_moves(b, p):
            return 0
        best_val = worst
        BestMove = None
        if d == 1:  # handles case of depth being one = target depth, where we return best possible move
            for move in legal_moves(b, p):
                s = successor(b, p, move)
                if compare(score(s), best_val):
                    best_val = score(s)
                    BestMove = move
            return BestMove
        for move in legal_moves(b, p):
            s = successor(b, p, move)
            if player == 'X':  # turn for 'O'
                v = value(s,'O',d-1)
            else:  # turn for 'X'
                v = value(s,'X',d-1)
            if compare(v, best_val):
                best_val = v
                BestMove = move
        return BestMove

    if player == 'X':
        return find_move(board, 'X', depth, greater, -float('inf'))
    else:
        return find_move(board, 'O', depth, less, float('inf'))


def print_board(board):
    print(' 01234567')
    for i in range(8):
        print(str(i) + board[i] + str(i))
    print(' 01234567')
    print()



"""
Edited code below to make it play against itself, 

Interestingly something we found was that at certain depths, even when faced against a worse opponent, the better one will 
lose. This is most likely because of the horizon problem that we discussed in class

"""

def main():
    board = INITIAL_STATE
    player = 'X'
    while True:
        moves = legal_moves(board, player)
        if not moves:
            break
        if moves == ['pass']:
            move = 'pass'
        elif player == 'X':
            move = best_move(board, player, 1)  # Adjust this number for a stronger, slower player
        else:
            move = best_move(board, player, 5)
        board = successor(board, player, move)
        print_board(board)
        player = opposite(player)
    w = score(board)
    if w > 0:
        print('X wins!')
    elif w < 0:
        print('O wins!')
    else:
        print('Tie.')


if __name__ == '__main__':
    main()