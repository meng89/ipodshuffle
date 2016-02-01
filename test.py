#!/usr/bin/env python3
# -*- coding: utf-8 -*-


b = open('/media/data/temp/iPod_Control/iTunes/iTunesSD', 'rb').read()[4976:4980]
n = int.from_bytes(b, 'little')
print(b)
print(n)
