import pygame
from .direction import Dir

class Player:
    def __init__(self, y, x, tile_size):
        self.y = y
        self.x = x
        self.off_x = 0
        self.off_y = 0
        self.last_offset = (0, 0)
        self.dir = Dir.E
        self.next_dir = Dir.E
        self.tile = pygame.Rect(0, 0, tile_size, tile_size)
