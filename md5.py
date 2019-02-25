#!/usr/bin/env python3

import hashlib
from functools import partial
import argparse


def md5sum(filename):
    with open(filename, mode="rb") as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b""):
            d.update(buf)
    return d.hexdigest()


def checkmd5sum(filename, file_md5):
    """
    Verify 'filename' md5sum is 'file_md5'
    return True or False
    """
    if md5sum(filename) == file_md5:
        return True
    else:
        return False


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file_to_md5",
        nargs="+",
        help="""
        one or more files for which to calculate MD5 sum.
        """,
    )

    args = parser.parse_args()

    for nextfile in args.file_to_md5:
        print(md5sum(nextfile), nextfile)

    """
    Nothing to do, I will print my own MD5sum...
    """
    print(md5sum("md5.py"))


if __name__ == "__main__":
    main()
