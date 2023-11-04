import ast
from os import environ
from pathlib import Path

import nltk


def main() -> None:
    environ["NLTK_DATA"] = "tmp/"
    nltk.download("punkt")
    nltk.download("averaged_perceptron_tagger")
    with Path("prm/sample.py").open() as file:
        code = file.read()
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            tokens = nltk.word_tokenize(node.id)
            pos_tags = nltk.pos_tag(tokens)
            if pos_tags and pos_tags[0][1].startswith("N"):
                assert True
            else:
                raise AssertionError


if __name__ == "__main__":
    main()
