import pygame
from .convert import Convert
from .models.maze import Maze
from pygame.locals import K_ESCAPE, KEYDOWN, K_SPACE, K_UP, K_DOWN, K_LEFT, K_RIGHT
from .models.render import Render
from .entitys.player import Player
from .entitys.direction import Dir


class Game:
    def __init__(self, args):
        pygame.display.init()
        self.maze = Maze(width=args.width, height=args.height, seed=args.seed)
        self.maze.tiles = Convert.cell2tiles(self.maze)
        self.maze.height *= 3
        self.maze.width *= 3
        self.maze.add_super_gum()
        self.fps = 60
        self.run = True
        self.render = Render(self.maze.width, self.maze.height, self.maze.tiles)
        self.audio_enabled = True
        self.player = Player(
            direction=Dir.W,
            speed=1 * self.render.scale,
            accumulator=1,
            alive=True,
            offset_xy=(0, 0),
            desired_direction=Dir.W,
            position=self.maze.get_spawn(),
            last_position=self.maze.get_spawn(),
            tiles=[
            pygame.transform.scale(
                pygame.image.load(f"images/sprites/{str(i).zfill(3)}.png"),
                (self.render.tile_size, self.render.tile_size)) for i in range(33)])

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
            self.player.update(self.maze)
            self.render.draw_entity(self.player)
            clock.tick(self.fps)
            pygame.display.flip()
        pygame.quit()
