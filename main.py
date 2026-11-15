#!/usr/bin/env python3
"""The Smallest Surfer on the Biggest Wave.

Copies the entry artwork (entry.png, next to this script) into the
make.fun output directory. Standard library only, no network access,
fully deterministic: the output is a byte-for-byte copy of the source.
"""

import hashlib
import os
import shutil
import sys

SOURCE_NAME = "entry.png"
MAX_BYTES = 1_048_576


def sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(script_dir, SOURCE_NAME)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    dest = os.path.join(output_dir, SOURCE_NAME)

    if not os.path.isfile(source):
        print(f"error: source image not found: {source}", file=sys.stderr)
        return 1

    src_size = os.path.getsize(source)
    if src_size > MAX_BYTES:
        print(
            f"error: source image too large: {src_size} bytes "
            f"(limit {MAX_BYTES})",
            file=sys.stderr,
        )
        return 1

    os.makedirs(output_dir, exist_ok=True)
    shutil.copyfile(source, dest)

    dst_size = os.path.getsize(dest)
    if dst_size != src_size:
        print(
            f"error: size mismatch after copy: source {src_size} bytes, "
            f"output {dst_size} bytes",
            file=sys.stderr,
        )
        return 1

    if sha256_file(dest) != sha256_file(source):
        print("error: checksum mismatch after copy", file=sys.stderr)
        return 1

    print(f"wrote {dest} ({dst_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
