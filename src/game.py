import pygame
from .convert import Convert
from .models.maze import Maze
from pygame.locals import K_ESCAPE, KEYDOWN
from .models.render import Render
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
        self.maze = self.init_maze(args.width, args.height, args.seed)
        self.fps = 60
        self.level = 1
        self.score = 0
        self.total_pellet: int = 0
        self.run = True
        self.ghosts_state = GhostMode.CHASE
        self.frightened_timer: float = 0.0
        self.global_timer: float = 0.0
        self.render = Render(self.maze)
        self.audio_enabled = True
        self.player = self.init_player(0)
        self.player2 = None
        self.ghosts = self.init_ghosts()
        self.player.surf.blit(self.player.tiles[1], (0, 0))
        self.clock = pygame.time.Clock()
        # les 33 premières tiles sont des pacmans

    def monitor(self):
        while self.run:
            action = self.menu()
            if action == "play":
                self.play()
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

    def menu(self):
        self.render.screen.fill(0)
        w, h = self.render.screen.get_size()
        size = (int(w * 0.2), int(w * 0.2 * 248 / 1179))
        btns = [
            pygame.transform.smoothscale(
                pygame.image.load(f"images/buttons/btn{i}.png")
                .convert_alpha(), size) for i in range(3)
        ]
        btn_w, btn_h = btns[0].get_size()
        bloc_size = btn_h * 6
        pad_w = (w - 0) // 2
        pad_h = (h - bloc_size) // 2
        play = btns[0].get_rect(center=(pad_w, pad_h))
        param = btns[1].get_rect(center=(pad_w, pad_h + btn_h * 2))
        quit = btns[2].get_rect(center=(pad_w, pad_h + btn_h * 4))
        btns_rect = [play, param, quit]
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    return ""
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if play.collidepoint(event.pos):
                            self.render.erase(btns_rect)
                            return "play"
                        elif quit.collidepoint(event.pos):
                            self.run = False
                            return ""
                        elif param.collidepoint(event.pos):
                            if not self.player2:
                                self.player2 = self.init_player(1)
            self.render.hoover_opacity70(btns, btns_rect)
            self.render.draw_obj(btns, btns_rect)
            pygame.display.flip()

    def play(self):
        eat_flag = [False, False]
        dt = self.clock.tick(self.fps)
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
            if self.player2:
                self.player2.update(self.maze, self.render.tile_size)
            self.player.update(self.maze, self.render.tile_size)
            for g in self.ghosts:
                g.update(self.player, self.maze, self.ghosts_state)
            self.render.draw_maze_on_surf_screen()
            if self.player2:
                self.render.draw_entity(self.player2)
            self.render.draw_entity(self.player)
            for g in self.ghosts:
                self.render.draw_entity(g)
            self.update_game_state(dt)
            self.render.putstr("Highscore: " + str(self.player.score))
            pygame.display.flip()
            self.clock.tick(self.fps)  # vaux un sleep qui sync sur fps / 1000
        pygame.quit()

    def update_game_state(self, dt: float):
        self.global_timer += dt
        self.check_collision(self.player, self.ghosts)
        if self.update_pellets(self.player, self.maze.map):
            self.frightened_timer = self.global_timer
            self.ghosts_state = GhostMode.FRIGHTENED
            self.modify_ghosts_state(GhostMode.FRIGHTENED)
        self.update_ghosts_state()
        self.draw_lives()
        print(f"{self.global_timer / 100000=}")
        print(f"{self.frightened_timer / 100000=}")
        for g in self.ghosts:
            print(f"{g.mode}")

    def update_ghosts_state(self) -> None:
        if self.ghosts_state == GhostMode.FRIGHTENED:
            if (self.global_timer - self.frightened_timer) / 100000 >= 7:
                self.ghosts_state = GhostMode.CHASE
                self.modify_ghosts_state(GhostMode.CHASE)
        else:
            pass

    def modify_ghosts_state(self, state: GhostMode) -> None:
        for g in self.ghosts:
            if not g.mode == GhostMode.EYES:
                g.mode = state
                g.direction = g.direction.opposite

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

    def update_pellets(self, player: Player, map: list[list[int]]) -> int:
        # if not all(self.player.offset_xy): == si il est a offsetxy = (0, 0) donc si a bougé
        # return True quand energizer a été mangé
        energizer = False
        if not all(player.offset_xy):
            x, y = player.position
            if map[y][x] == 1:
                player.score += 10  # a modifier
                self.total_pellet += 1
            elif map[y][x] == 2:
                player.score += 50
                energizer = True
            map[y][x] = 0
            self.render.draw_cell(0, y, x)

        if self.player2 and not all(self.player2.offset_xy):
            x, y = self.player2.position
            self.maze.map[y][x] = 0
            self.render.draw_cell(0, y, x)

        return energizer

    def check_collision(self, player: Player, ghosts: list[Ghost]) -> None:
        for ghost in ghosts:
            if ghost.mode == GhostMode.EYES:
                continue
            if ghost.position == player.position:
                # à creuser: bug trouvé -> passé à travers un fantome dans un virage a cause du fast turn
                # plus permissif pour meilleur visuel? si chaque entité d'un bout et l'autre d'une tile, soit 8 pixels d'écart, ça touche
                if ghost.mode == GhostMode.CHASE or \
                        ghost.mode == GhostMode.SCATTER:
                    if self.player_died(player, ghosts) <= 0:
                        self.game_is_over()
                elif ghost.mode == GhostMode.FRIGHTENED:
                    ghost.alive = False
                    ghost.mode = GhostMode.EYES
                    player.score += self.point_per_ghost  # todo: x2 à chaque victime puis reset

    def player_died(self, player: Player, ghosts: list[Ghost]) -> int:
        player.alive = False
        player.lives -= 1
        # animation de mort, décompte 2 secondes avant de reprendre
        for g in ghosts:
            g.position = g.spawn
            g.offset_xy = (0, 0)
        player.position = player.spawn
        player.offset_xy = (0, 0)
        player.direction = Dir.X

        return player.lives

    def game_is_over(self) -> None:
        print("GAME OVER GROS NOOB")
        self.run = False
        #   animation de game_over, tableau highscore, retourner main menu
