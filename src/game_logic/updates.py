from __future__ import annotations
from typing import TYPE_CHECKING
from .speed import update_speeds
from .collision import check_collision
from ..interface.drawing import draw_lives, draw_fruits

if TYPE_CHECKING:
    from ..game import Game
    from ..entitys.player import Player
    from ..maze.maze import Maze


def update_entitys(game: Game) -> None:
    if game.player2:
        game.player2.update(game.maze)
    game.player.update(game.maze)
    flashing = game.state_manager.is_flashing(game)
    for g in game.ghosts:
        g.update(game, flashing)


def update_game_state(game: Game):
    game.global_timer += 1
    state_manager = game.state_manager
    if game.eaten_pellet == game.total_pellet:
        game.level_is_won()
    update_speeds(game.level, game.ghosts, game.player,
                  state_manager.actual_state)
    check_collision(game, game.player, game.ghosts)

    if game.player2:
        check_collision(game, game.player2, game.ghosts)
        if update_pellets(game, game.player2, game.maze.map):
            state_manager.get_frightened(game)

    if update_pellets(game, game.player, game.maze.map):
        # si une super_pacgum a été mangée
        state_manager.get_frightened(game)
    state_manager.update_ghosts_state(game)
    draw_lives(game)


def update_pellets(game: Game, player: Player, map: list[list[int]]) -> bool:
    # return True quand energizer a été mangé
    energizer = False
    if player and (player.offset_xy) == (0, 0):
        x, y = player.position
        if map[y][x] == 1:
            player.score += game.points_per_pacgum
            game.eaten_pellet += 1
            # game.render.draw_on_maze(game.maze.tiles[0], y, x)
        elif map[y][x] == 2:
            player.score += game.points_per_super_pacgum
            energizer = True
            # game.render.draw_on_maze(game.maze.tiles[0], y, x)
        elif map[y][x] == 3:
            player.score += 100
            draw_fruits(game)
            # a fix , actuellement si on mange
            # fruit2 il affiche les 2 d'un coup
        map[y][x] = 0
        game.render.draw_on_maze(game.maze.tiles[0], y, x)

    return energizer


def get_fruits(game: Game, maze: Maze, tile_size: int):
    if (game.eaten_pellet == 7) and maze.flag_fruit == 0:
        maze.flag_fruit = 0b1
        game.render.fruits[0].blit(maze.add_fruit(game.player.position,
                                                  tile_size, 3), (0, 0))
    elif (game.eaten_pellet == 17) and maze.flag_fruit == 1:
        maze.flag_fruit = 0b11
        game.render.fruits[1].blit(maze.add_fruit(game.player.position,
                                                  tile_size, 3), (0, 0))
