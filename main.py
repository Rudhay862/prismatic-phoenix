#!/usr/bin/env python3
"""Copy entry.png to the make.fun output directory, verifying SHA-256.

The entry image is the file ``entry.png`` that sits next to this script
(a 1024x1024 PNG, "Prismatic Phoenix"). This program copies it to the
directory given by the ``MAKEFUN_OUTPUT_DIR`` environment variable
(default ``/output``), then proves the copy is byte-identical by checking
that both the file size and the SHA-256 hash of the copy match the source.

Exit status is 0 on success and 1 on any failure (missing source file,
unwritable output directory, or a size/hash mismatch after copying).
"""
import hashlib
import os
import shutil
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not os.path.isfile(SRC):
        print(f"error: source image not found: {SRC} "
              "(expected entry.png next to main.py)", file=sys.stderr)
        sys.exit(1)
    try:
        os.makedirs(OUT_DIR, exist_ok=True)
    except OSError as exc:
        print(f"error: cannot create output directory {OUT_DIR}: {exc}",
              file=sys.stderr)
        sys.exit(1)
    try:
        shutil.copyfile(SRC, DST)
    except OSError as exc:
        print(f"error: failed to copy {SRC} to {DST}: {exc}",
              file=sys.stderr)
        sys.exit(1)
    src_size = os.path.getsize(SRC)
    dst_size = os.path.getsize(DST)
    if src_size != dst_size:
        print(f"error: size mismatch after copy: source {src_size} bytes "
              f"!= copy {dst_size} bytes", file=sys.stderr)
        sys.exit(1)
    src_hash = sha256(SRC)
    dst_hash = sha256(DST)
    if src_hash != dst_hash:
        print(f"error: SHA-256 mismatch: source {src_hash} != copy {dst_hash}",
              file=sys.stderr)
        sys.exit(1)
    print(f"copied {SRC} -> {DST} ({src_size} bytes)")
    print(f"size verified: {src_size} bytes")
    print(f"SHA-256 verified: {src_hash}")


if __name__ == "__main__":
    main()
