import zipfile
from pathlib import Path
from os import environ

import nltk

from main import check_naming_convention


def main() -> None:
    environ["NLTK_DATA"] = "tmp/"
    zipfile.ZipFile('tmp/nltk_data/tokenizers/punkt.zip').extractall(
        path='tmp/nltk_data/tokenizers/'
    )
    zipfile.ZipFile('tmp/nltk_data/taggers/averaged_perceptron_tagger.zip').extractall(
        path='tmp/nltk_data/taggers/'
    )
    tokenizer = nltk.data.load('tmp/nltk_data/tokenizers/punkt/english.pickle')
    output = tokenizer.tokenize('Hello. This is a test!')
    print(output)


if __name__ == "__main__":
    main()
