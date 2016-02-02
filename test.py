#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shuffle.itunessd

itunessd = open('iTunesSD', 'rb').read()

a, b, c = shuffle.itunessd.itunessd_to_dics(itunessd)

print(a)
print(b)
print(c)
