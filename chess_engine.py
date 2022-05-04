class GameState():
    """
    This class is responsible for storing all the information about the current state of a chess game.
    It will also be responsible for determining the valid moves at the current state.
    It will also keep a move Log.
    """
    def __init__(self):
        # The Board is an 8x8 2D list.
        # Each piece consists of 2 characters, the first represents whether it's white or black,
        # while the second represents the type of the piece Empty spaces are marked as
        # "--" as it adds to the symmetry of the board
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.white_to_move = True
        self.move_log = []
        
    def make_move(self, move):
        """
        Takes a move as a parameter and executes it (It won't work on castling and enpassant, 
        and promotion)
        """
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move) # Log the move to undo it later
        self.white_to_move = not self.white_to_move

    def undo_move(self):
        """
        Undo the last move
        """
        if self.move_log:      # Make sure there's at least one move played
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

    def get_valid_moves(self):
        """
        All moves considering checks
        """
        return self.get_possible_moves()

    def get_possible_moves(self):
        """
        All moves not considering checks
        """
        moves = []
        # pylint: disable=locally-disabled, invalid-name
        for r, _ in enumerate(self.board):
            for c, _ in enumerate(self.board[r]):
                turn = self.board[r][c][0]
                if(turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[r][c][1]
                    if piece == 'P':
                        self.get_pawn_moves(r, c, moves)
                    if piece == 'R':
                        self.get_rock_moves(r, c, moves)
        return moves

    def get_pawn_moves(self, r, c, moves):       
        """
        Get all possible moves for the pawn located at (r, w) and add them the list of all 
        possible moves
        """
        pass
    def get_rock_moves(self, r, c, moves):       
        """
        Get all possible moves for the rock located at (r, w) and add them the list of all 
        possible moves
        """
        pass

class Move():
    # maps keys to values for chess notation
    ranks_to_rows = {"8": 0, "7": 1, "6": 2, "5": 3,
                     "4": 4, "3": 5, "2": 6, "1": 7}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}
    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]  
        # Unique Id for each move
        self.move_id = self.start_row * 1000 + \
            self.start_col * 100 + self.end_row * 10 + self.end_col
        print(self.move_id)
    def __eq__(self, other):
        """
        Overriding the equals method
        """
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False
    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]