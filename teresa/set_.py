from ipodshuffle.shuffle import Shuffle

from .utils import str2bool

from .utils import add_optional_group, add_args_help, add_args_ipod_base

from . import translate as _

description = "Set enable_voiceover and max_volume"


def set_(args):
    ipod = Shuffle(args.base)

    if args.voiceover is not None:
        ipod.enable_voiceover = args.voiceover

    if args.max_volume is not None:
        ipod.max_volume = args.max_volume

    ipod.write_db()


def register(parser):
    import argparse
    # optional_group = parser.add_argument_group(_('optional arguments'))
    # parser_set = optional_group.add_argument('-h', '--help', action='help', help=_('show this help message and exit'))

    parser_set = parser.add_parser('set', help=_('set voiceover enable or disable, set max volume'),
                                   formatter_class=argparse.RawTextHelpFormatter,

                                   epilog=_('Example of use:') + '\n' +
                                   '  %(prog)s -b /media/ipod_base -v true -m 15',

                                   add_help=False,
                                   )

    optional_group = add_optional_group(parser_set)

    add_args_help(optional_group)

    add_args_ipod_base(optional_group)

    optional_group.add_argument('-v', dest='voiceover', metavar='<bool>', type=str2bool,
                                help=_('enable or disable voiceover, true for enable, false for disable'))

    optional_group.add_argument('-m', dest='max_volume', metavar='<int>', type=int,
                                help=_('max volume, 0 is do not limit'))

    optional_group.set_defaults(func=set_)
