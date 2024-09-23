import dataclasses
import json


@dataclasses.dataclass
class PrintItem:
    path: str


class Printer:
    def print(self, items: list[PrintItem]) -> None:
        raise NotImplementedError


class JsonPrinter(Printer):
    def __init__(self, out_path: str) -> None:
        self._out_path = out_path

    def print(self, items: list[PrintItem]) -> None:
        with open(self._out_path, "w") as f:
            json.dump([dataclasses.asdict(item) for item in items], f)


class StdOutPrinter(Printer):
    def print(self, items: list[PrintItem]) -> None:
        for item in items:
            print(f"{item.path}")
