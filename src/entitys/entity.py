# from pydantic import dataclass
# dis moi pk ct la dataclass de pydantic
from dataclasses import dataclass
from ..entitys.direction import Dir
from pygame import Surface

@dataclass
class Entity:
    direction: Dir
    speed: int
    accumulator: float
    alive: bool
    offset_xy: tuple[int, int]
    tile_xy: tuple[int, int]
    cell_xy: tuple[int, int]
    px_pos: tuple[int, int]
    last_px_pos: tuple[int, int]
    anim_frame: int
    tiles: list[Surface]