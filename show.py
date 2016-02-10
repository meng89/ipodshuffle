import ipodshuffle.shuffle


from ipodshuffle.shuffle import PL_MAPS
from ipodshuffle.audio import TYPE_MAP

L1 = '=' * 80
L2 = '-' * 50


def show(ipod):
    shuffle = ipodshuffle.shuffle.Shuffle(ipod)

    print(L1)
    print('enable_voiceover: ', shuffle.enable_voiceover)
    print('max_volumex: ', shuffle.max_volume)
    print('number of tracks: ', len(shuffle.tracks))
    print('number of playlists: ', len(shuffle.playlists))
    print(L1)
    print()

    print('Tracks:')
    print(L1)
    for track in shuffle.tracks:
        print('index: ', shuffle.tracks.index(track))
        print('type: ', TYPE_MAP[track.type])
        print('filename: ', track.filename)
        print('dbid: ', track.dbid)
        if track != shuffle.tracks[-1]:
            print(L2)
    print(L1)

    print()

    print('Playlists:')
    print(L1)
    for pl in shuffle.playlists:
        print('type: ', PL_MAPS[pl.type])

        print('dbid: ', pl.dbid)
        print('number of tracks: ', len(pl.tracks))
        print('index of tracks: ', [shuffle.tracks.index(track) for track in pl.tracks])
        if pl != shuffle.playlists[-1]:
            print(L2)
    print(L1)
