# from pydantic import dataclass
# dis moi pk ct la dataclass de pydantic
from dataclasses import dataclass
from .direction import Dir
from pygame import Surface
from ..models.maze import Maze


@dataclass
class Entity:
    direction: Dir
    speed: int
    accumulator: float
    alive: bool
    offset_xy: tuple[int, int]
    position: tuple[int, int]
    tiles: list[Surface]
    last_position: tuple[int, int]

    # def update_position(self) -> None:
    #     """
    #     sauvegarde où on était avant pour la suppression opti
    #     ajoute les pixels dans la direction en cours
    #     puis réajuste l'offset
    #     réajuste aussi la position en cours en coupant les 3 bits basses
    #     """
    #     self.last_position = self.position
    #     x, y = self.direction.add_delta(self.direction.delta[0], self.direction.delta[1])
    #     self.offset_xy = (x & 7, y & 7)     # == % 8
    #     self.position = (x >> 3, y >> 3)     # == // 8


