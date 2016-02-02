#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint

import shuffle.itunessd

itunessd = open('iTunesSD', 'rb').read()

a, b, c = shuffle.itunessd.itunessd_to_dics(itunessd)

pp = pprint.PrettyPrinter(indent=4)
# pa = pprint.pprint(a)
# pb = pprint.pprint(b)
# pc = pprint.pprint(c)

print(pp.pprint(a), end='\n\n\n')
print(pp.pprint(b), end='\n\n\n')
print(pp.pprint(c), end='\n\n\n')
