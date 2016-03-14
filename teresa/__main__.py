#!/usr/bin/env python3
# encoding=utf-8

import argparse

import ipodshuffle.version
from . import version as self_version
from . import translate as _
from .utils import add_optional_group, add_args_help


def main():

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        # usage='%(prog)s <command> [options]',
        epilog=_("Try '%(prog)s <command> -h' for command help."),
        add_help=False
    )
    optional_group = add_optional_group(parser)
    add_args_help(optional_group)
    optional_group.add_argument('-v', '--version',
                                action='version',
                                help=_("show program's version number and exit"),
                                version='%(prog)s {} (use ipodshuffle {})'.format(
                                    self_version.__version__,
                                    ipodshuffle.version.__version__)
                                )

    subparsers = parser.add_subparsers(title=_('commands'),  metavar='<command>')

    from . import show, set_, sync

    set_.register(subparsers)

    show.register(subparsers)

    sync.register(subparsers)

    args = parser.parse_args()

    if not hasattr(args, 'func'):
        exit(parser.print_help())

    args.func(args)

if __name__ == '__main__':
    main()
