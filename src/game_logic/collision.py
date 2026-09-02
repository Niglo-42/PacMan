from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..entitys.ghosts import Ghost
    from ..entitys.player import Player
    from ..game import Game


def check_collision(self: Game, player: Player, ghosts: list[Ghost]) -> None:
    from ..entitys.ghosts import GhostMode
    for ghost in ghosts:
        if ghost.mode == GhostMode.EYES:
            continue
        if ghost.position == player.position:
            # à creuser: bug trouvé -> passé à travers un fantome dans
            # un virage a cause du fast turn
            # plus permissif pour meilleur visuel? si chaque entité d'un
            # bout et l'autre d'une tile, soit 8 pixels d'écart, ça touche
            if ghost.mode == GhostMode.CHASE or \
                    ghost.mode == GhostMode.SCATTER:
                if self.player_died(player, ghosts) <= 0:
                    self.game_is_over()
            elif ghost.mode == GhostMode.FRIGHTENED:
                ghost.alive = False
                ghost.mode = GhostMode.EYES
                ghost.target = self.maze.get_opposite_corner(ghost.position)
                player.score += self.point_per_ghost * \
                    sum([not g.alive for g in ghosts])
