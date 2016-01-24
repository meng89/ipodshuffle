#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shuffle.audiorec

d = '/media/data/temp/sounds/'


for one in os.listdir(d):
    path = d + one
    if os.path.isfile(path):
        print(path, shuffle.audiorec.get_filetype(path))
