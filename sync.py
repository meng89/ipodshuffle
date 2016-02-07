#!/usr/bin/env python3

import os
import langdetect

import ipodshuffle

from ipodshuffle.itunessd import NORMAL,PODCAST,AUDIOBOOK


dir_path = '/media/data/temp/sounds/'


def visit(dir_files_list, dirname, names):
    dir_files_list.append(dirname, names)


def get_dirs(src):
    dirs = []
    # os.path.walk(src, visit, dir_files_list)
    for top, sub_dirs, names in os.walk(src):
        dirs.append(top)
    return dirs


def get_files(dire):
    files = []
    for top, sub_dirs, names in os.walk(dire, followlinks=True):
        files.extend([os.path.join(top, name) for name in names])
    return files


def guess_playlist_type(files):
    pl_type = NORMAL

    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext == '.m4b' and True:
            pl_type = AUDIOBOOK
            break
        elif ext == '.rss':
            pl_type = PODCAST
            break

    return pl_type


def sync(src, ipod=None):
    dires = get_dirs(src)

    for dire in dires:
        file


if __name__ == '__main__':

    # sync(dir_path)
    for one in sorted(get_files(dir_path)):
        print(one)
