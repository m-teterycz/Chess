from board import Board
from piece import Piece
import pygame

class Renderer:
    def __init__(self, surface):
        self.surface = surface

    def draw(self, board):
        for square in board.squares:
            pygame.draw.rect(self.surface, square.color, (square.x, square.y, square.w, square.w))

        board.pieces_group.draw(self.surface)