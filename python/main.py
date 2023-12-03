from __future__ import annotations

import ast
import unittest
from os import environ
from pathlib import Path
from shutil import copyfile

import nltk


def check_naming_convention(code_input: str | bytes) -> list[str]:
    warnings = []
    environ["NLTK_DATA"] = "tmp/nltk_data"
    if not Path("tmp/nltk_data").exists():
        nltk.download("punkt")
        nltk.download("averaged_perceptron_tagger")
    if isinstance(code_input, str):
        with Path(code_input).open() as file:
            root = ast.parse(file.read())
    else:
        root = ast.parse(code_input.decode())
    for node in ast.walk(root):
        if isinstance(node, ast.Assign):
            tokens = node.targets[0].id.split("_")  # type: ignore[attr-defined]
            pos_tags = nltk.pos_tag(tokens)
            if not (
                pos_tags[0][1] == "NN"
                and (len(pos_tags) == 1 or pos_tags[1][1].startswith(("JJ", "RB")))
            ):
                warnings.append(
                    f"line: {node.lineno}, variable name: {pos_tags[0][0]}",
                )
        elif isinstance(node, ast.FunctionDef):
            tokens = node.name.split("_")
            pos_tags = nltk.pos_tag(tokens)
            if pos_tags[0][1] != "VB":
                warnings.append(
                    f"line: {node.lineno}, variable name: {pos_tags[0][0]}",
                )
            if len(pos_tags) < 2:  # noqa: PLR2004
                warnings.append(
                    f"line: {node.lineno}, variable: {pos_tags}",
                )
            elif pos_tags[1][1] != "NN":
                warnings.append(
                    f"line: {node.lineno}, variable name: {pos_tags[1][0]}",
                )
    return warnings


class Tests(unittest.TestCase):
    def test_check_naming_convention_bytes_input(self: Tests) -> None:
        with Path("prm/main.py").open(encoding="utf-8") as file:
            output = check_naming_convention(file.read().encode())
        assert len(output) == 0

    def test_check_naming_convention_file_input(self: Tests) -> None:
        copyfile("prm/main.py", "tmp/main_processed.py")
        output = check_naming_convention("tmp/main_processed.py")
        assert len(output) == 0


def main() -> None:
    import fire

    fire.Fire(check_naming_convention)


if __name__ == "__main__":
    unittest.main()
