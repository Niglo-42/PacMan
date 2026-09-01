import pygame
import random
from .maze.convert import Convert
from .maze.maze import Maze
from pygame.locals import K_ESCAPE, KEYDOWN
from .interface.render import Render
from .interface.menu import Menu
from .interface.parameters import set_parameters
from .entitys.player import Player
from .entitys.ghosts import Ghost, Blinky, Pinky, Inky, Clyde, GhostMode
from .game_logic.direction import Dir
from .game_logic.ghosts_state import modify_ghosts_state, update_ghosts_state
from .game_logic.speed import update_speeds


class Game:
    def __init__(self, args):
        pygame.display.init()
        pygame.font.init()
        self.args = args
        self.start_new_game(self.args)

    def start_new_game(self, args):
        self.fps = 60
        self.run = True
        self.points_per_pacgum = args.points_per_pacgum
        self.points_per_super_pacgum = \
            args.points_per_super_pacgum
        self.point_per_ghost = args.points_per_ghost
        self.total_pellet: int = 0
        self.maze = self.init_maze(args.width, args.height, args.seed)
        self.level = 1
        self.score = 0
        self.eaten_pellet: int = 0
        self.run = True
        self.ghosts_state = GhostMode.SCATTER
        self.frightened_timer: float = 0.0
        self.global_timer: int = 0
        self.state_timer: tuple[int, float] = (0, 0)
        self.render = Render(self.maze)
        self.menu = Menu(self.render)
        self.audio_enabled = True
        self.player = self.init_player(0)
        self.player2 = None
        self.ghosts = self.init_ghosts()
        self.player.surf.blit(self.player.tiles[1], (0, 0))
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
                set_parameters()
        pygame.quit()

    def init_audio(self):
        self.audio_enabled = False
        # la suite fonctionnera que sur les imac pas sur mon intel #snif
        # try:
        #     pygame.mixer.init()
        #     self.audio_enabled = True
        # except pygame.error:
        #     self.audio_enabled = False

    def init_ghosts(self) -> list[Ghost]:
        Ghost.load_common_tiles(self.render.tile_size)
        ghost_classes = [Blinky, Pinky, Inky, Clyde]
        ghost_spawns = self.maze.get_ghosts_spawns()
        ghosts = [cls(spawn, self.render.tile_size) for cls, spawn in
                  zip(ghost_classes, ghost_spawns)]
        ghosts[2].blinky = ghosts[0]
        return ghosts

    def init_maze(self, width: int, height: int, seed: int) -> Maze:
        maze = Maze(width=width, height=height, seed=seed)
        maze.map = Convert.cell2tiles(maze)
        maze.height *= 3
        maze.width *= 3
        maze.add_super_gum()
        maze.kills_caves()

        self.total_pellet = sum(row.count(1) for row in maze.map)
        return maze

    def init_player(self, id) -> Player:
        spawn = self.maze.get_spawn()
        player = Player(
            id=id, name=str(id), idx_anim=0,
            anim=[
                    [23, 24, 2, 24],    # n
                    [0, 1, 2, 1],  # e
                    [31, 32, 2, 32],  # s
                    [14, 15, 2, 15]  # w
                ],
            spawn=spawn,
            position=spawn,
            surf=pygame.Surface((self.render.tile_size * 2,
                                 self.render.tile_size * 2), pygame.SRCALPHA),
            tiles=[pygame.transform.scale
                   (pygame.image.load(f"images/sprites/{str(i).zfill(3)}."
                                      "png").convert_alpha(),
                    (self.render.tile_size * 2, self.render.tile_size * 2))
                   for i in range(33)])
        return player

    def play(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
            self.update_entitys()
            self.render.draw_maze_on_surf_screen()
            self.draw_entitys()
            self.update_game_state()
            highscore = self.score + self.player.score if self.level > 1 \
                else self.player.score
            self.render.putstr(f"Highscore: {highscore}\nLevel: {self.level}")
            pygame.display.flip()
            self.clock.tick(self.fps)  # vaut un sleep qui sync sur fps / 1000
        pygame.quit()

    def update_entitys(self) -> None:
        if self.player2:
            self.player2.update(self.maze)
        self.player.update(self.maze)
        for g in self.ghosts:
            g.update(self.player, self.maze, self.ghosts_state,
                     (self.global_timer - self.frightened_timer)
                     >= self.fps * 3)

    def draw_entitys(self) -> None:
        if self.player2:
            self.render.draw_entity(self.player2)
        self.render.draw_entity(self.player)
        for g in self.ghosts:
            self.render.draw_entity(g)
        self.get_fruits(self.maze, self.render.tile_size)

    def get_fruits(self, maze: Maze, tile_size: int):
        if (self.eaten_pellet == 70) and maze.flag_fruit == 0:
            maze.flag_fruit = 0b1
            maze.add_fruit(self.player.position, tile_size)
        elif (self.eaten_pellet == 170) and maze.flag_fruit == 1:
            maze.flag_fruit = 0b11
            maze.add_fruit(self.player.position, tile_size)

    def update_game_state(self):
        update_speeds(self.level, self.ghosts, self.player, self.ghosts_state)
        if self.eaten_pellet == self.total_pellet:
            self.level_is_won()
        self.global_timer += 1
        self.check_collision(self.player, self.ghosts)

        if self.update_pellets(self.player, self.maze.map) or \
                self.update_pellets(self.player2, self.maze.map):
            # si une pacman a été mangé
            self.frightened_timer = self.global_timer
            self.ghosts_state = modify_ghosts_state(self, GhostMode.FRIGHTENED)
        update_ghosts_state(self)
        self.draw_lives()

    def draw_lives(self):
        x, y = self.render.lives_pad
        for i in range(3):
            dx = x + i * self.render.tile_size * 2
            rect = self.render.lives.get_rect(topleft=(dx, y))
            if i < self.player.lives:
                self.render.draw_obj([self.render.lives], [rect])
            else:
                self.render.screen.fill((0, 0, 0), rect)

    def update_pellets(self, player: Player, map: list[list[int]]) -> bool:
        # return True quand energizer a été mangé
        energizer = False
        if player and (player.offset_xy) == (0, 0):
            x, y = player.position
            if map[y][x] == 1:
                player.score += 10  # a modifier
                self.eaten_pellet += 1
            elif map[y][x] == 2:
                player.score += 50
                energizer = True
            map[y][x] = 0
            self.render.draw_cell(0, y, x)
        return energizer

    def check_collision(self, player: Player, ghosts: list[Ghost]) -> None:
        for ghost in ghosts:
            if ghost.mode == GhostMode.EYES:
                continue
            if ghost.position == player.position:
                # à creuser: bug trouvé -> passé à travers un fantome dans
                # un virage a cause du fast turn
                # plus permissif pour meilleur visuel? si chaque entité d'un
                # bout et l'autre d'une tile, soit 8 pixels d'écart, ça touche
                if ghost.mode == GhostMode.CHASE or \
                        ghost.mode == GhostMode.SCATTER:
                    if self.player_died(player, ghosts) <= 0:
                        self.game_is_over()
                elif ghost.mode == GhostMode.FRIGHTENED:
                    ghost.alive = False
                    ghost.mode = GhostMode.EYES
                    player.score += self.point_per_ghost * \
                        sum([not g.alive for g in ghosts])

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
            self.render.putstr("GAY'M OVER BITCH")
            pygame.display.flip()
        if self.menu.pause_menu() == "play":
            self.start_new_game(self.args)
            self.run = True

        #   animation de game_over, tableau highscore, retourner main menu

    def level_is_won(self) -> None:
        self.play_intermission()
        self.init_new_level()
        pygame.time.wait(500)

    def init_new_level(self) -> None:
        saved_lives = self.player.lives
        self.level += 1
        self.score += self.player.score
        self.eaten_pellet = 0
        self.global_timer = 0
        self.state_timer = (0, 0)
        self.frightened_timer = 0
        self.ghosts_state = GhostMode.SCATTER

        self.maze = self.init_maze(self.maze.width // 3, self.maze.height // 3,
                                   seed=random.randint(0, 256))
        self.player = self.init_player(0)
        self.player.lives = saved_lives
        self.ghosts = self.init_ghosts()
        self.render = Render(self.maze)

    def play_intermission(self) -> None:
        duration_frames = self.fps * 3
        screen_w, screen_h = self.render.screen.get_size()
        y_pos = screen_h // 2
        pacman_x = -60.0
        ghost_x = -180.0
        speed = (screen_w + 240) / duration_frames
        rndm_ghost = random.randint(0, len(self.ghosts) - 1)

        for frame in range(duration_frames):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    return
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return

            pacman_x += speed
            ghost_x += speed

            self.render.screen.fill((0, 0, 0))
            self.render.putstr("READY FOR NEXT LEVEL?")

            anim_tile = self.player.tiles[(frame // 6) % 4]
            self.render.screen.blit(anim_tile, (int(pacman_x), y_pos))

            if self.ghosts:
                self.render.screen.blit(self.ghosts[rndm_ghost].surf,
                                        (int(ghost_x), y_pos))
            pygame.display.flip()
            self.clock.tick(self.fps)
