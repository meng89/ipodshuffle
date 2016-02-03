#!/usr/bin/env python3

import re

db_table = (
    {'name': 'header_id',                  'size': 4,  'type': 'unknown', 'value': b'bdhs'},
    {'name': 'unknown_1',                  'size': 4,  'type': 'unknown', 'value': b'\x01\x00\x01\x02'},
    {'name': 'legth',                      'size': 4,  'type': 'number'},
    {'name': 'number_of_tracks',           'size': 4,  'type': 'number'},
    {'name': 'number_of_playlists',        'size': 4,  'type': 'number'},
    {'name': 'unknown_2',                  'size': 8,  'type': 'unknown'},
    {'name': 'max_volume',                 'size': 1,  'type': 'number'},
    {'name': 'enable_voiceover',           'size': 1,  'type': 'bool'},
    {'name': 'unknown_3',                  'size': 2,  'type': 'unknown'},

    # Does not include podcasts or audiobooks in the count.
    {'name': 'number_of_tracks2',          'size': 4,  'type': 'number'},

    {'name': 'tracks_header_offset',       'size': 4,  'type': 'number'},
    {'name': 'playlists_header_offset',    'size': 4,  'type': 'number'},
    {'name': 'unknown_4',                  'size': 20, 'type': 'unknown'}
)


tracks_header_table = (
    {'name': 'header_id',                'size': 4, 'type': 'unknown', 'value': b'hths'},
    {'name': 'length',                   'size': 4, 'type': 'number'},
    {'name': 'number_of_tracks',         'size': 4, 'type': 'number'},
    {'name': 'unknown_1',                'size': 8, 'type': 'unknown'},

    # offset_of_track                    'size': 4
    # offset_of_track
    # ......
)
tracks_subs_offset_size = 4


track_table = (
    {'name': 'header_id',                      'size': 4,   'type': 'unknown', 'value': b'rths'},
    {'name': 'length',                         'size': 4,   'type': 'number'},
    {'name': 'start_at_pos_ms',                'size': 4,   'type': 'number'},  # 从几秒开始播放？
    {'name': 'stop_at_pos_ms',                 'size': 4,   'type': 'number'},  # 从几秒后结束？
    {'name': 'volume_gain',                    'size': 4,   'type': 'number'},

    {'name': 'filetype',                       'size': 4,   'type': 'number'},

    {'name': 'filename',                       'size': 256, 'type': 'string'},

    {'name': 'bookmark',                       'size': 4,   'type': 'number'},  # 书签？ 暂停位置？
    {'name': 'dont_skip_on_shuffle',           'size': 1,   'type': 'bool'},
    {'name': 'remember_playing_pos',           'size': 1,   'type': 'bool'},    #
    {'name': 'part_of_uninterruptable_album',  'size': 1,   'type': 'bool'},    # ?
    {'name': 'unknown_1',                      'size': 1,   'type': 'unknown'},
    {'name': 'pregap',                         'size': 4,   'type': 'number'},  # 播放之前空闲几秒？
    {'name': 'postgap',                        'size': 4,   'type': 'number'},  # 播放之后空闲几秒？
    {'name': 'number_of_sampless',             'size': 4,   'type': 'number'},  # 采样率？
    {'name': 'unknown_file_related_data1',     'size': 4,   'type': 'unknown'},
    {'name': 'gapless_data',                   'size': 4,   'type': 'number'},  # 无缝数据？
    {'name': 'unknown_file_related_data2',     'size': 4,   'type': 'unknown'},
    {'name': 'album_id',                       'size': 4,   'type': 'number'},  # ?
    {'name': 'track_number',                   'size': 2,   'type': 'number'},  # ?
    {'name': 'disc_number',                    'size': 2,   'type': 'number'},  # ?
    {'name': 'unknown_2',                      'size': 8,   'type': 'unknown'},
    {'name': 'dbid',                           'size': 8,   'type': 'number'},
    {'name': 'artist_id',                      'size': 4,   'type': 'number'},  # ?
    {'name': 'unknown_3',                      'size': 32,  'type': 'unknown'},
)


playlists_header_table = (
    {'name': 'header_id',                      'size': 4,  'type': 'unknown', 'value': b'hphs'},
    {'name': 'length',                         'size': 4,  'type': 'number'},

    # include the master playlist
    {'name': 'number_of_all_playlists',        'size': 4,  'type': 'number'},

    # \xFF * 4 if number_of_normal_pls is 0, else 1
    {'name': 'flag1',                          'size': 4,  'type': 'number'},

    {'name': 'number_of_normal_playlists',     'size': 4,  'type': 'number'},

    # \xFF * 4 if number_of_audiobook_pls is 0, else no_of_master_pl + no_of_normal_pls + no_of_podcast_pls
    {'name': 'flag2',                          'size': 4,  'type': 'number'},

    {'name': 'number_of_audiobook_playlists',  'size': 4,  'type': 'number'},

    # \xFF * 4 if number_of_podcast_pls is 0, else no_of_master_pl + no_of_normal_pls
    {'name': 'flag3',                          'size': 4,  'type': 'number'},

    {'name': 'number_of_podcast_playlists',    'size': 4,  'type': 'number'},

    {'name': 'unknown_1',                      'size': 4,  'type': 'unknown', 'value': b'\xFF'*4},
    {'name': 'unknown_2',                      'size': 4,  'type': 'unknown'},
    {'name': 'unknown_3',                      'size': 4,  'type': 'unknown', 'value': b'\xFF'*4},
    {'name': 'unknown_4',                      'size': 20, 'type': 'unknown'},

    # offset_of_playlist                       'size': 4
    # offset_of_playlist
    # ....
)
playlists_subs_offset_size = 4


playlist_header_table = (
    {'name': 'header_id',                 'size': 4,  'type': 'unknown', 'value': b'lphs'},
    {'name': 'length',                    'size': 4,  'type': 'number'},

    {'name': 'number_of_all_track',       'size': 4,  'type': 'number'},

    # Number of non podcast or audiobook songs.
    {'name': 'number_of_normal_track',    'size': 4,  'type': 'number'},

    # when type is 1, dbid is all 0, voice use iPod_Control/Speakable/Messages/sv01-sv0a.wav
    {'name': 'dbid',                      'size': 8,  'type': 'number'},

    # 1: master,  2: normal,  3: podcast,  4: audiobook
    {'name': 'type',                      'size': 4,  'type': 'number'},
    {'name': 'unknown_1',                 'size': 16, 'type': 'unknown'},

    # index_of_all_tracks                 'size': 4
    # index_of_all_tracks
    # ....
)
playlist_tracks_index_size = 4
# Playlist type
MASTER = 1
NORMAL = 2
PODCAST = 3
AUDIOBOOK = 4


class ChunkError(Exception):
    pass


class SizeError(Exception):
    pass


def split_by_step(data, step):
    return [data[i:i+step] for i in range(0, len(data), step)]


def int_from_bytes(data):
    return int.from_bytes(data, byteorder='little')


def dbid_from_bytes(data):
    return '{:X}'.format(int_from_bytes(data))


def get_table_size(table):
    return sum([i['size'] for i in table])


def check_header_id(dic, table):
    row = get_cow('header_id', table)
    if dic['header_id'] == row['value']:
        return True
    else:
        return False


def get_cow(name, table):
    cow = None
    for COW in table:
        if COW['name'] == name:
            cow = COW
            break
    return cow

###############################################################################
###############################################################################


def split(bytes_data, table):
    dic = {}
    i = 0
    for item in table:
        dic[item['name']] = bytes_data[i: i + item['size']]
        i += item['size']
    return dic


def join(dic_data, table):
    b = b''
    for cow in table:
        if len(dic_data[cow['name']]) != cow['size']:
            raise SizeError

        b += dic_data[cow['name']]
    return b

###############################################################################
###############################################################################


def clean_unknown_type(dic, table):
    new_dic = {}
    for key, value in dic.items():
        cow = get_cow(key, table)
        if cow['type'] != 'unknown':
            new_dic[key] = value
    return new_dic


def replenish_unknown_type(dic, table):
    new_dic = {}
    for cow in table:
        if cow['name'] not in dic.keys() and cow['type'] == 'unknown':
            if 'value' in cow.keys():
                new_dic[cow['name']] = cow['value']
            else:
                new_dic[cow['name']] = b'\x00' * cow['size']

    new_dic.update(dic)
    return new_dic

###############################################################################
###############################################################################


def decode(dic, table):
    decoded_dic = {}
    for key, value in dic.items():
        cow = get_cow(key, table)

        if cow['type'] == 'string':
            unpad_value = re.sub('\x00+$', '', value.decode())
            decoded_value = unpad_value
        elif cow['type'] == 'number':
            decoded_value = int.from_bytes(value, 'little')
        elif cow['type'] == 'bool':
            decoded_value = bool(int.from_bytes(value, 'little'))
        else:
            raise TypeError
        decoded_dic[key] = decoded_value

    return decoded_dic


def encode(dic, table):
    encoded_dic = {}
    for key, value in dic.items():
        cow = get_cow(key, table)
        if cow['type'] == 'string':
            padded_value = value + '\x00' * (cow['size'] - len(value))
            encoded_value = padded_value.encode()
        elif cow['type'] == 'number':
            encoded_value = value.to_bytes(cow['size'], 'little')
        elif cow['type'] == 'bool':
            encoded_value = int(value).to_bytes(cow['size'], 'little')
        else:
            raise TypeError
        encoded_dic[key] = encoded_value

    return encoded_dic

###############################################################################
###############################################################################


def chunk_to_dic(chunk, table, do_check_must_be=True):
    _dic = split(chunk, table)

    if do_check_must_be and not check_header_id(_dic, table):
        raise ChunkError

    return decode(clean_unknown_type(_dic, table), table)


def dic_to_chunk(dic, table, do_check_must_be=True):
    _dic = replenish_unknown_type(encode(dic, table), table)

    if do_check_must_be and not check_header_id(_dic, table):
        raise ChunkError

    return join(_dic, table)

########################################################################################################################
###############################################################################


def get_dic_sub_numbers(itunessd, offset, table, sub_int_size=None):
    sub_int_size = sub_int_size or 4

    header_size = get_table_size(table)
    # dic = chunk_to_dic(itunessd[offset: offset + header_size], table)
    dic = decode(clean_unknown_type(split(itunessd[offset: offset + header_size], table), table), table)

    offset_of_subs_start = offset + header_size
    offset_of_subs_end = offset + dic['length']

    subs_offsets_bytes = split_by_step(itunessd[offset_of_subs_start: offset_of_subs_end], sub_int_size)

    subs_offsets = []
    for one in subs_offsets_bytes:
        subs_offsets.append(int.from_bytes(one, 'little'))

    return dic, subs_offsets

# -------------------------------------------------------------------------------------------------------


def itunessd_to_dics(itunessd):

    db_size = get_table_size(db_table)
    db_header_bytes = itunessd[0:db_size]

    db_dic = chunk_to_dic(db_header_bytes, db_table)

    # tracks
    tracks_header_dic, tracks_offsets = get_dic_sub_numbers(itunessd, db_dic['tracks_header_offset'],
                                                            tracks_header_table)
    tracks_dics = []
    for track_offset in tracks_offsets:
        track_dic = chunk_to_dic(itunessd[track_offset:], track_table)

        tracks_dics.append(track_dic)

    # playlists
    playlists_header_dic, playlists_offsets = get_dic_sub_numbers(itunessd, db_dic['playlists_header_offset'],
                                                                  playlists_header_table)
    playlists_dics_and_indexes = []
    for playlist_offset in playlists_offsets:
        playlist_header_dic, indexes_of_tracks = get_dic_sub_numbers(itunessd, playlist_offset, playlist_header_table)

        playlists_dics_and_indexes.append((playlist_header_dic, indexes_of_tracks))

    return db_dic, tracks_dics, playlists_dics_and_indexes

########################################################################################################################


def get_offsets_chunk(length_before_offsets, chunks):
    offsets_bytes = b''
    offset = length_before_offsets + 4 * len(chunks)
    for dic in chunks:
        offsets_bytes += offset.to_bytes(length=4, byteorder='little')
        offset += len(dic)
    return offsets_bytes

# ----------------------------------------------------------------------------------------------------------------------


def dics_to_itunessd(db_dic, track_dics, playlists_dics_and_indexes):
    itunessd = b''

    db_chunk = dic_to_chunk(db_dic, db_table)

    itunessd += db_chunk
    ####################################################################################################################
    # tracks
    ####################################################################################################################
    tracks_header_dic = {'length': get_table_size(tracks_header_table) + 4 * len(track_dics),
                         'number_of_tracks': len(track_dics)}
    tracks_header_chunk = dic_to_chunk(tracks_header_dic, tracks_header_table)

    _length_before_tracks_offsets = len(db_chunk) + len(tracks_header_chunk)
    _tracks_chunks = [dic_to_chunk(dic, track_table) for dic in track_dics]
    tracks_offsets_chunck = get_offsets_chunk(_length_before_tracks_offsets, _tracks_chunks)
    all_tracks_chunck = b''.join(_tracks_chunks)

    itunessd += tracks_header_chunk + tracks_offsets_chunck + all_tracks_chunck
    ####################################################################################################################
    # playlists
    ####################################################################################################################
    #   header
    _playlists_dics = [playlist_indexes[0] for playlist_indexes in playlists_dics_and_indexes]
    _types = [playlist_dic['type'] for playlist_dic in _playlists_dics]
    playlists_header_dic = {
        'length': get_table_size(playlists_header_table) + 4 * len(playlists_dics_and_indexes),
        'number_of_all_playlists': len(_types),
        'flag1': 0xffffffff if _types.count(NORMAL) == 0 else 1,
        'number_of_normal_playlists': _types.count(NORMAL),
        'flag2': 0xffffffff if _types.count(AUDIOBOOK) == 0 else (_types.count(MASTER) + _types.count(NORMAL) +
                                                                  _types.count(PODCAST)),
        'number_of_audiobook_playlists': _types.count(AUDIOBOOK),
        'flag3': 0xffffffff if _types.count(PODCAST) == 0 else _types.count(1) + _types.count(NORMAL),
        'number_of_podcast_playlists': _types.count(PODCAST)
    }

    playlists_header_chunk = dic_to_chunk(playlists_header_dic, playlists_header_table)

    # offsets
    _length_before_playlists_offsets = len(itunessd) + len(playlists_header_chunk)

    _playlists_chunks = []
    for playlist_header_dic, indexes in playlists_dics_and_indexes:
        dic = playlist_header_dic.copy()
        dic['number_of_all_track'] = len(indexes)
        dic['number_of_normal_track'] = len(indexes) if dic['type'] in (1, 2) else 0

        _playlist_header_chunk = dic_to_chunk(dic, playlist_header_table)
        _indexes_chunk = b''.join([i.to_bytes(length=4, byteorder='little') for i in indexes])
        playlist_chunk = _playlist_header_chunk + _indexes_chunk

        _playlists_chunks.append(playlist_chunk)

    playlists_offsets_chunk = get_offsets_chunk(_length_before_playlists_offsets, _playlists_chunks)
    all_playlists_chunk = b''.join(_playlists_chunks)

    itunessd += playlists_header_chunk + playlists_offsets_chunk + all_playlists_chunk

    return itunessd
