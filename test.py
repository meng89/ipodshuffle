#!/usr/bin/env python3

import sys


def a(fun, **kwargs1):
    print('in a')

    def wrapper(text, lang):
        print('in wrapper')
        fun(text, lang, **kwargs1)

    return wrapper


def b(text, lang, **k):
    print('in b')

    key = k.pop('key')

    if key != 'llmf':
        raise Exception

    print(text, lang)


def get_tts_fun(**kwargs):
    return a(b, **kwargs)


kwargs2 = {'key': 'llmf', 'jbm': 2}


tts_fun = a(b, **kwargs2)
# tts_fun = b(**kwargs2)

tts_fun(text='a text', lang='a lang')
