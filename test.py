#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint

import ipodshuffle.itunessd
import ipodshuffle.itunesstats

import ipodshuffle


from ipodshuffle.shuffle import dbid_from_bytes, dbid_to_bytes, dbid_to_number


dbid = '4F0995477FAF2AA7'

chunk = dbid_to_bytes(dbid)

dbid2 = dbid_from_bytes(chunk)


print(dbid == dbid2)
print(dbid, dbid2)
