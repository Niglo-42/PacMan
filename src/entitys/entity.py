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

    def update_position(self) -> None:
        """
        sauvegarde où on était avant pour la suppression opti
        ajoute les pixels dans la direction en cours
        puis réajuste l'offset
        réajuste aussi la position en cours en coupant les 3 bits basses
        """
        # self.last_px_pos = self.px_pos
        # x, y = self.direction.add_delta(self.px_pos, self.speed)
        # self.px_pos = (x, y)
        # self.offset_xy = (x & 7, y & 7)
        # self.cell_xy = (x >> 3, y >> 3)

    def update_direction_player(self, maze: Maze) -> None:
        pass
        # if maze.is_open(self.tile_xy, self.desired_direction):
        #     self.direction = self.desired_direction