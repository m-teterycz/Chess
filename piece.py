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
       
        self.square_length = square_length
        self.position = position
        self.color = color

        self.image = pygame.image.load(self.pngs[color + piece_type]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (square_length - 3, square_length - 3))

        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def move(self, board, square):
        self.row, self.col = screenpos_to_boardindex(self.position, self.square_length)
        self.new_row, self.new_col = screenpos_to_boardindex(square.rect.center, self.square_length)

        board[self.row][self.col] = "."
        board[self.new_row][self.new_col] = self.color + "P"

        self.row = self.new_row
        self.col = self.new_col
        
        self.position = square.rect.center
        self.rect.center = square.rect.center

        self.moved = True

        return board


class Pawn(Piece):
    def __init__(self, color, position, square_length, piece_type):
        super().__init__(color, position, square_length, piece_type)
        self.row, self.col = screenpos_to_boardindex(self.rect.center, self.square_length)
        self.moved = False
        self.rect.center = position

        if self.color == "W":
            self.direction = -1
        else:
            self.direction = 1


    def get_moves(self, board):
        self.moves = []

        # FORWARD MOVES
        if board[self.row + self.direction][self.col] == ".":
            self.moves.append((self.rect.center[0], self.rect.center[1] + self.square_length * self.direction))

        if board[self.row + self.direction * 2][self.col] == "." and self.moved == False:
            self.moves.append((self.rect.center[0], self.rect.center[1] + self.square_length * self.direction * 2))

        # CAPTURES
        if self.col != 7:
            if board[self.row + self.direction][self.col + 1][0] != self.color and board[self.row + self.direction][self.col + 1] != ".":
                self.moves.append((self.rect.center[0] + self.square_length, self.rect.center[1] + self.square_length * self.direction))

        if self.col != 0:
            if board[self.row + self.direction][self.col - 1][0] != self.color and board[self.row + self.direction][self.col - 1] != ".":
                self.moves.append((self.rect.center[0] - self.square_length, self.rect.center[1] + self.square_length * self.direction))

        return self.moves

    def move(self, board, square):
        return super().move(board, square)

class Knight(Piece):
    def __init__(self, color, position, square_length, piece_type):
        super().__init__(color, position, square_length, piece_type)
        self.row, self.col = screenpos_to_boardindex(self.rect.center, self.square_length)
        self.moved = False
        self.rect.center = position

        if self.color == "W":
            self.direction = -1
        else:
            self.direction = 1

    def get_moves(self, board):
        self.moves = []
        self.moves.append((50, 50))

        return self.moves

    def move(self, board, square):
            return super().move(board, square)

class Bishop(Piece):
    def __init__(self, color, position, square_length, piece_type):
        super().__init__(color, position, square_length, piece_type)

class Rook(Piece):
    def __init__(self, color, position, square_length, piece_type):
        super().__init__(color, position, square_length, piece_type)

class Queen(Piece):
    def __init__(self, color, position, square_length, piece_type):
        super().__init__(color, position, square_length, piece_type)

class King(Piece):
    def __init__(self, color, position, square_length, piece_type):
        super().__init__(color, position, square_length, piece_type)