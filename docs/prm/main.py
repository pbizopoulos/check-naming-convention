import warnings
import zipfile
from os import environ
from pathlib import Path

import nltk
from js import ace, document
from pyodide.ffi.wrappers import add_event_listener

from main import check_naming_convention  # type: ignore[attr-defined]

editor_input = ace.edit("editor-input")
editor_input.setOption("maxLines", float("inf"))
editor_output = ace.edit("editor-output")
editor_output.setOption("maxLines", float("inf"))
editor_output.setReadOnly(True)  # noqa: FBT003
warnings.filterwarnings("error")


def on_keyup_editor_input(_: None) -> None:
    input_ = editor_input.getValue()
    try:
        output = check_naming_convention(input_.encode("utf-8"))
        editor_output.setValue(output.decode())
    except Exception as exception:  # noqa: BLE001
        editor_output.setValue(str(exception))


async def on_change_file_input(e) -> None:  # type: ignore[no-untyped-def] # noqa: ANN001
    file_list = e.target.files
    first_item = file_list.item(0)
    editor_input.setValue(await first_item.text())
    on_keyup_editor_input(None)


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
        editor_input.setValue(file.read())
    on_keyup_editor_input(None)
    add_event_listener(
        document.getElementById("editor-input"),
        "keyup",
        on_keyup_editor_input,
    )
    add_event_listener(
        document.getElementById("file-input"),
        "change",
        on_change_file_input,
    )


if __name__ == "__main__":
    main()
