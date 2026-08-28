# from pydantic import dataclass
# dis moi pk ct la dataclass de pydantic
from dataclasses import dataclass
from .direction import Dir
from pygame import Surface
from ..models.maze import Maze
import numpy as np


@dataclass
class Entity:
    direction: Dir
    speed: int
    id: int
    accumulator: float
    alive: bool
    offset_xy: tuple[int, int]
    position: tuple[int, int]
    tiles: list[Surface]
    surf: Surface
    anim: list[int]
    idx_anim: int
    dir_anim: int


    def update_position(self, maze: Maze) -> None:
        moved = False
        if not maze.is_open(self.position, self.direction):
            return
        x, y = self.position
        d_x, d_y = self.direction.add_delta_speed_f(self.offset_xy, self.speed)
        if d_x >= 8:
            moved = True
            d_x = 0
            x += 1
        elif d_x <= -8:
            moved = True
            d_x = 0
            x -= 1
        elif d_y > 8:
            moved = True
            d_y = 0
            y += 1
        elif d_y <= -8:
            moved = True
            d_y = 0
            y -= 1
        if moved:
            if maze.map[y][x] == 1:
                self.score += 10 # a modifier
                self.total_pellet += 1
            elif maze.map[y][x] == 2:
                self.score += 50
                #afraid mode
        self.position = (x, y)
        self.offset_xy = (d_x, d_y)
