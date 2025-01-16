# jewelbrow

CLI tool to help parse and process chezmoi status output.

## Installation

```bash
pip install jewelbrow
```

## Usage

Process chezmoi status output either via stdin or from a file:

```bash
# Via stdin
chezmoi status | jewelbrow status

# From a file
chezmoi status > status.txt
jewelbrow status -f status.txt
```

## Example Output

Show status summary:

```bash
$ chezmoi status | jewelbrow status

Status Summary:
----------------------------------------

Status AD:
  .config/app/config.toml

Status DA:
  .config/old_app

Status MM:
  .config/zsh/aliases
  .bashrc

Statistics:
----------------------------------------
Total entries: 4
Unique status combinations: 3
```

Show actionable commands:

```bash
$ chezmoi status | jewelbrow actions
# Individual commands:
chezmoi diff /home/user/.config/app/config.toml
chezmoi diff /home/user/.config/old_app/config.toml
chezmoi re-add /home/user/.config/app/config.toml
chezmoi destroy --force /home/user/.config/old_app/config.toml

# Batch commands:
chezmoi diff /home/user/.config/app/config.toml /home/user/.config/old_app/config.toml
chezmoi re-add /home/user/.config/app/config.toml
chezmoi destroy --force /home/user/.config/old_app/config.toml
```

## Status Types

First column indicates the difference between the last state written by chezmoi and the actual state:

- `A` - Entry was created
- `D` - Entry was deleted
- `M` - Entry was modified
- Space - No change

Second column indicates the difference between the actual state and the target state:

- `A` - Entry will be created
- `D` - Entry will be deleted
- `M` - Entry will be modified
- `R` - Script will be run
- Space - No change
