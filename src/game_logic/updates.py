from __future__ import annotations
from typing import TYPE_CHECKING
from .speed import update_speeds
from .collision import check_collision
from .ghosts_state import modify_ghosts_state, update_ghosts_state
from ..interface.drawing import draw_lives

if TYPE_CHECKING:
    from ..game import Game
    from ..entitys.player import Player


def update_entitys(self: Game) -> None:
    if self.player2:
        self.player2.update(self.maze)
    self.player.update(self.maze)
    for g in self.ghosts:
        g.update(self.player, self.maze, self.ghosts_state,
                 (self.global_timer - self.frightened_timer)
                 >= self.fps * 5)


def update_game_state(self: Game):
    from ..entitys.ghosts import GhostMode
    if self.eaten_pellet == self.total_pellet:
        self.level_is_won()
    self.global_timer += 1
    update_speeds(self.level, self.ghosts, self.player, self.ghosts_state)
    check_collision(self, self.player, self.ghosts)

    if update_pellets(self, self.player, self.maze.map) or \
            update_pellets(self, self.player2, self.maze.map):
        # si une pacman a été mangé
        self.frightened_timer = self.global_timer
        modify_ghosts_state(self, GhostMode.FRIGHTENED)
    update_ghosts_state(self)
    draw_lives(self)


def update_pellets(self: Game, player: Player, map: list[list[int]]) -> bool:
    # return True quand energizer a été mangé
    energizer = False
    if player and (player.offset_xy) == (0, 0):
        x, y = player.position
        if map[y][x] == 1:
            player.score += self.points_per_pacgum
            self.eaten_pellet += 1
        elif map[y][x] == 2:
            player.score += self.points_per_super_pacgum
            energizer = True
        map[y][x] = 0
        self.render.draw_cell(0, y, x)
    elroy_mode(self)
    return energizer


def elroy_mode(self: Game) -> None:
    from ..entitys.ghosts import GhostMode
    triggers = {1: [20, 10],
                2: [30, 15],
                3: [40, 20],
                6: [50, 25],
                9: [60, 30],
                12: [80, 40],
                15: [100, 50],
                19: [120, 60]}

    target_lvl = max(lvl for lvl in triggers if lvl <= self.level)
    dots = triggers[target_lvl]

    if (self.total_pellet - self.eaten_pellet) <= dots[0] <= dots[1] and\
            self.ghosts_state != GhostMode.FRIGHTENED:
        self.ghosts[0].mode = GhostMode.ELROY1
        return
    if self.total_pellet - self.eaten_pellet <= dots[1] and\
            self.ghosts_state != GhostMode.FRIGHTENED:
        self.ghosts[0].mode = GhostMode.ELROY2
