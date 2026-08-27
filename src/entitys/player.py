# from pydantic import dataclass
from dataclasses import dataclass
from ..entitys.entity import Entity
from ..models.maze import Maze
from ..entitys.direction import Dir
import pygame


@dataclass
class Player(Entity):
    desired_direction: Dir
    total_pellet: int
    score: int

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

    def update_desire(self, maze: Maze) -> None:
        if self.offset_xy != (0, 0):
            return
        if self.direction == self.desired_direction:
            return
        if maze.is_open(self.position, self.desired_direction):
            self.direction = self.desired_direction
            self.dir_anim = self.direction.get_idx

    def update_tile(self):
        self.surf.fill(0)
        self.surf.blit(
            self.tiles[
                self.anim[
                    self.dir_anim][
                        self.idx_anim >> 2
                    ]], (0, 0))
        self.idx_anim += 1
        self.idx_anim &= 0xf

    def update(self, maze: Maze, tile_size: int) -> None:
        self._input()
        self.update_desire(maze)
        self.update_position(maze)
        self.update_tile()
        if (self.total_pellet == 70) and maze.flag_fruit == 0:
            maze.flag_fruit = 0b1
            maze.add_fruit(self.position, tile_size)
        elif (self.total_pellet == 170) and maze.flag_fruit == 1:
            maze.flag_fruit = 0b11
            maze.add_fruit(self.position, tile_size)