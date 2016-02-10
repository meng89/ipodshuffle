#!/usr/bin/env python3

import sys

import pprint

import ipodshuffle.itunessd
import ipodshuffle.itunesstats

import ipodshuffle


def show(ipod):
    shuffle = ipodshuffle.Shuffle(ipod)
    print('=' * 50)
    print('enable_voiceover: ', shuffle.enable_voiceover)
    print('max_volumex: ', shuffle.max_volume)
    print('number of tracks: ', len(shuffle.tracks))
    print('number of playlists: ', len(shuffle.playlists))
    print('=' * 50)

    print()

    print('=' * 50)
    for track in shuffle.tracks:
        print('filename: ', track.filename)
        print('dbid: ', track.dbid)
    print('=' * 50)

    print()

    print('=' * 50)
    for pl in shuffle.playlists:
        print('type: ', pl.type)
        print('dbid: ', pl.dbid)
        print('number of tracks: ', len(pl.tracks))
        print('index of tracks: ', [shuffle.tracks.index(track) for track in pl.tracks])
    print('=' * 50)


if __name__ == '__main__':
    show(sys.argv[1])
