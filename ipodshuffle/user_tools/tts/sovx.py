import os
import tempfile

from .error import LangCodeError, GetTTSError


def tts(text, lang):
    if not is_available(lang):
        raise LangCodeError(lang)

    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_file_name = tmp_file.name + '.wav'
    tmp_file.close()

    cmd = 'pico2wave --wave={} --lang={} {}'.format(tmp_file_name, lang, repr(text))
    # print('\n\n', cmd, '\n')
    os.system(cmd)

    f = open(tmp_file_name, 'rb')
    data = f.read()

    if len(data) < 10000:
        raise GetTTSError

    os.remove(tmp_file_name)

    return data

langs = [
    'en-US',
    'en-GB',
    'de-DE',
    'es-ES',
    'fr-FR',
    'it-IT',
]


def is_available(lang):
    return lang.lower() in [l.lower() for l in langs]


def lang_to_langid_code(lang):
    langid_code = None
    for l in langs:
        if l == lang:
            langid_code = l.split('-')[0]
            break
    return langid_code
