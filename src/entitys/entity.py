# from pydantic import dataclass
# dis moi pk ct la dataclass de pydantic
from dataclasses import dataclass, field
from .direction import Dir
from pygame import Surface
from ..models.maze import Maze


@dataclass
class Entity:
    direction: Dir = Dir.X
    speed: int = 1
    id: int = 0
    accumulator: float = 0.0
    alive: bool = True
    offset_xy: tuple[int, int] = (0, 0)
    position: tuple[int, int] = (0, 0)
    tiles: list[Surface] = field(default_factory=list)
    surf: Surface = None
    anim: list[int] = field(default_factory=list)
    idx_anim: int = 0
    dir_anim: int = 0

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
                self.score += 10  # a modifier
                self.total_pellet += 1
            elif maze.map[y][x] == 2:
                self.score += 50
                # afraid mode
        self.position = (x, y)
        self.offset_xy = (d_x, d_y)

    def update_ghost_position(self, maze: Maze) -> None:
        if not maze.is_open(self.position, self.direction):
            return
        x, y = self.position
        d_x, d_y = self.direction.add_delta_speed_f(self.offset_xy, self.speed)
        if d_x >= 8:
            d_x = 0
            x += 1
        elif d_x <= -8:
            d_x = 0
            x -= 1
        elif d_y > 8:
            d_y = 0
            y += 1
        elif d_y <= -8:
            d_y = 0
            y -= 1
        self.position = (x, y)
        self.offset_xy = (d_x, d_y)
