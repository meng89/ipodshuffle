import os
import json
import uuid


import gtts
import tempfile
import pydub

logs_filename = 'voice_logs.json'

logs_fullpath = os.path.expanduser("~") + os.sep + '.'


def read_logs():
    logs = json.loads(open(logs_fullpath).read())
    return logs


def write_logs(logs):
    open(logs_fullpath, 'w').write(json.dumps(logs))


def _get_log(text, lang):
    log = None
    for l in read_logs():
        if l['text'] == text and l['lang'] == lang:
            log = l
            break
    return log


def get_from_cache(text, lang):

    log = _get_log(text, lang)

    return log['filename'] if log else None


def write_to_cache(text, lang):
    log = _get_log(text, lang)

    if not log:
        filename = None
        while True:
            filename = uuid.uuid1()
            if filename not in [info['filename'] for info in read_logs()]:
                break

        log['text'] = text
        log['lang'] = lang

        log['filename'] = filename

    mp3_fp = tts(text, lang)
    wav_fp = mp3_to_wav(mp3_fp)

    open(log['filename'], 'wb').write(wav_fp.read())

    logs = read_logs()
    logs.append(log)


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


def clean():
    pass
