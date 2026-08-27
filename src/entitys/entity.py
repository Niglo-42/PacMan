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
    accumulator: float
    alive: bool
    offset_xy: tuple[int, int]
    position: tuple[int, int]
    tiles: list[Surface]
    surf: Surface


    def update_position(self, maze: Maze) -> None:
        if not maze.is_open(self.position, self.direction):
            return
        x, y = self.position
        d_x, d_y = self.direction.add_delta(*self.offset_xy)
        if d_x == 8:
            d_x = 0
            x += 1
        elif d_x == -8:
            d_x = 0
            x -= 1
        elif d_y == 8:
            d_y = 0
            y += 1
        elif d_y == -8:
            d_y = 0
            y -= 1
        self.position = (x, y)
        self.offset_xy = (d_x, d_y)
