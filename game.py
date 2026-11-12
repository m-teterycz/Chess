import pygame, math
from piece import create_piece, check_valid_bounds

class Game:
    def __init__(self, screen, WIDTH, HEIGHT, engine_enabled, renderer, move_generator):
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.screen = screen
        self.turn = "W"
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.engine_enabled = engine_enabled
        self.selected_piece = None
        self.renderer = renderer
        self.move_generator = move_generator
        self.square_length = min(WIDTH, HEIGHT) // 8
        self.possible_moves = []

    def reset_square_colors(self):
        for square in self.renderer.squares:
            square.displayed_color = square.color

    def get_clicked_piece(self, mouse_pos, board):
        self.col = math.floor(mouse_pos[0] / self.square_length)
        self.row = math.floor(mouse_pos[1] / self.square_length)
        self.click_pos = self.col + self.row * 16
        piece = board.piece_at(self.click_pos)

        if piece != "." and piece.isupper() == self.turn.isupper(): # Check if its the players turn
            self.piece_pos = self.click_pos
            self.selected_piece = piece
            self.possible_moves = self.move_generator.generate_moves(self.piece_pos, piece, board)

            
            self.reset_square_colors()
            for move in self.possible_moves:
                row = move // 16
                col = move % 16
                move = row * 8 + col

                square = self.renderer.squares[move]
                square.displayed_color = square.highlighted_color

        else:
            self.reset_square_colors()

    def make_move(self, board):
        if self.selected_piece == None:
            return None

        if self.click_pos in self.possible_moves:
            board.move_to(self.piece_pos, self.click_pos)
        #self.reset_square_colors()
        #self.turn = "B" if self.turn == "W" else "W"

        """
        if self.selected_piece.piece_type == "P":
            board.halfmove = 0
        elif piece_count != len(board.pieces):
            board.halfmove = 0
        else:
            board.halfmove += 1
        board.fullmove += 1
        return True
        """

    def make_engine_move(self, piece, move, board):
        piece_count = len(board.pieces)
        board.make_move(piece, move, move, board.get_piece_pos(piece))
        if piece.piece_type == "P":
            if move[0] == 0 and piece.color == "W":
                self.promote(piece, "Q", board)
            elif move[0] == 7 and piece.color == "B":
                self.promote(piece, "Q", board)
            board.halfmove = 0
        elif piece_count != len(board.pieces):
            board.halfmove = 0
        else:
            board.halfmove += 1
        if self.turn == "B":
            board.fullmove += 1
        self.turn = "B" if self.turn == "W" else "W"

    def check_and_display_gameend(self, board):
            if board.check_checkmate(self.turn):
                won = "Black" if self.turn == "W" else "White"
                text_surface = self.my_font.render(f'Checkmate: {won} wins!', True, (0, 0, 0))
                rect = text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
                self.screen.blit(text_surface, rect)
                return True
            elif board.check_stalemate(self.turn):
                text_surface = self.my_font.render(f'Stalemate', True, (0, 0, 0))
                rect = text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
                self.screen.blit(text_surface, rect)
                return True
            return False

    def check_promotion(self, board):
        for piece in board.pieces:
            piece_pos = board.get_piece_pos(piece)
            if piece.piece_type == "P" and (piece_pos[0] == 7 or piece_pos[0] == 0):
                return piece


    def promote(self, piece_to_promote, selected_piece, board):
        row, col = board.get_piece_pos(piece_to_promote)
        new_piece = create_piece(piece_to_promote.color, selected_piece, board.square_length, board.PNGS_enabled)
        board.pieces.remove(piece_to_promote)
        board.pieces.append(new_piece)
        board.positions[row][col] = new_piece

    def handle_promote_screen(self):
        queen_rect, rook_rect, bishop_rect, knight_rect = self.renderer.draw_promote_screen()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if queen_rect.collidepoint(event.pos):
                        return "Q"
                    elif rook_rect.collidepoint(event.pos):
                        return "R"
                    elif bishop_rect.collidepoint(event.pos):
                        return "B"
                    elif knight_rect.collidepoint(event.pos):
                        return "N"

    def check_special_rules(self, board):
        if board.halfmove == 150:
            print("Draw")
        elif board.halfmove == 100:
            print("Allow draw from either side.")

    