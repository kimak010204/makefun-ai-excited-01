#!/usr/bin/env python3
"""Copy the entry image to the output directory.

The competition entry is the image ``entry.png`` that sits next to this
script. Running this script copies it to ``$MAKEFUN_OUTPUT_DIR/entry.png``
(default ``/output/entry.png``) and verifies the copy byte for byte, so the
file that reaches the judge is exactly the image that was built.

Deterministic: the same input always produces the same output bytes.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import sys
from pathlib import Path

MAX_SOURCE_BYTES = 1 << 20  # 1 MiB


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    source = Path(__file__).resolve().parent / "entry.png"
    raw_output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    if not raw_output_dir.strip():
        print("error: MAKEFUN_OUTPUT_DIR is set but empty", file=sys.stderr)
        return 1
    output_dir = Path(raw_output_dir)
    target = output_dir / "entry.png"

    if not source.is_file():
        print(f"error: source image missing: {source}", file=sys.stderr)
        return 1

    source_size = source.stat().st_size
    if source_size == 0:
        print(f"error: source image is empty: {source}", file=sys.stderr)
        return 1
    if source_size > MAX_SOURCE_BYTES:
        print(
            f"error: source image too large: {source_size} bytes "
            f"(limit {MAX_SOURCE_BYTES})",
            file=sys.stderr,
        )
        return 1

    if output_dir.resolve() == source.parent.resolve():
        print(
            "error: output directory is the source directory: "
            f"{output_dir}",
            file=sys.stderr,
        )
        return 1

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(
            f"error: cannot create output directory {output_dir}: {exc}",
            file=sys.stderr,
        )
        return 1

    try:
        shutil.copyfile(source, target)
    except OSError as exc:
        print(f"error: cannot copy {source} to {target}: {exc}", file=sys.stderr)
        return 1

    target_size = target.stat().st_size
    if target_size != source_size:
        print(
            f"error: size mismatch after copy: source {source_size} bytes, "
            f"output {target_size} bytes",
            file=sys.stderr,
        )
        return 1

    if _sha256(target) != _sha256(source):
        print("error: sha256 mismatch after copy", file=sys.stderr)
        return 1

    print(f"copied {source} -> {target} ({target_size} bytes, sha256 verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
