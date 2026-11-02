import pygame, math
from piece import create_piece, check_valid_bounds

class Game:
    def __init__(self, screen, WIDTH, HEIGHT, engine_enabled, renderer):
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.screen = screen
        self.turn = "W"
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.engine_enabled = engine_enabled
        self.selected_piece = None
        self.renderer = renderer

    def reset_square_colors(self, board):
        for i in range(len(board.squares)):
            for j in range(len(board.squares)):
                board.squares[i][j].displayed_color = board.squares[i][j].color   

    def get_clicked_piece(self, mouse_pos, board):
        self.col = math.floor(mouse_pos[0] / board.square_length)
        self.row = math.floor(mouse_pos[1] / board.square_length)
        if not(check_valid_bounds(self.col, self.row)):
            return None
        square = board.squares[self.row][self.col]

        if board.positions[self.row][self.col] != "." and board.positions[self.row][self.col].color == self.turn:
            self.selected_piece = board.positions[self.row][self.col]
            self.piece_row, self.piece_col = self.row, self.col

            self.possible_moves = self.selected_piece.get_moves(board, [self.row, self.col])
            board.get_legal_moves(self.turn, self.selected_piece)
            self.possible_moves = self.selected_piece.moves
            self.reset_square_colors(board)
            for move in self.possible_moves:
                square = board.squares[move[0]][move[1]]
                square.displayed_color = square.highlighted_color
                    
        else:
            self.reset_square_colors(board)

    def make_move(self, board):
        piece_count = len(board.pieces)
        if self.selected_piece == None:
            return None
        if board.make_move(self.selected_piece, self.possible_moves, [self.row, self.col], [self.piece_row, self.piece_col]):
            self.possible_moves = []
            self.reset_square_colors(board)
            self.turn = "B" if self.turn == "W" else "W"

            if self.selected_piece.piece_type == "P":
                board.halfmove = 0
            elif piece_count != len(board.pieces):
                board.halfmove = 0
            else:
                board.halfmove += 1
            board.fullmove += 1
            return True

    def make_engine_move(self, piece, move, board):
        piece_count = len(board.pieces)
        board.make_move(piece, move, move, board.get_piece_pos(piece))
        if piece.piece_type == "P":
            board.halfmove = 0
        elif piece_count != len(board.pieces):
            board.halfmove = 0
        else:
            board.halfmove += 1
        self.turn = "B" if self.turn == "W" else "W"
        board.fullmove += 1


    def check_and_display_gameend(self, board):
            if board.check_checkmate(self.turn):
                won = "Black" if self.turn == "W" else "White"
                text_surface = self.my_font.render(f'Checkmate: {won} wins!', True, (0, 0, 0))
                rect = text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
                self.screen.blit(text_surface, rect)
            elif board.check_stalemate(self.turn):
                text_surface = self.my_font.render(f'Stalemate', True, (0, 0, 0))
                rect = text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
                self.screen.blit(text_surface, rect)

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

    