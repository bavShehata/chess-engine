from lzma import CHECK_ID_MAX
import random

# Scoring each piece
piece_score = {'K':0, 'Q': 10, 'R': 5, 'B': 3, 'N': 3, 'P': 1} # King's values doesn't matter since no way to capture it,
CHECKMATE = 1000        # Checkmate is the most important
STALEMATE = 0       # Stalemate is better than a losing position
DEPTH = 2

def find_random_move(valid_moves):
    """
    This function just returns one valid move at random
    """
    return valid_moves[random.randint(0, len(valid_moves) - 1)]
    
def find_greedy_move(gs, valid_moves):
    """
    This function uses a greedy algorithms to return a move that gives the current player the highest score based only on one move ahead.
    """
    turn_multiplier = 1 if gs.white_to_move else -1    # 1 if white to move, otherwise -1, for zero-sum game
    max_score = -CHECKMATE
    best_move = None
    random.shuffle(valid_moves)     # Prevents the agent from being predictable when multiple moves have same score
    for player_move in valid_moves:
        gs.make_move(player_move)
        if gs.check_mate:
            score = CHECKMATE
        elif gs.stale_mate:
            score = STALEMATE
        else:
            score = turn_multiplier * score_material(gs.board)
        if(score > max_score):
            max_score = score
            best_move = player_move
        gs.undo_move()
    return best_move

def find_minimax_move_iteratively(gs, valid_moves):
    """
    This function uses minimax algorithm iteratively to return the best move by looking 2 moves ahead. 
    This essentially now gives the AI agent the ability to checkmate better and think about trading pieces
    """
    turn_multiplier = 1 if gs.white_to_move else -1    # 1 if white to move, otherwise -1, for zero-sum game
    opponent_minimax_score = CHECKMATE      # I want to minimize this score
    best_player_move = None
    random.shuffle(valid_moves)     # Prevents the agent from being predictable when multiple moves have same score
    for player_move in valid_moves:
        gs.make_move(player_move)
        # Finding best move for opponent
        opponent_moves = gs.get_valid_moves()
        # If the player is in stalemate or checkmate, there's no need to check the opponent's moves
        if gs.check_mate:
            opponent_max_score = -CHECKMATE
        elif gs.stale_mate:
            opponent_max_score = STALEMATE
        else:
            opponent_max_score = -CHECKMATE     # I want to maximize this score since this will be the ideal move for the opponent
            for opponent_move in opponent_moves:
                gs.make_move(opponent_move)
                gs.get_valid_moves()
                if gs.check_mate:
                    score = CHECKMATE
                elif gs.stale_mate:
                    score = STALEMATE
                else:
                    score = -turn_multiplier * score_material(gs.board)
                if(score > opponent_max_score):
                    opponent_max_score = score
                gs.undo_move()
        if opponent_max_score < opponent_minimax_score: # If their new score is less than their previous, then that's the move I should go for
            opponent_minimax_score = opponent_max_score
            best_player_move = player_move
        gs.undo_move()
    return best_player_move


def find_best_move_minimax(gs, valid_moves):
    """
    A helper function for the first recursive call of find_minimax_move_recursively() function 
    that will return the global variable next_move
    """
    global next_move
    next_move = None
    find_minimax_move_recursively(gs, valid_moves, DEPTH, gs.white_to_move)
    return next_move

def find_minimax_move_recursively(gs, valid_moves, depth, white_to_move):
    """
    This function uses minimax algorithm recursively to return the best move by looking multiple moves ahead. 
    This essentially now gives the AI agent the ability to checkmate better and think about trading pieces
    """
    global next_move
    if depth == 0:
        return score_board(gs)
    
    if white_to_move:
        max_score = -CHECKMATE
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = find_minimax_move_recursively(gs, next_moves, depth - 1, False)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return max_score
    else:
        min_score = CHECKMATE
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = find_minimax_move_recursively(gs, next_moves, depth - 1, True)
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return min_score
            
def score_board(gs):
    """
    Score the board based on material AND other rules.
    A positive score is good for white, while a negative score is good for black
    """
    if gs.check_mate:
        if gs.white_to_move:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.stale_mate:
        return STALEMATE
    
    score = 0
    for row in gs.board:
        for square in row:
            # Since this is a zero-sum game, whatever points white gains, black loses, so white would
            # add to the score, while black will subtract
            if square[0] == 'w':        # If it's a white piece
                score += piece_score[square[1]]
            elif square[0] == 'b':
                score -= piece_score[square[1]]
    return score
def score_material(board):
    """
    Score the board based on material
    """
    score = 0
    for row in board:
        for square in row:
            # Since this is a zero-sum game, whatever points white gains, black loses, so white would
            # add to the score, while black will subtract
            if square[0] == 'w':        # If it's a white piece
                score += piece_score[square[1]]
            elif square[0] == 'b':
                score -= piece_score[square[1]]
    return score