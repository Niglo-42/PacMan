import pygame
from .entitys.entity import Entity
from .entitys.player import Player
from .entitys.direction import Dir
from .maze import Maze

def update_position(entity: Entity) -> None:
    """
    sauvegarde où on était avant pour la suppression opti
    ajoute les pixels dans la direction en cours
    puis réajuste l'offset
    réajuste aussi la position en cours en coupant les 3 bits basses
    """
    entity.last_px_pos = entity.px_pos
    x, y = entity.direction.add_delta(entity.px_pos, entity.speed)
    entity.px_pos = (x, y)
    entity.offset_xy = (x & 7, y & 7)
    entity.cell_xy = (x >> 3, y >> 3)

