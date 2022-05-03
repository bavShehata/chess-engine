'''
This is our main driver file. It ill be responsible for handling user input and displaying the current Game State object.
'''
import pygame as p
import chessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8 # A chess board is 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # For animations
IMAGES = {}

'''
Initialize the global dictionary of IMAGES only once to save on computation
'''
def load_images():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))
    #NOTE: we can access each image  by 'Images['wP]' for example
    print(IMAGES)
    
'''
The main driver, handling user input, and updating graphics
'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessEngine.GameState()
    load_images()
    draw_game_state(screen, gs)
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        clock.tick(MAX_FPS)
        p.display.flip()
    
'''
Responsible for all the graphics withing our current game state
'''
def draw_game_state(screen, gs):
    draw_board(screen) # Draw squares on the board
    draw_pieces(screen, gs.board) # Draw pieces on top of the board
    
''' Draw the squares on the board. The top left square is always light '''
def draw_board(screen):
    colors = {'light': (245, 230, 190), 'dark': (100, 70, 60)}
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors["light"] if (r+c) % 2 == 0 else colors["dark"]
            square = p.Rect(SQ_SIZE*c, SQ_SIZE*r, SQ_SIZE, SQ_SIZE)
            p.draw.rect(screen, color, square)


''' Draw the pieces on the board using the current state '''    
def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(SQ_SIZE*c, SQ_SIZE*r, SQ_SIZE, SQ_SIZE))

# Best practice to ensure the function only runs when the file is run directly
if __name__ == "__main__":
    main()