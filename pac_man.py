from config.parser_config import Parser, print_obj
from src.game import Game
import sys


def main(argv: list[str]) -> int:
    try:
        args = Parser.parse_config(argv)
        print_obj(args)
    except ValueError as e:
        print(e)
    game = Game(args)
    game.monitor()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:2]))
