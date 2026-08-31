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
    spawn: tuple[int, int] = (0, 0)
    position: tuple[int, int] = (0, 0)
    tiles: list[Surface] = field(default_factory=list)
    surf: Surface = None
    anim: list[int] = field(default_factory=list)
    idx_anim: int = 0
    name: str = ""

    def update_position(self, maze: Maze) -> None:
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

    def update_ghost_tile(self, ghost_afraid, eyes, afraid_end):
        self.surf.fill(0)
        if eyes:
            self.surf.blit(ghost_afraid[self.direction.value[5]], (0, 0))
        else:
            self.surf.blit(ghost_afraid[self.idx_anim >> 3 - 1 * (afraid_end)],
                           (0, 0))

    def update_tile(self) -> None:
        self.surf.fill(0)
        self.surf.blit(
            self.tiles[self.anim[self.direction.value[3]][self.idx_anim >> 2]],
            (0, 0))
        self.idx_anim += 1
        self.idx_anim &= 0xf
