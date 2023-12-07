from __future__ import annotations

import ast
import unittest
from os import environ
from pathlib import Path
from shutil import copyfile

import nltk
from nltk.stem.wordnet import WordNetLemmatizer

word_net_lemmatizer = WordNetLemmatizer()


def check_naming_convention(code_input: str | bytes) -> list[str]:  # noqa: C901,PLR0912
    warnings = []
    environ["NLTK_DATA"] = "tmp/nltk_data"
    if not Path("tmp/nltk_data").exists():
        nltk.download("averaged_perceptron_tagger")
        nltk.download("punkt")
        nltk.download("wordnet")
        nltk.download("words")
    if isinstance(code_input, str):
        with Path(code_input).open() as file:
            root = ast.parse(file.read())
    else:
        root = ast.parse(code_input.decode())
    for node in ast.walk(root):
        if isinstance(node, ast.Assign):
            if isinstance(node.targets[0], ast.Name):
                tokens = node.targets[0].id.split("_")
                words = nltk.corpus.words.words()
                for token in tokens:
                    if token not in words:
                        token_lemmatized = word_net_lemmatizer.lemmatize(token)
                        warnings.append(
                            f"line: {node.lineno}, {token_lemmatized} not in dictionary",  # noqa: E501
                        )
                pos_tags = nltk.pos_tag(tokens)
                if (pos_tags[0][1] == "NNS") and len(pos_tags) == 1:
                    continue
                if pos_tags[0][1] == "NN":
                    if len(pos_tags) == 1:
                        continue
                    if pos_tags[1][1].startswith(("JJ", "RB")):
                        continue
                warnings.append(
                    f"line: {node.lineno}, {pos_tags[0][0]} is wrong",
                )
        elif isinstance(node, ast.FunctionDef):
            if node.name == "main":
                continue
            tokens = node.name.split("_")
            pos_tags = nltk.pos_tag(tokens)
            if pos_tags[0][1] != "VB" and tokens[0] != "test":
                warnings.append(
                    f"line: {node.lineno}, {pos_tags[0][0]} is wrong",
                )
            if len(pos_tags) < 2:  # noqa: PLR2004
                warnings.append(
                    f"line: {node.lineno}, variable: {pos_tags}",
                )
            elif pos_tags[1][1] != "NN":
                warnings.append(
                    f"line: {node.lineno}, {pos_tags[1][0]} is wrong",
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
