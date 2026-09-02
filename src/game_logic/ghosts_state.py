from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..entitys.ghosts import GhostMode
    from ..game import Game

FRIGHT_TIMER = 7

#  SCATTER / CHASE alternance
PHASE_DURATIONS = [[7, 20, 7, 20, 5, 20, 5],
                   [7, 20, 7, 20, 5, 1033, 1/60],
                   [5, 20, 5, 20, 5, 1037, 1/60]]


def update_ghosts_state(self: Game) -> None:
    from ..entitys.ghosts import GhostMode
    states = [GhostMode.SCATTER, GhostMode.CHASE]
    acc_state, state_timer = self.state_timer

    if self.level <= 1:
        level_index = 0
    elif self.level <= 4:
        level_index = 1
    else:
        level_index = 2

    if self.ghosts_state == GhostMode.FRIGHTENED:
        if (self.global_timer - self.frightened_timer) >= (
                self.fps * FRIGHT_TIMER):
            modify_ghosts_state(self, GhostMode.CHASE)
    else:
        length = len(PHASE_DURATIONS[level_index])
        if acc_state < length:
            phase_duration = PHASE_DURATIONS[level_index][acc_state]
            if (self.global_timer - state_timer) >= \
                    (phase_duration * self.fps):
                acc_state += 1
                state_timer = self.global_timer
                modify_ghosts_state(self, states[acc_state & 1])

            self.state_timer = (acc_state, state_timer)
        else:
            modify_ghosts_state(self, GhostMode.CHASE)


def modify_ghosts_state(self: Game, state: GhostMode) -> None:
    from ..entitys.ghosts import GhostMode
    self.ghosts_state = state
    for g in self.ghosts:
        if g.mode != GhostMode.EYES and g.mode != state:
            g.mode = state
            g.changing_side = True
