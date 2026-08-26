# from pydantic import dataclass
from dataclasses import dataclass
from ..entitys.entity import Entity
from ..entitys.direction import Dir


@dataclass
class Player(Entity):
    desired_direction: Dir

    def _input(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.desired_direction = Dir.N
        elif keys[pygame.K_DOWN]:
            self.desired_direction = Dir.S
        elif keys[pygame.K_RIGHT]:
            self.desired_direction = Dir.E
        elif keys[pygame.K_LEFT]:
            self.desired_direction = Dir.W
