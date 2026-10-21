import pygame
from board import Board
from renderer import Renderer

WIDTH = 800
HEIGHT = 800

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
clock.tick(60)

Board1 = Board(WIDTH, HEIGHT, screen)
Board1.create_board()
Board1.setup_pieces()

renderer = Renderer(screen)

possible_moves = []
selected_piece = None
turn = "W"

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos

                for piece in Board1.pieces_group:
                    if piece.rect.collidepoint(mouse_pos) and piece.color == turn:
                        selected_piece = piece
                        possible_moves = piece.get_moves(Board1)
                       

                for square in Board1.squares:
                    if square.rect.center in possible_moves:
                        square.displayed_color = square.highlighted_color
                       
                    if square.rect.collidepoint(mouse_pos) and selected_piece != None and square.rect.center != selected_piece.position and square.rect.center in possible_moves: # Moved a piece
                        for piece in Board1.pieces_group:
                            if piece.rect.center == square.rect.center:
                                piece.kill()
                        Board1.positions = selected_piece.move(Board1, square)
                        selected_piece = None

                        turn = "B" if turn == "W" else "W"
                       
                        for square in Board1.squares:
                            square.displayed_color = square.color
                        possible_moves = []
                       
            for square in Board1.squares:
                if square.rect.center not in possible_moves:
                    square.displayed_color = square.color
   
    screen.fill((0, 0, 0))

   
    renderer.draw(Board1)


    pygame.display.flip()
   
pygame.quit()
