from pydantic import dataclass
from ..entitys.entity import Entity
from ..entitys.direction import Dir


@dataclass
class Player(Entity):
    desired_direction: Dir
