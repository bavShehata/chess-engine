from lzma import CHECK_ID_MAX
import random

# Scoring each piece
piece_score = {'K':0, 'Q': 10, 'R': 5, 'B': 3, 'N': 3, 'P': 1} # King's values doesn't matter since no way to capture it,
CHECKMATE = 1000        # Checkmate is the most important
STALEMATE = 0       # Stalemate is better than a losing position


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

def find_minimax_move(gs, valid_moves):
    """
    THis function uses minimax algorithm to return the best move by looking 2 moves ahead. 
    This essentially now gives the AI agent the ability to checkmate better and think about trading pieces
    """
    turn_multiplier = 1 if gs.white_to_move else -1    # 1 if white to move, otherwise -1, for zero-sum game
    opponent_minimax_score = CHECKMATE      # I want to minimize this score
    best_player_move = None
    random.shuffle(valid_moves)     # Prevents the agent from being predictable when multiple moves have same score
    for player_move in valid_moves:
        gs.make_move(player_move)
        # Finding best move for opponent
        opponent_moves = gs.get_valid_moves
        opponent_max_score = -CHECKMATE     # I want to maximize this score since this will be the ideal move for the opponent
        for opponent_move in opponent_moves:
            gs.make_move(opponent_move)
            if gs.check_mate:
                score = -turn_multiplier * CHECKMATE
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