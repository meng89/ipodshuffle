#!/usr/bin/env python3


db_table = (
    {'name': 'header_id',                  'size': 4,  'type': 'string',  'must_be': 'bdhs'},
    {'name': 'unknown_1',                  'size': 4,  'type': 'unknown', 'seems_always_be': b'\x01\x00\x01\x02'},
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
    {'name': 'header_id',                'size': 4, 'type': 'string', 'must_be': 'hths'},
    {'name': 'length',                   'size': 4, 'type': 'number'},
    {'name': 'number_of_tracks',         'size': 4, 'type': 'number'},
    {'name': 'unknown_1',                'size': 8, 'type': 'unknown'},

    # offset_of_track                    'size': 4
    # offset_of_track
    # ......
)
tracks_subs_offset_size = 4


track_table = (
    {'name': 'header_id',                      'size': 4,   'type': 'string', 'must_be': 'rths'},
    {'name': 'length',                         'size': 4,   'type': 'number'},
    {'name': 'start_at_pos_ms',                'size': 4,   'type': 'number'},  # 从几秒开始播放？
    {'name': 'stop_at_pos_ms',                 'size': 4,   'type': 'number'},  # 从几秒后结束？
    {'name': 'volume_gain',                    'size': 4,   'type': 'number'},

    {'name': 'filetype',                       'size': 4,   'type': 'number'},

    {'name': 'filename',                       'size': 256, 'type': 'string'},

    {'name': 'bookmark',                       'size': 4,   'type': 'number'},
    {'name': 'dont_skip_on_shuffle',           'size': 1,   'type': 'bool'},
    {'name': 'remember_playing_pos',           'size': 1,   'type': 'bool'},
    {'name': 'part_of_uninterruptable_album',  'size': 1,   'type': 'bool'},
    {'name': 'unknown_1',                      'size': 1,   'type': 'unknown'},
    {'name': 'pregap',                         'size': 4,   'type': 'number'},  # 播放之前空闲几秒？
    {'name': 'postgap',                        'size': 4,   'type': 'number'},  # 播放之后空闲几秒？
    {'name': 'number_of_sampless',             'size': 4,   'type': 'number'},  # 采样率？
    {'name': 'unknown_file_related_data1',     'size': 4,   'type': 'unknown'},
    {'name': 'gapless_data',                   'size': 4,   'type': 'number'},  # 无缝数据？
    {'name': 'unknown_file_related_data2',     'size': 4,   'type': 'unknown'},
    {'name': 'album_id',                       'size': 4,   'type': 'number'},
    {'name': 'track_number',                   'size': 2,   'type': 'number'},
    {'name': 'disc_number',                    'size': 2,   'type': 'number'},
    {'name': 'unknown_2',                      'size': 8,   'type': 'unknown'},
    {'name': 'dbid',                           'size': 8,   'type': 'number'},
    {'name': 'artist_id',                      'size': 4,   'type': 'number'},
    {'name': 'unknown_3',                      'size': 32,  'type': 'unknown'},
)


playlists_header_table = (
    {'name': 'header_id',                      'size': 4,  'type': 'string', 'must_be': 'hphs'},
    {'name': 'length',                         'size': 4,  'type': 'number'},

    # include the master playlist
    {'name': 'number_of_all_playlists',        'size': 4,  'type': 'number'},

    # \xFF*4 if no_of_normal_pls is 0 else 1
    {'name': 'playlist_flag_normal',           'size': 4,  'type': 'number'},

    {'name': 'number_of_normal_playlists',     'size': 4,  'type': 'number'},

    # \xFF*4 if no_of_audiobook_pls is 0, else no_of_master_pl + no_of_normal_pls + no_of_podcast_pls
    {'name': 'playlist_flag_audiobook',        'size': 4,  'type': 'number'},

    {'name': 'number_of_audiobook_playlists',  'size': 4,  'type': 'number'},

    # \xFF*4 if no_of_podcast_pls is 0, else no_of_master_pl + no_of_normal_pls
    {'name': 'playlist_flag_podcast',          'size': 4,  'type': 'number'},

    {'name': 'number_of_podcast_playlists',    'size': 4,  'type': 'number'},

    {'name': 'unknown_1',                      'size': 4,  'type': 'unknown', 'seems_always_be': b'\xFF'*4},
    {'name': 'unknown_2',                      'size': 4,  'type': 'unknown'},
    {'name': 'unknown_3',                      'size': 4,  'type': 'unknown', 'seems_always_be': b'\xFF'*4},
    {'name': 'unknown_4',                      'size': 20, 'type': 'unknown'},

    # offset_of_playlist                       'size': 4
    # offset_of_playlist
    # ....
)
playlists_subs_offset_size = 4


playlist_header_table = (
    {'name': 'header_id',                 'size': 4,  'type': 'string', 'must_be': 'lphs'},
    {'name': 'length',                    'size': 4,  'type': 'number'},

    {'name': 'number_of_all_track',       'size': 4,  'type': 'number'},

    # Number of non podcast or audiobook songs.
    {'name': 'number_of_normal_track',    'size': 4,  'type': 'number'},

    # when type is 1, dbid is all 0, voice use iPod_Control/Speakable/Messages/sv01-sv0a.wav
    {'name': 'dbid',                      'size': 8,  'type': 'number'},

    # 1: master,  2: normal,  3: podcast,  4: audiobook
    {'name': 'TYPE',                      'size': 4,  'type': 'number'},
    {'name': 'unknown_1',                 'size': 16, 'type': 'unknown'},

    # index_of_all_tracks                 'size': 4
    # index_of_all_tracks
    # ....
)
playlist_tracks_index_size = 4


class BytesDataError(Exception):
    pass


class DicDataError(Exception):
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


def check_must_be(dic, table):
    for key, value in dic.items():
        row = get_cow(key, table)
        if 'must_be' in row.keys():
            if value != row['must_be']:
                return False
    return True


def get_cow(name, table):
    cow = None
    for COW in table:
        if COW['name'] == name:
            cow = COW
            break
    return cow


########################################################################

def split_to_dic(data, table):
    dic = {}
    i = 0
    for item in table:
        dic[item['name']] = data[i: i+item['size']]
        i += item['size']
    return dic


def join_to_bytes(dic, table):
    b = b''
    for cow in table:
        if len(dic[cow['name']]) != cow['size']:
            raise SizeError

        b += dic[cow['name']]
    return b

#########################################################################
#########################################################################


def clean_unknown(dic, table):
    new_dic = {}
    for key, value in dic.items():
        cow = get_cow(key, table)
        if cow['type'] != 'unknown':
            new_dic[key] = value
    return new_dic


def replenish_unknown(dic, table):
    new_dic = {}
    for cow in table:
        if cow['type'] == 'unknown':
            if 'seems_always_be' in cow.keys():
                new_dic[cow['name']] = cow['seems_always_be']
            else:
                new_dic[cow['name']] = b'\x00' * cow['size']

    new_dic.update(dic)
    return new_dic

#########################################################################
#########################################################################


def decode_dic(dic, table, ):
    decoded_dic = {}
    for key, value in dic.items():
        cow = get_cow(key, table)

        if cow['type'] == 'string':
            # decoded_value = value.decode()
            import re
            decoded_value = re.sub('\x00+$', '', value.decode())
        elif cow['type'] == 'number':
            decoded_value = int.from_bytes(value, byteorder='little')
        elif cow['type'] == 'bool':
            decoded_value = bool(int.from_bytes(value, byteorder='little'))
        else:
            raise BytesDataError

        decoded_dic[key] = decoded_value

    return decoded_dic


def encode_dic(dic, table):
    encoded_dic = {}
    for key, value in dic.items():
        cow = get_cow(key, table)

        if cow['type'] == 'string':
            encoded_value = value.encode()
        elif cow['type'] == 'number':
            encoded_value = value.to_bytes(byteorder='little', length=cow['size'])
        elif cow['type'] == 'bool':
            encoded_value = int(value).to_bytes(byteorder='little', length=cow['size'])
        else:
            continue

        encoded_dic[key] = encoded_value

    return encoded_dic

#########################################################################
#########################################################################


def bytes_to_dic(data, table):
    return decode_dic(clean_unknown(split_to_dic(data, table), table), table)


def dic_to_bytes(dic, table):
    return join_to_bytes(replenish_unknown(encode_dic(dic, table), table), table)

#########################################################################
#########################################################################


def get_dic_sub_numbers(itunessd, offset, table, sub_int_size=None):
    sub_int_size = sub_int_size or 4

    header_size = get_table_size(table)
    dic = decode_dic(clean_unknown(split_to_dic(itunessd[offset: offset + header_size], table), table), table)

    offset_of_subs_start = offset + header_size
    offset_of_subs_end = offset + dic['length']

    subs_offsets_bytes = split_by_step(itunessd[offset_of_subs_start: offset_of_subs_end], sub_int_size)

    subs_offsets = []
    for one in subs_offsets_bytes:
        subs_offsets.append(int.from_bytes(one, 'little'))

    return dic, subs_offsets


def get_bytes(dics, length_before_offsets, table):

    offsets_bytes = b''
    dics_bytes = b''

    offset = length_before_offsets + 4 * len(dics)
    for dic in dics:
        offsets_bytes += offset.to_bytes(length=4, byteorder='little')

        offset += get_table_size(table)

        dics_bytes += dic_to_bytes(dic, table)

    return offsets_bytes + dics_bytes


########################################################################
########################################################################


def itunessd_to_dics(itunessd):

    db_size = get_table_size(db_table)
    db_header_bytes = itunessd[0:db_size]

    db_dic = bytes_to_dic(db_header_bytes, db_table)

    if not check_must_be(db_dic, db_table):
        raise BytesDataError

    # tracks
    tracks_header_dic, tracks_offsets = get_dic_sub_numbers(itunessd, db_dic['tracks_header_offset'],
                                                            tracks_header_table)
    tracks_dics = []
    for track_offset in tracks_offsets:
        track_dic = decode_dic(clean_unknown(split_to_dic(itunessd[track_offset:], track_table), track_table), track_table)

        if not check_must_be(track_dic, track_table):
            raise BytesDataError

        tracks_dics.append(track_dic)

    # playlists
    playlists_header_dic, playlists_offsets = get_dic_sub_numbers(itunessd, db_dic['playlists_header_offset'],
                                                                  playlists_header_table)
    playlists_dics_and_indexes = []
    for playlist_offset in playlists_offsets:
        playlist_header_dic, indexes_of_tracks = get_dic_sub_numbers(itunessd, playlist_offset, playlist_header_table)

        if not check_must_be(playlist_header_dic, playlist_header_table):
            raise BytesDataError

        playlists_dics_and_indexes.append((playlist_header_dic, indexes_of_tracks))

    return db_dic, tracks_dics, playlists_dics_and_indexes


def dics_to_itunessd(db_dic, track_dics, playlists_dics_and_indexes):

    db_bytes = dic_to_bytes(db_dic, db_table)

    tracks_header_dic = {'length': get_table_size(tracks_header_table) + 4 * len(track_dics),
                         'number_of_tracks': len(track_dics)}

    tracks_header_bytes = dic_to_bytes(tracks_header_dic, tracks_header_table)

    _length_before_tracks_offsets = get_table_size(db_table) + get_table_size(tracks_header_table)
    all_tracks_offsets_bytes_tracks_bytes = get_bytes(track_dics, _length_before_tracks_offsets, track_table)

    playlists_header_dic = {'length': get_table_size(playlists_header_table) + 4 * len(playlists_dics_and_indexes),
                            'number_of_all_playlists': len(playlists_dics_and_indexes),
                            }
    playlists_header_bytes = dic_to_bytes(playlists_header_dic, playlists_header_table)

    _length_before_playlists_offsets = _length_before_tracks_offsets \
        + len(all_tracks_offsets_bytes_tracks_bytes) + get_table_size(playlists_header_table)

    all_playlists_bytes_list = []
    for playlist_header_dic, indexes in playlists_dics_and_indexes:
        dic = playlist_header_dic.copy()
        dic['number_of_all_track'] = len(indexes)
        dic['number_of_normal_track'] = len(indexes)
        _one_playlist_header_bytes = dic_to_bytes(dic, playlist_header_table)

        _one_playlist_subs_indexes_bytes = b''.join([i.to_bytes(length=4, byteorder='little') for i in indexes])

        all_playlists_bytes_list.append(_one_playlist_header_bytes + _one_playlist_subs_indexes_bytes)

    playlists_offsets_bytes = b''
    all_playlists_bytes = b''
    offset = _length_before_playlists_offsets + 4 * len(playlists_dics_and_indexes)
    for playlist_bytes in all_playlists_bytes_list:
        playlists_offsets_bytes += offset.to_bytes(4, 'little')
        offset += len(playlist_bytes)
        all_playlists_bytes += playlist_bytes

    itunessd = db_bytes + tracks_header_bytes + all_tracks_offsets_bytes_tracks_bytes +\
        playlists_header_bytes + playlists_offsets_bytes + all_playlists_bytes

    return itunessd
