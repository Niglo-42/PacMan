from dataclasses import dataclass
from enum import Enum, auto
from ..entitys.entity import Entity
from ..models.maze import Maze


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

    def get_spawn(self, maze: Maze):
        pass


class Blinky(Ghost):
    def __init__(self):
        self.name = "Blinky"
        self.spawn = self.get_spawn()


class Pinky(Ghost):
    def __init__(self):
        self.name = "Pinky"
        self.spawn = self.get_spawn()


class Inky(Ghost):
    def __init__(self):
        self.name = "Inky"
        self.spawn = self.get_spawn()


class Clyde(Ghost):
    def __init__(self):
        self.name = "Clyde"
        self.spawn = self.get_spawn()
