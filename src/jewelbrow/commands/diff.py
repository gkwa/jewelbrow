import pathlib
import shlex
import sys

from .. import parser


def _escape_path(path: str) -> str:
    return shlex.quote(path) if " " in path else path


def diff_command(file_input: str | None = None) -> None:
    if file_input:
        with open(file_input, "r") as f:
            status_output = f.read()
    else:
        status_output = sys.stdin.read()

    parser_inst = parser.ChezmoiStatusParser()
    entries = parser_inst.parse_status_output(status_output)

    paths = []
    home = pathlib.Path.home()

    # Individual commands
    for entry in entries:
        abs_path = _escape_path(str(home / entry.path))
        paths.append(abs_path)
        print(f"chezmoi diff {abs_path}")

    # Batch command
    if paths:
        print("\n# Batch command:")
        print(f"chezmoi diff {' '.join(paths)}")
