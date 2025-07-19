#!/usr/bin/env python3
import argparse
from pathlib import Path

# built‑in excludes
DEFAULT_EXCLUDES = {
    "changelog.md",
    "generate_tree.py",
    "mod.ini",
    "mod_files.txt",        # never list the output file
    "mod_version.ini",
}

def load_excludes(exclude_file: Path) -> set[str]:
    """
    Read one-relative-path-per-line (ignore blank/# lines) and return a set.
    """
    excludes = set()
    if exclude_file and exclude_file.is_file():
        for line in exclude_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            excludes.add(line)
    return excludes

def build_mod_files(root: Path, excludes: set[str]):
    """
    Walk root, write all non‑excluded files as "add REL_PATH" into mod_files.txt.
    """
    out_path = root / "mod_files.txt"
    all_files = sorted(p for p in root.rglob("*") if p.is_file())
    with out_path.open("w", encoding="utf-8") as outf:
        for p in all_files:
            rel = p.relative_to(root).as_posix()
            if rel in excludes:
                continue
            outf.write(f"add {rel}\n")
    return out_path

def main():
    parser = argparse.ArgumentParser(
        description="Scan a directory and emit mod_files.txt of all files, excluding specified ones."
    )
    parser.add_argument(
        "-d", "--directory",
        type=Path,
        default=Path("."),
        help="Root directory to scan (default: current directory)"
    )
    parser.add_argument(
        "-e", "--exclude-file",
        type=Path,
        help="Optional extra exclude-list (one relative path per line)."
    )
    args = parser.parse_args()

    root = args.directory.resolve()

    # Start with the built‑ins
    excludes = set(DEFAULT_EXCLUDES)

    # Add any user‑supplied excludes
    if args.exclude_file:
        excludes |= load_excludes(args.exclude_file.resolve())

    # Generate mod_files.txt
    out_file = build_mod_files(root, excludes)
    print(f"Wrote add‑list to {out_file}")

if __name__ == "__main__":
    main()
