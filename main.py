import pygame, math
from board import Board
from renderer import Renderer

WIDTH = 800
HEIGHT = 800

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
clock.tick(60)

Board1 = Board(WIDTH, HEIGHT, screen)
Board1.create_board()
Board1.setup_pieces()

renderer = Renderer(screen, Board1.square_length)

possible_moves = []
selected_piece = None
turn = "W"
piece_row = None
piece_col = None


def reset_square_colors():
    for i in range(len(Board1.squares)):
        for j in range(len(Board1.squares)):
            Board1.squares[i][j].displayed_color = Board1.squares[i][j].color


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos

                col = math.floor(mouse_pos[0] / Board1.square_length)
                row = math.floor(mouse_pos[1] / Board1.square_length)
                square = Board1.squares[row][col]

                if Board1.positions[row][col] != "." and Board1.positions[row][col].color == turn:
                    selected_piece = Board1.positions[row][col]
                    piece_row, piece_col = row, col

                    possible_moves = selected_piece.get_moves(Board1, [row,col])
                    Board1.get_legal_moves(turn, selected_piece)
                    possible_moves = selected_piece.moves
                    reset_square_colors()
                    for move in possible_moves:
                        square = Board1.squares[move[0]][move[1]]
                        square.displayed_color = square.highlighted_color
                
                else:
                    reset_square_colors()

                if Board1.make_move(selected_piece, possible_moves, [row, col], [piece_row, piece_col]):
                    possible_moves = []
                    reset_square_colors()
                    turn = "B" if turn == "W" else "W"    


    screen.fill((0, 0, 0))
   
    renderer.draw(Board1)

    if Board1.check_checkmate(turn):
        won = "Black" if turn == "W" else "White"
        text_surface = my_font.render(f'Checkmate: {won} wins!', True, (0, 0, 0))
        rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text_surface, rect)
    elif Board1.check_stalemate(turn):
        text_surface = my_font.render(f'Stalemate', True, (0, 0, 0))
        rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text_surface, rect)


    pygame.display.flip()
   
pygame.quit()