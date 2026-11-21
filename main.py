import pygame, time
from renderer import Renderer
from game import Game
from engine_connection import ChessEngine

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

engine = ChessEngine()
game = Game(screen, WIDTH, HEIGHT, engine_enabled, renderer, engine)

game.turn = "W"
running = True
move_made = False
game_over = False
game.engine_enabled = False

start = time.time_ns()
print(engine.perft(5))
print((time.time_ns() - start) / (10 ** 9))

while running:
    clock.tick(60)
    screen.fill((128, 128, 128))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                if game.engine_enabled:
                    if game.turn == player_color:
                        game.get_clicked_piece(mouse_pos, engine)

                        if game.check_promotion():
                            renderer.draw(engine.get_board())
                            choice = game.handle_promote_screen()

                            if game.selected_piece == "p":
                                choice = choice.lower()

                            game.make_move(engine, choice)
                        else:
                            game.make_move(engine)
                        move_made = True

                else:
                    game.get_clicked_piece(mouse_pos, engine)

                    if game.check_promotion():
                        renderer.draw(engine.get_board())
                        choice = game.handle_promote_screen()

                        if game.selected_piece == "p":
                            choice = choice.lower()

                        game.make_move(engine, choice)
                    else:
                        game.make_move(engine)
                    move_made = True
    """
        if move_made:
            game_over = game.check_and_display_gameend(Board1)
            move_made = False
    """
    
    renderer.draw(engine.get_board())
    #renderer.draw_eval_bar(0)
    

    pygame.display.flip()
   
pygame.quit()
