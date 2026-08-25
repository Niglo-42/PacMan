import pygame
from .convert import Convert
from .models.maze import Maze
from pygame.locals import K_ESCAPE, KEYDOWN, K_SPACE, K_UP, K_DOWN, K_LEFT, K_RIGHT
from .models.render import Render

class Game:
    def __init__(self, args):
        pygame.display.init()
        self.fps = 60
        self.run = True
        self.maze = Convert.trad(
        Maze(width=args.width, height=args.height, seed=args.seed))
        self.render = Render(self.maze, args.width, args.height)
        self.audio_enabled = True


    def init_audio(self):
        self.audio_enabled = False
        # la suite fonctionnera que sur les imac pas sur mon intel #snif
        # try:
        #     pygame.mixer.init()
        #     self.audio_enabled = True
        # except pygame.error:
        #     self.audio_enabled = False


    def play(self):        
        self.init_audio()
        clock = pygame.time.Clock()
        self.render.draw_maze()
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.run = False
            clock.tick(self.fps)  
        pygame.quit()
