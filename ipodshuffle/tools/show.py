
from ipodshuffle import Shuffle, PL_MAP, Master, Normal, Podcast, Audiobook

from ipodshuffle.audio import AUDIO_MAP


L1 = '=' * 80
L2 = '-' * 50


description = "Show player's information"


def help_():
    print()
    print('usage: ', end='')
    print('base=<path_to_ipod>')
    print('Only show. No control.')
    print()


def show(args):

    ipod = Shuffle(args.base)

    print(L1)
    print('enable_voiceover: ', ipod.enable_voiceover)
    print('max_volumex: ', ipod.max_volume)
    print('number of playlists: ', len(ipod.playlists))
    print(L1)
    print()

    print('Tracks:')
    print(L1)
    print(L1)

    print()

    print('Playlists:')
    print(L1)
    for pl in ipod.playlists:
        print('type: ', type(pl))
        print('number of tracks: ', len(pl.tracks))
        if not isinstance(pl, Master):
            try:
                text, lang = pl.voice
                print('voice: ', lang, text)
            except KeyError:
                raise KeyError
        if pl != ipod.playlists[-1]:
            print(L2)
    print(L1)


def register(parser):
    import argparse

    parser_show = parser.add_parser('show', help='show ipod informations',
                                    formatter_class=argparse.RawTextHelpFormatter,
                                    epilog='Example of use:\n'
                                           '  %(prog)s -b /media/ipod_base'
                                    )

    parser_show.add_argument('-b', dest='base', help='ipod base path', metavar='<path>', required=True)

    parser_show.set_defaults(func=show)
