import shlex


def escape_path(path: str) -> str:
    return shlex.quote(path) if " " in path else path
