#!/usr/bin/env python3

import argparse

from ipodshuffle.tools import show, set_, sync

import ipodshuffle.version
from . import version as self_version


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        # usage='%(prog)s <command> [options]',
        epilog="Try '%(prog)s <command> -h' for command help!"
    )

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {} (use ipodshuffle {})'.format(
                            self_version.__version__,
                            ipodshuffle.version.__version__))

    subparsers = parser.add_subparsers(title='Commands',  metavar='<command>')
    # subparsers = parser.add_subparsers()

    set_.register(subparsers)

    show.register(subparsers)

    sync.register(subparsers)

    args = parser.parse_args()

    args.func(args)

if __name__ == '__main__':
    main()
