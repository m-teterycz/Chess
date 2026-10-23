import pygame

def create_piece(color, piece_type, position, square_length):
    piece_classes = {
        "Q": Queen,
        "K": King,
        "R": Rook,
        "B": Bishop,
        "N": Knight,
        "P": Pawn,
    }

    return piece_classes[piece_type](color, position, square_length, piece_type)

def screenpos_to_boardindex(screenpos, square_length):
    x,y = screenpos

    row = int((y - square_length // 2) // square_length)
    col = int((x - square_length // 2) // square_length)

    return row, col

def boardindex_to_screenpos(boardindex, square_length):
    return boardindex[0] * square_length + square_length // 2, boardindex[1] * square_length + square_length // 2

def check_valid_bounds(x, y, board, color):
    if y > 7 or y < 0 or x > 7 or x < 0 or board[y][x][0] == color:
        return False
    return True


def get_piece_at_index(position, board):
    screen_pos = boardindex_to_screenpos(position, board.square_length)
    for piece in board.pieces_group:
        if piece.rect.center == screen_pos:
            return piece


class Piece(pygame.sprite.Sprite):
    def __init__(self, color, position, square_length, piece_type):
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
        self.position = position
        self.color = color

        self.image = pygame.image.load(self.pngs[color + piece_type]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (square_length - 3, square_length - 3))

        self.rect = self.image.get_rect()
        self.rect.center = self.position
       
        self.row, self.col = screenpos_to_boardindex(self.rect.center, self.square_length)
        self.rect.center = position

    def move(self, board, square):
        self.row, self.col = screenpos_to_boardindex(self.position, self.square_length)
        self.new_row, self.new_col = screenpos_to_boardindex(square.rect.center, self.square_length)

        board.positions[self.row][self.col] = "."
        board.positions[self.new_row][self.new_col] = self.color + self.piece_type

        self.row = self.new_row
        self.col = self.new_col
       
        self.position = square.rect.center
        self.rect.center = square.rect.center

        self.moved = True

        return board.positions


class Pawn(Piece):
    def __init__(self, color, position, square_length, piece_type):
        super().__init__(color, position, square_length, piece_type)
        self.moved = False

        if self.color == "W":
            self.direction = -1
        else:
            self.direction = 1


    def get_moves(self, board):
        self.moves = []

        # FORWARD MOVES
        if board.positions[self.row + self.direction][self.col] == ".":
            self.moves.append((self.rect.center[0], self.rect.center[1] + self.square_length * self.direction))

        if board.positions[self.row + self.direction * 2][self.col] == "." and self.moved == False:
            self.moves.append((self.rect.center[0], self.rect.center[1] + self.square_length * self.direction * 2))         

        # CAPTURES
        if self.col != 7:
            if board.positions[self.row + self.direction][self.col + 1][0] != self.color and board.positions[self.row + self.direction][self.col + 1] != ".":
                self.moves.append((self.rect.center[0] + self.square_length, self.rect.center[1] + self.square_length * self.direction))

        if self.col != 0:
            if board.positions[self.row + self.direction][self.col - 1][0] != self.color and board.positions[self.row + self.direction][self.col - 1] != ".":
                self.moves.append((self.rect.center[0] - self.square_length, self.rect.center[1] + self.square_length * self.direction))

        return self.moves

    def move(self, board, square):
        return super().move(board, square)

class Knight(Piece):
    def __init__(self, color, position, square_length, piece_type):
        super().__init__(color, position, square_length, piece_type)

    def get_moves(self, board):
        self.moves = []
        directions = ((-2, -1), (-2,  1), (-1, -2), (-1,  2), ( 1, -2), ( 1,  2), ( 2, -1), ( 2,  1))

        for direction in directions:
            new_x = self.col + direction[0]
            new_y = self.row + direction[1]

            if not(check_valid_bounds(new_x, new_y, board.positions, self.color)):
                continue

            new_pos = boardindex_to_screenpos([new_x, new_y], self.square_length)
            
            self.moves.append(new_pos)

        return self.moves

    def move(self, board, square):
        return super().move(board, square)

class Bishop(Piece):
    def __init__(self, color, position, square_length, piece_type):
        super().__init__(color, position, square_length, piece_type)

    def get_moves(self, board):
        self.moves = []
        directions = [(1,1), (-1,1), (1,-1), (-1,-1)]
       
        for direction in directions:
            new_x = self.col
            new_y = self.row
            while True:
                new_x += direction[0]
                new_y += direction[1]
                if not(check_valid_bounds(new_x, new_y, board.positions, self.color)):
                    break

                elif board.positions[new_y][new_x] != ".":
                    self.moves.append(boardindex_to_screenpos((new_x, new_y), self.square_length))
                    break
               
                self.moves.append(boardindex_to_screenpos((new_x, new_y), self.square_length))
        return self.moves
   
    def move(self, board, square):
        return super().move(board, square)

class Rook(Piece):
    def __init__(self, color, position, square_length, piece_type):
        super().__init__(color, position, square_length, piece_type)
   
    def get_moves(self, board):
        self.moves = []
        directions = [(1,0), (0,1), (-1, 0), (0, -1)]
       
        for direction in directions:
            new_x = self.col
            new_y = self.row
            while True:
                new_x += direction[0]
                new_y += direction[1]

                if not(check_valid_bounds(new_x, new_y, board.positions, self.color)):
                    break

                elif board.positions[new_y][new_x] != ".":
                    self.moves.append(boardindex_to_screenpos((new_x, new_y), self.square_length))
                    break
               
                self.moves.append(boardindex_to_screenpos((new_x, new_y), self.square_length))
               
        return self.moves
   
    def move(self, board, square):
        return super().move(board, square)

class Queen(Rook, Bishop):
    def __init__(self, color, position, square_length, piece_type):
        super().__init__(color, position, square_length, piece_type)
   
    def get_moves(self, board): # Cannot use something like .extend since both classes return self.moves which override eachother.
        rook_moves = Rook.get_moves(self, board)
        bishop_moves = Bishop.get_moves(self, board)

        self.moves = rook_moves + bishop_moves
        return self.moves
           
    def move(self, board, square):
        return super().move(board, square)
   
   
class King(Piece):
    def __init__(self, color, position, square_length, piece_type):
        super().__init__(color, position, square_length, piece_type)

    def get_moves(self, board):
        self.moves = []
        directions = [(1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1), (0,1)]
        self.danger_squares = []

        for piece in board.pieces_group: # get all the enemy pieces to see which squares are dangerous
            if piece.color != self.color and piece.piece_type != "K":
                self.danger_squares.extend(piece.get_moves(board))
            elif piece.piece_type == "K" and piece.color != self.color:
                y,x = screenpos_to_boardindex(piece.rect.center, self.square_length)
                for direction in directions:
                    self.danger_squares.append(boardindex_to_screenpos((x + direction[0], y + direction[1]), self.square_length))
        
        for direction in directions:
            new_x = self.col + direction[0]
            new_y = self.row + direction[1]

            if not(check_valid_bounds(new_x, new_y, board.positions, self.color)) or boardindex_to_screenpos((new_x, new_y), self.square_length) in self.danger_squares:
                continue

            new_pos = boardindex_to_screenpos((new_x, new_y), self.square_length)

            self.moves.append((new_pos[0], new_pos[1]))

        return self.moves

    def move(self, board, square):
        return super().move(board, square)