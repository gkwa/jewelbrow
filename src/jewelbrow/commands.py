import os
import sys

from . import parser


def status_command(file_input: str | None = None) -> None:
    if file_input:
        with open(file_input, "r") as f:
            status_output = f.read()
    else:
        status_output = sys.stdin.read()

    parser_inst = parser.ChezmoiStatusParser()
    entries = parser_inst.parse_status_output(status_output)
    changes = parser_inst.summarize_changes(entries)

    print("\nStatus Summary:")
    print("-" * 40)
    for (first, second), paths in sorted(changes.items()):
        status_desc = f"{first}{second}"
        print(f"\nStatus {status_desc}:")
        for path in sorted(paths):
            print(f"  {path}")

    print("\nStatistics:")
    print("-" * 40)
    print(f"Total entries: {len(entries)}")
    print(f"Unique status combinations: {len(changes)}")


def actions_command(file_input: str | None = None) -> None:
    if file_input:
        with open(file_input, "r") as f:
            status_output = f.read()
    else:
        status_output = sys.stdin.read()

    parser_inst = parser.ChezmoiStatusParser()
    entries = parser_inst.parse_status_output(status_output)

    home = os.path.expanduser("~")
    for entry in entries:
        if entry.first_col in ["M", "A"]:
            abs_path = os.path.join(home, entry.path)
            print(f"chezmoi re-add {abs_path}")
