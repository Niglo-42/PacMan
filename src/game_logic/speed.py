from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..entitys.ghosts import Ghost, GhostMode
    from ..entitys.player import Player

BASE_SPEED = 1.7

#  normal / normal dots / fright / fright dots
PAC_MAN_SPEED = [[0.8, 0.71, 0.9, 0.79],  # 1
                 [0.9, 0.79, 0.95, 0.83],  # 2-4
                 [1, 0.87, 1, 0.87],  # 5 -20
                 [0.9, 0.79, 1, 1]]  # 21+

#  normal / fright / tunnel / elroy1 / elroy 2
GHOST_SPEED = [[0.75, 0.5, 0.4, 0.8, 0.85],  # 1
               [0.85, 0.55, 0.4, 0.9, 0.95],  # 2-4
               [0.95, 0.6, 0.5, 1, 1.05],  # 5-20
               [0.95, 1, 0.5, 1, 1.05]]  # 21+


def update_speeds(level: int, ghosts: list[Ghost], player: Player,
                  ghoststate: GhostMode) -> None:
    for ghost in ghosts:
        update_ghost_speed(level, ghost)
    update_player_speed(level, player, ghoststate)


def update_ghost_speed(level: int, ghost: Ghost) -> None:
    from ..entitys.ghosts import GhostMode
    if level == 1:
        range = GHOST_SPEED[0]
    elif level <= 4:
        range = GHOST_SPEED[1]
    elif level <= 20:
        range = GHOST_SPEED[2]
    else:
        range = GHOST_SPEED[3]

    if ghost.mode == GhostMode.EYES:
        ghost.speed = BASE_SPEED * 1.25
    elif ghost.mode == GhostMode.FRIGHTENED:
        ghost.speed = range[1] * BASE_SPEED
    elif ghost.mode == GhostMode.ELROY1:
        ghost.speed = range[3] * BASE_SPEED
    elif ghost.mode == GhostMode.ELROY2:
        ghost.speed = range[4] * BASE_SPEED
    else:
        ghost.speed = range[0] * BASE_SPEED


def update_player_speed(level: int, player: Player, ghoststate: GhostMode):
    from ..entitys.ghosts import GhostMode
    if level == 1:
        range = PAC_MAN_SPEED[0]
    elif level <= 4:
        range = PAC_MAN_SPEED[1]
    elif level <= 20:
        range = PAC_MAN_SPEED[2]
    else:
        range = PAC_MAN_SPEED[3]

    if ghoststate == GhostMode.FRIGHTENED:
        player.speed = range[2] * BASE_SPEED
    else:
        player.speed = range[0] * BASE_SPEED
