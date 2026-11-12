import pygame
from renderer import Renderer
from game import Game
from engine import Engine
import time, math, random
import copy
import chess_engine

WIDTH = 850
HEIGHT = 800

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player_color = "W"
engine_color = "B"
engine_enabled = False


renderer = Renderer(screen, WIDTH, HEIGHT)

Board1 = chess_engine.Board()
Move_Generator = chess_engine.MoveGenerator()

game = Game(screen, WIDTH, HEIGHT, engine_enabled, renderer, Move_Generator)

game.turn = "W"
running = True
move_made = False
game_over = False
game.engine_enabled = False
while running:
    clock.tick(60)
    screen.fill((128, 128, 128))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if game.engine_enabled:
                    if game.turn == player_color:
                        mouse_pos = event.pos
                        game.get_clicked_piece(mouse_pos, Board1)
                        game.make_move(Board1)
                        move_made = True

                else:
                    mouse_pos = event.pos
                    game.get_clicked_piece(mouse_pos, Board1)
                    game.make_move(Board1)
                    move_made = True
    """
        if move_made:
            game_over = game.check_and_display_gameend(Board1)
            move_made = False
    """
    """
    if game.check_promotion(Board1) != None:
        promoted_piece = game.check_promotion(Board1)
        renderer.draw(Board1)
        choice = game.handle_promote_screen()
        game.promote(promoted_piece, choice, Board1)
    
    """
    renderer.draw(Board1)
    #renderer.draw_eval_bar(0)
    

    pygame.display.flip()
   
pygame.quit()
