import pathlib
import subprocess
import sys

from .. import parser, paths


def get_source_path(target_path: str) -> str:
    try:
        result = subprocess.run(
            ["chezmoi", "source-path", target_path],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""


def get_paths_by_action(entries: list[parser.StatusEntry]) -> dict[str, list[str]]:
    actions = {
        "add": [],
        "destroy": [],
        "diff": [],
        "reset_source": [],
        "reset_target": [],
    }
    home = pathlib.Path.home()

    for entry in entries:
        abs_path = str(home / entry.path)
        escaped_path = paths.escape_path(abs_path)

        if entry.first_col in ["M", "A"]:
            actions["add"].append(escaped_path)

            # Add reset paths
            source_path = get_source_path(abs_path)
            if source_path:
                actions["reset_source"].append(paths.escape_path(source_path))
                actions["reset_target"].append(escaped_path)

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
    actions = get_paths_by_action(entries)

    # Individual commands
    print("# Individual commands:")
    for abs_path in actions["diff"]:
        print(f"chezmoi diff {abs_path}")

    for abs_path in actions["add"]:
        print(f"chezmoi re-add {abs_path}")

    for abs_path in actions["destroy"]:
        print(f"chezmoi destroy --force {abs_path}")

    for src, tgt in zip(actions["reset_source"], actions["reset_target"]):
        print(f"cp {src} {tgt}")

    # Print batch commands if files exist for each action
    print("\n# Batch commands:")
    if actions["diff"]:
        print(f"chezmoi diff {' '.join(actions['diff'])}")

    if actions["add"]:
        print(f"chezmoi re-add {' '.join(actions['add'])}")

    if actions["destroy"]:
        print(f"chezmoi destroy --force {' '.join(actions['destroy'])}")

    if actions["reset_source"]:
        reset_commands = [
            f"cp {src} {tgt}"
            for src, tgt in zip(actions["reset_source"], actions["reset_target"])
        ]
        print(" && ".join(reset_commands))
