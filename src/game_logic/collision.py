from __future__ import annotations
from typing import TYPE_CHECKING
from ..entitys.ghosts import GhostMode
import math

if TYPE_CHECKING:
    from ..entitys.ghosts import Ghost
    from ..entitys.player import Player
    from ..game import Game


def check_collision(self: Game, player: Player, ghosts: list[Ghost]) -> None:
    for ghost in ghosts:
        if ghost.mode == GhostMode.EYES:
            continue
        if offset_detection(self, ghost, player) or \
                swept_check_detection(self, ghost, player):
            if ghost.mode.is_lethal:
                if self.player_died(player, ghosts) <= 0:
                    self.game_is_over()
            elif ghost.mode == GhostMode.FRIGHTENED:
                ghost.alive = False
                ghost.mode = GhostMode.EYES
                ghost.target = self.maze.get_opposite_corner(ghost.position)
                player.score += self.point_per_ghost * \
                    sum([not g.alive for g in ghosts])


def offset_detection(self: Game, ghost: Ghost, player: Player) -> bool:
    center_tile_size = self.render.half_size
    hitbox = center_tile_size * 0.7
    px, py = player.position
    pox, poy = player.offset_xy
    p_absolute_pos = (px * center_tile_size + pox, py * center_tile_size + poy)

    gx, gy = ghost.position
    gox, goy = ghost.offset_xy
    g_absolute_pos = (gx * center_tile_size + gox, gy * center_tile_size + goy)

    dist = math.dist(p_absolute_pos, g_absolute_pos)
    if dist <= hitbox:
        return True
    return False


def swept_check_detection(self: Game, ghost: Ghost, player: Player) -> bool:
    if ghost.position == player.last_pos and ghost.last_pos == player.position:
        return True
    return False
