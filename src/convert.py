from .entitys.direction import Dir
from .models.maze import Maze
from .models.cell import Cell

class Convert:
    # - 16 = external walls
    match_int = (
    ((0, 0, 0), (0, 0, 0), (0, 0, 0)),
    ((24, 24, 24), (0, 0, 0), (0, 0, 0)),  # N
    ((0, 0, 25), (0, 0, 25), (0, 0, 25)),  # E
    ((24, 24, 21), (0, 0, 25), (0, 0, 25)),  # NE
    ((0, 0, 0), (0, 0, 0), (26, 26, 26)),  # S
    ((24, 24, 24), (0, 0, 0), (26, 26, 26)),  # SN
    ((0, 0, 25), (0, 0, 25), (26, 26, 22)),  # SE
    ((24, 24, 21), (0, 0, 25), (26, 26, 22)),  # SEN
    ((27, 0, 0), (27, 0, 0), (27, 0, 0)),  # W
    ((20, 24, 24), (27, 0, 0), (27, 0, 0)),  # WN
    ((27, 0, 25), (27, 0, 25), (27, 0, 25)),  # WE
    ((20, 24, 21), (27, 0, 25), (27, 0, 25)),  # WEN
    ((27, 0, 0), (27, 0, 0), (23, 26, 26)),  # WS
    ((20, 24, 24), (27, 0, 0), (23, 26, 26)),  # WSN
    ((27, 0, 25), (27, 0, 25), (23, 26, 22)),  # WSE
    ((20, 24, 21), (27, 0, 25), (23, 26, 22)),  # WSEN
)

    corner_match = [
        # 0 not applicated
        (0, 0, 0, 0),
        (0, 0, 18, 19), #n
        (16, 0, 0, 19), #e
        (0, 0, 0, 19),
        (16, 17, 0, 0), #s
        (0, 0, 0, 0),
        (16, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 17, 18, 0), #w
        (0, 0 , 18, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 17, 0, 0), #ws
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0)
    ]

    @staticmethod
    def get_trad(w, s, e, n, val) -> list[list[int]]:
        res = [list(row) for row in Convert.match_int[val]]
        total = sum([w, s, e, n])
        if total == 0:
            return res
        if n:
            res[0] = [x - 16 if x > 16 else x
                        for x in res[0]]
        if e:
            for row in res:
                if row[2] > 16:
                    row[2] -= 16 
        if s:
            res[2] = [x - 16 if x > 16 else x
                        for x in res[2]]
        if w:
            for row in res:
                if row[0] > 16:
                    row[0] -= 16
        if total == 1:
            if n:
                if val & Dir.E.bit:
                    res[0][2] = 29
                if val & Dir.W.bit:
                    res[0][0] = 28
            if s:
                if val & Dir.E.bit:
                    res[2][2] = 30
                if val & Dir.W.bit:
                    res[2][0] = 31
            if e:
                if val & Dir.S.bit:
                    res[2][2] = 14
                if val & Dir.N.bit:
                    res[0][2] = 13
            if w:
                if val & Dir.S.bit:
                    res[2][0] = 15
                if val & Dir.N.bit:
                    res[0][0] = 12
        return res

    def modify_corner(grid, corner, row, col) -> list[list[Cell]]:
        for y in range(row):
            for x in range(col):
                current = corner[y * col + x]
                offset = y * col + x
                if current[0]:
                    grid[y][x].set_tile(2, 2, corner[offset][0])
                if current[1]:
                    grid[y][x + 1].set_tile(2, 0, corner[offset][1])
                if current[2]:
                    grid[y + 1][x + 1].set_tile(0, 0, corner[offset][2])
                if current[3]:
                    grid[y + 1][x].set_tile(0, 2, corner[offset][3])
        return grid

    @staticmethod
    def trad(maze: Maze) -> list[list[Cell]]:
        grid2 = []
        corner = []
        for y in range(maze.height):
            grid2.append([])
            for x in range(maze.width):
                w, s = x == 0 , y == maze.height - 1,
                e, n = x == maze.width - 1,  y == 0
                cell = Cell(x, y, Convert.get_trad(w, s, e, n, maze.grid[y][x]))
                grid2[y].append(cell)
                if not e and not s:
                    corner.append(Convert.corner_match[Convert.get_corner(maze, y, x)])
        grid2 = Convert.modify_corner(grid2, corner, maze.height - 1, maze.width - 1)
        return grid2


    def get_corner(maze, y, x) -> int:
        res = (maze.grid[y][x] & 6)
        if res & Dir.E.bit:
            res &= 13
            res |= Dir.N.bit
        if res & Dir.S.bit:
            res &= 11
            res |= Dir.W.bit
        res |= (maze.grid[y][x + 1] & Dir.S.bit) >> 1
        res |= (maze.grid[y + 1][x] & Dir.E.bit) << 1
        return res