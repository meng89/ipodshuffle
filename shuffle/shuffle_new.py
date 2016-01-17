#!/usr/bin/env python3

import os

from .baseclasses import List


class DataError(Exception):
    pass


def split_shxx(data, table):
    d = {}
    i = 0
    for item in table:
        d[item['name']] = data[i:i+item['size']]
        i += item['size']
    return d


def split_by_step(data, step):
    return [data[i:i+step] for i in range(0, len(data), step)]


def int_from_bytes(data):
    return int.from_bytes(data, byteorder='little')


def dbid_from_bytes(data):
    return '{:X}'.format(int_from_bytes(data))


def get_header_size(table):
    return sum([i['size'] for i in table])


def get_dic_and_subs(bytes_data, header_offset, table, sub_offset_size):

    header_size = get_header_size(hths_header_table)

    header_bytes = bytes_data[header_offset: header_offset + header_size]

    dic = split_shxx(header_bytes, table)

    length = dic['length']

    subs_offsets = split_by_step(bytes_data[header_offset + header_size: header_offset + length], sub_offset_size)

    return dic, subs_offsets


bdhs_table = (
    {'name': 'header_id',                  'size': 4,  'type': 'string',  'must_be': 'bdhs'},
    {'name': 'unknown_1',                  'size': 4,  'type': 'unknown', 'seems_always_be': b'\x01\x00\x01\x02'},
    {'name': 'legth',                      'size': 4,  'type': 'number'},
    {'name': 'number_of_tracks',           'size': 4,  'type': 'number'},
    {'name': 'number_of_playlists',        'size': 4,  'type': 'number'},
    {'name': 'unknown_2',                  'size': 8,  'type': 'unknown'},
    {'name': 'max_volume',                 'size': 1,  'type': 'number'},
    {'name': 'enable_voiceover',           'size': 1,  'type': 'number'},
    {'name': 'unknown_3',                  'size': 2,  'type': 'unknown'},
    {'name': 'number_of_tracks2',          'size': 4,  'type': 'number'},   # Does not include podcasts or audiobooks
                                                                            #   in the count.
    {'name': 'sounds_header_offset',       'size': 4,  'type': 'number'},
    {'name': 'playlists_header_offset',    'size': 4,  'type': 'number'},
    {'name': 'unknown_4',                  'size': 20, 'type': 'unknown'}
)


class Shuffle:
    def __init__(self, directory):
        self.dir = os.path.abspath(directory)

        self.sounds = List()
        self.playlists = List()

        ipod_control_folder = 'iPod_Control'

        self._itunessd_path = self.dir + os.sep + ipod_control_folder + os.sep + 'iTunesSD'
        itunessd_bytes = open(self._itunessd_path, 'rb').read()

        if os.path.exists(self._itunessd_path):
            bdhs_size = get_header_size(bdhs_table)

            bdhs_header_bytes = itunessd_bytes[0:bdhs_size]

            dic = split_shxx(bdhs_header_bytes, bdhs_table)
            if dic['header_id'].decode() != 'bdhs':
                raise DataError

            self.enable_voiceover = bool(int_from_bytes(dic['enable_voiceover']))
            self.max_volume = int_from_bytes(dic['max_volume'])

            self.sounds = Sounds(itunessd_bytes, dic['sounds_header_offset'])
            self.playlists = Playlists(itunessd_bytes, dic['playlists_header_offset'], self.sounds)

        else:
            pass

        self.voiceover_lang = ''
        self.max_volume = ''

        self.sounds_voices = List()
        self.playlists_voices = List()





hths_header_table = (
    {'name': 'header_id',        'size': 4, 'type': 'string', 'must_be': 'hths'},
    {'name': 'length',           'size': 4, 'type': 'number'},
    {'name': 'number_of_tracks', 'size': 4, 'type': 'number'},
    {'name': 'unknown_1',        'size': 8, 'type': 'unknown'},

    # offset_of_track             4
    # offset_of_track
    # ......
)
hths_subs_offset_size = 4


class Sounds(List):
    def __init__(self, itunessd_bytes=None, offset=None):
        super().__init__()

        if itunessd_bytes and offset:
            dic, sounds_offsets = get_dic_and_subs(itunessd_bytes, offset,
                                                   hths_header_table, hths_subs_offset_size)

            if dic['header_id'].decode() != 'hths':
                raise DataError

            for sound_offset in sounds_offsets:
                self.append(Sound(itunessd_bytes, int_from_bytes(sound_offset)))

    def _get_ituned_bytes(self):
        pass


rths_table = (
    {'name': 'header_id',                     'size': 4,   'type': 'string', 'must_be': 'rths'},
    {'name': 'length',                        'size': 4,   'type': 'number'},
    {'name': 'start_at_pos_ms',               'size': 4,   'type': 'number'},  # 从几秒开始播放？
    {'name': 'stop_at_pos_ms',                'size': 4,   'type': 'number'},  # 从几秒后结束？
    {'name': 'volume_gain',                   'size': 4,   'type': 'number'},

    {'name': 'filetype',                      'size': 4,   'type': 'number'},
    {'name': 'filename',                      'size': 256, 'type': 'string'},

    {'name': 'bookmark',                      'size': 4,   'type': 'number'},
    {'name': 'dont_skip_on_shuffle',          'size': 1,   'type': 'bool'},
    {'name': 'remember_playing_pos',          'size': 1,   'type': 'bool'},
    {'name': 'part_of_uninterruptable_album', 'size': 1,   'type': 'bool'},
    {'name': 'unknown_1',                     'size': 1,   'type': 'unknown'},
    {'name': 'pregap',                        'size': 4,   'type': 'number'},  # 播放之前空闲几秒？
    {'name': 'postgap',                       'size': 4,   'type': 'number'},  # 播放之后空闲几秒？
    {'name': 'number_of_sampless',            'size': 4,   'type': 'number'},  # 采样率？
    {'name': 'unknown_file_related_data1',    'size': 4,   'type': 'unknown'},
    {'name': 'gapless_data',                  'size': 4,   'type': 'number'},  # 无缝数据？
    {'name': 'unknown_file_related_data2',    'size': 4,   'type': 'unknown'},
    {'name': 'album_id',                      'size': 4,   'type': 'number'},
    {'name': 'track_number',                  'size': 2,   'type': 'number'},
    {'name': 'disc_number',                   'size': 2,   'type': 'number'},
    {'name': 'unknown_2',                     'size': 8,   'type': 'unknown'},
    {'name': 'dbid',                          'size': 8,   'type': 'number'},
    {'name': 'artist_id',                     'size': 4,   'type': 'number'},
    {'name': 'unknown_3',                     'size': 32,  'type': 'unknown'},
)


class Sound:
    def __init__(self, itunessd_bytes=None, offset=None):

        if itunessd_bytes and offset:
            _size = sum([i['size'] for i in rths_table])
            data = itunessd_bytes[offset: offset + _size]
            d = split_shxx(data, rths_table)
            if d['header_id'] != b'rths':
                raise DataError

            self.start_at_pos_ms = int_from_bytes(d['start_at_pos_ms'])
            self.stop_at_pos_ms = int_from_bytes(d['stop_at_pos_ms'])
            self.volume_gain = int_from_bytes(d['volume_gain'])

            self.book_mark = int_from_bytes(d['bookmark'])
            self.dont_skip_on_shuffle = bool(int_from_bytes(d['dont_skip_on_shuffle']))
            self.remember_playing_pos = bool(int_from_bytes(d['remember_playing_pos']))
            self.part_of_uninterruptable_album = bool(int_from_bytes(d['part_of_uninterruptable_album']))

            self.album_id = int_from_bytes(d['album_id'])
            self.track_number = int_from_bytes(d['track_number'])
            self.dbid = dbid_from_bytes(d['dbid'])
            self.artist_id = int_from_bytes(d['artist_id'])

        else:
            pass


hphs_header_table = (
    {'name': 'header_id',                      'size': 4,  'type': 'string', 'must_be': 'hphs'},
    {'name': 'length',                         'size': 4,  'type': 'number'},
    {'name': 'number_of_all_playlists',        'size': 4,  'type': 'number'},

    {'name': 'playlist_flag_normal',           'size': 4,  'type': 'number'},  # \xFF if normal pls is 0 else 1
    {'name': 'number_of_normal_playlists',     'size': 4,  'type': 'number'},

    {'name': 'playlist_flag_audiobook',        'size': 4,  'type': 'number'},  # \xFF if audiobook pls is 0,
                                                                               #   else master + normal + podcast
    {'name': 'number_of_audiobook_playlists',  'size': 4,  'type': 'number'},

    {'name': 'playlist_flag_podcast',          'size': 4,  'type': 'number'},  # \xFF if podcast pls is 0,
                                                                               #   else master + normal
    {'name': 'number_of_podcast_playlists',    'size': 4,  'type': 'number'},

    {'name': 'unknown_1',                      'size': 4,  'type': 'unknown', 'seems_always_be': b'\xFF'*4},
    {'name': 'unknown_2',                      'size': 4,  'type': 'unknown'},
    {'name': 'unknown_3',                      'size': 4,  'type': 'unknown', 'seems_always_be': b'\xFF'*4},
    {'name': 'unknown_4',                      'size': 20, 'type': 'unknown'},

    # offset_of_playlist                       'size': 4
    # offset_of_playlist
    # ....
)
hphs_subs_offset_size = 4


class Playlists(List):
    def __init__(self, itunessd_bytes=None, offset=None, _sounds=None):
        super().__init__()

        if itunessd_bytes and offset:

            dic, playlists_offsets = get_dic_and_subs(itunessd_bytes, offset,
                                                      hphs_header_table, hphs_subs_offset_size)

            if dic['header_id'].decode() != 'hphs':
                raise DataError

            for playlist_offset in playlists_offsets:
                self.append(Playlist(itunessd_bytes, int_from_bytes(playlist_offset), _sounds=_sounds))


lphs_header_table = (
    {'name': 'header_id',                 'size': 4,  'type': 'string', 'must_be': 'lphs'},
    {'name': 'length',                    'size': 4,  'type': 'number'},
    {'name': 'number_of_all_sound',       'size': 4,  'type': 'number'},
    {'name': 'number_of_normal_sound',    'size': 4,  'type': 'number'},
    {'name': 'dbid',                      'size': 8,  'type': 'number'},
    {'name': 'TYPE',                      'size': 4,  'type': 'number'},  # 1 master, 2 normal, 3 podcast, 4 audiobook
    {'name': 'unknown_1',                 'size': 16, 'type': 'unknown'},

    # index_of_all_tracks                 'size': 4
    # index_of_all_tracks
    # ....
)
lphs_subs_index_size = 4


class Playlist(List):
    def __init__(self, itunessd_bytes=None, offset=None, _sounds=None):
        super().__init__()
        if itunessd_bytes and offset:
            dic, sounds_indexes = get_dic_and_subs(itunessd_bytes, offset, lphs_header_table, lphs_subs_index_size)
            if dic['header_id'].decode() != 'lphs':
                raise DataError

            for index in sounds_indexes:
                self.append(_sounds(index))
