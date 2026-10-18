import pygame

class Piece(pygame.sprite.Sprite):
    def __init__(self, piece_type, position):
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
       
        self.x = 0
        self.y = 0
        self.position = position

        self.piece_type = piece_type
        self.image = pygame.image.load(self.pngs[piece_type]).convert_alpha()
   
    def draw(self):
        screen.blit(self.image, (0,0))
       
class Board:
    def __init__(self):
        self.squares = None
   
    def create_board(self):
        self.squares = []
        self.coordinates = {}

        if WIDTH > HEIGHT:
            square_length = HEIGHT // 8
        else:
            square_length = WIDTH // 8

        DARK_SQUARE_COLOR = (0, 0, 0)
        WHITE_SQUARE_COLOR = (255, 255, 255)
        current_color = None

        for i in range(8):
            for j in range(8):
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0):
                    current_color = WHITE_SQUARE_COLOR
                else:
                    current_color = DARK_SQUARE_COLOR
                self.squares.append(Square(square_length * j, square_length * i, square_length, current_color))
                self.coordinates[f"{chr(65 + j)}{i + 1}"] = ((square_length * j) + square_length // 2, (HEIGHT - (square_length * i))  - square_length // 2)

   
    def draw_board(self):
        for square in self.squares:
            square.draw()

    def setup_pieces(self):
        self.pieces = []

        pieces = [["RNBQKBNR"], ["P" * 8]] # From the black perspective.

        for piece in pieces:
            pass

        
        

   
class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, w, color):
        self.x = x
        self.y = y
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, w, w)
   
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
       
   


WIDTH = 1280
HEIGHT = 720

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
clock.tick(60)

Board1 = Board()
Board1.create_board()
Board1.setup_pieces()

pieces = pygame.sprite.Group()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
   
    screen.fill((100, 100, 100))
    Board1.draw_board()
    pygame.display.flip()
   
pygame.quit()