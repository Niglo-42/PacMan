import pygame
from .convert import Convert
from .maze import Maze
from pygame.locals import K_ESCAPE, KEYDOWN, K_SPACE, K_UP, K_DOWN, K_LEFT, K_RIGHT

class Game:
    def __init__(self, args):
        pygame.display.init()
        info = pygame.display.Info()
        self.screen = pygame.display.set_mode((info.current_w, info.current_h))
        self.maze = Convert.trad(Maze(width=args.width, height=args.height, seed=args.seed))
        self.w  = len(self.maze[0])
        self.h = len(self.maze)
        self.tile_size = 8
        width, height = self.screen.get_size()
        self.ratio = int(min(height // (self.h + 2),
                             width // (self.w + 2)))
        self.scale = self.ratio // (self.tile_size * 3)
        self.tile_size *= self.scale
        self.tiles = [
            pygame.transform.scale(
                pygame.image.load(
                    "images/maze/" + str(i) + ".png"),
                     (self.tile_size, self.tile_size)) for i in range(32)]
        self.fps = 60
        self.screen_w = (self.w + 2) * self.tile_size * 3
        self.screen_h = (self.h + 2) * self.tile_size * 3
        self.pad = self.tile_size * 3
        self.screen = None
        self.run = True


    def init_audio(self):
        self.audio_enabled = False
        # la suite fonctionnera que sur les imac pas sur mon intel #snif
        # try:
        #     pygame.mixer.init()
        #     self.audio_enabled = True
        # except pygame.error:
        #     self.audio_enabled = False


    def play(self):
        def print_grid(grid):
            for y, row in enumerate(self.maze):
                print(f"ROW {y}")
                for x, cell in enumerate(row):
                    print(f"  CELL ({x}, {y})")
                    for line in cell:
                        print("   ", line)
        
        self.init_audio()
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        pygame.display.set_caption("Pac-Man")
        clock = pygame.time.Clock()
        # print_grid(self.maze)
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.run = False
            # clear screen
            self.screen.fill("black")
            for i, row in enumerate(self.maze):
                for j, tile in enumerate(row):
                    for k, row_tile in enumerate(tile):
                        for l, col_tile in enumerate(row_tile):
                            self.screen.blit(
                                self.tiles[col_tile],
                                    (self.pad + j * self.tile_size * 3 + l * self.tile_size ,
                                    self.pad + i * self.tile_size * 3 + k * self.tile_size))
                            # self.draw_tiles_bond(i, j, l, k)
            pygame.display.flip()
            clock.tick(self.fps)  
        pygame.quit()


    def draw_tiles_bond(self, i, j, l, k):
        pygame.draw.rect(
    self.screen,
    (50, 50, 50),
    (
        self.pad + j * self.tile_size * 3 + l * self.tile_size,
        self.pad + i * self.tile_size * 3 + k * self.tile_size,
        self.tile_size,
        self.tile_size
    ),
    1
)
        pygame.draw.rect(
            self.screen,
            (0, 100, 0),
            (
                self.pad + j * self.tile_size * 3,
                self.pad + i * self.tile_size * 3,
                self.tile_size * 3,
                self.tile_size * 3
            ),
            2
        )