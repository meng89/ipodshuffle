#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint

import shuffle.itunessd

itunessd1 = open('iTunesSD', 'rb').read()

a, b, c = shuffle.itunessd.itunessd_to_dics(itunessd1)

pp = pprint.PrettyPrinter(indent=4)

print(pp.pprint(a), end='\n\n\n')
print(pp.pprint(b), end='\n\n\n')
print(pp.pprint(c), end='\n\n\n')

itunessd2 = shuffle.itunessd.dics_to_itunessd(a, b, c)

print(len(itunessd1), len(itunessd2), itunessd1 == itunessd2)

if itunessd1 != itunessd2:
    open('iTunesSD2', 'wb').write(itunessd2)
    i = 0
    while len(itunessd1) > i:
        if itunessd1[i] != itunessd2[i]:
            print(i, itunessd1[i:i+1], itunessd2[i:i+1])

        i += 1
