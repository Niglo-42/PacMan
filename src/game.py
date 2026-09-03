import pygame
from pygame.locals import K_ESCAPE, KEYDOWN
from .interface.render import Render
from .interface.menu import Menu
from .interface.drawing import draw_entitys, play_intermission
# from .interface.parameters import set_parameters
from .entitys.player import Player
from .entitys.ghosts import Ghost, GhostMode
from .game_logic.direction import Dir
from .game_logic.updates import update_entitys, update_game_state, get_fruits
from .init import init_ghosts, init_maze, init_player, init_new_level


class Game:
    def __init__(self, args):
        pygame.display.init()
        pygame.font.init()
        self.args = args
        self.start_new_game(self.args)

    def start_new_game(self, args):
        self.fps = 60
        self.run = True
        self.cheat_mode = False
        self.points_per_pacgum = args.points_per_pacgum
        self.points_per_super_pacgum = \
            args.points_per_super_pacgum
        self.point_per_ghost = args.points_per_ghost
        self.total_pellet: int = 0
        self.maze = init_maze(self, args.width, args.height, args.seed)
        self.level = 1
        self.score = 0
        self.eaten_pellet: int = 0
        self.run = True
        self.ghosts_state = GhostMode.SCATTER
        self.frightened_timer: float = 0.0
        self.global_timer: int = 0
        self.state_timer: tuple[int, int] = (0, 0)
        self.render = Render(self.maze)
        self.menu = Menu(self.render)
        self.audio_enabled = True
        self.player = init_player(self, 0, args.lives)
        self.player2 = None
        self.ghosts = init_ghosts(self)
        self.player.surf.blit(self.player.tiles[1], (0, 0))
        self.max_lives = 3
        self.clock = pygame.time.Clock()
        # les 33 premières tiles sont des pacmans

    def monitor(self):
        while self.run:
            action = self.menu.pause_menu()
            if action == "play":
                self.play()
            elif action == "quit":
                self.run = False
            elif action == "param":
                self.player2 = init_player(self, 1, self.args.lives)
                # set_parameters()
        pygame.quit()

    def play(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
            update_entitys(self)
            self.render.draw_maze_on_surf_screen()
            draw_entitys(self)
            get_fruits(self, self.maze, self.render.tile_size)
            update_game_state(self)
            highscore = self.score + self.player.score if self.level > 1 \
                else self.player.score
            self.render.putstr(f"Highscore: {highscore}", self.render.score, 0)
            self.render.putstr(f"Level: {self.level}", self.render.lvl, 1)
            pygame.display.flip()
            self.clock.tick(self.fps)  # vaut un sleep qui sync sur fps / 1000
        pygame.quit()

    def player_died(self, player: Player, ghosts: list[Ghost]) -> int:
        player.alive = False
        player.lives -= 1
        # animation de mort, décompte 2 secondes avant de reprendre
        player.position = player.spawn
        player.offset_xy = (0, 0)
        player.direction = Dir.X
        player.desired_direction = Dir.X
        for g in ghosts:
            g.position = g.spawn
            g.offset_xy = (0, 0)

        return player.lives

    def game_is_over(self) -> None:
        self.run = False
        duration_frames = self.fps * 30
        for frame in range(duration_frames):
            self.render.screen.fill((0, 0, 0))
            self.render.putstr("GAY'M OVER BITCH", self.render.score, 0)
            pygame.display.flip()
        if self.menu.pause_menu() == "play":
            self.start_new_game(self.args)
            self.run = True

        #   animation de game_over, tableau highscore, retourner main menu

    def level_is_won(self) -> None:
        play_intermission(self)
        init_new_level(self)
        pygame.time.wait(500)
