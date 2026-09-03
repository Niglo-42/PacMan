import pygame
from ..maze.maze import Maze
from ..entitys.entity import Entity


def collide_rect(a: pygame.Rect, b: pygame.Rect) -> bool:
    return (a.x < b.x + b.width and a.x + a.width > b.x and
            a.y < b.y + b.height and a.y + a.height > b.y)


def collide_point(rect: pygame.Rect, x: int, y: int) -> bool:
    return (rect.x <= x <= rect.x + rect.width and
            rect.y <= y <= rect.y + rect.height)


class Render:
    def __init__(self, maze: Maze):
        info = pygame.display.Info()
        pygame.display.set_caption("Pac-Man")
        self.screen = pygame.display.set_mode(
            (info.current_w, info.current_h), pygame.NOFRAME)
        self.screen_rect = self.screen.get_rect()
        self.h = maze.height
        self.w = maze.width

        self.maze = maze
        self.tile_size = 8
        ratio = min(info.current_h // (self.h + 2),
                    info.current_w // (self.w + 2))
        self.scale = max(1, ratio // self.tile_size)
        self.tile_size *= self.scale
        self.half_size = self.tile_size // 2

        self.font = pygame.font.Font("font/press_start_2p.ttf", self.tile_size)

        self.maze.tiles = [
            pygame.transform.scale(
                pygame.image.load(f"images/maze/{i}.png").convert_alpha(),
                (self.tile_size, self.tile_size)) for i in range(32)]
        self.maze.fruit_tiles = [
            pygame.transform.scale(
                pygame.image.load(
                    f"images/sprites/{str(i).zfill(3)}.png").convert_alpha(),
                (self.tile_size, self.tile_size)) for i in range(33, 41)]

        self.maze.surf = pygame.Surface((self.w * self.tile_size,
                                          self.h * self.tile_size))
        self.score = pygame.Surface((self.maze.surf.get_width(), self.tile_size))
        self.lvl = pygame.Surface((self.maze.surf.get_width(), self.tile_size))
        self.fruits = [pygame.Surface((self.tile_size, self.tile_size)) for _ in range(2)]

        self.maze_rect = self.maze.surf.get_rect(
            center=self.screen.get_rect().center)

        self.lives_img = pygame.transform.scale(
            pygame.image.load("images/sprites/015.png").convert_alpha(),
            (self.tile_size * 2, self.tile_size * 2))
        self.lives_rect = self.lives_img.get_rect(
            topleft=self.maze_rect.bottomleft)

        self.build_maze()

    def build_maze(self):
        for i, row in enumerate(self.maze.map):
            for j, col in enumerate(row):
                self.draw_on_maze(self.maze.tiles[col], i, j)

    def draw_on_maze(self, surf, y, x):
        self.maze.surf.blit(surf, (x * self.tile_size, y * self.tile_size))

    def draw_maze_on_surf_screen(self):
        self.screen.blit(self.maze.surf, self.maze_rect)

    def blit_at(self, surf: pygame.Surface, rect: pygame.Rect):
        self.screen.blit(surf, rect.move(self.maze_rect.topleft))

    def draw_entity(self, entity: Entity):
        col, row = entity.position
        x = col * self.tile_size + entity.offset_xy[0] * self.scale
        y = row * self.tile_size + entity.offset_xy[1] * self.scale
        entity.rect = entity.surf.get_rect(topleft=(x - self.half_size, y - self.half_size))

        self.blit_at(entity.surf, entity.rect)

    def draw_obj(self, objs, objs_rect):
        for obj, rect in zip(objs, objs_rect):
            self.screen.blit(obj, rect)

    def hoover_opacity70(self, buttons, rects):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for rect, btn in zip(rects, buttons):
            btn.set_alpha(180)
            if collide_point(rect, mouse_x, mouse_y):
                self.screen.fill(0, rect)

    def erase(self, rects):
        for rect in rects:
            self.screen.fill(0, rect)

    def putstr(self, string: str, surf: pygame.Surface, backslash_n: int):
        text = self.font.render(string, False, "#dedeff")
        surf.fill(0)
        surf.blit(text, (0, 0))
        target_rect = surf.get_rect(
            midtop=(self.screen_rect.centerx,
                    10 + text.get_height() * backslash_n))
        self.screen.blit(surf, target_rect)