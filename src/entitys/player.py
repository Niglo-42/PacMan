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

    def update_desire(self, maze: Maze) -> bool:
        if maze.is_open(self.position, self.desired_direction):
            self.direction = self.desired_direction

    def update(self, maze: Maze) -> bool:
        self._input()
        self.update_desire(maze)
        return self.update_position(maze)

        # print(f"{self.position=}")
