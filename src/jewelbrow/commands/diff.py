import pathlib
import sys

from .. import parser, paths


def diff_command(file_input: str | None = None) -> None:
    if file_input:
        with open(file_input, "r") as f:
            status_output = f.read()
    else:
        status_output = sys.stdin.read()

    parser_inst = parser.ChezmoiStatusParser()
    entries = parser_inst.parse_status_output(status_output)

    commands = []
    home = pathlib.Path.home()

    # Individual commands
    for entry in entries:
        abs_path = paths.escape_path(str(home / entry.path))
        commands.append(abs_path)
        print(f"chezmoi diff {abs_path}")

    # Batch command
    if commands:
        print("\n# Batch command:")
        print(f"chezmoi diff {' '.join(commands)}")
