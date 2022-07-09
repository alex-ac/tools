import argparse

from typing import Optional


def run(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(__package__)
    parser.parse_args(argv)
    return 0
