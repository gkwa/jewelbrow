import dataclasses
import sys
import typing


@dataclasses.dataclass
class StatusEntry:
    first_col: str
    second_col: str
    path: str

    def __str__(self) -> str:
        return f"{self.first_col}{self.second_col} {self.path}"


class ChezmoiStatusParser:
    VALID_FIRST_COL = {" ", "A", "D", "M"}
    VALID_SECOND_COL = {" ", "A", "D", "M", "R"}

    @staticmethod
    def parse_line(line: str) -> StatusEntry:
        if len(line) < 3:
            raise ValueError(f"Invalid line format: {line}")
        first_col = line[0]
        second_col = line[1]
        path = line[3:].rstrip()
        if first_col not in ChezmoiStatusParser.VALID_FIRST_COL:
            raise ValueError(f"Invalid first column status: {first_col}")
        if second_col not in ChezmoiStatusParser.VALID_SECOND_COL:
            raise ValueError(f"Invalid second column status: {second_col}")
        return StatusEntry(first_col, second_col, path)

    @staticmethod
    def parse_status_output(status_output: str) -> typing.List[StatusEntry]:
        entries = []
        for line in status_output.splitlines():
            if line.strip():
                try:
                    entry = ChezmoiStatusParser.parse_line(line)
                    entries.append(entry)
                except ValueError as e:
                    print(f"Warning: Skipping invalid line: {e}", file=sys.stderr)
        return entries

    @staticmethod
    def summarize_changes(
        entries: typing.List[StatusEntry],
    ) -> typing.Dict[typing.Tuple[str, str], typing.List[str]]:
        changes = {}
        for entry in entries:
            status_key = (entry.first_col, entry.second_col)
            if status_key not in changes:
                changes[status_key] = []
            changes[status_key].append(entry.path)
        return changes


def process_chezmoi_status(file_input: typing.Optional[str] = None) -> None:
    if file_input:
        with open(file_input, "r") as f:
            status_output = f.read()
    else:
        status_output = sys.stdin.read()

    parser = ChezmoiStatusParser()
    entries = parser.parse_status_output(status_output)
    changes = parser.summarize_changes(entries)

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
