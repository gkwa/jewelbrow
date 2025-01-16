import pathlib
import shlex
import sys

from .. import parser


def _escape_path(path: str) -> str:
    return shlex.quote(path) if " " in path else path


def _get_paths_by_action(entries: list[parser.StatusEntry]) -> dict[str, list[str]]:
    actions = {"add": [], "destroy": [], "diff": []}

    home = pathlib.Path.home()
    for entry in entries:
        abs_path = str(home / entry.path)
        escaped_path = _escape_path(abs_path)

        if entry.first_col in ["M", "A"]:
            actions["add"].append(escaped_path)
        elif entry.first_col == "D" and entry.second_col == "A":
            actions["destroy"].append(escaped_path)

        # All files get diff command
        actions["diff"].append(escaped_path)

    return actions


def actions_command(file_input: str | None = None) -> None:
    if file_input:
        with open(file_input, "r") as f:
            status_output = f.read()
    else:
        status_output = sys.stdin.read()

    parser_inst = parser.ChezmoiStatusParser()
    entries = parser_inst.parse_status_output(status_output)
    actions = _get_paths_by_action(entries)

    # Individual commands
    print("# Individual commands:")
    for abs_path in actions["diff"]:
        print(f"chezmoi diff {abs_path}")
    for abs_path in actions["add"]:
        print(f"chezmoi re-add {abs_path}")
    for abs_path in actions["destroy"]:
        print(f"chezmoi destroy --force {abs_path}")

    # Print batch commands if files exist for each action
    print("\n# Batch commands:")
    if actions["diff"]:
        print(f"chezmoi diff {' '.join(actions['diff'])}")
    if actions["add"]:
        print(f"chezmoi re-add {' '.join(actions['add'])}")
    if actions["destroy"]:
        print(f"chezmoi destroy --force {' '.join(actions['destroy'])}")
