import mazegenerator
from random import randint, choices, choice
from ..entitys.direction import Dir


class MazeGenError(Exception):
    pass


class Maze:
    """Labyrinthe sous forme de grille de connectivité.

        Chaque cellule est un couloir ; sa valeur (0-15) code par bits les
        passages ouverts vers ses voisins. Les murs sont donc sur les arêtes.

        Convention : les coordonnées publiques sont (col, row) — x puis y.
        L'indexation interne `cells[row][col]` ne sort jamais de cette classe.
        """
    def __init__(self, width: int, height: int, seed: int) -> None:
        self.height = height
        self.width = width
        self.seed = seed
        self.grid = self.maze_loader()
        self.map = None
        self.tiles = None
        self.surf = None

    def get_first_zero(self, pacman_x, pacman_y):
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if col <= 3 and \
                    y != pacman_y and x != pacman_x:
                    return (x, y)
        return (1, 1)

    def add_fruit(self, fruits, pacman_pos):
        #range des index des fruits à determiner avec les noms des png
        def random_fruit(fruits):
            return (choices(range(len(fruits)),
                weights=range(len(fruits), 0, -1), k=1)[0])
        fruit_idx = random_fruit(fruits) + 3
        x, y = self.get_first_zero(*pacman_pos)
        self.map[y][x] = fruit_idx

    def add_super_gum(self) -> None:
        """
        replace 3 % of the pellets to superGum
        position = left or right
        """
        y_bottom = self.height * 95 // 100
        y_top = self.height * 5 // 100
        seq = [((1), (1, y_top)),
               ((self.width - 2), (1, y_top)),
               ((1), (y_bottom, self.height - 2)),
               ((self.width - 2), (y_bottom, self.height - 2))]
        for s in seq:
            x = s[0]
            low = min(s[1][0], s[1][1])
            high = max(s[1][0], s[1][1])
            y = randint(low, high)
            if y == 0:
                y = 1
            elif y == self.height - 1:
                y -= 1
            self.map[y][x] = 2

    def is_open(self, position: tuple[int, int],
                direction: Dir) -> bool:
        col, row = position
        d_x, d_y = direction.delta
        cell = self.map[row + d_y][col + d_x]
        return cell <= 2

    def maze_loader(self) -> list[list[int]]:
        try:
            maze_gen = mazegenerator.MazeGenerator(size=(self.width, self.height),
                                                   perfect=False, seed=self.seed)

            maze_grid = maze_gen.maze
            return maze_grid

        except Exception as e:
            raise MazeGenError(f"Error occured while loading the maze: {e}")

    def is_in42(self, y, x) -> bool:
        if self.map[y - 1][x] != 24:
            return False
        if self.map[y][x + 1] != 25:
            return False
        if self.map[y][x - 1] != 27:
            return False
        if self.map[y + 1][x] != 26:
            return False
        return True

    def kills_caves(self) -> bool:
        def is_four_pellets(y, x):
            if self.map[y - 1][x] != 1:
                return False
            if self.map[y][x + 1] != 1:
                return False
            if self.map[y][x - 1] != 1:
                return False
            if self.map[y + 1][x] != 1:
                return False
            return True

        old_map = [row[:] for row in self.map]
        dirs = [Dir.E, Dir.S, Dir.W, Dir.N]
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if is_four_pellets(y, x):
                    old_map[y][x] = 255

        island = set()
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if old_map[y][x] != 255:
                    continue
                queue = [(y, x)]
                old_map[y][x] = 0       # 0 = visited
                
                # BFS
                while queue:
                    dy, dx = queue.pop(0)
                    island.add((dy, dx))
                    for direction in dirs:
                        ny, nx = direction.add_delta(dx, dy)
                        if ny < self.height and nx < self.width:
                            if old_map[ny][nx] == 255:
                                old_map[ny][nx] = 0
                                queue.append((ny, nx))

        for y, x in island:
            cardinal = 0
            cardinal = (y - 1, x) in island  
            cardinal |= ((y, x + 1) in island) << 1
            cardinal |= ((y + 1, x) in island) << 2
            cardinal |= ((y, x - 1) in island) << 3
            if cardinal != 0 and  not (cardinal & cardinal - 1):
                if cardinal & 1: # nord
                    self.map[y][x] = 24
                if cardinal & 2: # est
                    self.map[y][x] = 25
                if cardinal & 4: # sud
                    self.map[y][x] = 26
                if cardinal & 8: # ouest
                    self.map[y][x] = 27
            else:
                if cardinal & 6 == 6: # NW
                    self.map[y][x] = 20
                if cardinal & 12 == 12: # NE
                    self.map[y][x] = 21
                if cardinal & 9 == 9: # SE
                    self.map[y][x] = 22
                if cardinal & 3 == 3: # NW
                    self.map[y][x] = 23
            # 20 if corner, # 24 if junction

                        



    def get_spawn(self):
        mid_x, mid_y = self.width // 2, self.height // 2
        if mid_x == 0 and mid_y == 0:
            return (mid_x, mid_y)
        queue = [(mid_y, mid_x)]
        visited = {(mid_y, mid_x)}
        while queue:
            y, x = queue.pop(0)
            if not self.is_in42(y, x):
                if self.map[y][x] <= 3:
                    return (x, y)
            for d in Dir:
                if self.is_open((x, y), d):
                    nx, ny = d.add_delta(x, y)
                    if (ny, nx) not in visited:
                        visited.add((ny, nx))
                        queue.append((ny, nx))

    def get_ghosts_spawns(self) -> list[tuple[int, int]]:
        w, h = self.width, self.height
        corners = [(1, 1), (w - 2, 1), (1, h - 2), (w - 2, h - 2)]
        return corners
