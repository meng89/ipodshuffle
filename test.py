#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint

import shuffle.itunessd, shuffle.itunesstats

itunessd_path = 'iTunesSD'
itunesstats_path = 'iTunesStats'

itunessd = open(itunessd_path, 'rb').read()

itunesstats = open(itunesstats_path, 'rb').read()

pp = pprint.PrettyPrinter(indent=4)

# print(pp.pprint(a), end='\n\n\n')
# print(pp.pprint(b), end='\n\n\n')
# print(pp.pprint(c), end='\n\n\n')


def test_itunessd():
    a, b, c = shuffle.itunessd.itunessd_to_dics(itunessd)
    itunessd2 = shuffle.itunessd.dics_to_itunessd(a, b, c)

    print(len(itunessd), len(itunessd2), itunessd == itunessd2)

    if itunessd != itunessd2:
        open('iTunesSD2', 'wb').write(itunessd2)
        i = 0
        while len(itunessd) > i:
            if itunessd[i] != itunessd2[i]:
                print(i, itunessd[i:i + 1], itunessd2[i:i + 1])

            i += 1


def test_itunesstats():
    tracks_dics = shuffle.itunesstats.itunesstats_to_dics(itunesstats)
    itunesstats2 = shuffle.itunesstats.dics_to_itunesstats(tracks_dics)
    print(len(itunesstats), len(itunesstats2), itunesstats == itunesstats2)


def tmp2():
    db_dic, tracks_dics, playlists_dics_and_indexes = shuffle.itunessd.itunessd_to_dics(itunessd)

    for track_dic in tracks_dics:
        if track_dic['filename'] == '/iPod_Control/Music/F02/KVRT.m4a':
            track_dic['remember_playing_pos'] = True
            # 4294967289 old
            # 4294967295 number max
            #                           very samll
            # 4294967280 > 4294967250 > 4294967200 =? 4294967170
            #

            # track_dic['pregap'] = 0
            # track_dic['postgap'] = 0

    new_itunessd = shuffle.itunessd.dics_to_itunessd(db_dic, tracks_dics, playlists_dics_and_indexes)

    open(itunessd_path, 'wb').write(new_itunessd)
    # print(pp.pprint(tracks_dics))


def print1():
    a, b, c = shuffle.itunessd.itunessd_to_dics(open(itunessd_path, 'rb').read())
    print(pp.pprint(b))

if __name__ == '__main__':
    # tmp2()
    # print1()
    test_itunessd()
    test_itunesstats()
