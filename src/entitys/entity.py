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

    # def update_position(self) -> None:
    #     """
    #     sauvegarde où on était avant pour la suppression opti
    #     ajoute les pixels dans la direction en cours
    #     puis réajuste l'offset
    #     réajuste aussi la position en cours en coupant les 3 bits basses
    #     """
    #     self.last_position = self.position
    #     x, y = self.direction.add_delta(self.direction.delta[0], self.direction.delta[1])
    #     self.offset_xy = (x & 7, y & 7)     # == % 8
    #     self.position = (x >> 3, y >> 3)     # == // 8

    def update_position(self, maze: Maze) -> bool:
        if not maze.is_open(self.position, self.direction):
            return
        moved = False
        x, y = self.position
        d_x, d_y = self.direction.add_delta(*self.offset_xy)
        if (0 <= x <= maze.width - 1) and (0 <= y <= maze.height - 1):
            if d_x == 8:
                moved = True
                d_x = 0
                x += 1
            elif d_x == -1:
                moved = True
                d_x = 7
                x -= 1
            elif d_y == 8:
                moved = True
                d_y = 0
                y += 1
            elif d_y == -1:
                moved = True
                d_y = 7
                y -= 1
        self.position = (x, y)
        self.offset_xy = (d_x, d_y)
        print(self.offset_xy)
        return moved
