import os
import json
import uuid


logs_filename = 'voice_info.json'

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
    wav_data = None

    log = _get_log(text, lang)

    if log:
        wav_data = open(log['filename'], 'rb').read()

    return wav_data


def write_to_cache(text, lang, wav_data):
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

    open(log['filename'], 'wb').write(wav_data)

    logs = read_logs()
    logs.append(log)


def clean_bad_cache():
    pass
