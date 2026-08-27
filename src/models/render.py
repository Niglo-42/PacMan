import pygame
from operator import add, mul, sub


class Render:
    def __init__(self, w, h, maze):
        self.h = h
        self.w = w
        self.maze = maze
        info = pygame.display.Info()
        self.tile_size = 8
        ratio = min(info.current_h // (self.h + 2),
                    info.current_w // (self.w + 2))
        self.scale = max(1, ratio // (self.tile_size))
        self.tile_size *= self.scale
        self.half_size = self.tile_size // 2
        self.pad = self.tile_size
        self.screen_w = (self.w + 2) * self.tile_size
        self.screen_h = (self.h + 2) * self.tile_size
        self.tiles = [
            pygame.transform.scale(
                pygame.image.load(f"images/maze/{i}.png"),
                (self.tile_size, self.tile_size)) for i in range(32)]
        self.screen = pygame.display.set_mode((info.current_w, info.current_h))
        pygame.display.set_caption("Pac-Man")
        self.maze_surface = pygame.Surface(
            (self.screen_w, self.screen_h)
        )
        self.build_maze()

    def build_maze(self):
        for i, row in enumerate(self.maze):
            for j, col in enumerate(row):
                self.draw_cell(col, i, j)
                # pygame.draw.rect(self.maze_surface, "#659e65", (j * self.tile_size, i * self.tile_size, self.tile_size, self.tile_size), 1)

    def draw_maze(self):
        self.screen.blit(self.maze_surface, (self.pad, self.pad))

    def draw_cell(self, col, i, j):
        self.maze_surface.blit(self.tiles[col],
                               (j * self.tile_size, i * self.tile_size))

    def op_pos_px(self, xy: tuple, op: callable, value: int):
        x, y = xy
        return op(x, value), op(y, value)

    def draw_entity(self, entity):
        xy = self.op_pos_px(entity.position, mul, self.tile_size) # get_offset
        xy = self.op_pos_px(xy, sub, self.half_size) # centrage
        self.maze_surface.blit(entity.surf, xy)
        self.screen.blit(self.maze_surface, (self.pad, self.pad))
