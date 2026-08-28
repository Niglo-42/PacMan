import pygame
from operator import add, mul, sub
from .maze import Maze
from ..entitys.entity import Entity

class Render:
    def __init__(self, maze: Maze):
        info = pygame.display.Info()
        pygame.display.set_caption("Pac-Man")
        self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.NOFRAME)
        self.h = maze.height
        self.w = maze.width

        self.maze = maze
        self.tile_size = 8
        ratio = min(info.current_h // (self.h + 2),
                    info.current_w // (self.w + 2))
        self.scale = max(1, ratio // (self.tile_size))
        self.tile_size *= self.scale
        self.half_size = self.tile_size // 2
        self.screen_w = (self.w) * self.tile_size
        self.screen_h = (self.h) * self.tile_size
        self.font = pygame.font.Font("font/press_start_2p.ttf", self.tile_size)
        self.maze.tiles = [
            pygame.transform.scale(
                pygame.image.load(f"images/maze/{i}.png").convert_alpha(),
                (self.tile_size, self.tile_size)) for i in range(32)]
        self.maze.fruit_tiles = [
            pygame.transform.scale(
                pygame.image.load(f"images/sprites/{str(i).zfill(3)}.png").convert_alpha(),
                (self.tile_size, self.tile_size)) for i in range(33, 41)]
        self.maze.surf = pygame.Surface(
            (self.screen_w, self.screen_h)
        )
        self.pad_h = (self.screen.get_size()[1] - self.maze.surf.get_size()[1]) // 2
        self.pad_w = (self.screen.get_size()[0] - self.maze.surf.get_size()[0]) // 2
        self.build_maze()

    def build_maze(self):
        for i, row in enumerate(self.maze.map):
            for j, col in enumerate(row):
                self.draw_cell(col, i, j)
                # pygame.draw.rect(self.maze.surf, "#659e65", (j * self.tile_size, i * self.tile_size, self.tile_size, self.tile_size), 1)

    def draw_maze_on_surf_screen(self):
        self.screen.blit(self.maze.surf, (self.pad_w, self.pad_h))

    def draw_cell(self, col, y, x):
        self.maze.surf.blit(self.maze.tiles[col],
                               (x * self.tile_size, y * self.tile_size))

    def op_pos_px(self, xy: tuple, op: callable, value: int):
        x, y = xy
        return op(x, value), op(y, value)

    def op_tuple(self, ab: tuple, cd: tuple, op: callable) -> tuple:
        a, b = ab
        c, d = cd
        return op(a, c), op(b, d)

    def draw_entity(self, entity: Entity):
        col, row = entity.position
        x = col * self.tile_size + entity.offset_xy[0] * entity.speed
        y = row * self.tile_size + entity.offset_xy[1] * entity.speed
        x, y = self.op_pos_px((x, y), sub, self.half_size) # centrage
        x, y = x + self.pad_w, y + self.pad_h
        self.screen.blit(entity.surf, (x, y))

    def hoover_opacity70(self, buttons: pygame.Surface, rects):
        for rect, btn in zip(rects, buttons):
            if rect.collidepoint(pygame.mouse.get_pos()):
                btn.set_alpha(180)
                self.screen.fill(0, rect)
            else:
                btn.set_alpha(180)

    def erase(self, rects):
        for rect in rects:
            self.screen.fill(0, rect)

    def draw_obj(self, objs, objs_rect):
        """print l'object a pos du rect.center"""
        for obj, rect in zip(objs, objs_rect):
            self.screen.blit(obj, rect)

    def putstr(self, string):
        text = self.font.render(string, False, "#dedeff")
        mid_maze = self.maze.surf.get_size() // 2
        self.screen.blit(text, (self.pad_w + mid_maze, self.pad_h + mid_maze))
