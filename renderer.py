import pygame, math


def boardindex_to_screenpos(boardindex, square_length):  # Col and Row swapped since in list terms it is (y,x) but screen is (x,y)
    return boardindex[1] * square_length, boardindex[0] * square_length

class Renderer:
    def __init__(self, surface, WIDTH, HEIGHT):
        self.surface = surface
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.square_length = min(WIDTH, HEIGHT) // 8
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)

    def draw(self, board):
        for row in board.squares:
            for square in row:
                pygame.draw.rect(self.surface, square.displayed_color, (square.x, square.y, square.w, square.w))

        for row in range(len(board.positions)):
            for col in range(len(board.positions)):
                if board.positions[row][col] != ".":
                    piece = board.positions[row][col]
                    self.surface.blit(piece.image, boardindex_to_screenpos([row, col], self.square_length))

    def draw_promote_screen(self):
        smallest_dimension = min(self.WIDTH, self.HEIGHT)
        background = pygame.Rect(0, 0, 400, 400)
        queen_text = self.my_font.render("QUEEN", True, (255, 255, 255))
        rook_text = self.my_font.render("ROOK", True, (255, 255, 255))
        bishop_text = self.my_font.render("BISHOP", True, (255, 255, 255))
        knight_text = self.my_font.render("KNIGHT", True, (255, 255, 255))

        background.center = (smallest_dimension // 2, smallest_dimension // 2)
        queen_rect = queen_text.get_rect(center=(smallest_dimension//2, smallest_dimension//2 - 50))
        rook_rect = rook_text.get_rect(center=(smallest_dimension//2, smallest_dimension//2))
        bishop_rect = bishop_text.get_rect(center=(smallest_dimension//2, smallest_dimension//2 + 50))
        knight_rect = knight_text.get_rect(center=(smallest_dimension//2, smallest_dimension//2 + 100))

        pygame.draw.rect(self.surface, (0, 0, 0), background)
        self.surface.blit(queen_text, queen_rect)
        self.surface.blit(rook_text, rook_rect)
        self.surface.blit(bishop_text, bishop_rect)
        self.surface.blit(knight_text, knight_rect)

        pygame.display.flip()
        return queen_rect, rook_rect, bishop_rect, knight_rect

    def draw_eval_bar(self, evaluation):
        upper_bar = pygame.Rect(0, 0, self.WIDTH - self.HEIGHT, self.HEIGHT)
        lower_bar = pygame.Rect(0, 0, self.WIDTH - self.HEIGHT, self.HEIGHT // 2)
        eval_font = pygame.font.SysFont('Comic Sans MS', 25)

        if evaluation > 0:
            color = (0, 0, 0)
            center = (self.WIDTH - upper_bar.width // 2, self.HEIGHT - 100)
        else:
            color = (255, 255, 255)
            center = (self.WIDTH - upper_bar.width // 2, 100)

        advantage_text = eval_font.render(f"{round(evaluation.item(), 1)}", True, color)
        advantage_rect = advantage_text.get_rect(center = center)

        upper_bar.topright = (self.WIDTH, 0)
        lower_bar.bottomright = (self.WIDTH, self.HEIGHT)

        lower_bottom = lower_bar.bottom
        lower_width = lower_bar.width

        lower_bar.height = self.HEIGHT * (0.5 + (math.atan(evaluation / 3)) / math.pi)

        lower_bar.bottom = lower_bottom
        lower_bar.width = lower_width

        pygame.draw.rect(self.surface, (0, 0, 0), upper_bar)
        pygame.draw.rect(self.surface, (255, 255, 255), lower_bar)
        self.surface.blit(advantage_text, advantage_rect)