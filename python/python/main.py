from __future__ import annotations

import ast
import sys
from io import TextIOWrapper
from os import environ
from pathlib import Path

import nltk

environ["NLTK_DATA"] = "tmp/"
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")


def naming_convention(code_input: str | TextIOWrapper) -> None:
    if isinstance(code_input, str):
        with Path(code_input).open() as file:
            root = ast.parse(file.read())
    elif isinstance(code_input, TextIOWrapper):
        root = ast.parse(code_input.read())
    for node in ast.walk(root):
        if isinstance(node, ast.Name):
            tokens = nltk.word_tokenize(node.id)
            pos_tags = nltk.pos_tag(tokens)
            if not (
                pos_tags[0][1] == "NN"
                and (len(pos_tags) == 1 or pos_tags[1][1].startswith(("JJ", "RB")))
            ):
                msg = f"line: {node.lineno}, variable name: {pos_tags[0][0]}"
                raise AssertionError(
                    msg,
                )
        elif isinstance(node, ast.FunctionDef):
            tokens = node.name.split("_")
            pos_tags = nltk.pos_tag(tokens)
            if len(pos_tags) < 2:  # noqa: PLR2004
                msg = f"line: {node.lineno}, variable: {pos_tags}"
                raise AssertionError(msg)
            if pos_tags[0][1] != "VB":
                msg = f"line: {node.lineno}, variable name: {pos_tags[0][0]}"
                raise AssertionError(
                    msg,
                )
            if pos_tags[1][1] != "NN":
                msg = f"line: {node.lineno}, variable name: {pos_tags[1][0]}"
                raise AssertionError(
                    msg,
                )


def main() -> None:
    num_arguments_allowed = 2
    if len(sys.argv) == num_arguments_allowed:
        naming_convention(sys.argv[1])


if __name__ == "__main__":
    main()
