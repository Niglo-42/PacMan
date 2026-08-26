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
        self.fps = 60
        self.run = True
        maze = Maze(width=args.width, height=args.height, seed=args.seed)
        self.maze = Convert.trad(maze)
        self.render = Render(self.maze, args.width, args.height)
        self.audio_enabled = True
        cell_pos, tile_pos = maze.get_spawn()
        px_x, px_y = cell_pos[0] * self.render.cell_size, \
        cell_pos[1] * self.render.cell_size
        self.player = Player(
            direction=Dir.W,
            speed=1 * self.render.scale,
            accumulator=1,
            alive=True,
            offset_xy=(0, 0),
            cell_xy=cell_pos,
            px_pos=(px_x, px_y),
            last_px_pos=(px_x, px_y),
            anim_frame=0,
            desired_direction=Dir.W,
            tile_xy=tile_pos,
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
            self.render.draw_player(self.player)
            clock.tick(self.fps)
            pygame.display.flip()
        pygame.quit()
