import pygame, math


def boardindex_to_screenpos(boardindex, square_length):  # Col and Row swapped since in list terms it is (y,x) but screen is (x,y)
    return boardindex[1] * square_length + square_length // 2, boardindex[0] * square_length + square_length // 2

class Renderer:
    def __init__(self, surface, WIDTH, HEIGHT):
        self.DARK_SQUARE_COLOR = (181, 136, 99)
        self.WHITE_SQUARE_COLOR = (240, 217, 181)

        self.surface = surface
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.square_length = min(WIDTH, HEIGHT) // 8
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.squares = []

        for i in range(8): # Create all squares
            for j in range(8):
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0):
                    current_color = self.WHITE_SQUARE_COLOR
                else:
                    current_color = self.DARK_SQUARE_COLOR
                self.squares.append(Square(self.square_length * j, self.square_length * i, self.square_length, current_color))

            self.pngs = {"p":"assets/BP.png",
                "r":"assets/BR.png",
                "b":"assets/BB.png",
                "n":"assets/BN.png",
                "k":"assets/BK.png",
                "q":"assets/BQ.png",
                "P":"assets/WP.png",
                "R":"assets/WR.png",
                "B":"assets/WB.png",
                "N":"assets/WN.png",
                "K":"assets/WK.png",
                "Q":"assets/WQ.png",}
    
    def create_image(self, piece_letter):
        image = pygame.image.load(self.pngs[piece_letter]).convert_alpha()
        image = pygame.transform.scale(image, (self.square_length - 3, self.square_length - 3))
    
        rect = image.get_rect()
        return rect, image
    

    def draw_squares(self):
        for square in self.squares:
            pygame.draw.rect(self.surface, square.displayed_color, (square.x, square.y, square.w, square.w))

    def draw(self, board):
        self.draw_squares()
        for i in range(0, 128, 16):
            for j in range(8):
                piece = board.squares[i + j]
                if piece != ".":
                    screen_pos = boardindex_to_screenpos([i // 16, j], self.square_length)
                    imagerect, image = self.create_image(piece)
                    imagerect.center = screen_pos
                    self.surface.blit(image, imagerect)

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



class Square:
    def __init__(self, x, y, w, color):
        self.x = x
        self.y = y
        self.w = w
        self.color = color
        self.highlighted_color = (130, 151, 105, 120)
        self.displayed_color = color
        self.rect = pygame.Rect(self.x, self.y, self.w, self.w)