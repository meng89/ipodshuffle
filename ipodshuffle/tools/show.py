import os
import pprint

from ipodshuffle.db import Shuffle as ShuffleDB


L1 = '=' * 80
L2 = '-' * 50


def show(args):
    base = args.base
    _ctrl = 'iPod_Control'

    _itunessd_chunk = open(base + '/' + _ctrl + '/iTunes/iTunesSD', 'rb').read()

    _itunesstats_chunk = None
    _itunesstats_path = base + '/' + _ctrl + '/iTunes/iTunesStats'

    if os.path.exists(_itunesstats_path):
        _itunesstats_chunk = open(_itunesstats_path, 'rb').read()

    shuffledb = ShuffleDB(_itunessd_chunk, _itunesstats_chunk)

    print(L1)
    print('enable_voiceover: ', shuffledb.enable_voiceover)
    print('max_volumex: ', shuffledb.max_volume)
    print('number of playlists: ', len(shuffledb.playlists))
    print(L1)
    print()

    print('Tracks:')
    print(L1)
    for track in shuffledb.tracks:
        print('INDEX: ', shuffledb.tracks.index(track))
        itunes_sd, itunes_stats = track.get_dics()
        print('ITUNES_SD:')
        pprint.pprint(itunes_sd)
        print('ITUNES_STATS:')
        pprint.pprint(itunes_stats)

        if track != shuffledb.tracks[-1]:
            print(L2)

    print(L1)

    print()

    print('Playlists:')
    print(L1)
    for pl in shuffledb.playlists:
        print('type: ', pl.type)
        print('index of tracks: ', pl.indexes_of_tracks)
        print('dbid: ', pl.dbid)

        if pl != shuffledb.playlists[-1]:
            print(L2)
    print(L1)


def register(parser):
    import argparse
    from .teresa import add_optional_group, add_args_help, add_args_ipod_base
    from .teresa import translate as _

    parser_show = parser.add_parser('show', help=_('show ipod low level DB'),
                                    formatter_class=argparse.RawTextHelpFormatter,

                                    epilog=_('Example of use:') + '\n' +
                                    '  %(prog)s -b /media/ipod_base',

                                    add_help=False
                                    )

    optionl_group = add_optional_group(parser_show)

    add_args_help(optionl_group)

    add_args_ipod_base(optionl_group)

    optionl_group.set_defaults(func=show)
