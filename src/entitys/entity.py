from pydantic import dataclass
from ..entitys.direction import Dir


@dataclass
class Entity:
    d_x: int
    d_y: int
    col: int
    row: int
    offset_x: int
    offset_y: int
    direction: Dir
    accumulator: float
    speed: float
    alive: bool
    anim_frame: int
