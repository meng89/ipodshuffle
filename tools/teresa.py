#!/usr/bin/env python3

import argparse

from ipodshuffle.tools import set_, sync

from tools import show


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(title='Commands')

    set_.register(subparsers)

    show.register(subparsers)

    sync.register(subparsers)

    args = parser.parse_args()

    args.func(args)

if __name__ == '__main__':
    main()
