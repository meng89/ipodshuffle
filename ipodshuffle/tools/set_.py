from ipodshuffle.shuffle import Shuffle

from . import str2bool

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
    parser_set = parser.add_parser('set', help='set voiceover enable or disable, set max volume',
                                   formatter_class=argparse.RawTextHelpFormatter,
                                   epilog='Two examples of use:\n'
                                          '  %(prog)s -b /media/ipod_base -v true -m 15'
                                   )

    parser_set.add_argument('-b', dest='base', help='ipod base path', metavar='<path>', required=True)

    parser_set.add_argument('-v', dest='voiceover', metavar='BOOL', type=str2bool,
                            help='enable or disable voiceover, true for enable, false for disable')

    parser_set.add_argument('-m', dest='max_volume', metavar='<NUM>', type=int,
                            help='max volume, 0 is do not limit')

    parser_set.set_defaults(func=set_)
