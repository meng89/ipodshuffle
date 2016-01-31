#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import string

b = open('/media/data/temp/iPod_Control/iTunes/iTunesSD', 'rb').read()[0x344:0x34c]


def a():
    return 'a', 1


l = []
for one in range(10):
    l.append(a())

print(l)
