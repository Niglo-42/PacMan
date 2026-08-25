from enum import Enum


class Dir(Enum):
    N = (0, -1, 1, 2)
    E = (1,  0, 2, 0)
    S = (0,  1, 4, 3)
    W = (-1, 0, 8, 1)
    VOID = (0, 0, 0, 0)

    @property
    def delta(self) -> tuple[int, int]:
        return self.value[0], self.value[1]

    @property
    def add_delta(self, x, y) -> tuple[int, int]:
        return self.value[0] + x, self.value[1] + y

    @property
    def bit(self) -> int:
        return self.value[2]

    @classmethod
    def from_index(cls, index: int) -> "Dir":
        return (cls.N, cls.E, cls.S, cls.W)[index]

    @property
    def idx_tile(self) -> int:
        return self.value[3]

    @property
    def opposite(self) -> "Dir":
        dx, dy = self.delta
        return next(d for d in Dir if d.delta == (-dx, -dy))