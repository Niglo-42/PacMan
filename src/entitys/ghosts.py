from dataclasses import dataclass
from enum import Enum, auto
from ..entitys.entity import Entity
from ..entitys.player import Player


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
    target: tuple[int, int] = (0, 0)

    def update(self, player: Player) -> None:
        self.accumulator += self.speed
        while self.accumulator >= 1:
            pass

    @property
    def get_target(self, player: Player) -> tuple[int, int]:
        raise NotImplementedError


class Blinky(Ghost):
    def __init__(self, spawn: tuple[int, int]):
        self.name = "Blinky"
        self.spawn = spawn

    @property
    def get_target(self, player: Player) -> tuple[int, int]:
        pass


class Pinky(Ghost):
    def __init__(self, spawn: tuple[int, int]):
        self.name = "Pinky"
        self.spawn = spawn


class Inky(Ghost):
    def __init__(self, spawn: tuple[int, int]):
        self.name = "Inky"
        self.spawn = spawn
        self.blinky = Blinky


class Clyde(Ghost):
    def __init__(self, spawn: tuple[int, int]):
        self.name = "Clyde"
        self.spawn = spawn
