"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    
    Xcnt = 0
    Ocnt = 0

    for row in board:
        Xcnt += row.count(X)
        Ocnt += row.count(O)

    if Xcnt <= Ocnt:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    
    moves = set()

    for idx1, row in enumerate(board):
        for idx2, item in enumerate(row):
            if item == None:
                moves.add((idx1, idx2))

    return moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    player_move = player(board)
    board1 = deepcopy(board)

    i, j = action

    if board[i][j] != None:
        raise Exception
    else:
        board1[i][j] = player_move

    return board1

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    for player in (X, O):
        
        # check vertical
        for row in board:
            if row == [player] * 3:
                return player
            
        # check horizantal
        for i in range(3):
            col = [board[x][i] for x in range(3)]
            if col == [player] * 3:
                return player
            
        # Diagonals
        if [board[i][i] for i in range(3)] == [player] * 3:
            return player
        elif [board[i][~i] for i in range(3)] == [player] * 3:
            return player
        
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    if winner(board) != None:
        return True
    
    for row in board:
        if EMPTY in row:
            return False
        
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    first = winner(board)
    
    if first == X:
        return 1
    elif first == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    def max_val(board):
        opt = ()
        if terminal(board):
            return utility(board), opt
        else:
            v = -2
            for action in actions(board):
                minval = min_val(result(board, action))[0]
                if minval > v:
                    v = minval
                    opt = action
            
            return v, opt
        
    def min_val(board):
        opt = ()

        if terminal(board):
            return utility(board), opt
        else:
            v = 2
            for action in actions(board):
                maxval = max_val(result(board, action))[0]
                if maxval < v:
                    v = maxval
                    opt = action
            
            return v, opt
        
    cur = player(board)

    if terminal(board):
        return None
    
    if cur == X:
        return max_val(board)[1]
    else:
        return min_val(board)[1]