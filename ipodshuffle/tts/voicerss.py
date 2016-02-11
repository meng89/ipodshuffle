#!/usr/bin/env python

import urllib.request
import urllib.parse


class GetTTSError(Exception):
    pass


class LangCodeError(Exception):
    pass


def tts(text, lang, key):
    if not is_available(lang):
        raise LangCodeError

    url = 'http://api.voicerss.org/?'

    parameters = {'src': text, 'hl': lang, 'key': key, 'c': 'WAV', 'f': '22khz_16bit_mono'}

    req = urllib.request.Request(url, urllib.parse.urlencode(parameters).encode('ascii'))

    response = urllib.request.urlopen(req)

    content_length = None
    for k, v in response.getheaders():
        if k == 'Content-Length':
            content_length = int(v)

    if content_length < 100:
        raise GetTTSError(response.read().decode())

    return response.read()

langs = [
    ['ca-es', 'Catalan'],
    ['zh-cn', 'Chinese (China)'],
    ['zh-hk', 'Chinese (Hong Kong)'],
    ['zh-tw', 'Chinese (Taiwan)'],
    ['da-dk', 'Danish'],
    ['nl-nl', 'Dutch'],
    ['en-au', 'English (Australia)'],
    ['en-ca', 'English (Canada)'],
    ['en-gb', 'English (Great Britain)'],
    ['en-in', 'English (India)'],
    ['en-us', 'English (United States)'],
    ['fi-fi', 'Finnish'],
    ['fr-ca', 'French (Canada)'],
    ['fr-fr', 'French (France)'],
    ['de-de', 'German'],
    ['it-it', 'Italian'],
    ['ja-jp', 'Japanese'],
    ['ko-kr', 'Korean'],
    ['nb-no', 'Norwegian'],
    ['pl-pl', 'Polish'],
    ['pt-br', 'Portuguese (Brazil)'],
    ['pt-pt', 'Portuguese (Portugal)'],
    ['ru-ru', 'Russian'],
    ['es-mx', 'Spanish (Mexico)'],
    ['es-es', 'Spanish (Spain)'],
    ['sv-se', 'Swedish (Sweden)']
]


def is_available(lang):
    return lang.lower() in [l[0].lower() for l in langs]


def to_langid_code(lang):
    langid_code = None
    for l in langs:
        if l[0].lower() == lang.lower():
            langid_code = l[0].split('-')[0]
            break
    return langid_code


def to_langs(langid_code):
    print('here')
    _langs = []

    for lang in [lang[0] for lang in langs]:
        code = lang.split('-')[0]
        if code.lower() == langid_code:
            _langs.append(lang)

    return _langs


def get_lang_map():
    lang_map = {}
    for l in langs:
        langid_code = to_langid_code(l[0])
        lang_map[langid_code] = l[0]
    return lang_map
