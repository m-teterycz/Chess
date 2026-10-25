import pygame
from piece import *
import copy

class Board:
    def __init__(self, WIDTH, HEIGHT, screen):
        self.coordinates = {}
        self.positions = self.grid = [
            ["." for _ in range(8)]
            for _ in range(8)
        ]
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.screen = screen
        self.last_up2_pawn = None
   
    def create_board(self):
        self.squares = []
        self.pieces = []
       
        if self.WIDTH > self.HEIGHT:
            self.square_length = self.HEIGHT // 8
        else:
            self.square_length = self.WIDTH // 8

        DARK_SQUARE_COLOR = (181, 136, 99)
        WHITE_SQUARE_COLOR = (240, 217, 181)
        current_color = None

        for i in range(8):
            temp = []
            for j in range(8):
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0):
                    current_color = WHITE_SQUARE_COLOR
                else:
                    current_color = DARK_SQUARE_COLOR
                temp.append(Square(self.square_length * j, self.square_length * i, self.square_length, current_color))
            self.squares.append(temp)


    def setup_pieces(self):
        piece_format = "RNBQKBNR"
        for i,piece in enumerate(piece_format): # Generate the white side first
            current_piece = create_piece("W", piece, self.square_length)
            current_pawn = create_piece("W", "P", self.square_length)
            self.positions[6][i] = current_pawn
            self.positions[7][i] = current_piece
            self.pieces.append(current_piece)
            self.pieces.append(current_pawn)
        
        for i,piece in enumerate(piece_format): # Generate the black side
            current_piece = create_piece("B", piece, self.square_length)
            current_pawn = create_piece("B", "P", self.square_length)
            self.positions[1][i] = current_pawn
            self.positions[0][i] = current_piece
            self.pieces.append(current_piece)
            self.pieces.append(current_pawn)
        


    def get_piece_pos(self, piece):
        for row in range(len(self.positions)):
            for col in range(len(self.positions)):
                if self.positions[row][col] == piece:
                    return [row, col]

    def check_enpassant_remove(self, new_pos, piece):
        if piece.color == "W":
            direction = 1
        else:
            direction = -1
    
        if piece.piece_type == "P" and new_pos in piece.en_passant_moves:
            captured_piece = self.positions[new_pos[0] + direction][new_pos[1]]
            self.pieces.remove(captured_piece)
            self.positions[new_pos[0] + direction][new_pos[1]] = "."

    def check_check(self, turn):
        for piece in self.pieces:
            if piece.color == turn and piece.piece_type == "K":
                king = piece

        king_pos = self.get_piece_pos(king)
        danger_squares = king.get_threats(self, king_pos)
        if king_pos in danger_squares:
            return True
        return False

    def copy_board_pos(self):
        copy_pos = []
        for row in self.positions:
            copy_pos.append(row.copy())
        return copy_pos

    def get_legal_moves(self, turn, piece):
        if piece.color == turn:
            legal_moves = []
            piece_row, piece_col = self.get_piece_pos(piece)
            moves = piece.get_moves(self, [piece_row, piece_col])

            for move in moves:
                board_copy = copy.copy(self)
                board_copy.positions = self.copy_board_pos()
                board_copy.pieces = self.pieces.copy()

                board_copy.positions[piece_row][piece_col] = "."

                if board_copy.positions[move[0]][move[1]] != ".":
                    enemy_piece = board_copy.positions[move[0]][move[1]]
                    board_copy.pieces.remove(enemy_piece)
                board_copy.positions[move[0]][move[1]] = piece
                if piece.piece_type == "P":
                    board_copy.check_enpassant_remove([move[0], move[1]], piece)

                if board_copy.check_check(turn):
                    pass
                else:
                    legal_moves.append([move[0], move[1]])
            piece.moves = legal_moves

    def make_move(self, selected_piece, possible_moves, clicked_square, piece_pos):
        row,col = clicked_square
        piece_row, piece_col = piece_pos

        if piece_row == None or piece_col == None:
            return False

        if [row, col] in possible_moves: # The player clicked a square which the piece can move to.
            if selected_piece.piece_type == "P": # Check if en passant happened
                if [row, col] in selected_piece.en_passant_moves:     
                    self.check_enpassant_remove([row, col], selected_piece)

            self.positions = selected_piece.move(self, [row, col], [piece_row, piece_col])

            if selected_piece.piece_type == "P" and abs(row - piece_row) == 2:
                self.last_up2_pawn = selected_piece
            else:
                self.last_up2_pawn = None

            return True

    def check_checkmate(self, turn):
        if self.check_check(turn) != True:
            return False
        for piece in self.pieces:
            if piece.color == turn:
                self.get_legal_moves(turn, piece)
                if len(piece.moves) != 0:
                    return False
        return True

    def check_stalemate(self, turn):
        for piece in self.pieces:
            if piece.color == turn:
                self.get_legal_moves(turn, piece)
                if len(piece.moves) != 0:
                    return False
        return True


   
class Square:
    def __init__(self, x, y, w, color):
        self.x = x
        self.y = y
        self.w = w
        self.color = color
        self.highlighted_color = (50, 50, 50)
        self.displayed_color = color
        self.rect = pygame.Rect(self.x, self.y, self.w, self.w)
