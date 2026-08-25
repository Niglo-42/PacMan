import pygame
from .entitys.entity import Entity
from .entitys.player import Player
from .maze import Maze


class MovementSystem:
    def update_pos(self, entity: Entity) -> None:
        if entity.d_x != 0 and entity.d_y == 0:
            entity.offset_x += entity.d_x
            if entity.offset_x == 8:
                entity.offset_x = 0
                entity.col += 1
            elif entity.offset_x == -1:
                entity.offset_x = 7
                entity.col -= 1
        elif entity.d_x == 0 and entity.d_y != 0:
            entity.offset_y += entity.d_y
            if entity.offset_y == 8:
                entity.offset_y = 0
                entity.row += 1
            elif entity.offset_y == -1:
                entity.offset_y = 7
                entity.row -= 1

    def player_input(self, player: Player) -> None:
        keys = pygame.key.get_pressed()
        position = (player.col, player.row)
        direction = (player.d_x, player.d_y)
        if keys[pygame.K_UP] and not self.wall_collision(position, direction):
            player.d_x = 0
            player.d_y = -1
        if keys[pygame.K_DOWN]:
            player.d_x = 0
            player.d_y = 1
        if keys[pygame.K_RIGHT]:
            player.d_x = 1
            player.d_y = 0
        if keys[pygame.K_LEFT]:
            player.d_x = -1
            player.d_y = 0 

    def wall_collision(self, maze: Maze, position, direction) -> bool:
        return maze.is_open(position, direction)
