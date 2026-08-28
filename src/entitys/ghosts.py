from dataclasses import dataclass
from enum import Enum, auto
from ..entitys.entity import Entity
from ..entitys.player import Player
from ..entitys.direction import Dir
from ..models.maze import Maze
import numpy as np
import pygame


class GhostMode(Enum):
    SCATTER = auto()
    CHASE = auto()
    FRIGHTENED = auto()
    EYES = auto()
    CAGED = auto()
    EXITING = auto()
    ENTERING = auto()


@dataclass
class Ghost(Entity):
    name: str = ""
    mode: GhostMode = GhostMode.CHASE
    spawn: tuple[int, int] = (0, 0)
    target: tuple[int, int] = (0, 0)

    def update(self, player: Player, maze: Maze) -> None:
        if self.offset_xy == (0, 0):
            self.target = self.get_target(player)
            self.update_dir(self.target, maze)
        self.update_ghost_position(maze)

    def update_dir(self, target: tuple[int, int], maze: Maze):
        banned = [self.direction.opposite, Dir.X]
        candidates = [d for d in Dir if maze.is_open(self.position, d)
                      and d not in banned]
        if not candidates:
            return self.actual_direction.opposite
        best_c = None
        best_dist = float("inf")
        for c in candidates:
            tried_pos = c.add_delta_speed(self.position, 1)
            distance = np.linalg.norm(np.subtract(target, tried_pos))
            if distance < best_dist:
                best_dist = distance
                best_c = c
            continue
        self.direction = best_c

    def get_target(self, player: Player) -> tuple[int, int]:
        if self.mode == GhostMode.EYES or self.mode == GhostMode.SCATTER:
            return self.spawn
        elif self.mode == GhostMode.FRIGHTENED:
            return self.frightened_pos(self.position, player.position)
        raise NotImplementedError

    def frightened_pos(self, ghost_pos: tuple[int, int],
                       player_pos: tuple[int, int]) -> tuple[int, int]:
        diff_x = ghost_pos[0] - player_pos[0]
        diff_y = ghost_pos[1] - player_pos[1]
        target = (ghost_pos[0] + diff_x, ghost_pos[1] + diff_y)
        return target


class Blinky(Ghost):
    def __init__(self, spawn: tuple[int, int]):
        super().__init__()
        self.name = "Blinky"
        self.spawn = spawn
        self.position = spawn
        self.surf = pygame.Surface((32, 32))
        self.surf.fill((255, 0, 0))

    def get_target(self, player: Player) -> tuple[int, int]:
        if self.mode == GhostMode.CHASE:
            return player.position
        return super().get_target(player)


class Pinky(Ghost):
    def __init__(self, spawn: tuple[int, int]):
        super().__init__()
        self.name = "Pinky"
        self.spawn = spawn
        self.position = spawn
        self.surf = pygame.Surface((32, 32))
        self.surf.fill((255, 184, 255))

    def get_target(self, player: Player) -> tuple[int, int]:
        if self.mode == GhostMode.CHASE:
            return player.direction.add_delta_speed(player.position, 4)
        return super().get_target(player)


class Inky(Ghost):
    def __init__(self, spawn: tuple[int, int]):
        super().__init__()
        self.name = "Inky"
        self.spawn = spawn
        self.blinky = Blinky
        self.position = spawn
        self.surf = pygame.Surface((32, 32))
        self.surf.fill((0, 255, 255))

    def get_target(self, player):
        if self.mode == GhostMode.CHASE:
            player_x, player_y = player.position
            d_x, d_y = player.direction.delta
            pivot = (player_x + 2 * d_x, player_y + 2 * d_y)
            blinky_x, blinky_y = self.blinky.position
            target = (2 * pivot[0] - blinky_x, 2 * pivot[1] - blinky_y)
            return target
        return super().get_target(player)


class Clyde(Ghost):
    def __init__(self, spawn: tuple[int, int]):
        super().__init__()
        self.name = "Clyde"
        self.spawn = spawn
        self.position = spawn
        self.surf = pygame.Surface((32, 32))
        self.surf.fill((255, 184, 82))

    def get_target(self, player):
        if self.mode == GhostMode.CHASE:
            dist = np.linalg.norm(np.subtract(self.position, player.position))
            if dist < 8:
                return self.spawn
            return player.position
        return super().get_target(player)
