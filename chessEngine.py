'''
This class is responsible for storing all the information about the current state of a chess game. It will also be
esponsible for determining the valid moves at the current state. It will also keep a move Log.
'''
class GameState():
    def __init__(self):
        # The Board is an 8x8 2D list. 
        # Each piece consists of 2 characters, the first represents whether it's white or black, while the second represents the type of the piece
        # Empty spaces are marked as "--" as it adds to the symmetry of the board
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
        self.whiteToMove = True
        self.moveLog = []
        
        