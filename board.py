import pygame
from piece import *
import copy

class Board:
    def __init__(self, WIDTH, HEIGHT, screen, PNGS_enabled = True):
        self.coordinates = {}
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.screen = screen
        self.last_up2_pawn = None
        self.PNGS_enabled = PNGS_enabled
        self.square_length = min(WIDTH, HEIGHT) // 8
        self.FEN = None

        self.halfmove = 0
        self.fullmove = 1

    def char_to_col(self, char):
        return ord(char) - 97

    
    def create_board(self):
        self.squares = []
        self.pieces = []

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


    def setup_pieces(self, game, FEN = None):
        self.pieces = []
        self.positions = self.grid = [
            ["." for _ in range(8)]
            for _ in range(8)
        ]
        if FEN != None: # use a custom position with FEN format
            FEN = FEN.split(" ")
            self.FEN = FEN
            row = 0
            col = 0
            self.WKR = None
            self.WQR = None
            self.BKR = None
            self.BQR = None
            for char in FEN[0]: # get all pieces
                if char == "/":
                    col = 0
                    row += 1

                elif char.isnumeric():
                    col += int(char)

                elif char.islower(): # must be black
                    current_piece = create_piece("B", char.upper(), self.square_length, self.PNGS_enabled)
                    self.positions[row][col] = current_piece
                    self.pieces.append(current_piece)
                    if current_piece.piece_type == "R" and [row, col] == [0, 0]:
                        self.BQR = current_piece
                        current_piece.move_count = 1
                    elif current_piece.piece_type == "R" and [row, col] == [0, 7]:
                        self.BKR = current_piece
                        current_piece.move_count = 1
                    elif current_piece.piece_type == "P" and row != 1:
                        current_piece.move_count = 1

                    col += 1


                elif char.isupper(): # must be white
                    current_piece = create_piece("W", char.upper(), self.square_length, self.PNGS_enabled)
                    self.positions[row][col] = current_piece
                    self.pieces.append(current_piece)
                    if current_piece.piece_type == "R" and [row, col] == [7, 0]:
                        self.WQR = current_piece
                        current_piece.move_count = 1
                    elif current_piece.piece_type == "R" and [row, col] == [7, 7]:
                        self.WKR = current_piece
                        current_piece.move_count = 1   
                    elif current_piece.piece_type == "P" and row != 6:
                        current_piece.move_count = 1



                    col += 1

            game.turn = FEN[1].upper()

            for char in FEN[2]:
                if char == "K" and self.WKR != None:
                    self.WKR.move_count = 0
                elif char == "Q" and self.WQR != None:
                    self.WQR.move_count = 0
                elif char == "k" and self.BKR != None:
                    self.BKR.move_count = 0
                elif char == "q" and self.BQR != None:
                    self.BQR.move_count = 0

            en_passant_target = FEN[3]
            if en_passant_target != "-":
                row, col = 8 - int(en_passant_target[1]), self.char_to_col(en_passant_target[0])
                for piece in self.pieces:
                    if piece.piece_type == "P":
                        captures = piece.get_threats(self.get_piece_pos(piece))
                        direction = 1 if piece.color == "W" else -1
                        if [row, col] not in captures:
                            continue
                        self.last_up2_pawn = self.positions[row + direction][col]


            self.halfmove = int(FEN[4])
            self.fullmove = int(FEN[5])

            return None
        
        piece_format = "RNBQKBNR"
        for i,piece in enumerate(piece_format): # Generate the white side first
            current_piece = create_piece("W", piece, self.square_length, self.PNGS_enabled)
            current_pawn = create_piece("W", "P", self.square_length, self.PNGS_enabled)
            self.positions[6][i] = current_pawn
            self.positions[7][i] = current_piece
            self.pieces.append(current_piece)
            self.pieces.append(current_pawn)
        
        for i,piece in enumerate(piece_format): # Generate the black side
            current_piece = create_piece("B", piece, self.square_length, self.PNGS_enabled)
            current_pawn = create_piece("B", "P", self.square_length, self.PNGS_enabled)
            self.positions[1][i] = current_pawn
            self.positions[0][i] = current_piece
            self.pieces.append(current_piece)
            self.pieces.append(current_pawn)

        self.WKR = self.positions[7][7]
        self.WQR = self.positions[7][0]
        self.BKR = self.positions[0][7]
        self.BQR = self.positions[0][0]

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

            return True
        return False

    def check_check(self, turn):
        direction = -1 if turn == "W" else 1
        sliding_directions = [(1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1), (0,1)]
        knight_directions = [(-2, -1), (-2,  1), (-1, -2), (-1,  2), ( 1, -2), ( 1,  2), ( 2, -1), ( 2,  1)]

        for piece in self.pieces:
            if piece.color == turn and piece.piece_type == "K":
                king_pos = self.get_piece_pos(piece)
                break

        
        for i in range(-1,2, 2): # Check for pawn threats
            if not(check_valid_bounds(king_pos[0] + direction, king_pos[1] + i)):
                continue
            possible_enemy = self.positions[king_pos[0] + direction][king_pos[1] + i]
            if possible_enemy != "." and possible_enemy.color != turn and possible_enemy.piece_type == "P":
                return True
        
        for direction in knight_directions:
            new_col = king_pos[1]
            new_row = king_pos[0]

            new_col += direction[0]
            new_row += direction[1]
            if not(check_valid_bounds(new_col, new_row)):
                continue

            piece = self.positions[new_row][new_col]
            if piece != "." and piece.color != turn and piece.piece_type == "N":
                return True
        
        for direction in sliding_directions:
            iterations = 0
            diagonal = False
            new_col = king_pos[1]
            new_row = king_pos[0]
            if direction[0] != 0 and direction[1] != 0:
                diagonal = True
            while True:
                iterations += 1
                new_col += direction[0]
                new_row += direction[1]
                if not(check_valid_bounds(new_col, new_row)):
                    break

                piece = self.positions[new_row][new_col]
                if piece != "." and piece.piece_type == "K" and piece.color != turn and iterations == 1:
                    return True
                if diagonal:
                    if piece != "." and piece.color != turn and (piece.piece_type == "Q" or piece.piece_type == "B"):
                        return True
                    elif piece != ".":
                        break
                else:
                    if piece != "." and piece.color != turn and (piece.piece_type == "Q" or piece.piece_type == "R"):
                        return True
                    elif piece != ".":
                        break

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
            board_copy = copy.copy(self)
            board_copy.positions = self.copy_board_pos()
            board_copy.pieces = self.pieces.copy()

            for move in moves:
                move_record = board_copy.simulate_move(board_copy, piece, turn, move)
                if not(board_copy.check_check(turn)):
                    move = [move_record[0], move_record[1]]
                    legal_moves.append(move)
                board_copy.undo_simulated_move(board_copy, move_record)
                
            piece.moves = legal_moves

    def simulate_move(self, board_copy, piece, turn, move):
        piece_row, piece_col = self.get_piece_pos(piece)
        enemy_piece = None
        ep_piece = None
        is_en_passant = False
        is_castle = False
        original_last_up2_pawn = board_copy.last_up2_pawn

        board_copy.positions[piece_row][piece_col] = "."

        if board_copy.positions[move[0]][move[1]] != ".": # Capture
            enemy_piece = board_copy.positions[move[0]][move[1]]
            board_copy.pieces.remove(enemy_piece)
        board_copy.positions[move[0]][move[1]] = piece

        if piece.piece_type == "P": # check if the move was enpassant
            ep_piece = board_copy.positions[piece_row][move[1]]
            is_en_passant = board_copy.check_enpassant_remove([move[0], move[1]], piece)
            if abs(piece_row - move[0]) == 2: # moved up 2 squares
                board_copy.last_up2_pawn = piece
                piece.moved = True # GET RID OF MOVED AND INSTEAD RELY ON move_count EVERYWHERE FIX IN PIECE.py
            else:
                board_copy.last_up2_pawn = None
        else: # not enpassant
            board_copy.last_up2_pawn = None

        if piece.piece_type == "K": # check if the opponent castled
            if piece_col + 1 != move[1] and piece_col - 1 != move[1] and piece_col != move[1]: # Must be a castle since he moved farther than one square
                is_castle = True
                if move[1] == 6:
                    rook = board_copy.positions[piece_row][7]
                    board_copy.positions[piece_row][7] = "."
                    board_copy.positions[piece_row][5] = rook
                else:
                    rook = board_copy.positions[piece_row][0]
                    board_copy.positions[piece_row][0] = "."
                    board_copy.positions[piece_row][3] = rook
                rook.move_count = 1

        piece.move_count += 1
        move_record = (move[0], move[1], piece, piece_row, piece_col, ep_piece, is_en_passant, enemy_piece, is_castle, original_last_up2_pawn)
        return move_record


    def undo_simulated_move(self, board_copy, move_record):
        move1, move2, piece, piece_row, piece_col, ep_piece, is_en_passant, enemy_piece, is_castle, original_last_up2_pawn = move_record
        move = [move1, move2]
        direction = -1 if piece.color == "W" else 1

        board_copy.positions[move[0]][move[1]] = "."
        board_copy.positions[piece_row][piece_col] = piece
        if is_en_passant:
            board_copy.positions[move[0] - direction][move[1]] = ep_piece
            board_copy.pieces.append(ep_piece)
            board_copy.last_up2_pawn = ep_piece
        if is_castle:
            if move[1] == 6: # Right side
                rook = board_copy.positions[piece_row][5]
                board_copy.positions[piece_row][5] = "."
                board_copy.positions[piece_row][7] = rook
            elif move[1] == 2: # Left side
                rook = board_copy.positions[piece_row][3]
                board_copy.positions[piece_row][3] = "."
                board_copy.positions[piece_row][0] = rook
            board_copy.positions[piece_row][piece_col] = piece
            rook.move_count = 0
        if enemy_piece != None:
            board_copy.positions[move[0]][move[1]] = enemy_piece
            board_copy.pieces.append(enemy_piece)
        piece.move_count -= 1
        board_copy.last_up2_pawn = original_last_up2_pawn

    def make_move(self, selected_piece, possible_moves, clicked_square, piece_pos):
        row,col = clicked_square
        piece_row, piece_col = piece_pos

        if piece_row == None or piece_col == None:
            return False

        if [row, col] in possible_moves or [row, col] == possible_moves: # The player clicked a square which the piece can move to.
            if selected_piece.piece_type == "P": # Check if en passant happened
                if [row, col] in selected_piece.en_passant_moves:     
                    self.check_enpassant_remove([row, col], selected_piece)

            elif selected_piece.piece_type == "K" and [row, col] in selected_piece.get_castle(self):
                self.handle_castle(clicked_square, selected_piece.color)

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

    def handle_castle(self, move, turn):
        for piece in self.pieces:
            if piece.piece_type == "K" and piece.color == turn:
                king = piece

        row = 7 if turn == "W" else 0

        king_castle_moves = king.get_castle(self)
        if move == [row, 2] and move in king_castle_moves: # left side castle
            rook = self.positions[row][0]
            rook.move(self, [row, 3], [row, 0])

        elif move == [row, 6] and move in king_castle_moves:
            rook = self.positions[row][7]
            rook.move(self, [row, 5], [row, 7])

   
class Square:
    def __init__(self, x, y, w, color):
        self.x = x
        self.y = y
        self.w = w
        self.color = color
        self.highlighted_color = (130, 151, 105, 120)
        self.displayed_color = color
        self.rect = pygame.Rect(self.x, self.y, self.w, self.w)
