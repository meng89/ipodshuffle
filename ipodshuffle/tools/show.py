
from ipodshuffle import Shuffle
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


def show(base):

    player = Shuffle(base)

    print(L1)
    print('enable_voiceover: ', player.db.enable_voiceover)
    print('max_volumex: ', player.db.max_volume)
    print('number of tracks: ', len(player.db.tracks))
    print('number of playlists: ', len(player.db.playlists))
    print(L1)
    print()

    print('Tracks:')
    print(L1)
    for track in player.db.tracks:
        print('INDEX: ', player.db.tracks.index(track))
        print('type: ', AUDIO_MAP[track.type])
        print('filename: ', track.filename)
        text, lang = player.db.tracks_voicedb.get_text_lang(track.dbid + '.wav')
        print('dbid: {}, lang: {}, text: {}.'.format(track.dbid, repr(lang), repr(text)))

        if track != player.db.tracks[-1]:
            print(L2)
    print(L1)

    print()

    print('Playlists:')
    print(L1)
    for pl in player.db.playlists:
        print('type: ', PL_MAP[pl.type])
        if pl.type != MASTER:
            text, lang = player.db.playlists_voicedb.get_text_lang(pl.dbid + '.wav')
            print('dbid: {} (lang: {}, text: {})'.format(pl.dbid, repr(lang), repr(text)))
        else:
            print()
            # print('<TEXT AND LANG WAS DEFINED IN MESSAGES>')
        print('number of tracks: ', len(pl.Tracks_indexes))
        print('index of tracks: ', [player.db.tracks.index(track) for track in pl.Tracks_indexes])
        if pl != player.db.playlists[-1]:
            print(L2)
    print(L1)

fun = show


def get_help_strings(indet=None):
    indet = indet or 0
    s = ' ' * indet + 'usage:  base=<path>\n'
    return s
