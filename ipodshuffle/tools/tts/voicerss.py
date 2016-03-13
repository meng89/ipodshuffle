import urllib.request
import urllib.parse

import argparse

from .error import LangCodeError, GetVoiceDataError


default_format = '22khz_16bit_mono'


def get_tts_func(args):
    key = args.key

    def tts(text, lang):
        if lang not in legal_langs:
            raise LangCodeError(lang)

        tts_lang = lang

        c = 'WAV'

        url = 'http://api.voicerss.org/?'

        parameters = {'src': text, 'hl': tts_lang, 'key': key, 'c': c, 'f': args.format or default_format}

        req = urllib.request.Request(url, urllib.parse.urlencode(parameters).encode('ascii'))

        response = urllib.request.urlopen(req)

        content_length = None
        for k, v in response.getheaders():
            if k == 'Content-Length':
                content_length = int(v)

        if content_length < 10000:
            raise GetVoiceDataError(response.read().decode())

        return response.read()

    return tts

my_langs = [
    'ca-es',  # 'Catalan'],
    'zh-cn',  # 'Chinese (China)'],
    'zh-hk',  # 'Chinese (Hong Kong)'],
    'zh-tw',  # 'Chinese (Taiwan)'],
    'da-dk',  # 'Danish'],
    'nl-nl',  # 'Dutch'],
    'en-au',  # 'English (Australia)'],
    'en-ca',  # 'English (Canada)'],
    'en-gb',  # 'English (Great Britain)'],
    'en-in',  # 'English (India)'],
    'en-us',  # 'English (United States)'],
    'fi-fi',  # 'Finnish'],
    'fr-ca',  # 'French (Canada)'],
    'fr-fr',  # 'French (France)'],
    'de-de',  # 'German'],
    'it-it',  # 'Italian'],
    'ja-jp',  # 'Japanese'],
    'ko-kr',  # 'Korean'],
    'nb-no',  # 'Norwegian'],
    'pl-pl',  # 'Polish'],
    'pt-br',  # 'Portuguese (Brazil)'],
    'pt-pt',  # 'Portuguese (Portugal)'],
    'ru-ru',  # 'Russian'],
    'es-mx',  # 'Spanish (Mexico)'],
    'es-es',  # 'Spanish (Spain)'],
    'sv-se',  # 'Swedish (Sweden)']
]


legal_langs = my_langs


def add_arg(parser):
    g = parser.add_argument_group(title=_('voicerss engine options'))

    g.add_argument('-k', dest='key', metavar='<key>',
                   help=_('API key string, get a key from {}').format('http://www.voicerss.org/'))

    g.add_argument('-f', dest='format', metavar='<format>',
                   help=_('audio format, default format is {}').format(default_format))

