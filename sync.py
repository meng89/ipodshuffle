#!/usr/bin/env python3

import os
import tempfile

import langid

import ipodshuffle.tts.voicerss
import ipodshuffle.tts.tts_db

import ipodshuffle.tools as tools

import ipodshuffle

from character_detect import has_ja_char, has_ko_char

from ipodshuffle.audio import get_type as get_audio_type

from ipodshuffle.itunessd import MASTER, NORMAL, PODCAST, AUDIOBOOK


dir_path = '/media/data/temp/sounds/'
dir_path2 = '/media/data/ipod_src/'

config_dir = os.path.join(os.path.expanduser('~'), '.config/ipodshuffle')
cache_dir = os.path.join(os.path.expanduser('~'), '.cache/ipodshuffle')
os.makedirs(config_dir, exist_ok=True)
os.makedirs(cache_dir, exist_ok=True)


def visit(dir_files_list, dirname, names):
    dir_files_list.append(dirname, names)


def get_all_dires(dire):
    dirs = []
    # os.path.walk(src, visit, dir_files_list)
    for top, sub_dirs, names in os.walk(dire, followlinks=True):
        dirs.append(top)
    return dirs


def get_normals(dire):
    pls = []
    dires = get_all_dires(dire)
    for dire in dires:
        legal_files = [file for file in tools.get_all_files(dire) if get_audio_type(file)]
        if legal_files:
            pls.append((os.path.split(dire)[1], sorted(legal_files)))

    return pls


def get_podcasts(dire):
    podcasts = []

    return podcasts


def get_audiobooks(dire):
    audiobooks = []

    return audiobooks


def cjk_fix(seted_langs, code, text):
    fixed_code = code
    if not seted_langs or 'zh' in seted_langs:
        if code == 'ja':
            if not has_ja_char(text):
                fixed_code = 'zh'
        elif code == 'ko':
            if not has_ko_char(text):
                fixed_code = 'zh'

    return fixed_code


def sync(src=None, ipod=None, enable_voiceover=True, langs=None, ttskey=None):

    src = src or dir_path2

    tts_engine = ipodshuffle.tts.voicerss

    src = os.path.realpath(src)

    langs = langs or []

    pls = get_normals(src+'/'+'music')
    master_files = pls[0][1]
    normals = pls[1:]
    podcasts = get_podcasts(src+'/'+'podcasts')
    audiobooks = get_audiobooks(src+'/'+'audiobooks')

    shuffle = ipodshuffle.Shuffle(ipod)
    shuffle.enable_voiceover = enable_voiceover
    shuffle.sounds.clean_logs()

    shuffle.playlists.clear()
    shuffle.tracks.clear()

    master_pl = shuffle.playlists.add()
    master_pl.type = MASTER

    ttsdb = ipodshuffle.tts.tts_db.Db(os.path.join(cache_dir, 'tts_logs.json'), os.path.join(cache_dir, 'voices'))

    tts_codes = {}

    for code in langs:
        if not tts_engine.is_available(code):
            raise Exception
        iso_639_1_code = tts_engine.to_iso_639_1(code)
        tts_codes[iso_639_1_code] = code

    if tts_codes:
        langid.set_languages(tts_codes.keys())

    for file in master_files:
        text = os.path.splitext(os.path.split(file)[1])[0]
        # text = text.split('-')[1]

        langid_code = langid.classify(text)[0]

        tts_code = tts_codes[langid_code] if langid_code in tts_codes.keys()\
            else tts_engine.to_lang_codes(langid_code)[0]

        path_in_ipod = shuffle.sounds.add(file)

        track = None
        for TRACK in shuffle.tracks:
            if TRACK.filename == path_in_ipod:
                track = TRACK

        if not track:
            track = shuffle.tracks.add(path_in_ipod)

        # print(tts_code, text)

        master_pl.tracks.append(track)

        track_dbid = shuffle.tracks_voicedb.get_dbid(text, tts_code)

        if not track_dbid:  # the voice not in ipod

            tts_path = ttsdb.get_path_by_text_lang(text, tts_code)

            if not tts_path:  # the voice not in local
                data = tts_engine.tts(text, tts_code, ttskey)
                print('Get a new voice: {}, {}'.format(tts_code, text))
                tmp_file = tempfile.NamedTemporaryFile(delete=False)
                tmp_file_name = tmp_file.name
                tmp_file.close()

                with open(tmp_file_name, 'wb') as f:
                    f.write(data)

                ttsdb.add(tmp_file_name, text, tts_code)
                tts_path = ttsdb.get_path_by_text_lang(text, tts_code)

            shuffle.tracks_voicedb.add(tts_path, text, tts_code)

            track_dbid = shuffle.tracks_voicedb.get_dbid(text, tts_code)

        track.dbid = track_dbid

    shuffle.write()
