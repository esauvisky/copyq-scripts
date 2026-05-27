#!/usr/bin/env python3
"""Export CopyQ commands and split them into importable command files."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


COMMAND_KEY_RE = re.compile(r"^(\d+)\\(.+?)=(.*)$")
SIZE_RE = re.compile(r"^size=\d+\s*$")


def run_copyq_export(start_server: bool) -> str:
    cmd = ["copyq"]
    if start_server:
        cmd.append("--start-server")
    cmd.extend(["eval", "exportCommands(commands())"])

    result = subprocess.run(cmd, check=False, text=True, capture_output=True)
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        raise SystemExit(result.returncode)

    return result.stdout


def parse_blocks(export_text: str) -> list[tuple[str, list[str]]]:
    blocks: dict[str, list[str]] = {}
    order: list[str] = []
    current_index: str | None = None

    for line in export_text.splitlines():
        if line == "[Commands]" or SIZE_RE.match(line):
            current_index = None
            continue

        match = COMMAND_KEY_RE.match(line)
        if match:
            current_index = match.group(1)
            if current_index not in blocks:
                blocks[current_index] = []
                order.append(current_index)
            blocks[current_index].append(line)
        elif current_index is not None:
            blocks[current_index].append(line)

    return [(index, blocks[index]) for index in sorted(order, key=int)]


def command_name(block: list[str], fallback: str) -> str:
    for line in block:
        match = COMMAND_KEY_RE.match(line)
        if match and match.group(2) == "Name":
            return match.group(3).strip().strip('"') or fallback
    return fallback


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return slug or "command"


def reindex_block(block: list[str]) -> list[str]:
    out: list[str] = []
    for line in block:
        match = COMMAND_KEY_RE.match(line)
        if match:
            out.append(f"1\\{match.group(2)}={match.group(3)}")
        else:
            out.append(line)
    return out


def write_command_files(export_text: str, commands_dir: Path) -> list[Path]:
    if commands_dir.exists():
        shutil.rmtree(commands_dir)
    commands_dir.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for position, (_index, block) in enumerate(parse_blocks(export_text), start=1):
        name = command_name(block, f"Command {position}")
        path = commands_dir / f"{position:02d}-{slugify(name)}.ini"
        path.write_text(
            "[Commands]\n"
            + "\n".join(reindex_block(block))
            + "\n"
            + "size=1\n",
            encoding="utf-8",
        )
        written.append(path)

    return written


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export CopyQ commands using CopyQ's native export format."
    )
    parser.add_argument(
        "--output",
        default="all_commands.ini",
        type=Path,
        help="Path for the full native command export.",
    )
    parser.add_argument(
        "--commands-dir",
        default="commands",
        type=Path,
        help="Directory for one native INI file per command.",
    )
    parser.add_argument(
        "--start-server",
        action="store_true",
        help="Pass --start-server to CopyQ before evaluating the export command.",
    )
    args = parser.parse_args()

    export_text = run_copyq_export(start_server=args.start_server)
    args.output.write_text(export_text, encoding="utf-8")
    written = write_command_files(export_text, args.commands_dir)

    print(f"Wrote {args.output}")
    print(f"Wrote {len(written)} command files to {args.commands_dir}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
