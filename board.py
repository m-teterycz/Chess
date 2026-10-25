import pygame
from piece import *

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
        piece_format_W = "RNBQKBNR"
        piece_format_B = "RNBKQBNR"

        for i,piece in enumerate(piece_format_W): # Generate the white side first
            current_piece = create_piece("W", piece, self.square_length)
            current_pawn = create_piece("W", "P", self.square_length)
            self.positions[6][i] = current_pawn
            self.positions[7][i] = current_piece
            self.pieces.append(current_piece)
            self.pieces.append(current_pawn)
       
        for i,piece in enumerate(piece_format_B): # Generate the black side
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

    def check_enpassant(self, new_pos, piece):
        if piece.color == "W":
            direction = 1
        else:
            direction = -1
    
        self.row, self.col = self.get_piece_pos(piece)
        if abs(new_pos[0] - self.row) == 1 and abs(new_pos[1] - self.col) == 1 and piece.piece_type == "P": # Must be en_passant
            self.positions[new_pos[0] + direction][new_pos[1]] = "."


   
class Square:
    def __init__(self, x, y, w, color):
        self.x = x
        self.y = y
        self.w = w
        self.color = color
        self.highlighted_color = (50, 50, 50)
        self.displayed_color = color
        self.rect = pygame.Rect(self.x, self.y, self.w, self.w)
