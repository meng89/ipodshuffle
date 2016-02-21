import urllib.request
import urllib.parse

from .error import LangCodeError, GetTTSError


def get_tts_func(args):
    key = args.key
    format_ = args.format or '22khz_16bit_mono'

    def tts(text, lang):
        if lang not in legal_langs:
            raise LangCodeError(lang)

        tts_lang = lang

        c = 'WAV'

        url = 'http://api.voicerss.org/?'

        parameters = {'src': text, 'hl': tts_lang, 'key': key, 'c': c, 'f': format_}

        req = urllib.request.Request(url, urllib.parse.urlencode(parameters).encode('ascii'))

        response = urllib.request.urlopen(req)

        content_length = None
        for k, v in response.getheaders():
            if k == 'Content-Length':
                content_length = int(v)

        if content_length < 10000:
            raise GetTTSError(response.read().decode())

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


def register(parser):
    parser_voicerss = parser.add_parser('voicerss', help='An http TTS engine')

    parser_voicerss.add_argument('-k', '--key', help='API key, visit to get: http://www.voicerss.org/',
                                 metavar='<string>')

    parser_voicerss.add_argument('-f', '--format', help='audio format')
