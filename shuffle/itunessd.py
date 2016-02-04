import re

header_table = (
    {'name': 'header_id',                  'size': 4,  'type': 'unknown', 'value': b'bdhs'},
    {'name': 'unknown_1',                  'size': 4,  'type': 'unknown', 'value': b'\x01\x00\x01\x02'},
    {'name': 'length',                     'size': 4,  'type': 'number'},
    {'name': 'number_of_tracks',           'size': 4,  'type': 'number'},
    {'name': 'number_of_playlists',        'size': 4,  'type': 'number'},
    {'name': 'unknown_2',                  'size': 8,  'type': 'unknown'},
    {'name': 'max_volume',                 'size': 1,  'type': 'number',  'is_custom': True},
    {'name': 'enable_voiceover',           'size': 1,  'type': 'bool',    'is_custom': True},
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

# pos = position
track_table = (
    {'name': 'header_id',                      'size': 4,   'type': 'unknown', 'value': b'rths'},
    {'name': 'length',                         'size': 4,   'type': 'number'},

    # 起点 (毫秒)
    {'name': 'start_at_pos_ms',                'size': 4,   'type': 'number', 'is_custom': True},
    # 0: playing util end
    {'name': 'stop_at_pos_ms',                 'size': 4,   'type': 'number', 'is_custom': True},

    # have effect. what is the value meaning?
    {'name': 'volume_gain',                    'size': 4,   'type': 'number', 'is_custom': True},  # 音量增益

    {'name': 'type',                           'size': 4,   'type': 'number', 'is_custom': True},

    {'name': 'filename',                       'size': 256, 'type': 'string', 'is_custom': True},

    # seems not work on 4gen, I don't know if work on 3gen
    {'name': 'bookmark',                       'size': 4,   'type': 'unknown'},

    {'name': 'dont_skip_on_shuffle',           'size': 1,   'type': 'bool',   'is_custom': True},
    # save where?
    {'name': 'remember_playing_pos',           'size': 1,   'type': 'bool',   'is_custom': True},
    {'name': 'part_of_uninterruptable_album',  'size': 1,   'type': 'bool',   'is_custom': True},
    {'name': 'unknown_1',                      'size': 1,   'type': 'unknown'},

    # ?? seems not work
    {'name': 'pregap',                         'size': 4,   'type': 'number', 'is_custom': True},  # 不是播放之前空闲几秒
    {'name': 'postgap',                        'size': 4,   'type': 'number', 'is_custom': True},  # 不是播放之后空闲几秒

    # ?? tested ok when filetype 2 is set 0，
    {'name': 'number_of_sampless',             'size': 4,   'type': 'number', 'is_custom': True},  # 采样率？

    {'name': 'unknown_file_related_data1',     'size': 4,   'type': 'unknown'},
    {'name': 'gapless_data',                   'size': 4,   'type': 'number', 'is_custom': True},  # 无缝数据？
    {'name': 'unknown_file_related_data2',     'size': 4,   'type': 'unknown'},
    {'name': 'album_id',                       'size': 4,   'type': 'number', 'is_custom': True},  # ?
    {'name': 'track_number',                   'size': 2,   'type': 'number', 'is_custom': True},  # ?
    {'name': 'disc_number',                    'size': 2,   'type': 'number', 'is_custom': True},  # ?
    {'name': 'unknown_2',                      'size': 8,   'type': 'unknown'},
    {'name': 'dbid',                           'size': 8,   'type': 'number', 'is_custom': True},
    {'name': 'artist_id',                      'size': 4,   'type': 'number', 'is_custom': True},  # ?
    {'name': 'unknown_3',                      'size': 32,  'type': 'unknown'},
)


playlists_header_table = (
    {'name': 'header_id',                      'size': 4,  'type': 'unknown', 'value': b'hphs'},
    {'name': 'length',                         'size': 4,  'type': 'number'},

    # Include the master playlist
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

    # When type is 1, dbid is 0, voice use iPod_Control/Speakable/Messages/sv01-sv0a.wav
    {'name': 'dbid',                      'size': 8,  'type': 'number', 'is_custom': True},

    # 1: master,  2: normal,  3: podcast,  4: audiobook
    {'name': 'type',                      'size': 4,  'type': 'number', 'is_custom': True},
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


def split(chunk, table):
    dic = {}
    i = 0
    for item in table:
        dic[item['name']] = chunk[i: i + item['size']]
        i += item['size']
    return dic


def join(dic, table):
    b = b''
    for cow in table:
        if len(dic[cow['name']]) != cow['size']:
            raise SizeError

        b += dic[cow['name']]
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
    new_dic = {}
    for key, value in dic.items():
        cow = get_cow(key, table)

        if cow is None:
            continue

        if cow['type'] == 'string':
            unpad_value = re.sub('\x00+$', '', value.decode())
            new_value = unpad_value
        elif cow['type'] == 'number':
            new_value = int.from_bytes(value, 'little')
        elif cow['type'] == 'bool':
            new_value = bool(int.from_bytes(value, 'little'))
        else:
            # raise TypeError
            new_value = value

        new_dic[key] = new_value

    return new_dic


def encode(dic, table):
    new_dic = {}
    for key, value in dic.items():
        cow = get_cow(key, table)

        if cow is None:
            continue

        if cow['type'] == 'string':
            padded_value = value + '\x00' * (cow['size'] - len(value))
            new_value = padded_value.encode()
        elif cow['type'] == 'number':
            new_value = value.to_bytes(cow['size'], 'little')
        elif cow['type'] == 'bool':
            new_value = int(value).to_bytes(cow['size'], 'little')
        else:
            # raise TypeError
            new_value = value

        new_dic[key] = new_value

    return new_dic

###############################################################################
###############################################################################


def chunk_to_dic(chunk, table, do_check_header_id=True, do_clean_unknown_type=True):
    _dic = split(chunk, table)

    if do_check_header_id and 'header_id' in get_all_fields(table) and not check_header_id(_dic, table):
        raise ChunkError

    if do_clean_unknown_type:
        _dic = clean_unknown_type(_dic, table)

    return decode(_dic, table)


def dic_to_chunk(dic, table, do_check_header_id=True):
    _dic = replenish_unknown_type(encode(dic, table), table)

    if do_check_header_id and 'header_id' in get_all_fields(table) and not check_header_id(_dic, table):
        raise ChunkError

    return join(_dic, table)

###########################################################################
####################################


def get_custom_fields(table):
    fields = []
    for cow in table:
        if 'is_custom' in cow.keys() and cow['is_custom'] is True:
            fields.append(cow['name'])
    return fields


def get_all_fields(table):
    return [cow['name'] for cow in table]


def get_dic_by_fields(dic, fields):
    new_dic = {}
    for key, value in dic.items():
        if key in fields:
            new_dic[key] = value
    return new_dic


def get_custom_fields_dic(dic, table):
    return get_dic_by_fields(dic, get_custom_fields(table))


def get_legal_fields_dic(dic, table):
    return get_dic_by_fields(dic, get_all_fields(table))

########################################################################################################################
###############################################################################


def get_dic_sub_numbers(itunessd, offset, table, sub_int_size=None):
    sub_int_size = sub_int_size or 4

    header_size = get_table_size(table)

    header_dic = decode(clean_unknown_type(split(itunessd[offset: offset + header_size], table), table), table)

    offset_of_subs_start = offset + header_size
    offset_of_subs_end = offset + header_dic['length']

    subs_offsets_chunks = split_by_step(itunessd[offset_of_subs_start: offset_of_subs_end], sub_int_size)

    chunks = []
    for chunk in subs_offsets_chunks:
        chunks.append(int.from_bytes(chunk, 'little'))

    return header_dic, chunks

# -------------------------------------------------------------------------------------------------------


def itunessd_to_dics(itunessd):
    # header
    header_size = get_table_size(header_table)
    header_chunk = itunessd[0:header_size]

    header_dic = chunk_to_dic(header_chunk, header_table)

    # tracks
    tracks_header_dic, tracks_offsets = get_dic_sub_numbers(itunessd, header_dic['tracks_header_offset'],
                                                            tracks_header_table)
    tracks_dics = []
    for track_offset in tracks_offsets:
        _track_dic = chunk_to_dic(itunessd[track_offset:], track_table)
        track_dic = get_custom_fields_dic(_track_dic, track_table)
        tracks_dics.append(track_dic)

    # playlists
    playlists_header_dic, playlists_offsets = get_dic_sub_numbers(itunessd, header_dic['playlists_header_offset'],
                                                                  playlists_header_table)
    playlists_dics_and_indexes = []
    for playlist_offset in playlists_offsets:
        _playlist_header_dic, indexes_of_tracks = get_dic_sub_numbers(itunessd, playlist_offset, playlist_header_table)
        playlist_header_dic = get_custom_fields_dic(_playlist_header_dic, playlist_header_table)
        playlists_dics_and_indexes.append((playlist_header_dic, indexes_of_tracks))

    return get_custom_fields_dic(header_dic, header_table), tracks_dics, playlists_dics_and_indexes

########################################################################################################################


def get_offsets_chunk(length_before_offsets, chunks):
    offsets_chunk = b''
    offset = length_before_offsets + 4 * len(chunks)
    for dic in chunks:
        offsets_chunk += offset.to_bytes(length=4, byteorder='little')
        offset += len(dic)
    return offsets_chunk

# ----------------------------------------------------------------------------------------------------------------------


def dics_to_itunessd(header_dic, tracks_dics, playlists_dics_and_indexes):
    ############################################
    # header
    ######

    header_dic['length'] = get_table_size(header_table)
    header_dic['number_of_tracks'] = len(tracks_dics)
    header_dic['number_of_playlists'] = len(playlists_dics_and_indexes)
    header_dic['number_of_tracks2'] = 0

    header_part_size = get_table_size(header_table)

    ####################################################################################################################
    # tracks
    ##########

    # Chunk of header
    tracks_header_dic = {
        'length': get_table_size(tracks_header_table) + 4 * len(tracks_dics),
        'number_of_tracks': len(tracks_dics)
    }
    tracks_header_chunk = dic_to_chunk(tracks_header_dic, tracks_header_table)

    # Chunk of all tracks

    [track_dic.update({'length': get_table_size(track_table)}) for track_dic in tracks_dics]

    _tracks_chunks = [dic_to_chunk(dic, track_table) for dic in tracks_dics]

    all_tracks_chunck = b''.join(_tracks_chunks)

    # Chunk of offsets
    _length_before_tracks_offsets = header_part_size + len(tracks_header_chunk)
    tracks_offsets_chunck = get_offsets_chunk(_length_before_tracks_offsets, _tracks_chunks)

    # Put chunks together
    track_part_chunk = tracks_header_chunk + tracks_offsets_chunck + all_tracks_chunck

    ####################################################################################################################
    # playlists
    #############

    # Chunk of header
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

    # Chunk of all playlists
    _playlists_chunks = []
    for playlist_header_dic, indexes in playlists_dics_and_indexes:
        dic = playlist_header_dic.copy()
        dic['length'] = get_table_size(playlist_header_table) + 4 * len(indexes)
        dic['number_of_all_track'] = len(indexes)
        dic['number_of_normal_track'] = len(indexes) if dic['type'] in (1, 2) else 0

        if dic['type'] == MASTER:
            header_dic['number_of_tracks2'] = len(indexes)

        _playlist_header_chunk = dic_to_chunk(dic, playlist_header_table)
        _indexes_chunk = b''.join([i.to_bytes(4, 'little') for i in indexes])
        playlist_chunk = _playlist_header_chunk + _indexes_chunk

        _playlists_chunks.append(playlist_chunk)

    all_playlists_chunk = b''.join(_playlists_chunks)

    # Chunk of offsets
    _length_before_playlists_offsets = header_part_size + len(track_part_chunk) + len(playlists_header_chunk)
    playlists_offsets_chunk = get_offsets_chunk(_length_before_playlists_offsets, _playlists_chunks)

    # Put chunks together
    playlists_part_chunk = playlists_header_chunk + playlists_offsets_chunk + all_playlists_chunk

    ########################################################################
    header_dic['tracks_header_offset'] = header_part_size
    header_dic['playlists_header_offset'] = header_part_size + len(track_part_chunk)
    header_part_chunk = dic_to_chunk(header_dic, header_table)
    ########################################################################

    itunessd = header_part_chunk + track_part_chunk + playlists_part_chunk

    return itunessd
