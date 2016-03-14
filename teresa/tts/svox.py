import os
import tempfile

from .error import LangCodeError, GetVoiceDataError


def tts(text, lang):

    if lang not in legal_langs:
        raise LangCodeError(lang)

    tts_lang = lang[:3] + lang[3:].upper()

    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_file_name = tmp_file.name + '.wav'
    tmp_file.close()

    cmd = 'pico2wave --wave={} --lang={} {}'.format(tmp_file_name, tts_lang, repr(text))
    # print('\n\n', cmd, '\n')
    os.system(cmd)

    f = open(tmp_file_name, 'rb')
    data = f.read()

    if len(data) < 10000:
        raise GetVoiceDataError

    os.remove(tmp_file_name)

    return data

my_langs = [
    'en-US',
    'en-GB',
    'de-DE',
    'es-ES',
    'fr-FR',
    'it-IT',
]


legal_langs = [l.lower() for l in my_langs]


def get_tts_func(args):
    return tts


def add_arg(parser):
    pass
