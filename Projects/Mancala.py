'''
Mancala GUI using Tkinter
Game performs a variation of Mancala I used to play:  
if you end in a non-zero pit you pick up and keep going unless you finish in your goal (go again) or in a pit with nothing (end turn)

Simple board design just using basics of Tkinter 

'''


from tkinter import *


class Boards:
    def __init__(self):
        self.l1, self.l2, self.amount = init_boards()
        self.hand = 0
        self.player1_score = 0
        self.player2_score = 0
        self.p1_valid_moves = 'ABCDEF'
        self.p2_valid_moves = 'HIJKLM'
        self.current_player = 1
        self.buttons = []

def Close():
    quit()

def create_circle(x, y, r, canvas): # xy are center coordinates, r is radius
    # taken from stack overflow
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1)

def four_circles(x, y, r, canvas): #coords where the 4 circles are centered around
    d = 1.5 * r # less than diameter, just visual
    c1 = create_circle(x, y+d, r, canvas)
    c2 = create_circle(x + d, y, r, canvas)
    c3 = create_circle(x, y - d, r, canvas)
    c4 = create_circle(x-d, y, r, canvas)
    return c1, c2, c3, c4

def draw_board(board):
    no_goal_letters = 'MLKJIHABCDEF'
    count_for_button = 0
    grid = [[4 for _ in range(8)] for _ in range(2)]
    canvas_padx = 10
    canvas_pady = 10

    for r in range(2):
        for c in range(8):
            if (r == 0 and c == 0) or (r == 0 and c == 7):
                grid[r][c] = canvas.create_rectangle(c * SQUARE_WIDTH,
                                                          r * SQUARE_WIDTH,
                                                          c * SQUARE_WIDTH + (SQUARE_WIDTH - 1),
                                                          r * SQUARE_WIDTH + 2*(SQUARE_WIDTH-0.5),
                                                          outline='white')
                continue
            elif (r == 1 and c == 0) or (r == 1 and c == 7):
                continue

            grid[r][c] = canvas.create_rectangle(c * SQUARE_WIDTH,
                                                          r * SQUARE_WIDTH,
                                                          c * SQUARE_WIDTH + (SQUARE_WIDTH - 1),
                                                          r * SQUARE_WIDTH + (SQUARE_WIDTH - 1),
                                                          outline='white')
            let = no_goal_letters[count_for_button]
            but = Button(root, text= let, command=lambda letter=let: do_turn(True, board, board.current_player, letter),
                         activebackground = 'green',
                         borderwidth = 0,
                         relief = 'flat',
                         bg = 'green',
                         highlightthickness = 0)
            but.place(x= c * SQUARE_WIDTH + canvas_padx,
                      y= r * SQUARE_WIDTH + 5.8 * canvas_pady, #manual visual change
                      height = 0.5 * SQUARE_WIDTH,
                      width = 0.5 * SQUARE_WIDTH)
            board.buttons.append(but)
            count_for_button +=1
            update_display_amounts(board)
            text = 'This variation of Mancala makes you continue you turn if you\n end on a non-zero or non-goal pit'
            how_lab = Label(root, textvariable=StringVar(root, text))
            how_lab.place(x=20,y=200)



    return grid

def update_current_player_display(board):
    current_p = f'current player turn: {board.current_player}'
    var = StringVar(root, current_p)
    lab2 = Label(root, textvariable=var)
    lab2.place(x=100, y=150)

def update_display_amounts(board):
    update_current_player_display(board)
    letters = 'NMLKJIHGABCDEF' #need in this order to align amounts correctly
    count_for_letters = 0
    for r in range(2):
        for c in range(8):
            if (r == 0 and c == 0) or (r == 0 and c == 7):
                a = board.amount[letters[count_for_letters]]
                text_var = StringVar()
                text_var.set(a)
                label = Label(root, textvariable=text_var)
                label.place(x=c *SQUARE_WIDTH + (SQUARE_WIDTH - 1) -16, y=r * SQUARE_WIDTH + 2 * (SQUARE_WIDTH - 0.5)+5)
                count_for_letters += 1
                continue
            elif (r == 1 and c == 0) or (r == 1 and c == 7):
                continue
            a = board.amount[letters[count_for_letters]]
            text_var = StringVar()
            text_var.set(a)
            label = Label(root, textvariable=text_var)
            label.place(x=c * SQUARE_WIDTH + (SQUARE_WIDTH - 1) -18, y=r * SQUARE_WIDTH + 2*(SQUARE_WIDTH - 1)-5)
            count_for_letters += 1

def init_boards():
    letter1 = {'A':'B', 'B':'C','C':'D', 'D':'E','E':'F','F':'G',
             'G':'H', 'H':'I', 'I':'J' , 'J':'K','K':'L', 'L':'M', 'M':'A'}
    letter2 = {'A':'B', 'B':'C','C':'D', 'D':'E','E':'F',
             'F':'H', 'H':'I','I':'J', 'J':'K','K':'L', 'L':'M', 'M':'N', 'N': 'A'}
    board = {}
    for l in 'ABCDEFGHIJKLMN':
        board[l] = 4 #starting with 4 beads per hole
    board['G'] = 0 #goal for player 1
    board['N'] = 0 #goal for player 2
    return letter1, letter2, board

def do_turn(restrain, board, player, curr_spot):
    #--- bulletproofing
    if restrain: #do this only when a player chooses turn, not when we call recursively
        if player == 1: #checking if all valid pits are 0 for a player
            if all(board.amount[l] == 0 for l in board.p1_valid_moves):
                print('player 1 has no moves, player 2 turn')
                board.current_player = 2
                update_current_player_display(board)
                return
        elif all(board.amount[l] == 0 for l in board.p2_valid_moves):
            print('player 2 has no moves, player 1 turn')
            board.current_player = 1
            update_current_player_display(board)
            return
        if player != board.current_player: #mainly used in testing, not possible when using GUI
            print('invalid move, wrong player turn')
            return
        if player == 1 and (curr_spot not in board.p1_valid_moves):
            print(f'invalid move, select pit from {board.p1_valid_moves}')
            return
        elif player == 2 and (curr_spot not in board.p2_valid_moves):
            print(f'invalid move, select pit from {board.p2_valid_moves}')
            return
        if board.amount[curr_spot] == 0:
            print('invalid move, no beads in pit')
            return
    #---

    if player == 1:
        next_spot = board.l1[curr_spot]
        goal = 'G'
    else:
        next_spot = board.l2[curr_spot]
        goal = 'N'
    board.hand += board.amount[curr_spot]
    board.amount[curr_spot] = 0
    while board.hand > 1:
        if next_spot == goal: #could make code more concise below
            if player == 1:
                board.player1_score +=1
                board.amount[next_spot] += 1
                board.hand -= 1
                next_spot = board.l1[next_spot]
            else:
                board.player2_score +=1
                board.amount[next_spot] += 1
                board.hand -= 1
                next_spot = board.l2[next_spot]
        else:
            if player == 1:
                board.amount[next_spot] += 1
                board.hand -= 1
                next_spot = board.l1[next_spot]
            else:
                board.amount[next_spot] += 1
                board.hand -= 1
                next_spot = board.l2[next_spot]
    #now dealing with last bead
    if next_spot == goal: #take another turn by player
        if player == 1:
            board.player1_score +=1
            print(f'goal for player one, updated score: {board.player1_score}')
        else:
            board.player2_score +=1
            print(f'goal for player two, updated score: {board.player2_score}')
        board.amount[next_spot] +=1
        board.hand = 0
        print(f'just played: {curr_spot}, take another turn player {player}')
        print(board.amount)
        update_display_amounts(board)
        check_end_game(board) #check if game over
        return board.amount

    elif board.amount[next_spot] > 0: #VARIATION, pick up pit and continue by recursive call
        do_turn(False, board, player, next_spot)
        #restrain false allows us to bypass normal restraints, letting a player play moves
        #on the other side of the board which is what we want in this variation

    else: #means 0 pit ending, so end player turn
        if player == 1:
            board.current_player = 2
        else:
            board.current_player = 1
        board.amount[next_spot] += 1
        board.hand = 0
        print(f'just played: {curr_spot}, turn done for player {player}')
        print(board.amount)
        update_display_amounts(board)
        return board.amount

def check_end_game(board):
    if board.amount['G'] + board.amount['N'] == 48: #all beads in goals
        print('GAME OVER')
        for b in board.buttons: #turn off buttons
            b["state"] = "disabled"
        if board.player1_score > board.player2_score:
            print('player 1 wins')
        elif board.player2_score > board.player1_score:
            print('player 2 wins')
        else:
            print('tie')

if __name__ == "__main__":
    root = Tk()
    root.geometry("450x450")

    exit_button = Button(root, text="Exit", command=Close)
    exit_button.pack(pady=10)

    SQUARE_WIDTH = 40
    canvas = Canvas(root, width = 450, height = 450, bg = 'Green', highlightthickness = 0)
    canvas.pack(side = RIGHT, padx = 10, pady = 10)



    board = Boards()
    draw_board(board)
    #four_circles(50,50,7,canvas)

    root.mainloop()





