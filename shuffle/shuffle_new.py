#!/usr/bin/env python3

import os

from .baseclasses import List


class DataError(Exception):
    pass


bdhs_items_table = (
    {'name': 'header_id',                    'size': 4,  'must_be': b'bdhs'},
    {'name': 'unknown_1',                    'size': 4,  'seems_always_be': b'\x01\x00\x01\x02'},
    {'name': 'header_legth',                 'size': 4,  'type': 'number'},
    {'name': 'total_no_of_tracks',           'size': 4,  'type': 'number'},
    {'name': 'total_no_of_playlists',        'size': 4,  'type': 'number'},
    {'name': 'unknown_2',                    'size': 8,  'type': 'unknown'},
    {'name': 'max_volume',                   'size': 1,  'type': 'number'},
    {'name': 'enable_voiceover',             'size': 1,  'type': 'number'},
    {'name': 'unknown_3',                    'size': 2,  'type': 'unknown'},
    {'name': 'total_no_of_tracks2',          'size': 4,  'type': 'number'},
    {'name': 'sounds_header_offset',         'size': 4,  'type': 'number'},
    {'name': 'playlists_header_offset',      'size': 4,  'type': 'number'},
    {'name': 'unknown_4',                    'size': 20, 'type': 'unknown'}
)

bdhs_items_size = sum([i['size'] for i in bdhs_items_table])


def split_bdhs(data, xxhs):
    dic = {}
    i = 0
    for item in xxhs:
        dic[item['name']] = data[i:i+item['size']]
        i += item['size']
    return dic


def ifb(data):
    return int.from_bytes(data, byteorder='little')


class Shuffle:
    def __init__(self, directory):
        self.dir = os.path.abspath(directory)

        self.sounds = List()
        self.playlists = List()

        ipod_control_folder = 'iPod_Control'

        self._itunessd_path = self.dir + os.sep + ipod_control_folder + os.sep + 'iTunesSD'
        self._itunessd_data = open(self._itunessd_path, 'rb').read()

        if os.path.exists(self._itunessd_path):
            bdhs_header_bytes = self._itunessd_data[0:bdhs_items_size]
            dic = split_bdhs(bdhs_header_bytes, bdhs_items_table)
            if dic['header_id'] != b'bdhs':
                raise DataError

            self.enable_voiceover = bool(ifb(dic['enable_voiceover']))
            self.max_volume = ifb(dic['max_volume'])

            self.sounds = Sounds()
            self.playlists = Playlists()

        else:
            pass

        self.voiceover_lang = 'zh_CN'
        self.max_volume = ''


class Sounds(List):
    def __init__(self, itunessd_data=None, header_offset=None):
        super().__init__(initlist=None, limit=None, is_limit_when_init=True)
        if itunessd_data:
            pass


class Playlists(List):
    pass
