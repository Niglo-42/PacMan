from dataclasses import dataclass
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
    spawn: tuple[int, int] = (0, 0)

    


class Blinky(Ghost):
    def __init__(self, spawn: tuple[int, int]):
        self.name = "Blinky"
        self.spawn = spawn


class Pinky(Ghost):
    def __init__(self, spawn: tuple[int, int]):
        self.name = "Pinky"
        self.spawn = spawn


class Inky(Ghost):
    def __init__(self, spawn: tuple[int, int]):
        self.name = "Inky"
        self.spawn = spawn


class Clyde(Ghost):
    def __init__(self, spawn: tuple[int, int]):
        self.name = "Clyde"
        self.spawn = spawn
