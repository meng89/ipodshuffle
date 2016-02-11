#!/usr/bin/env python3

import os
import tempfile

from mutagen.easyid3 import EasyID3

import langid

import ipodshuffle

from ipodshuffle.audio import get_type as get_audio_type

from ipodshuffle.shuffle import MASTER, NORMAL, PODCAST, AUDIOBOOK

import ipodshuffle.tts.localdb

import ipodshuffle.utils

from ipodshuffle.tts.engine import ENGINE_MAP

from character_detect import has_ja_char, has_ko_char


CACHE_DIR = os.path.join(os.path.expanduser('~'), '.cache/ipodshuffle')
os.makedirs(CACHE_DIR, exist_ok=True)


def filename(path):
    return os.path.splitext(os.path.split(path)[1])[0]


def id3_title(path):
    title = None
    audio = EasyID3(path)
    titles = audio['title']
    if titles:
        title = titles[0]
    return title

###########################################################################


def get_all_dires(dire):
    dirs = []
    # os.path.walk(src, visit, dir_files_list)
    for top, sub_dirs, names in os.walk(dire, followlinks=True):
        dirs.append(top)
    return dirs


get_all_files = ipodshuffle.utils.get_all_files


def get_sub_files_dires(dire):
    files = []
    dires = []
    for one in sorted(os.listdir(dire)):
        path = os.path.join(dire, one)

        if os.path.isfile(path):
            files.append(path)
        elif os.path.isdir(path):
            dires.append(path)

    return files, dires


def get_legal_files(files):
    return [file for file in files if get_audio_type(file)]

###############################################################################


def get_master_normals(dire):
    titles_files = []

    dires = get_all_dires(dire)

    for _dire in dires:
        legal_files = get_legal_files(get_all_files(_dire))
        if legal_files:
            title = os.path.split(_dire)[1]
            titles_files.append((title, sorted(legal_files)))

    return titles_files


def get_podcasts(dire):
    titles_files = []

    dires = get_sub_files_dires(dire)[1]

    for _dire in dires:
        legal_files = get_legal_files(get_sub_files_dires(_dire)[0])
        if legal_files:
            title = os.path.split(_dire)[1]
            titles_files.append((title, legal_files))

    return titles_files


def get_audiobooks(dire):
    titles_files = []
    files, dires = get_sub_files_dires(dire)

    # Do single file audiobooks
    for file in get_legal_files(files):
        title = filename(file)
        titles_files.append((title, (file,)))

    for _dire in dires:
        legal_files = get_legal_files(get_sub_files_dires(_dire)[0])
        if legal_files:
            title = os.path.split(_dire)[1]
            titles_files.append((title, legal_files))

    return titles_files


def fix_cjk(seted_langs, code, text):
    fixed_code = code
    if not seted_langs or 'zh' in seted_langs:
        if code == 'ja':
            if not has_ja_char(text):
                fixed_code = 'zh'
        elif code == 'ko':
            if not has_ko_char(text):
                fixed_code = 'zh'

    return fixed_code


def wrapper_tts(_fun, **kwargs):

    def wrapper(text, lang):
        return _fun(text, lang, **kwargs)

    return wrapper


def voice_things(ipod_voicedb, local_voicedb, ttsengine, langs=None, **kwargs):

    tts_engine = ENGINE_MAP[ttsengine]

    langs = langs or []

    lang_map = {}
    for _lang in langs:
        if not tts_engine.is_available(_lang):
            raise Exception

        langid_code_ = tts_engine.to_langid_code(_lang)
        lang_map[langid_code_] = _lang

    if not lang_map:
        lang_map = tts_engine.get_lang_map()

    langid_codes_to_set = lang_map.keys()
    langid.set_languages(langid_codes_to_set)

    tts = wrapper_tts(tts_engine.tts, **kwargs)

    def get_dbid(text, langid_code):

        lang = lang_map[langid_code]

        dbid = ipod_voicedb.get_dbid(text, lang)
        if not dbid:  # The voice not in ipod tracks/playlists db
            print('Voice {} {} not in tracks/playlists, try to get from local ...'.format(repr(lang), repr(text)), end='')

            local_voice_path = local_voicedb.get_path_by_text_lang(text, lang)

            if local_voice_path:
                print('found!')

            else:  # The voice not in local
                print('Not in local, try to get from tts engine.')

                print('Get a new voice: "{}", "{}" ...'.format(lang, text), end='')
                voice_data = tts(text, lang)
                print(' done!')

                tmp_file = tempfile.NamedTemporaryFile(delete=False)
                tmp_file_name = tmp_file.name
                tmp_file.close()

                with open(tmp_file_name, 'wb') as f:
                    f.write(voice_data)

                local_voicedb.add(tmp_file_name, text, lang)
                local_voice_path = local_voicedb.get_path_by_text_lang(text, lang)

            ipod_voicedb.add(local_voice_path, text, lang)
            dbid = ipod_voicedb.get_dbid(text, lang)

        return dbid

    return get_dbid


description = "Sync tracks and playlists to player"


def sync(src, base, **tts_kwargs):
    # src=None, ipod=None, [tts_engine=None, [langs=None, tts_key=None, ... ]]

    src = os.path.realpath(src)
    base = os.path.realpath(base)

    player = ipodshuffle.Shuffle(base)

    player.sounds.clean()
    player.tracks_voicedb.clean()
    player.playlists_voicedb.clean()

    player.playlists.clear()
    player.tracks.clear()

    dires_funs = (
        (src + '/' + 'music', get_master_normals),
        (src + '/' + 'podcasts', get_podcasts),
        (src + '/' + 'audiobooks', get_audiobooks),
    )

    def x(y):
        z = []
        for dire, _fun in y:
            a = []
            if os.path.exists(dire) and os.path.isdir(dire):
                a = _fun(dire)
            z.append(a)
        return z

    master_normals, podcasts, audiobooks = x(dires_funs)

    master = []
    normals = []
    if master_normals:
        master = master_normals[0]
        normals = master_normals[1:]

    get_track_dbid = None
    get_playlist_dbid = None

    if player.enable_voiceover:

        local_voicedb = ipodshuffle.tts.localdb.LocalDB(os.path.join(CACHE_DIR, 'voices_logs.json'),
                                                        os.path.join(CACHE_DIR, 'voices'))

        get_track_dbid = voice_things(player.tracks_voicedb, local_voicedb, **tts_kwargs)
        get_playlist_dbid = voice_things(player.playlists_voicedb, local_voicedb, **tts_kwargs)

    def add_files_to_pl(pl, files, text_fun):

        for file in files:

            path_in_ipod = player.sounds.add(file)

            track = None
            for TRACK in player.tracks:
                if TRACK.path_in_ipod == path_in_ipod:
                    track = TRACK
            if not track:
                track = player.tracks.add(path_in_ipod)

            pl.tracks.append(track)

            if player.enable_voiceover:
                text = text_fun(file)

                langid_lang = langid.classify(text)[0]

                track.dbid = get_track_dbid(text, langid_lang)

    def add_playlists(title_files, pl_type, text_fun):

        for title, files in title_files:
            pl = player.playlists.add()
            pl.type = pl_type

            langid_lang = langid.classify(title)[0]

            if player.enable_voiceover:
                pl.dbid = get_playlist_dbid(title, langid_lang)

            add_files_to_pl(pl, files, text_fun)

    master_pl = player.playlists.add()
    master_pl.type = MASTER
    add_files_to_pl(master_pl, master[1], filename)

    add_playlists(normals, NORMAL, filename)
    add_playlists(podcasts, PODCAST, id3_title)
    add_playlists(audiobooks, AUDIOBOOK, filename)

    player.write()

fun = sync


def get_help_strings(indet=None):
    indet = indet or 0
    s = ' ' * indet + 'usage:  src=<path> base=<path> ttsengine=<enging> <arg1>=value1 <arg2>=value2 ... \n'
    return s
