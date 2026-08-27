import pygame
from operator import add, mul, sub
from .maze import Maze

class Render:
    def __init__(self, maze: Maze):
        info = pygame.display.Info()
        pygame.display.set_caption("Pac-Man")
        self.screen = pygame.display.set_mode((info.current_w, info.current_h))

        self.h = maze.height
        self.w = maze.width

        self.maze = maze
        self.tile_size = 8
        ratio = min(info.current_h // (self.h + 2),
                    info.current_w // (self.w + 2))
        self.scale = max(1, ratio // (self.tile_size))
        self.tile_size *= self.scale
        self.half_size = self.tile_size // 2
        self.pad = self.tile_size

        self.screen_w = (self.w) * self.tile_size
        self.screen_h = (self.h) * self.tile_size
        self.maze.tiles = [
            pygame.transform.scale(
                pygame.image.load(f"images/maze/{i}.png"),
                (self.tile_size, self.tile_size)) for i in range(32)]
        self.maze.surf = pygame.Surface(
            (self.screen_w, self.screen_h)
        )
        self.build_maze()

    def build_maze(self):
        for i, row in enumerate(self.maze.map):
            for j, col in enumerate(row):
                self.draw_cell(col, i, j)
                # pygame.draw.rect(self.maze_surface, "#659e65", (j * self.tile_size, i * self.tile_size, self.tile_size, self.tile_size), 1)

    def draw_maze_on_surf_screen(self):
        self.screen.blit(self.maze.surf, (self.pad, self.pad))

    def draw_cell(self, col, i, j):
        self.maze.surf.blit(self.maze.tiles[col],
                               (j * self.tile_size, i * self.tile_size))

    def op_pos_px(self, xy: tuple, op: callable, value: int):
        x, y = xy
        return op(x, value), op(y, value)

    def draw_entity(self, entity):
        xy = self.op_pos_px(entity.position, mul, self.tile_size) # get_offset
        xy = self.op_pos_px(xy, sub, self.half_size) # centrage
        xy = self.op_pos_px(xy, add, self.pad)
        self.screen.blit(entity.surf, xy)
