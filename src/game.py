import pygame
from .convert import Convert
from .models.maze import Maze
from pygame.locals import K_ESCAPE, KEYDOWN, K_SPACE, K_UP, K_DOWN, K_LEFT, K_RIGHT
from .models.render import Render
from .entitys.player import Player
from .entitys.ghosts import Ghost, Blinky, Pinky, Inky, Clyde
from .entitys.direction import Dir


class Game:
    def __init__(self, args):
        pygame.display.init()
        self.fps = 60
        self.run = True
        self.points_per_pacgum = args.points_per_pacgum
        self.points_per_super_pacgum = \
        args.points_per_super_pacgum
        self.maze = Maze(width=args.width, height=args.height, seed=args.seed)
        self.maze.map = Convert.cell2tiles(self.maze)
        self.maze.height *= 3
        self.maze.width *= 3
        self.maze.add_super_gum()
        self.maze.kills_caves()
        self.fps = 60
        self.level = 1
        self.score = 0
        self.run = True
        self.render = Render(self.maze)
        self.audio_enabled = True
        self.player = self.init_player()
        self.ghosts = self.init_ghosts()
        self.player.surf.blit(self.player.tiles[1], (0, 0))
        # les 33 premières tiles sont des pacmans

    def init_audio(self):
        self.audio_enabled = False
        # la suite fonctionnera que sur les imac pas sur mon intel #snif
        # try:
        #     pygame.mixer.init()
        #     self.audio_enabled = True
        # except pygame.error:
        #     self.audio_enabled = False

    def init_ghosts(self) -> list[Ghost]:
        ghost_classes = [Blinky, Pinky, Inky, Clyde]
        ghost_spawns = self.maze.get_ghosts_spawns()
        ghosts = [cls(spawn) for cls, spawn in
                  zip(ghost_classes, ghost_spawns)]
        ghosts[2].blinky = ghosts[0]
        return ghosts

    def init_player(self) -> Player:
        return Player(
            direction=Dir.X,
            speed=1 * self.render.scale,
            accumulator=0,
            total_pellet=0,
            score=0,
            alive=True,
            offset_xy=(0, 0),
            idx_anim=0,
            dir_anim=1,
            desired_direction=Dir.X,
            anim=[
                    [23, 24, 2, 24], #n
                    [0, 1, 2, 1],  # e
                    [31, 32, 2, 32],  # s
                    [14, 15, 2, 15]  # w
                ],
            position=self.maze.get_spawn(),
            surf=pygame.Surface((self.render.tile_size * 2,
                                 self.render.tile_size * 2), pygame.SRCALPHA),
            tiles=[pygame.transform.scale
                   (pygame.image.load(f"images/sprites/{str(i).zfill(3)}.png").convert_alpha(),
                    (self.render.tile_size * 2, self.render.tile_size * 2))
                   for i in range(33)])

    def play(self):
        clock = pygame.time.Clock()
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.run = False
            self.player.update(self.maze, self.render.tile_size)
            self.update_game_state()
            self.render.draw_maze_on_surf_screen()
            self.render.draw_entity(self.player)
            pygame.display.flip()
            clock.tick(self.fps) # vaux un sleep qui sync sur fps / 1000
        pygame.quit()

    def update_game_state(self):
        x, y = self.player.position
        self.maze.map[y][x] = 0
        self.render.draw_cell(0, y, x)
