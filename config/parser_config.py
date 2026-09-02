from io import TextIOWrapper
import json
import ast
from typing import Any


class Parser:
    clamps = {
            "highscore_filename": "highscore.json",
            "width": 33,
            "height": 33,
            "lives": 9,
            "pacgum": 42,
            "seed": 0xffff,
            "points_per_pacgum": 100,
            "points_per_super_pacgum": 500,
            "points_per_ghost": 1600
    }

    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    @staticmethod
    def clean_commentary(file: TextIOWrapper) -> tuple[dict[str, Any],
                                                       list[int], bool]:
        clean = []
        lines = []
        isline = False
        for i, line in enumerate(file, 1):
            if line.startswith("[") or line.startswith("]"):
                isline = True
            elif line.lstrip().startswith("#"):
                lines.append(i)
            else:
                clean.append(line)
        clean_json = '\n'.join(clean)
        return (ast.literal_eval(clean_json), lines, isline)

    def get_line_nb_including_coms(com_lines: list[int], line: int) -> int:
        acc = 0
        for com_line in com_lines:
            if line >= com_line:
                acc += 1
        return line + acc

    def parse_config(argv: list[str]) -> "Parser":
        if len(argv) != 1:
            raise ValueError(f"This program takes 1 arg, not {len(argv)}")
        try:
            with open(argv[0], "r", encoding="utf-8") as file:
                params, com_lines, islist = Parser.clean_commentary(file)
            if ".json" not in argv[0]:
                raise ValueError(f"{argv[0]} is not an accepted"
                                 "format, only .json are allowed")
        except Exception as e:
            print(e)
            return Parser(**Parser.clamps)
        for i, (k, v) in enumerate(params.items(), 2 + 1 * (islist)):
            real_line_nb = Parser.get_line_nb_including_coms(com_lines, i)
            if k not in Parser.clamps.keys():
                print(f"{k} is not accepted, line {real_line_nb}")
                return Parser(**Parser.clamps)
            if Parser.clamps["highscore_filename"] == v:
                if not isinstance(v, str):
                    params[k] = Parser.clamps[k]
                    print(
                    f"{v} is not an accepted path, error line: {real_line_nb}")
            else:
                try:
                    v = int(v)
                except ValueError as e:
                    print(e)
                    params[k] = Parser.clamps[k]
                    continue
                if v <= 0:
                    params[k] = 1
                if k == "width" or k == "height" and v <= 6:
                    params[k] = 7
                    print(
                        f"{k} has to be in the range, error line "
                        f"{real_line_nb}")
                elif v > Parser.clamps[k]:
                    params[k] = Parser.clamps[k]
                    print(
                        f"{k} has to be in the range, error line "
                        f"{real_line_nb}")
                else:
                    params[k] = v
        lenght = len(Parser.clamps)
        if len(params) != lenght:
            print(f"{lenght - len(params)} mandatory arg "
                  f"{'is' * (len(params) == lenght - 1)}"
                  f"{'are' *(len(params) != lenght - 1)} missing")
        config = Parser(**params)
        return config

    def print_obj(self) -> None:
        print(json.dumps(vars(self), indent=4))
