#!/usr/bin/env python

import urllib.request
import urllib.parse

url = 'http://api.voicerss.org/?'


def tts(text, lang, key):
    parameters = {'src': text, 'hl': lang, 'key': key, 'c': 'WAV', 'f': '48khz_16bit_stereo'}
    data = urllib.request.urlopen(url, urllib.parse.urlencode(parameters).encode('ascii'))

    return data.read()

