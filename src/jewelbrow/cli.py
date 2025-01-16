import argparse
import signal
import sys

from .commands import actions, status


def handle_sigint(signum, frame):
    print("\nOperation cancelled by user")
    sys.exit(0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process chezmoi status output")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Status command
    status_parser = subparsers.add_parser("status", help="Show status summary")
    status_parser.add_argument(
        "-f",
        "--file",
        help="Input file containing chezmoi status output (if not provided, reads from stdin)",
        type=str,
        default=None,
    )

    # Actions command
    actions_parser = subparsers.add_parser(
        "actions", help="Show chezmoi commands to run"
    )
    actions_parser.add_argument(
        "-f",
        "--file",
        help="Input file containing chezmoi status output (if not provided, reads from stdin)",
        type=str,
        default=None,
    )

    return parser.parse_args()


def cli() -> None:
    signal.signal(signal.SIGINT, handle_sigint)

    args = parse_args()
    try:
        if args.command == "status":
            status.status_command(args.file)
        elif args.command == "actions":
            actions.actions_command(args.file)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)


if __name__ == "__main__":
    cli()
