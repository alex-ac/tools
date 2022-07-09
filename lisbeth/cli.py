import argparse
import pathlib
import logging

from typing import Optional

from .recipy import Recipy, Context, BaseBuildContext


def run(argv: Optional[list[str]] = None) -> int:
    logging.basicConfig(level='INFO')
    parser = argparse.ArgumentParser(__package__)
    parser.add_argument('--root', type=pathlib.Path, required=True,
                        help='Root working directory.')
    args = parser.parse_args(argv)

    root = args.root.resolve()
    distfiles = root / 'distfiles'
    srcs = root / 'srcs'
    work = root / 'work'
    roots = root / 'roots'
    logs = root / 'logs'

    Recipy.collect()

    ctx = Context()
    base_ctx = BaseBuildContext(
        distfiles=distfiles,
        srcs=srcs,
        work=work,
        roots=roots,
        logs=logs)
    logging.info('Created context: %r', ctx)
    logging.info('Base build context: %r', base_ctx)

    return 0
