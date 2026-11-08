import pygame
from board import Board
from renderer import Renderer
from game import Game
from engine import Engine
import time, math, random
import cProfile
import pstats

WIDTH = 850
HEIGHT = 800

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
clock.tick(60)

player_color = "W"
engine_color = "B" 
engine_enabled = False

engine = Engine(engine_color, WIDTH, HEIGHT)

renderer = Renderer(screen, WIDTH, HEIGHT)

game = Game(screen, WIDTH, HEIGHT, engine_enabled, renderer)



chunk_size = 500000
validations_positions = 100000
total_positions = 5000000
epochs = 30

engine.get_data(r"C:/Users/user/Downloads/chessData.csv/chessData.csv", total_positions, validations_positions)
engine.bulkFEN_to_flatboard()
engine.extract_evals()
engine.data_to_validation_tensors()


"""
for get_best_move() smth like this needs to be done:
generate legal moves for the engine
save each pieces moves in a dict or smth
simulate each move on the board
call minimax with the opponenets turn since u made ur simulated move and depth - 1 since we looked one move ahead
minus the eval since it come for the opponents perspective
undo the move
if eval is higher than best remember the piece and that move
then return piece and move
make that move on the game board
shouldnt be that hard prob
"""




"""
profiler = cProfile.Profile()
profiler.enable()
"""


for epoch in range(epochs):
    chunks = math.ceil(len(engine.training_boards) / chunk_size)
    for i in range(chunks):
        start = time.time()
        engine.shuffle()
        print(f"Shuffle time {time.time() - start}")
        start = time.time()
        engine.data_to_training_tensors(chunk_size, i)
        print(f"time taken for data to tensors{time.time() - start}")
        start = time.time()
        engine.train()
        print(f"time taken to train {time.time() - start}")
    engine.validation()
"""
profiler.disable()

stats = pstats.Stats(profiler)
stats.sort_stats("cumulative")
stats.print_stats(30)
"""

engine.save_best_weights()



Board1 = Board(WIDTH, HEIGHT, screen)
Board1.create_board()
Board1.setup_pieces(game, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

game.turn = "W"
running = True
move_made = False
evaluation = engine.evaluate_position(Board1, game.turn)
while running:
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
                        move_made = engine.evaluate_position(Board1, game.turn)
                else:
                    mouse_pos = event.pos
                    game.get_clicked_piece(mouse_pos, Board1)
                    game.make_move(Board1)
                    move_made = engine.evaluate_position(Board1, game.turn)

        if move_made:
            evaluation = engine.evaluate_position(Board1, game.turn)

        if game.engine_enabled and game.turn == engine_color:
            engine.get_all_pieces(Board1)
            piece, move = engine.get_best_move(Board1)
            game.make_engine_move(piece, move, Board1)

    if game.check_promotion(Board1) != None:
        promoted_piece = game.check_promotion(Board1)
        renderer.draw(Board1)
        choice = game.handle_promote_screen()
        game.promote(promoted_piece, choice, Board1)
   
    renderer.draw(Board1)
    renderer.draw_eval_bar(evaluation)
    game.check_and_display_gameend(Board1)

    pygame.display.flip()
   
pygame.quit()