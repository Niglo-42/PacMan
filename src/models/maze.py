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
        self.tiles = None
        self.surf = None

    def get_first_zero(self, pacman_x, pacman_y):
        for y, row in enumerate(self.tiles):
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
        self.tiles[y][x] = fruit_idx

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
            self.tiles[y][x] = 2

    def is_open(self, position: tuple[int, int],
                direction: Dir) -> bool:
        col, row = position
        d_x, d_y = direction.delta
        cell = self.tiles[row + d_y][col + d_x]
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
        if self.tiles[y - 1][x] != 24:
            return False
        if self.tiles[y][x + 1] != 25:
            return False
        if self.tiles[y][x - 1] != 27:
            return False
        if self.tiles[y + 1][x] != 26:
            return False
        return True

    def get_spawn(self):
        mid_x, mid_y = self.width // 2, self.height // 2
        if mid_x == 0 and mid_y == 0:
            return (mid_x, mid_y)
        queue = [(mid_y, mid_x)]
        visited = {(mid_y, mid_x)}
        while queue:
            y, x = queue.pop(0)
            if not self.is_in42(y, x):
                if self.tiles[y][x] <= 3:
                    return (x, y)
            for d in Dir:
                if self.is_open((x, y), d):
                    nx, ny = d.add_delta(x, y)
                    if (ny, nx) not in visited:
                        visited.add((ny, nx))
                        queue.append((ny, nx))