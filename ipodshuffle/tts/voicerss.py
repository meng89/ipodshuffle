#!/usr/bin/env python

import urllib.request
import urllib.parse

import tempfile


class GetTtsError(Exception):
    pass

url = 'http://api.voicerss.org/?'


def tts(text, lang, key):
    parameters = {'src': text, 'hl': lang, 'key': key, 'c': 'WAV', 'f': '22khz_16bit_mono'}

    req = urllib.request.Request(url, urllib.parse.urlencode(parameters).encode('ascii'))

    response = urllib.request.urlopen(req)

    content_length = None
    for k, v in response.getheaders():
        if k == 'Content-Length':
            content_length = int(v)

    if content_length < 100:
        raise GetTtsError(response.read().decode())

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
    return lang in [l[0] for l in langs]


def to_iso_639_1(lang):
    iso_639_1_code = None
    for l in langs:
        if l[0] == lang:
            iso_639_1_code = l[0].split('-')[0]
            break
    return iso_639_1_code


def to_lang_codes(iso_639_1_code):
    print(iso_639_1_code)

    lang_codes = []
    for lang in [lang[0] for lang in langs]:
        code = lang.split('-')[0]
        if code == iso_639_1_code:
            lang_codes.append(lang)
    print(lang_codes)
    return lang_codes


