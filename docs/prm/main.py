import io
import zipfile
from os import environ
from pathlib import Path

import nltk
from js import document
from pyodide.ffi.wrappers import add_event_listener

from main import check_naming_convention


def on_keyup_input_textarea(_: None) -> None:
    document.getElementById("input-textarea").style.height = "1px"
    document.getElementById(
        "input-textarea",
    ).style.height = f'{document.getElementById("input-textarea").scrollHeight}px'
    input_ = document.getElementById("input-textarea").value
    reader = io.BufferedReader(io.BytesIO(input_.encode("utf-8")))  # type: ignore[arg-type]
    wrapper = io.TextIOWrapper(reader)
    try:
        check_naming_convention(wrapper)
    except Exception as exception:  # noqa: BLE001
        document.getElementById("output-pre").innerHTML = exception


async def on_change_file_input(e) -> None:
    file_list = e.target.files
    first_item = file_list.item(0)
    document.getElementById("input-textarea").value = await first_item.text()
    on_keyup_input_textarea(None)


def main() -> None:
    environ["NLTK_DATA"] = "tmp/nltk_data"
    nltk.data.path = ["tmp/nltk_data", *nltk.data.path]
    zipfile.ZipFile("tmp/nltk_data/tokenizers/punkt.zip").extractall(
        path="tmp/nltk_data/tokenizers/",
    )
    zipfile.ZipFile("tmp/nltk_data/taggers/averaged_perceptron_tagger.zip").extractall(
        path="tmp/nltk_data/taggers/",
    )
    with Path("main.py").open() as file:
        document.getElementById("input-textarea").value = file.read()
    on_keyup_input_textarea(None)
    add_event_listener(
        document.getElementById("input-textarea"),
        "keyup",
        on_keyup_input_textarea,
    )
    add_event_listener(
        document.getElementById("file-input"),
        "change",
        on_change_file_input,
    )


if __name__ == "__main__":
    main()
