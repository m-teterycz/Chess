import pygame

def create_piece(color, piece_type, square_length):
    piece_classes = {
        "Q": Queen,
        "K": King,
        "R": Rook,
        "B": Bishop,
        "N": Knight,
        "P": Pawn,
    }

    return piece_classes[piece_type](color, square_length, piece_type)

def check_valid_bounds(x, y):
    if y > 7 or y < 0 or x > 7 or x < 0:
        return False
    return True


def check_collide(board, position, color):
    row = position[0]
    col = position[1]
    if board[row][col] != ".":
        if board[row][col].color == color:
            return "Friendly"
        else:
            return "Enemy"
    return None


class Piece:
    def __init__(self, color, square_length, piece_type):
        super().__init__()

        self.pngs = {"BP":"assets/BP.png",
            "BR":"assets/BR.png",
            "BB":"assets/BB.png",
            "BN":"assets/BN.png",
            "BK":"assets/BK.png",
            "BQ":"assets/BQ.png",
            "WP":"assets/WP.png",
            "WR":"assets/WR.png",
            "WB":"assets/WB.png",
            "WN":"assets/WN.png",
            "WK":"assets/WK.png",
            "WQ":"assets/WQ.png",}

        self.piece_type = piece_type
        self.square_length = square_length
        self.color = color
        self.move_count = 0

        self.image = pygame.image.load(self.pngs[color + piece_type]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (square_length - 3, square_length - 3))

        self.rect = self.image.get_rect()

    def move(self, board, target_pos, piece_pos):
        self.row, self.col = piece_pos[0], piece_pos[1]
        self.t_row, self.t_col = target_pos[0], target_pos[1]

        if board.positions[self.t_row][self.t_col] != ".":
            board.pieces.remove(board.positions[self.t_row][self.t_col])

        piece = board.positions[self.row][self.col]
        board.positions[self.row][self.col] = "."
        board.positions[self.t_row][self.t_col] = piece

        self.moved = True
        self.move_count += 1

        return board.positions


class Pawn(Piece):
    def __init__(self, color, square_length, piece_type):
        super().__init__(color, square_length, piece_type)
        self.moved = False
        self.direction = -1 if self.color == "W" else 1
        self.en_passant_moves = []

    def get_en_passant_moves(self, board, board_pos, direction):
        self.en_passant_moves = []
        for i in range(-1, 2, 2):
            if not(check_valid_bounds(board_pos[1] + i, board_pos[0])):
                continue            
            if board.positions[board_pos[0]][board_pos[1] + i] != ".":
                piece = board.positions[board_pos[0]][board_pos[1] + i]
                if piece.color != self.color and piece.piece_type == "P" and piece == board.last_up2_pawn:
                    self.en_passant_moves.append([board_pos[0] + direction, board_pos[1] + i])     
        self.moves.extend(self.en_passant_moves)

    def get_captures(self, board, board_pos):
        captures = []
        for i in range(-1,2, 2): # Diagonal Captures
            new_row = board_pos[0] + self.direction
            new_col = board_pos[1] + i

            if not(check_valid_bounds(new_col, new_row)):
                continue

            current_square = board.positions[new_row][new_col]
            if current_square != ".":
                if current_square.color != self.color:
                    captures.append([new_row, new_col])
        return captures

    def get_threats(self, board_pos):
        captures = []
        for i in range(-1,2, 2): # Diagonal Captures
            new_row = board_pos[0] + self.direction
            new_col = board_pos[1] + i

            if not(check_valid_bounds(new_col, new_row)):
                continue

            captures.append([new_row, new_col])
        return captures    

    def get_forward_moves(self, board, board_pos):
        forward_moves = []
        if board.positions[board_pos[0] + self.direction][board_pos[1]] == ".": # Forward moves
            forward_moves.append([board_pos[0] + self.direction, board_pos[1]])
            if board.positions[board_pos[0] + self.direction * 2][board_pos[1]] == "." and self.moved == False:
                forward_moves.append([board_pos[0] + self.direction * 2, board_pos[1]])

        return forward_moves

    def get_moves(self, board, board_pos):
        self.moves = []
        self.en_passant_moves = []


        # FORWARD MOVES
        self.moves.extend(self.get_forward_moves(board, board_pos))


        captures = self.get_captures(board, board_pos)
        if len(captures) != 0:
            self.moves.extend(captures)


        if board_pos[0] == 3 and self.color == "W":
            self.get_en_passant_moves(board, board_pos, self.direction)

        elif board_pos[0] == 4 and self.color == "B":
            self.get_en_passant_moves(board, board_pos, self.direction)



        return self.moves

    def move(self, board, target_pos, board_pos):
        return super().move(board, target_pos, board_pos)

class Knight(Piece):
    def __init__(self, color, square_length, piece_type):
        super().__init__(color, square_length, piece_type)

    def get_moves(self, board, board_pos):
        self.moves = []
        self.threats = []
        directions = ((-2, -1), (-2,  1), (-1, -2), (-1,  2), ( 1, -2), ( 1,  2), ( 2, -1), ( 2,  1))

        for direction in directions:
            new_col = board_pos[1] + direction[1]
            new_row = board_pos[0] + direction[0]
            new_pos = [new_row, new_col]

            if not(check_valid_bounds(new_col, new_row)):
                continue

            self.threats.append(new_pos)

            if check_collide(board.positions, [new_row, new_col], self.color) == "Friendly":
                continue

            self.moves.append(new_pos)

        return self.moves

    def move(self, board, target_pos, board_pos):
        return super().move(board, target_pos, board_pos)

class Bishop(Piece):
    def __init__(self, color, square_length, piece_type):
        super().__init__(color, square_length, piece_type)

    def get_moves(self, board, board_pos):
        self.moves = []
        self.threats = []
        directions = [(1,1), (-1,1), (1,-1), (-1,-1)]
       
        for direction in directions:
            new_col = board_pos[1]
            new_row = board_pos[0]
            while True:
                new_col += direction[0]
                new_row += direction[1]
                if not(check_valid_bounds(new_col, new_row)):
                    break

                self.threats.append([new_row, new_col])
                result = check_collide(board.positions, [new_row, new_col], self.color)
                if result == "Friendly":
                    break
                elif result == "Enemy":
                    self.moves.append([new_row, new_col])
                    break

                self.moves.append([new_row, new_col])
        return self.moves
   
    def move(self, board, target_pos, board_pos):
        return super().move(board, target_pos, board_pos)

class Rook(Piece):
    def __init__(self, color, square_length, piece_type):
        super().__init__(color, square_length, piece_type)
   
    def get_moves(self, board, board_pos):
        self.moves = []
        self.threats = []
        directions = [(1,0), (0,1), (-1, 0), (0, -1)]
       
        for direction in directions:
            new_col = board_pos[1]
            new_row = board_pos[0]
            while True:
                new_col += direction[1]
                new_row += direction[0]

                if not(check_valid_bounds(new_col, new_row)):
                    break

                self.threats.append([new_row, new_col])
                result = check_collide(board.positions, [new_row, new_col], self.color)
                if result == "Friendly":
                    break
                elif result == "Enemy":
                    self.moves.append([new_row, new_col])
                    break
               
                self.moves.append([new_row, new_col])
               
        return self.moves
   
    def move(self, board, target_pos, board_pos):
        return super().move(board, target_pos, board_pos)

class Queen(Rook, Bishop):
    def __init__(self, color, square_length, piece_type):
        super().__init__(color, square_length, piece_type)
   
    def get_moves(self, board, board_pos): # Cannot use something like .extend since both classes return self.moves which override eachother.
        rook_moves = Rook.get_moves(self, board, board_pos)
        rook_threats = self.threats.copy()

        bishop_moves = Bishop.get_moves(self, board, board_pos)
        bishop_threats = self.threats.copy()

        self.threats = rook_threats + bishop_threats
        self.moves = rook_moves + bishop_moves
        return self.moves
           
    def move(self, board, target_pos, board_pos):
        return super().move(board, target_pos, board_pos)
   
   
class King(Piece):
    def __init__(self, color, square_length, piece_type):
        super().__init__(color, square_length, piece_type)

    def get_threats(self, board, board_pos):
        directions = [(1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1), (0,1)]
        danger_squares = []

        for piece in board.pieces: # get all the enemy pieces to see which squares are dangerous
            piece_pos = board.get_piece_pos(piece)
            if piece.color != self.color and piece.piece_type != "K" and piece.piece_type != "P":
                danger_squares.extend(piece.get_moves(board, piece_pos))
                danger_squares.extend(piece.threats) 
            elif piece.piece_type == "K" and piece.color != self.color:
                for direction in directions:
                    danger_squares.append([piece_pos[0] + direction[0], piece_pos[1] + direction[1]])
            elif piece.piece_type == "P" and piece.color != self.color:
                danger_squares.extend(piece.get_threats(piece_pos))

        return danger_squares

    def get_moves(self, board, board_pos):
        self.moves = []
        directions = [(1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1), (0,1)]
        row, col = board_pos[0], board_pos[1]

        self.danger_squares = self.get_threats(board, board_pos)
        
        for direction in directions:
            new_col = col + direction[1]
            new_row = row + direction[0]

            if not(check_valid_bounds(new_col, new_row)) or [new_row, new_col] in self.danger_squares:
                continue

            result = check_collide(board.positions, [new_row, new_col], self.color)
            if result == "Enemy":
                pass
            elif result == "Friendly":
                continue
            
            self.moves.append([new_row, new_col])

        return self.moves

    def move(self, board, target_pos, board_pos):
        return super().move(board, target_pos, board_pos)