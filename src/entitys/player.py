# from pydantic import dataclass
from dataclasses import dataclass
from ..entitys.entity import Entity
from ..models.maze import Maze
from ..entitys.direction import Dir
import pygame
import numpy as np


@dataclass
class Player(Entity):
    desired_direction: Dir

    def _input(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.desired_direction = Dir.N
        elif keys[pygame.K_DOWN]:
            self.desired_direction = Dir.S
        elif keys[pygame.K_RIGHT]:
            self.desired_direction = Dir.E
        elif keys[pygame.K_LEFT]:
            self.desired_direction = Dir.W

    def update(self, maze) -> None:
        self._input()
        self.update_desire(maze)
        self.update_position(maze)

    def update_desire(self, maze: Maze) -> bool:
        if maze.is_open(self.position, self.desired_direction):
            self.direction = self.desired_direction

    def update_position(self, maze: Maze) -> None:
        if not maze.is_open(self.position, self.direction):
            return
        x, y = self.position
        self.last_position = (x, y)
        d_x, d_y = tuple(np.add(self.offset_xy, self.direction.delta))
        if (0 <= x <= maze.width - 1) and (0 <= y <= maze.height - 1):
            if d_x == 8:
                d_x = 0
                x += 1
            elif d_x == -1:
                d_x = 7
                x -= 1
            elif d_y == 8:
                d_y = 0
                y += 1
            elif d_y == -1:
                d_y = 7
                y -= 1
        self.position = (x, y)
        self.offset_xy = (d_x, d_y)
