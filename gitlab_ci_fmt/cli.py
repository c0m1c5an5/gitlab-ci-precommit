import argparse
import pathlib
import sys

from gitlab_ci_fmt.utils import batch_format_files


def cli(argv: list[str] = sys.argv[1:]) -> None:
    sys.tracebacklimit = 0
    parser = argparse.ArgumentParser(prog=__package__)
    parser.add_argument("files", nargs="+", type=pathlib.Path, help="Files to format.")
    args = parser.parse_args(argv)

    batch_format_files(args.files)
