#!/usr/bin/env python3

import argparse

from ipodshuffle.tools import show, set_, sync


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Try '%(prog)s <command> --help' for more help!"
    )

    subparsers = parser.add_subparsers(title='Commands')

    set_.register(subparsers)

    show.register(subparsers)

    sync.register(subparsers)

    args = parser.parse_args()

    args.func(args)

if __name__ == '__main__':
    main()
