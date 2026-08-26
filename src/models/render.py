import pygame
from operator import add, mul

class Render:
    def __init__(self, maze, w, h):
        self.w = w
        self.h = h
        self.maze = maze
        info = pygame.display.Info()
        self.tile_size = 8
        ratio = min(info.current_h // (self.h + 2),
                    info.current_w // (self.w + 2))
        self.scale = ratio // (self.tile_size * 3)
        self.tile_size *= self.scale
        self.cell_size = self.tile_size * 3
        self.pad = self.cell_size
        self.screen_w = (self.w + 2) * self.pad
        self.screen_h = (self.h + 2) * self.pad
        self.tiles = [
            pygame.transform.scale(
                pygame.image.load(f"images/maze/{i}.png"),
                (self.tile_size, self.tile_size)) for i in range(32)]
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        pygame.display.set_caption("Pac-Man")
        self.maze_surface = pygame.Surface(
            (self.screen_w, self.screen_h)
        )
        self.build_maze()

    def build_maze(self):
        for i, row in enumerate(self.maze):
            for j, cell in enumerate(row):
                self.draw_cell(self.maze_surface, cell, i, j)

    def draw_maze(self):
        self.screen.blit(self.maze_surface, (0, 0))
        pygame.display.flip()

    def draw_cell(self, surface, cell, i, j):
        for y, row in enumerate(cell.tiles):
            for x, col in enumerate(row):
                surface.blit(
                self.tiles[cell.get_tile(y, x)],
                (self.pad + j * self.cell_size + x * self.tile_size ,
                self.pad + i * self.cell_size + y * self.tile_size))

    def op_pos_px(self, xy: tuple, op: callable, value: int):
        x, y = xy
        return op(x, value), op(y, value)

    def draw_entity(self, entity):
        xy = self.op_pos_px(entity.tile_xy, mul, self.tile_size)
        xy = self.op_pos_px(xy, add, self.pad)
        self.screen.blit(entity.tiles[1], xy)
