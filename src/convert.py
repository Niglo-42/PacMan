from .direction import Dir
from .maze import Maze
# from pygame import Surface

class Convert:
    match_table = [
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    [[8, 8, 8], [0, 0, 0], [0, 0, 0]], # N
    [[0, 0, 9], [0, 0, 9], [0, 0, 9]], # E
    [[8, 8, 5], [0, 0, 9], [0, 0, 9]], # NE
    [[0, 0, 0], [0, 0, 0], [10, 10, 10]], # 4 S
    [[8, 8, 8], [0, 0, 0], [10, 10, 10]], # SN
    [[0, 0, 9], [0, 0, 9], [10, 10, 6]], # SE
    [[8, 8, 5], [0, 0, 9], [10, 10, 6]], # SEN
    [[11, 0, 0], [11, 0, 0], [11, 0, 0]], # 8 W
    [[4, 8, 8], [11, 0, 0], [11, 0, 0]], # WN
    [[11, 0, 9], [11, 0, 9], [11, 0, 9]], # WE
    [[4, 8, 5], [11, 0, 9], [11, 0, 9]], # WEN
    [[11, 0, 0], [11, 0, 0], [7, 10, 10]], # 12 WS
    [[4, 8, 8], [11, 0, 0], [7, 10, 10]], # WSN
    [[11, 0, 0], [11, 0, 9], [7, 10, 6]], # WSE
    [[4, 8, 5], [11, 0, 9], [7, 10, 6]]  # WSEN
]

    @staticmethod
    def trad(maze: Maze) -> list[list[list[list[int]]]]:
        padding_top = 3
        grid2 = [[[[0 for col in range(3)] for row in range(3)] for x in range(maze.width)] for y in range(padding_top)]
        for y in range(maze.height):
            grid2.append([])
            for x in range(maze.width):
                grid2[y + padding_top].append(Convert.match_table[maze.grid[y][x]])

        return grid2


    def get_carrefour(self, x, y) -> int:
        res = (self.maze.grid[y][x] & 6)
        if res & Dir.E.bit:
            res &= 13
            res |= Dir.N.bit
        if res & Dir.S.bit:
            res &= 11
            res |= Dir.W.bit
        res |= (self.maze.grid[y][x + 1] & Dir.S.bit) >> 1
        res |= (self.maze.grid[y + 1][x] & Dir.E.bit) << 1
        return res