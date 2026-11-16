#!/usr/bin/env python3
"""Copy entry.png to $MAKEFUN_OUTPUT_DIR/entry.png and verify it byte-identical."""

import hashlib
import os
import shutil
import sys


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("error: MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1

    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    if not os.path.isfile(src):
        print(f"error: source not found: {src}", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)

    if sha256_of(src) != sha256_of(dst):
        print("error: copy is not byte-identical (sha256 mismatch)", file=sys.stderr)
        return 1

    print(f"ok: copied entry.png to {dst} (sha256 verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
