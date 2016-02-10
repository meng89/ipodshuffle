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

from ipodshuffle.shuffle import MASTER, NORMAL, PODCAST, AUDIOBOOK

from ipodshuffle.tts.engine import ENGINE_MAP

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


def add_files_to_pl(shuffle, pl, files, local_tts_db, lang_map, ttskey):

    for file in files:
        filename = os.path.splitext(os.path.split(file)[1])[0]
        text = filename

        lang = langid.classify(text)[0]

        if lang in lang_map.keys():
            tts_lang_code = lang_map[lang]
        else:
            tts_lang_code = tts_engine.to_lang_codes(lang)[0]

        path_in_ipod = shuffle.sounds.add(file)

        track = None
        for TRACK in shuffle.tracks:
            if TRACK.filename == path_in_ipod:
                track = TRACK

        if not track:
            track = shuffle.tracks.add(path_in_ipod)

        # print(tts_code, text)

        pl.tracks.append(track)

        track_dbid = shuffle.tracks_voicedb.get_dbid(text, tts_lang_code)

        if not track_dbid:  # the voice not in ipod

            tts_path = local_tts_db.get_path_by_text_lang(text, tts_lang_code)

            if not tts_path:  # the voice not in local

                print('Get a new voice: "{}", "{}" ...'.format(tts_lang_code, text), end='')
                data = tts_engine.tts(text, tts_lang_code, ttskey)
                print(' done.')

                tmp_file = tempfile.NamedTemporaryFile(delete=False)
                tmp_file_name = tmp_file.name
                tmp_file.close()

                with open(tmp_file_name, 'wb') as f:
                    f.write(data)

                local_tts_db.add(tmp_file_name, text, tts_lang_code)
                tts_path = local_tts_db.get_path_by_text_lang(text, tts_lang_code)

            shuffle.tracks_voicedb.add(tts_path, text, tts_lang_code)

            track_dbid = shuffle.tracks_voicedb.get_dbid(text, tts_lang_code)

        track.dbid = track_dbid


def sync(**kwargs):
    # src=None, ipod=None, [tts_engine=None, [langs=None, tts_key=None, ... ]]

    src = kwargs.pop('src')
    ipod_base = kwargs.pop('ipod_base')
    ipod = ipodshuffle.Shuffle(ipod_base)

    tts_engine = None
    tts_langs = None
    if ipod.enable_voiceover:
        tts_engine = ENGINE_MAP[kwargs.pop('tts_engine')]
        tts_langs = kwargs.pop('tts_langs')

    pls = get_normals(src + '/' + 'music')
    master_files = pls[0][1]
    normals = pls[1:]
    podcasts = get_podcasts(src + '/' + 'podcasts')
    audiobooks = get_audiobooks(src + '/' + 'audiobooks')

    ipod.sounds.clean_logs()
    ipod.playlists.clear()
    ipod.tracks.clear()

    master_pl = ipod.playlists.add()
    master_pl.type = MASTER

    if ipod.enable_voiceover:
        ttsdb = ipodshuffle.tts.tts_db.Db(os.path.join(cache_dir, 'tts_logs.json'), os.path.join(cache_dir, 'voices'))

        lang_map = {}
        for tts_lang in tts_langs:
            if not tts_engine.is_available(tts_lang):
                raise Exception
            iso639_1_lang = tts_engine.to_iso639_1(tts_lang)
            lang_map[iso639_1_lang] = tts_lang

        if lang_map:
            langid.set_languages(lang_map.keys())

    for file in master_files:
        filename = os.path.splitext(os.path.split(file)[1])[0]
        text = filename

        lang = langid.classify(text)[0]

        if lang in lang_map.keys():
            tts_lang_code = lang_map[lang]
        else:
            tts_lang_code = tts_engine.to_lang_codes(lang)[0]

        path_in_ipod = ipod.sounds.add(file)

        track = None
        for TRACK in ipod.tracks:
            if TRACK.filename == path_in_ipod:
                track = TRACK

        if not track:
            track = ipod.tracks.add(path_in_ipod)

        # print(tts_code, text)

        master_pl.tracks.append(track)

        track_dbid = ipod.tracks_voicedb.get_dbid(text, tts_lang_code)

        if not track_dbid:  # the voice not in ipod

            tts_path = ttsdb.get_path_by_text_lang(text, tts_lang_code)

            if not tts_path:  # the voice not in local

                print('Get a new voice: "{}", "{}" ...'.format(tts_lang_code, text), end='')
                data = tts_engine.tts(text, tts_lang_code, ttskey)
                print(' done.')

                tmp_file = tempfile.NamedTemporaryFile(delete=False)
                tmp_file_name = tmp_file.name
                tmp_file.close()

                with open(tmp_file_name, 'wb') as f:
                    f.write(data)

                ttsdb.add(tmp_file_name, text, tts_lang_code)
                tts_path = ttsdb.get_path_by_text_lang(text, tts_lang_code)

            ipod.tracks_voicedb.add(tts_path, text, tts_lang_code)

            track_dbid = ipod.tracks_voicedb.get_dbid(text, tts_lang_code)

        track.dbid = track_dbid

    ipod.write()
