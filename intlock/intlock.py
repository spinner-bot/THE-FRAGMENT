#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""intlock - lock/unlock a file with a single integer key.

Container format is documented in FORMAT.md.

Usage:
    python intlock.py lock   INPUT OUTPUT --key 123456789
    python intlock.py unlock INPUT OUTPUT --key 123456789
"""
import argparse
import hashlib
import hmac
import os
import struct
import sys
import tempfile

MAGIC = b"INTLOCK1"
SALT_LEN = 16
TAG_LEN = 16
DEFAULT_ITERATIONS = 600_000
HEADER_FIXED = len(MAGIC) + SALT_LEN + 4 + 8
MK_LEN = 64


def derive_keys(key_int: int, salt: bytes, iterations: int):
    """Return (encryption_key, mac_key) derived from the integer key."""
    password = str(key_int).encode("ascii")
    dk = hashlib.pbkdf2_hmac("sha256", password, salt, iterations, dklen=MK_LEN)
    return dk[:32], dk[32:]


def xor_keystream(data: bytes, enc_key: bytes) -> bytes:
    out = bytearray(len(data))
    for block_index, offset in enumerate(range(0, len(data), 32)):
        counter = block_index.to_bytes(8, "big")
        stream = hashlib.sha256(enc_key + counter).digest()
        chunk = data[offset:offset + 32]
        out[offset:offset + len(chunk)] = bytes(
            a ^ b for a, b in zip(chunk, stream)
        )
    return bytes(out)


def lock_bytes(data: bytes, key: int, iterations: int = DEFAULT_ITERATIONS) -> bytes:
    salt = os.urandom(SALT_LEN)
    enc_key, mac_key = derive_keys(key, salt, iterations)
    ciphertext = xor_keystream(data, enc_key)
    header = MAGIC + salt + struct.pack(">IQ", iterations, len(ciphertext))
    tag = hmac.new(mac_key, header + ciphertext, hashlib.sha256).digest()[:TAG_LEN]
    return header + ciphertext + tag


def unlock_bytes(blob: bytes, key: int) -> bytes:
    if len(blob) < HEADER_FIXED + TAG_LEN:
        raise ValueError("unlock failed: not an intlock container")
    if blob[:len(MAGIC)] != MAGIC:
        raise ValueError("unlock failed: not an intlock container")
    pos = len(MAGIC)
    salt = blob[pos:pos + SALT_LEN]
    pos += SALT_LEN
    iterations, length = struct.unpack(">IQ", blob[pos:pos + 12])
    pos += 12
    if iterations <= 0 or length != len(blob) - HEADER_FIXED - TAG_LEN:
        raise ValueError("unlock failed: not an intlock container")
    ciphertext = blob[pos:pos + length]
    tag = blob[pos + length:]

    enc_key, mac_key = derive_keys(key, salt, iterations)
    expected = hmac.new(mac_key, blob[:HEADER_FIXED] + ciphertext,
                        hashlib.sha256).digest()[:TAG_LEN]
    if not hmac.compare_digest(tag, expected):
        raise ValueError("unlock failed: wrong key or corrupted file")
    return xor_keystream(ciphertext, enc_key)


def _read(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def _write_atomic(path: str, data: bytes) -> None:
    directory = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".intlock-")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def parse_key(text: str) -> int:
    try:
        value = int(text, 10)
    except ValueError:
        raise argparse.ArgumentTypeError("key must be a non-negative decimal integer")
    if value < 0:
        raise argparse.ArgumentTypeError("key must be a non-negative decimal integer")
    return value


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Lock/unlock a file with an integer key.")
    sub = parser.add_subparsers(dest="command", required=True)

    for name, help_text in (("lock", "encrypt a file"), ("unlock", "decrypt a file")):
        p = sub.add_parser(name, help=help_text)
        p.add_argument("input")
        p.add_argument("output")
        p.add_argument("--key", required=True, type=parse_key,
                       help="non-negative integer key (decimal)")
        if name == "lock":
            p.add_argument("--iterations", type=int, default=DEFAULT_ITERATIONS,
                           help="PBKDF2 iterations (default: %d)" % DEFAULT_ITERATIONS)

    args = parser.parse_args(argv)
    try:
        if args.command == "lock":
            if args.iterations < 1:
                parser.error("iterations must be positive")
            _write_atomic(args.output, lock_bytes(_read(args.input), args.key,
                                                  args.iterations))
        else:
            _write_atomic(args.output, unlock_bytes(_read(args.input), args.key))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except OSError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
