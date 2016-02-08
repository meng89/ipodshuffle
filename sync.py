#!/usr/bin/env python3

import os

import langid

import langdetect

import ipodshuffle

from ipodshuffle.audio import get_type as get_audio_type

from ipodshuffle.itunessd import MASTER, NORMAL, PODCAST, AUDIOBOOK


dir_path = '/media/data/temp/sounds/'
dir_path2 = '/media/data/ipod_src/'


def visit(dir_files_list, dirname, names):
    dir_files_list.append(dirname, names)


def get_all_dires(dire):
    dirs = []
    # os.path.walk(src, visit, dir_files_list)
    for top, sub_dirs, names in os.walk(dire, followlinks=True):
        dirs.append(top)
    return dirs


def get_all_files(dire):
    files = []
    for top, sub_dirs, names in os.walk(dire, followlinks=True):
        files.extend([os.path.join(top, name) for name in names])
    return files


def get_normals(dire):
    pls = []
    dires = get_all_dires(dire)
    for dire in dires:
        legal_files = [file for file in get_all_files(dire) if get_audio_type(file)]
        if legal_files:
            pls.append((os.path.split(dire)[1], sorted(legal_files)))

    return pls


def get_podcasts(dire):
    podcasts = []

    return podcasts


def get_audiobooks(dire):
    audiobooks = []

    return audiobooks


def sync(src, ipod_base=None):

    src = os.path.realpath(src)

    pls = get_normals(src+'/'+'music')
    master = pls[0]
    normals = pls[1:]
    podcasts = get_podcasts(src+'/'+'podcasts')
    audiobooks = get_audiobooks(src+'/'+'audiobooks')

    # ipod = ipodshuffle.Shuffle(ipod)
    # ipod.playlists.clear()
    # ipod.tracks.clear()

    # master = ipod.playlists.add()
    # master.type = MASTER
    langid.set_languages(['en', 'zh', 'ja', 'de'])
    for file in master[1]:
        name = os.path.splitext(os.path.split(file)[1])[0]
        name2 = name
        print(langid.classify(name2), name2)


if __name__ == '__main__':
    sync(dir_path2)

