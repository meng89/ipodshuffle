import os
import json
import uuid


import gtts
import tempfile
import pydub

voice_info_filename = 'voice_info.json'

home = os.path.expanduser("~")

voice_info_fullpath = home + os.sep + '.'


def all_info():
    voice_info = json.load(open(voice_info_fullpath))
    return voice_info


def _get_info(text, lang):
    info = None
    for one in all_info():
        if one['text'] == text and one['lang'] == lang:
            info = one
            break
    return info


def get_from_cache(text, lang):

    info = _get_info(text, lang)

    return info['filename'] if info else None


def write_to_cache(text, lang):
    info = _get_info(text, lang)

    if not info:
        filename = None
        while True:
            filename = uuid.uuid1()
            if filename not in [info['filename'] for info in all_info()]:
                break

        info['text'] = text
        info['lang'] = lang

        info['filename'] = filename

    mp3_fp = tts(text, lang)
    wav_fp = mp3_to_wav(mp3_fp)

    open(info['filename'], 'wb').write(wav_fp.read())

    voice_info.append(info)


def tts(text, lang):
    s = gtts.gTTS(text=text, lang=lang)
    mp3_fp = tempfile.TemporaryFile()
    s.write_to_fp(mp3_fp)
    return mp3_fp


def mp3_to_wav(mp3_fp):
    mp3_audio = pydub.AudioSegment.from_mp3(mp3_fp)
    wav_fp = tempfile.TemporaryFile()
    mp3_audio.export(wav_fp)
    return wav_fp
