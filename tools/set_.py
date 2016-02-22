from ipodshuffle.shuffle import Shuffle

from tools import str2bool

description = "Set enable_voiceover and max_volume"


def set_(args):
    ipod = Shuffle(args.base)

    if args.voiceover is not None:
        ipod.enable_voiceover = args.voiceover

    if args.max_volume is not None:
        ipod.max_volume = args.max_volume

    ipod.write()


def register(parser):

    parser_set = parser.add_parser('set', help='set max_volume/enable_voiceover')

    parser_set.add_argument('-b', '--base', help='ipod base', metavar='<path>', required=True)

    parser_set.add_argument('-v', '--voiceover', type=str2bool, help='enable/disable voiceover')

    parser_set.add_argument('-m', '--max_volume', type=int, help='max volume, 0 is do not limit', metavar='<int>')

    parser_set.set_defaults(func=set_)
