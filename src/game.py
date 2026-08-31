import pygame
import random
from .convert import Convert
from .models.maze import Maze
from pygame.locals import K_ESCAPE, KEYDOWN
from .models.render import Render
from .models.menu import Menu
from .models.parameters import set_parameters
from .entitys.player import Player
from .entitys.ghosts import Ghost, Blinky, Pinky, Inky, Clyde, GhostMode
from .entitys.direction import Dir


class Game:
    def __init__(self, args):
        pygame.display.init()
        pygame.font.init()
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
            id=id, name=str(id), speed=1.7, idx_anim=0,
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

    # def menu(self):
    #     self.render.screen.fill(0)
    #     w, h = self.render.screen.get_size()
    #     size = (int(w * 0.2), int(w * 0.2 * 248 / 1179))
    #     btns = [
    #         pygame.transform.smoothscale(
    #             pygame.image.load(f"images/buttons/btn{i}.png")
    #             .convert_alpha(), size) for i in range(3)
    #     ]
    #     btn_w, btn_h = btns[0].get_size()
    #     bloc_size = btn_h * 6
    #     pad_w = (w - 0) // 2
    #     pad_h = (h - bloc_size) // 2
    #     play = btns[0].get_rect(center=(pad_w, pad_h))
    #     param = btns[1].get_rect(center=(pad_w, pad_h + btn_h * 2))
    #     quit = btns[2].get_rect(center=(pad_w, pad_h + btn_h * 4))
    #     btns_rect = [play, param, quit]
    #     while self.run:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 self.run = False
    #                 return ""
    #             elif event.type == pygame.MOUSEBUTTONDOWN:
    #                 if event.button == 1:
    #                     if play.collidepoint(event.pos):
    #                         self.render.erase(btns_rect)
    #                         return "play"
    #                     elif quit.collidepoint(event.pos):
    #                         self.run = False
    #                         return ""
    #                     elif param.collidepoint(event.pos):
    #                         if not self.player2:
    #                             self.player2 = self.init_player(1)
    #         self.render.hoover_opacity70(btns, btns_rect)
    #         self.render.draw_obj(btns, btns_rect)
    #         pygame.display.flip()

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
            self.player2.update(self.maze, self.render.tile_size)
        self.player.update(self.maze, self.render.tile_size)
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

    def update_game_state(self):
        if self.eaten_pellet == self.total_pellet:
            self.level_is_won()
        self.global_timer += 1
        self.check_collision(self.player, self.ghosts)

        if self.update_pellets(self.player, self.maze.map) or \
                self.update_pellets(self.player2, self.maze.map):
            # si une pacman a été mangé
            self.frightened_timer = self.global_timer
            self.modify_ghosts_state(GhostMode.FRIGHTENED)
        self.update_ghosts_state()
        self.draw_lives()

    def update_ghosts_state(self) -> None:
        states = [GhostMode.SCATTER, GhostMode.CHASE]
        acc_state, state_timer = self.state_timer

        PHASE_DURATIONS = [[7, 20, 7, 20, 5, 20, 5],
                           [7, 20, 7, 20, 5, 1033, 1/60],
                           [5, 20, 5, 20, 5, 1037, 1/60]]

        if self.level <= 1:
            level_index = 0
        elif self.level <= 4:
            level_index = 1
        else:
            level_index = 2

        if self.ghosts_state == GhostMode.FRIGHTENED:
            if (self.global_timer - self.frightened_timer) >= self.fps * 5:
                self.modify_ghosts_state(GhostMode.CHASE)
        else:
            if acc_state < len(PHASE_DURATIONS[level_index]):

                phase_duration = PHASE_DURATIONS[level_index][acc_state]
                if (self.global_timer - state_timer) >= \
                        (phase_duration * self.fps):
                    acc_state += 1
                    state_timer = self.global_timer
                    self.modify_ghosts_state(states[acc_state % 2])

                self.state_timer = (acc_state, state_timer)
            else:
                self.modify_ghosts_state(GhostMode.CHASE)

    def modify_ghosts_state(self, state: GhostMode) -> None:
        self.ghosts_state = state
        for g in self.ghosts:
            if g.mode != GhostMode.EYES:
                g.mode = state
                g.changing_side = True

    def draw_lives(self):
        # draw lives
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
        self.menu.pause_menu()
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
