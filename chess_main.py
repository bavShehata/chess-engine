'''
This is our main driver file. It ill be responsible for handling user input and displaying the current Game State object.
'''
import pygame as p
import chess_engine
import chess_ai_agent as ai

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
'''
The main driver, handling user input, and updating graphics
'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chess_engine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False        # Flag variable when a move is made, to prevent regenerating the function pointlessly
    animate = False         # Flag variable for when we should animate
    load_images()
    running = True
    sqSelected = () # No square is slected intially (row, col)
    playerClicks = [] # Keep track of player clicks [(6,4), (4,4)]
    game_over = False
    player_one = True # If a human is playing white, then this will be true.
    player_two = False # If a human is playing black , then this will be true.
    while running:
        human_turn = (gs.white_to_move and player_one) or (not gs.white_to_move and player_two)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over and human_turn:
                    location = p.mouse.get_pos() # (x,y) location of mouse
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if gs.board[row][col] == '--' and len(playerClicks) == 0:
                        continue
                    if sqSelected == (row, col): # The user clicked the same square twice
                        sqSelected = () # Deselect
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) # Append both the 1st and 2nd clicks
                    if len(playerClicks) == 2: # After 2nd click
                        move = chess_engine.Move(playerClicks[0], playerClicks[1], gs.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                gs.make_move(valid_moves[i])
                                move_made = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not move_made:
                            playerClicks = [sqSelected] # Enables resetting a click when a user clicks on two same-color pieces
            elif e.type == p.KEYDOWN:
                if e.key == p.K_u:      # Undo the board
                    gs.undo_move()
                    move_made = True
                    animate = False
                elif e.key == p.K_r:        # Reset the board
                    gs = chess_engine.GameState()
                    valid_moves = gs.get_valid_moves()
                    sqSelected = ()
                    playerClicks = []
                    move_made = False
                    animate = False
                    
        # AI agent
        if not game_over and not human_turn:
            ai_move = ai.find_greedy_move(gs, valid_moves)
            if ai_move is None:
                ai_move = ai.find_random_move(valid_moves) # Should never need to call this
            gs.make_move(ai_move)
            move_made = True
            animate = True
            
        if move_made:
            if animate:
                animate_move(gs.move_log[-1], screen, gs.board, clock)
            valid_moves = gs.get_valid_moves()
            move_made = False
            animate = False
        draw_game_state(screen, gs, valid_moves, sqSelected)
        
        if gs.check_mate:
            game_over = True
            if gs.white_to_move:
                drawText(screen, "Black wins by checkmate")
            else:
                drawText(screen, "White wins by checkmate")
        if gs.stale_mate:
            game_over = True
            drawText(screen, "Stalemate")
        clock.tick(MAX_FPS)
        p.display.flip()
    
def highlight_squares(screen, gs, valid_moves, sq_selected):
    """
    Highlight square selected and the piece's available moves
    """
    if sq_selected != ():
        r, c = sq_selected
        if gs.board[r][c][0] == ('w' if gs.white_to_move else 'b'):     # sq_selected is a piece that can be moved
            # Highlight square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(150) #transperncy value -> 0: transparent - 255: opaque
            s.fill(p.Color(170,140,110))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # Highlight moves from that square
            s.fill(p.Color(120,40,180, 150))
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (move.end_col*SQ_SIZE, move.end_row*SQ_SIZE))
            
            


'''
Responsible for all the graphics withing our current game state
'''
def draw_game_state(screen, gs, valid_moves, sq_selected):
    draw_board(screen) # Draw squares on the board
    highlight_squares(screen, gs,  valid_moves, sq_selected)
    draw_pieces(screen, gs.board) # Draw pieces on top of the board
    
    
''' Draw the squares on the board. The top left square is always light '''
def draw_board(screen):
    global colors
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

"""
Animating the move
"""
def animate_move(move, screen, board, clock):
    global colors
    d_r = move.end_row - move.start_row
    d_c = move.end_col - move.start_col
    frames_per_square = 10 # Frames to move one square
    frame_count = (abs(d_r) + abs(d_c)) * frames_per_square
    for frame in range(frame_count + 1):
        r, c = (move.start_row + d_r*(frame/frame_count), move.start_col + d_c*(frame/frame_count))
        draw_board(screen)
        draw_pieces(screen, board)
        # Erase the piece moved from its ending square
        color = colors['dark'] if (move.end_row + move.end_col) % 2 else colors['light']
        end_square = p.Rect(move.end_col*SQ_SIZE, move.end_row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, end_square)
        # Draw captured piece into rectangle
        if move.piece_captured != '--':
            screen.blit(IMAGES[move.piece_captured], end_square)
        # Draw moving piece
        screen.blit(IMAGES[move.piece_moved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)
       
       
def drawText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0,0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Gray'))
    screen.blit(textObject, textLocation.move(2,2))

# Best practice to ensure the function only runs when the file is run directly
if __name__ == "__main__":
    main()