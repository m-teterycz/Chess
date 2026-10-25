import pygame


def boardindex_to_screenpos(boardindex, square_length):  # Col and Row swapped since in list terms it is (y,x) but screen is (x,y)
    return boardindex[1] * square_length, boardindex[0] * square_length

class Renderer:
    def __init__(self, surface, square_length):
        self.surface = surface
        self.square_length = square_length

    def draw(self, board):
        for row in board.squares:
            for square in row:
                pygame.draw.rect(self.surface, square.displayed_color, (square.x, square.y, square.w, square.w))

        for row in range(len(board.positions)):
            for col in range(len(board.positions)):
                if board.positions[row][col] != ".":
                    piece = board.positions[row][col]
                    self.surface.blit(piece.image, boardindex_to_screenpos([row, col], self.square_length))