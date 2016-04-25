import os
import functools

import tempfile

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

import langid

from ipodshuffle import Shuffle, MASTER, NORMAL, PODCAST, AUDIOBOOK

from ipodshuffle.audio import get_type as get_audio_type

from ipodshuffle.storage.local import LocalVoiceDB, LocalFileLog

from .utils import str2list

from .tts import ENGINE_MAP

from .tts.error import GetVoiceDataError

from .fix_zh import fix_zh

import logging

log = logging.getLogger('sync')

#########################################################################


def filename(path):
    return os.path.splitext(os.path.split(path)[1])[0]


def beautify_text(text):
    new_text = None
    if '-' in text:
        new_text = text.replace('-', ',')

    return new_text


def id3_title_artist(path):
    title = None
    artist = None

    try:
        audio = EasyID3(path)
    except ID3NoHeaderError:
        pass
    else:

        for k, v in audio.items():
            if k == 'title':
                title = v[0]
            elif k == 'artist':
                artist = v[0]

    return title, artist


def title_artist_or_filename(path):

    title, artist = id3_title_artist(path)

    artist = artist.strip() if artist else ''

    if title:
        text = title.strip()
        if artist:
            if text[-1] in ('?', ',', '.'):
                pass
            else:
                text += ','

            text += ' ' + artist
    else:
        text = beautify_text(filename(path))

    return text


###########################################################################

def cmp_tracknumber(audio1, audio2):
    try:
        return int(EasyID3(audio1).get('tracknumber')[0]) - int(EasyID3(audio2).get('tracknumber')[0])
    except TypeError:
        return 0


def get_files(dire):
    return [os.path.join(dire, one) for one in os.listdir(dire) if os.path.isfile(os.path.join(dire, one))]


def get_dires(dire):
    return [os.path.join(dire, one) for one in os.listdir(dire) if os.path.isdir(os.path.join(dire, one))]


def del_unsupported_files(files):
    return [one for one in files if get_audio_type(one)]


###############################################################################


def get_pls(dire):
    pls = []

    audio_in_dire = sorted(del_unsupported_files(get_files(dire)))

    dires = get_dires(dire)
    if dires:
        for one in dires:
            pls += get_pls(one)
    else:
        audio_in_dire = sorted(audio_in_dire, key=functools.cmp_to_key(cmp_tracknumber))

    audio_files = []
    audio_files.extend(audio_in_dire)
    [audio_files.extend(pl[1]) for pl in pls]

    my_pl = (os.path.split(dire)[1], audio_files)

    pls.insert(0, my_pl)

    return pls


def get_normals(dire):
    pls = []

    dires = sorted(get_dires(dire))
    for one in dires:
        pls += get_pls(one)

    return pls


def get_master_audio(music_dire, normals):
    audio = sorted(del_unsupported_files(get_files(music_dire)))

    [audio.extend(_audio) for title, _audio in normals]

    return audio


def get_podcasts(dire):
    pls = []

    dires = get_dires(dire)

    for sub_dire in dires:
        audio = del_unsupported_files(get_files(sub_dire))
        if audio:
            title = os.path.split(sub_dire)[1]
            pls.append((title, audio))

    return pls


def get_audiobooks(dire):
    pls = []

    # Do single file audiobooks
    files = get_files(dire)
    for audio in del_unsupported_files(files):
        pls.append((filename(audio), (audio,)))

    dires = get_dires(dire)
    for sub_dire in dires:
        audio = del_unsupported_files(get_files(sub_dire))
        if audio:
            pls.append((os.path.split(sub_dire)[1], audio))

    return pls


def voice_things(local_voicedb, args):

    langs = args.langs or []

    tts_func = None
    if args.engine:
        tts_engine = ENGINE_MAP[args.engine]
        tts_func = tts_engine.get_tts_func(args)

        if not langs:
            langs = tts_engine.legal_langs

    lang_map = {}
    for _lang in langs:
        lang_map[_lang[:2]] = _lang

    languages_to_set = [lang_id_code for lang_id_code in lang_map.keys()]

    langid.set_languages(languages_to_set)

    def classify_lang_code(text):
        langid_code = langid.classify(text)[0]

        if 'zh' in languages_to_set:
            langid_code = fix_zh(langid_code, text)

        return lang_map[langid_code]

    def get_local_voice_path(text, lang):
        tts_lang = lang

        log.info('try local voice: {}, {}'.format(repr(lang), repr(text)))

        voice_path = local_voicedb.get_path(text, tts_lang)
        if not voice_path and callable(tts_func):  # The voice not in local
            log.info('not in local.', )
            log.info('try TTS engine {} ... '.format(args.engine))
            voice_data = tts_func(text, tts_lang)
            log.info('done!')

            tmp_file = tempfile.NamedTemporaryFile(delete=False)
            tmp_file_name = tmp_file.name
            tmp_file.close()

            with open(tmp_file_name, 'wb') as f:
                f.write(voice_data)

            local_voicedb.add_voice(tmp_file_name, text, tts_lang)

            os.remove(tmp_file_name)

            voice_path = local_voicedb.get_path(text, tts_lang)

        return voice_path

    return classify_lang_code, get_local_voice_path


def sync(args):

    cache_dir = os.path.join(os.path.expanduser('~'), '.cache/teresa')
    os.makedirs(cache_dir, exist_ok=True)

    src = os.path.realpath(args.src)
    base = os.path.realpath(args.base)

    ipod = Shuffle(base)
    if ipod.enable_voiceover:
        local_voicedb = LocalVoiceDB(os.path.join(cache_dir, 'voices_log.json'), os.path.join(cache_dir, 'voices'))
        local_voicedb.clean()
        classify_lang_code_func, get_local_voice_path_func = voice_things(local_voicedb, args)

        ipod.voice_path_func = get_local_voice_path_func

    ipod.audiodb.clean()

    ipod.tracks_voiceoverdb.clean()
    ipod.playlists_voiceoverdb.clean()

    ipod.playlists.clear()

    local_filelog = LocalFileLog(os.path.join(cache_dir, 'local_file_log.json'))

    def set_voice(obj, text, lang):
        try:
            obj.voice = text, lang
        except GetVoiceDataError as e:
            log('{}, ignornd.'.format(e))

    def add_files_to_playlist(pl, files, get_track_voice_title=None):
        for file in files:
            checksum = local_filelog.get_checksum(file)
            if not checksum:
                local_filelog.log_it(file)
                checksum = local_filelog.get_checksum(file)

            path_in_ipod = ipod.audiodb.get_filename(checksum)
            if not path_in_ipod:
                ipod.audiodb.add(file)
                path_in_ipod = ipod.audiodb.get_filename(checksum)

            track = ipod.create_track(path_in_ipod)
            pl.tracks.append(track)

            if ipod.enable_voiceover:
                text = get_track_voice_title(file)
                lang = classify_lang_code_func(text)

                set_voice(track, text, lang)

    def add_playlists(title_and_files, pl_type, text_fun):
        for title, files in title_and_files:

            pl = ipod.create_playlist(pl_type)
            ipod.playlists.append(pl)

            if ipod.enable_voiceover:

                lang = classify_lang_code_func(title)
                set_voice(pl, title, lang)

            add_files_to_playlist(pl, files, text_fun)

    def exists_and_isdir(path):
        return True if os.path.exists(path) and os.path.isdir(path) else False

    music_dir = os.path.join(src, 'music')
    podcasts_dir = os.path.join(src, 'podcasts')
    audiobooks_dir = os.path.join(src, 'audiobooks')

    if exists_and_isdir(music_dir):

        normals = get_normals(music_dir)
        master_audio = get_master_audio(music_dir, normals)

        for one in master_audio:
            print('master audio: ', one)

        for _title, audio in normals:
            print()
            for one in audio:
                print('{} audio: {}'.format(_title, one))

        if master_audio:
            master_pl = ipod.playlists.append_one(pl_type=MASTER)
            add_files_to_playlist(master_pl, master_audio, title_artist_or_filename)

        if normals:
            add_playlists(normals, NORMAL, title_artist_or_filename)

    if exists_and_isdir(podcasts_dir):
        podcasts = get_podcasts(podcasts_dir)
        if podcasts:
            add_playlists(podcasts, PODCAST, title_artist_or_filename)

    if exists_and_isdir(audiobooks_dir):
        audiobooks = get_audiobooks(audiobooks_dir)
        if audiobooks:
            add_playlists(audiobooks, AUDIOBOOK, filename)

    ipod.write_db()


def register(parser):
    import argparse
    from .utils import add_optional_group, add_args_help, add_args_ipod_base
    from . import translate as _

    parser_sync = parser.add_parser('sync', help=_('sync to ipod'),
                                    formatter_class=argparse.RawTextHelpFormatter,

                                    epilog=_('Legal lang codes of engines:') + '\n' +
                                    '\n'.join(['  {}: {}'.format(k, ', '.join(sorted(v.legal_langs)))
                                               for k, v in ENGINE_MAP.items()]) + '\n'
                                    '\n' +

                                    _('Two examples of use:') + '\n'
                                    '  %(prog)s -b /media/ipod_base -s /media/ipod_src -l en-gb '
                                    '-e svox\n'
                                    '  %(prog)s -b /media/ipod_base -s /media/ipod_src -l en-gb,zh-cn,ja-jp '
                                    '-e voicerss -k d279f919f7384d3bafa516caad0eae56' + '\n\n' +

                                    _('Source path folder structure see: {}')
                                    .format('http://ipodshuffle.readthedocs.org/' +
                                            'en/latest/teresa/index.html#source-path-folder-structure'),
                                    add_help=False
                                    )

    optional_group = add_optional_group(parser_sync)

    add_args_help(optional_group)

    add_args_ipod_base(optional_group)

    optional_group.add_argument('-s', dest='src', help=_('source path'),
                                metavar='<path>', required=True)
    optional_group.add_argument('-l', dest='langs',
                                help=_('comma-separated set of target language codes, e.g en-gb,zh-cn'),
                                type=str2list, metavar='<langs>')
    optional_group.add_argument('-e', dest='engine', choices=ENGINE_MAP.keys(), metavar='<engine>',
                                help=_('TTS engine, ') + _(' or ').join((ENGINE_MAP.keys())))

    for module in ENGINE_MAP.values():
        module.add_arg(optional_group)

    optional_group.set_defaults(func=sync)
