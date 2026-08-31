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
    mode: GhostMode = GhostMode.SCATTER
    spawn: tuple[int, int] = (0, 0)
    target: tuple[int, int] = (0, 0)
    fright_timer: float = 5.0
    changing_side: bool = False

    _afraid: list[pygame.Surface] | None = None
    _eyes: list[pygame.Surface] | None = None

    @staticmethod
    def _load_tiles(start: int, end: int, size: int) -> list[pygame.Surface]:
        return [
            pygame.transform.scale(
                pygame.image.load(f"images/sprites/{str(i).zfill(3)}.png").convert_alpha(),
                (size * 2, size * 2)
            )
            for i in range(start, end)
        ]

    @classmethod
    def load_common_tiles(cls, size: int) -> None:
        if cls._afraid is None:
            cls._afraid = cls._load_tiles(49, 53, size)
        if cls._eyes is None:
            cls._eyes = cls._load_tiles(61, 65, size)

    @property
    def afraid(self) -> list[pygame.Surface]:
        return Ghost._afraid

    @property
    def eyes(self) -> list[pygame.Surface]:
        return Ghost._eyes

    def update(self, player: Player, maze: Maze, ghoststate: GhostMode,
               afraid_end: bool) -> None:
        if self.mode == GhostMode.EYES and self.position == self.spawn:
            self.mode = ghoststate
        if self.offset_xy == (0, 0):
            if not self.changing_side:
                self.target = self.get_target(player)
                self.update_dir(self.target, maze)
            else:
                self.direction = self.direction.opposite
                self.changing_side = False
        self.update_position(maze)
        if self.mode == GhostMode.EYES:
            self.update_ghost_tile(Ghost._eyes, True, afraid_end)
        elif self.mode == GhostMode.FRIGHTENED:
            self.update_ghost_tile(Ghost._afraid, False, afraid_end)
        else:
            self.update_tile()

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
    def __init__(self, spawn: tuple[int, int], size):
        super().__init__()
        self.name = "Blinky"
        self.spawn = spawn
        self.position = spawn
        self.anim = [
                    [4, 5, 4, 5],  # n
                    [0, 1, 0, 1],  # e
                    [6, 7, 6, 7],  # s
                    [2, 3, 2, 3]   # w
                ]
        self.surf = pygame.Surface((size * 2,
                                    size * 2),
                                   pygame.SRCALPHA)
        self.tiles = [
            pygame.transform.scale(
                pygame.image.load(
                    f"images/sprites/{str(i).zfill(3)}."
                    "png").convert_alpha(),
                (size * 2,
                 size * 2)) for i in range(41, 49, 1)]

    def get_target(self, player: Player) -> tuple[int, int]:
        if self.mode == GhostMode.CHASE:
            return player.position
        return super().get_target(player)


class Pinky(Ghost):
    def __init__(self, spawn: tuple[int, int], size):
        super().__init__()
        self.name = "Pinky"
        self.spawn = spawn
        self.position = spawn
        self.anim = [
                    [4, 5, 4, 5],  # n
                    [0, 1, 0, 1],  # e
                    [6, 7, 6, 7],  # s
                    [2, 3, 2, 3]   # w
                ]
        self.surf = pygame.Surface((size * 2,
                                    size * 2),
                                   pygame.SRCALPHA)
        self.tiles = [
            pygame.transform.scale(
                pygame.image.load(
                    f"images/sprites/{str(i).zfill(3)}."
                                    "png").convert_alpha(),
                (size * 2,
                 size * 2)) for i in range(53, 61, 1)]

    def get_target(self, player: Player) -> tuple[int, int]:
        if self.mode == GhostMode.CHASE:
            return player.direction.add_delta_speed(player.position, 4)
        return super().get_target(player)


class Inky(Ghost):
    def __init__(self, spawn: tuple[int, int], size):
        super().__init__()
        self.name = "Inky"
        self.spawn = spawn
        self.blinky = Blinky
        self.position = spawn
        self.anim=[
                    [4, 5, 4, 5],  # n
                    [0, 1, 0, 1],  # e
                    [6, 7, 6, 7],  # s
                    [2, 3, 2, 3]   # w
                ]
        self.surf = pygame.Surface((size * 2,
                                size * 2),
                                pygame.SRCALPHA)
        self.tiles = [
            pygame.transform.scale(
                pygame.image.load(
                    f"images/sprites/{str(i).zfill(3)}."
                                    "png").convert_alpha(),
                (size * 2,
                 size * 2)) for i in range(65, 73, 1)]

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
    def __init__(self, spawn: tuple[int, int], size):
        super().__init__()
        self.name = "Clyde"
        self.spawn = spawn
        self.position = spawn
        self.anim=[
                    [4, 5, 4, 5],  # n
                    [0, 1, 0, 1],  # e
                    [6, 7, 6, 7],  # s
                    [2, 3, 2, 3]   # w
                ]
        self.surf = pygame.Surface((size * 2,
                                size * 2),
                                pygame.SRCALPHA)
        self.tiles = [
            pygame.transform.scale(
                pygame.image.load(
                    f"images/sprites/{str(i).zfill(3)}."
                                    "png").convert_alpha(),
                (size * 2,
                 size * 2)) for i in range(78, 86, 1)]

    def get_target(self, player):
        if self.mode == GhostMode.CHASE:
            dist = np.linalg.norm(np.subtract(self.position, player.position))
            if dist < 8:
                return self.spawn
            return player.position
        return super().get_target(player)
