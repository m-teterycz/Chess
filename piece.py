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

def screenpos_to_boardindex(screenpos, square_length):
    x,y = screenpos

    row = int((y - square_length // 2) // square_length)
    col = int((x - square_length // 2) // square_length)

    return row, col

def boardindex_to_screenpos(boardindex, square_length):
    return boardindex[0] * square_length, boardindex[1] * square_length

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


    def get_moves(self, board, board_pos):
        self.moves = []
        direction = -1 if self.color == "W" else 1


        # FORWARD MOVES
        if board.positions[board_pos[0] + direction][board_pos[1]] == ".": # Forward moves
            self.moves.append([board_pos[0] + direction, board_pos[1]])
            if board.positions[board_pos[0] + direction * 2][board_pos[1]] == "." and self.moved == False:
                self.moves.append([board_pos[0] + direction * 2, board_pos[1]])

        for i in range(-1,2, 2): # Diagonal Captures
            new_row = board_pos[0]
            new_col = board_pos[1]

            if not(check_valid_bounds(new_col, new_row)):
                continue

            current_square = board.positions[new_row + direction][new_col + i]
            if current_square != ".":
                if current_square.color != self.color:
                    self.moves.append([new_row + direction, new_col + i])

        if board_pos[0] == 3 and self.color == "W":
            if board.positions[board_pos[0]][board_pos[1] + 1] != ".":
                piece = board.positions[board_pos[0]][board_pos[1] + 1]
                if piece.color != self.color and piece.piece_type == "P" and piece.move_count == 1:
                    self.moves.append([board_pos[0] - 1, board_pos[1] + 1])

        return self.moves

    def move(self, board, target_pos, board_pos):
        return super().move(board, target_pos, board_pos)

class Knight(Piece):
    def __init__(self, color, square_length, piece_type):
        super().__init__(color, square_length, piece_type)

    def get_moves(self, board, board_pos):
        self.moves = []
        directions = ((-2, -1), (-2,  1), (-1, -2), (-1,  2), ( 1, -2), ( 1,  2), ( 2, -1), ( 2,  1))

        for direction in directions:
            new_col = board_pos[1] + direction[1]
            new_row = board_pos[0] + direction[0]

            if not(check_valid_bounds(new_col, new_row)):
                continue

            new_pos = [new_row, new_col]
            
            self.moves.append(new_pos)

        return self.moves

    def move(self, board, target_pos, board_pos):
        return super().move(board, target_pos, board_pos)

class Bishop(Piece):
    def __init__(self, color, square_length, piece_type):
        super().__init__(color, square_length, piece_type)

    def get_moves(self, board, board_pos):
        self.moves = []
        directions = [(1,1), (-1,1), (1,-1), (-1,-1)]
       
        for direction in directions:
            new_col = board_pos[1]
            new_row = board_pos[0]
            while True:
                new_col += direction[0]
                new_row += direction[1]
                if not(check_valid_bounds(new_col, new_row)):
                    break


                result = check_collide(board.positions, [new_row, new_col], self.color) == "Friendly"
                if result == "Friendly":
                    break
                elif result == "Enemy":
                    self.moves.append([new_row, new_col])
                    break

                    
               
                self.moves.append([new_row, new_col])
        return self.moves
   
    def move(self, board, square):
        return super().move(board, square)

class Rook(Piece):
    def __init__(self, color, square_length, piece_type):
        super().__init__(color, square_length, piece_type)
   
    def get_moves(self, board):
        self.moves = []
        directions = [(1,0), (0,1), (-1, 0), (0, -1)]
       
        for direction in directions:
            new_col = self.col
            new_row = self.row
            while True:
                new_col += direction[1]
                new_row += direction[0]

                if not(check_valid_bounds(new_col, new_row, board.positions, self.color)):
                    break

                elif board.positions[new_row][new_col] != ".":
                    self.moves.append(boardindex_to_screenpos((new_x, new_y), self.square_length))
                    break
               
                self.moves.append(boardindex_to_screenpos((new_x, new_y), self.square_length))
               
        return self.moves
   
    def move(self, board, square):
        return super().move(board, square)

class Queen(Rook, Bishop):
    def __init__(self, color, square_length, piece_type):
        super().__init__(color, square_length, piece_type)
   
    def get_moves(self, board): # Cannot use something like .extend since both classes return self.moves which override eachother.
        rook_moves = Rook.get_moves(self, board)
        bishop_moves = Bishop.get_moves(self, board)

        self.moves = rook_moves + bishop_moves
        return self.moves
           
    def move(self, board, square):
        return super().move(board, square)
   
   
class King(Piece):
    def __init__(self, color, square_length, piece_type):
        super().__init__(color, square_length, piece_type)

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