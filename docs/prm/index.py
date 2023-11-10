import io
from difflib import unified_diff
from pathlib import Path

from js import document, Blob, window
from main import comment_remover
from pyodide.ffi.wrappers import add_event_listener


def on_keyup_input_textarea(_: None) -> None:
    document.getElementById("input-textarea").style.height = "1px"
    document.getElementById(
        "input-textarea",
    ).style.height = f'{document.getElementById("input-textarea").scrollHeight}px'
    input_ = document.getElementById("input-textarea").value
    reader = io.BufferedReader(io.BytesIO(input_.encode("utf-8")))  # type: ignore[arg-type] # noqa: E501
    wrapper = io.TextIOWrapper(reader)
    try:
        output = comment_remover(wrapper)
        difference_line_list = list(
            unified_diff(input_.splitlines(), output.splitlines(), n=1000),
        )[3:]
        difference_styled_line_list = []
        for difference_line in difference_line_list:
            if difference_line.startswith("+"):
                difference_styled_line_list.append(
                    f'<span style="color:green;">{difference_line}</span>',
                )
            elif difference_line.startswith("-"):
                difference_styled_line_list.append(
                    f'<span style="color:red;">{difference_line}</span>',
                )
            else:
                difference_styled_line_list.append(difference_line)
        if document.getElementById("difference-select").value == "difference":
            document.getElementById("output-pre").innerHTML = "\n".join(
                difference_styled_line_list,
            )
        elif document.getElementById("difference-select").value == "output":
            document.getElementById("output-pre").innerHTML = output
    except Exception as exception:  # noqa: BLE001
        document.getElementById("output-pre").innerHTML = exception


async def on_change_file_input(e) -> None:
    file_list = e.target.files
    first_item = file_list.item(0)
    document.getElementById("input-textarea").value = await first_item.text()
    on_keyup_input_textarea(None)


def on_download_output(_: None) -> None:
    content = document.getElementById("output-pre").innerHTML;
    a = document.createElement("a")
    document.body.appendChild(a)
    a.style = "display: none"
    blob = Blob.new([content])
    url = window.URL.createObjectURL(blob)
    a.href = url
    a.download = "main.py"
    a.click()
    window.URL.revokeObjectURL(url)


def on_select_input_output_difference(_: None) -> None:
    on_keyup_input_textarea(_)


def main() -> None:
    with Path("before.py").open() as file:
        document.getElementById("input-textarea").value = file.read()[:-1]
    on_keyup_input_textarea(None)
    on_select_input_output_difference(None)
    add_event_listener(
        document.getElementById("input-textarea"),
        "keyup",
        on_keyup_input_textarea,
    )
    add_event_listener(
        document.getElementById("download-output"),
        "click",
        on_download_output,
    )
    add_event_listener(
        document.getElementById("difference-select"),
        "change",
        on_select_input_output_difference,
    )
    add_event_listener(
        document.getElementById("file-input"),
        "change",
        on_change_file_input,
    )


if __name__ == "__main__":
    main()
