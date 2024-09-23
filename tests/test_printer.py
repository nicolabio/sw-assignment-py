from typing import Any

from sw_assignment.printer import JsonPrinter, PrintItem


class TestJSONPrinter:
    def test_print__empty_input(self, out_file: Any) -> None:
        JsonPrinter(out_file.name).print([])

        got = out_file.readline()
        assert got == "[]"

    def test_print__single_item(self, out_file: Any) -> None:
        JsonPrinter(out_file.name).print([PrintItem(path="path", suffix=".dcm")])

        got = out_file.readlines()
        assert len(got) == 1
        assert got[0] == '[{"path": "path", "suffix": ".dcm"}]'

    def test_print__multiple_items(self, out_file: Any) -> None:
        JsonPrinter(out_file.name).print([
            PrintItem(path="path1", suffix=".dcm"),
            PrintItem(path="path2", suffix=".dcm"),
        ])

        got = out_file.readlines()
        assert len(got) == 1
        assert got[0] == '[{"path": "path1", "suffix": ".dcm"}, {"path": "path2", "suffix": ".dcm"}]'
