#!/usr/bin/env python3
import os
import sys

from ipod_shuffle_4 import Shuffle
from ipod_shuffle_4 import utils





shuffle = Shuffle('/media/data/mine/program/libre_shuffle/temp/ipod')
# shuffle = Shuffle("/run/media/obs/OBS' IPOD/")
print(len(shuffle.get_all_tracks()), len(shuffle.get_all_playlists()))

