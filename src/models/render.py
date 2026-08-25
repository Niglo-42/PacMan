import pygame

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
        self.pad = self.tile_size * 3
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
                (self.pad + j * self.tile_size * 3 + x * self.tile_size ,
                self.pad + i * self.tile_size * 3 + y * self.tile_size))