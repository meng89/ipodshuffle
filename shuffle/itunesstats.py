# Device will rebuild iPod_Control/iTunes/iTunesStats if the file is not exists

from .itunessd import get_table_size, chunk_to_dic, dic_to_chunk, split_by_step, get_custom_fields_dic

header_table = (
    {'name': 'number_of_tracks',  'size': 4,  'type': 'number'},
    {'name': 'unknown1',          'size': 4,  'type': 'unknown'}
)

track_table = (
    {'name': 'length',            'size': 4,  'type': 'number'},
    {'name': 'bookmark_time',     'size': 4,  'type': 'number',  'is_custom': True},
    {'name': 'play_count',        'size': 4,  'type': 'number',  'is_custom': True},
    {'name': 'time_of_last_play', 'size': 4,  'type': 'number',  'is_custom': True},
    {'name': 'skip_count',        'size': 4,  'type': 'number',  'is_custom': True},
    {'name': 'time_of_last_skip', 'size': 4,  'type': 'number',  'is_custom': True},
    {'name': 'unknown1',          'size': 4,  'type': 'unknown'},
    {'name': 'unknown2',          'size': 4,  'type': 'unknown'},
)


def itunesstats_to_dics(itunesstats):
    header_size = get_table_size(header_table)
    # header_chunk = itunesstats[0:header_size]
    # header_dic = chunk_to_dic(header_chunk, header_table)

    tracks_chunks = split_by_step(itunesstats[header_size:], get_table_size(track_table))

    _dics = []
    for track_chunk in tracks_chunks:
        _track_dic = chunk_to_dic(track_chunk, track_table)
        track_dic = get_custom_fields_dic(_track_dic, track_table)
        _dics.append(track_dic)

    return _dics


def dics_to_itunesstats(tracks_play_info_dics):
    _dics = tracks_play_info_dics

    header_dic = {'number_of_tracks': len(tracks_play_info_dics)}
    header_chunk = dic_to_chunk(header_dic, header_table)

    [dic.update({'length': get_table_size(track_table)}) for dic in _dics]

    _chunks = [dic_to_chunk(dic, track_table) for dic in _dics]

    all_tracks_chunck = b''.join(_chunks)

    return header_chunk + all_tracks_chunck
