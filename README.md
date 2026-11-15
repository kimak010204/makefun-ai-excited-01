# The Smallest Surfer on the Biggest Wave

A tiny mouse in a red cloak surfing a colossal wave that curls up into a
galaxy. The joke — and the thrill — is the scale: the smallest rider on
the biggest wave, riding pure momentum and energy straight into the stars.

## How it works

`main.py` (Python 3.13, standard library only, no network access) copies
the artwork `entry.png` sitting next to it into
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`), creating
the output directory if needed. After copying it verifies that the output
has the same size and the same SHA-256 checksum as the source, and exits
non-zero with a clear error message if the source is missing, too large
(over 1 MiB), or the copy does not match.

## Determinism

The output is a byte-for-byte copy of the bundled image, so every run
produces identical bytes: same SHA-256, every time.
