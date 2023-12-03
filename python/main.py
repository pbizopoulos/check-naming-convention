from __future__ import annotations

import ast
import unittest
import warnings
from os import environ
from pathlib import Path
from shutil import copyfile

import nltk


def check_naming_convention(code_input: str | bytes) -> None:
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
        if isinstance(node, ast.Name):
            tokens = nltk.word_tokenize(node.id)
            pos_tags = nltk.pos_tag(tokens)
            if not (
                pos_tags[0][1] == "NN"
                and (len(pos_tags) == 1 or pos_tags[1][1].startswith(("JJ", "RB")))
            ):
                warnings.warn(
                    f"line: {node.lineno}, variable name: {pos_tags[0][0]}",
                    stacklevel=1,
                )
        elif isinstance(node, ast.FunctionDef):
            tokens = node.name.split("_")
            pos_tags = nltk.pos_tag(tokens)
            if pos_tags[0][1] != "VB":
                warnings.warn(
                    f"line: {node.lineno}, variable name: {pos_tags[0][0]}",
                    stacklevel=1,
                )
            if len(pos_tags) < 2:  # noqa: PLR2004
                warnings.warn(
                    f"line: {node.lineno}, variable: {pos_tags}",
                    stacklevel=1,
                )
            elif pos_tags[1][1] != "NN":
                warnings.warn(
                    f"line: {node.lineno}, variable name: {pos_tags[1][0]}",
                    stacklevel=1,
                )


class Tests(unittest.TestCase):
    def test_check_naming_convention_bytes_input(self: Tests) -> None:
        with Path("prm/main.py").open(encoding="utf-8") as file:
            check_naming_convention(file.read().encode())

    def test_check_naming_convention_file_input(self: Tests) -> None:
        copyfile("prm/main.py", "tmp/main_processed.py")
        check_naming_convention("tmp/main_processed.py")


def main() -> None:
    import fire

    fire.Fire(check_naming_convention)


if __name__ == "__main__":
    unittest.main()
