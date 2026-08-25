import mazegenerator
# from random import randint, choices, choice
from enum import Enum
from .direction import Dir

class obj(Enum):
    PELLET = 1
    SUPER_GUM = 2


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
        self.obj = [[1 for x in range(width)]for y in range(height)]
        # self.add_super_gum()
        self.flag_obj = 0

    def is_open(self, position: tuple[int, int], direction: Dir) -> bool:
        x, y = position
        return not (self.grid[y][x] & direction.bit)

        def is_opposite(self, actual_dir: Dir, wanted_dir: Dir) -> bool:
            if actual_dir is None:
                return False
            return actual_dir.opposite == wanted_dir

    def is_open(self, position: tuple[int, int],
                direction: tuple[int, int]) -> bool:
        col, row = position
        d_x, d_y = direction
        cell = self.grid[col + d_x, row + d_y]
        return cell <= 2

    def maze_loader(self) -> list[list[int]]:
        try:
            maze_gen = mazegenerator.MazeGenerator(size=(self.width, self.height),
                                                   perfect=False, seed=self.seed)

            maze_grid = maze_gen.maze
            return maze_grid

        except Exception as e:
            raise MazeGenError(f"Error occured while loading the maze: {e}")

    def get_spawn(self):
        mid_x, mid_y = self.width // 2, self.height // 2
        queue = [(mid_y, mid_x)]
        while queue:
            y, x = queue.pop(0)
            if self.grid[y][x] != 15:
                return y, x
            queue.extend(d.add_delta(x, y) for d in Dir if self.is_open((x, y), d))
            