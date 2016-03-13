#!/usr/bin/env python3
# encoding=utf-8

import argparse

import ipodshuffle.version
from . import version as self_version

import gettext

import locale

_usr_share_locale = '/usr/share/locale'
_locale_dirs = gettext.find('teresa', _usr_share_locale)

locale_lang = gettext.translation("teresa",
                                  _usr_share_locale if _locale_dirs else 'ipodshuffle/tools/locale',
                                  languages=[locale.getlocale()[0]], fallback=True)
locale_lang.install(True)

translate = locale_lang.gettext
_ = translate


def add_optional_group(parser):
    return parser.add_argument_group(_('optional arguments'))


def add_args_ipod_base(parser):
    parser.add_argument('-b', dest='base', help=_('ipod base path'), metavar='<path>', required=True)


def add_args_help(parser):
    parser.add_argument('-h', '--help', action='help',  help=_('show this help message and exit'))


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

    from ipodshuffle.tools import show, set_, sync

    set_.register(subparsers)

    show.register(subparsers)

    sync.register(subparsers)

    args = parser.parse_args()

    if not hasattr(args, 'func'):
        exit(parser.print_help())

    args.func(args)

if __name__ == '__main__':
    main()
