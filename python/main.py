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
            if (
                pos_tags
                and pos_tags[0][1] == "NN"
                and (len(pos_tags) == 1 or pos_tags[1][1].startswith(("JJ", "RB")))
            ):
                assert True
            else:
                raise AssertionError
        elif isinstance(node, ast.FunctionDef):
            tokens = nltk.word_tokenize(node.name)
            pos_tags = nltk.pos_tag(tokens)
            if pos_tags and (pos_tags[0][1] == "VB" or pos_tags[0][1] == "VBP"):
                assert True
            else:
                raise AssertionError


if __name__ == "__main__":
    main()
