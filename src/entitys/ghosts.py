from pydantic import dataclass
from enum import Enum, auto
from ..entitys.entity import Entity


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
    mode: GhostMode = GhostMode.CAGED
