#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import string

b = open('/media/data/temp/iPod_Control/iTunes/iTunesSD', 'rb').read()[0x344:0x34c]


num = int.from_bytes(b, byteorder='little')
# print(hex(num)[2:].upper())

import random

# dbid_string = ''.join(random.sample('ABCDEF' + string.digits, 16))

# i = int('0x' + dbid_string, 16)

# print(dbid_string)
# print(hex(i)[2:].upper())


def get_dbid():
    return ''.join(random.sample('ABCDEF' + string.digits, 16))


def get_dbid2():
    dbid_string = ''
    for x in random.sample(range(0, 255), 8):
        s = hex(x)[2:]
        if len(s) == 1:
            s = '0' + s
        dbid_string += s.upper()
    return dbid_string



import json


a = {('abc', '123'): 'slkfjaslkfj'}

b = json.dumps(a)
print(b)