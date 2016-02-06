from shuffle.trash.utils import ifb, itb


item_name = []
type_fields = []
key_fields = []


def field(s, default=item_name):
    if s not in default:
        default.append(s)
        return s
    else:
        raise ()


K_NAME = field('name', key_fields)
K_SIZE = field('size', key_fields)
K_TYPE = field('type', key_fields)
K_DEFAULT = field('default', key_fields)
K_MUST_BE = field('must_be', key_fields)
K_SEEMS_BE = field('seems_be', key_fields)

T_STR = field('str', type_fields)
T_INT = field('int', type_fields)
T_BOOL = field('bool', type_fields)
T_UNKNOWN = field('unknown', type_fields)


unknown_1 = field('unknown_1')
unknown_2 = field('unknown_2')
unknown_3 = field('unknown_3')
unknown_4 = field('unknown_4')

header_id = field('header_id')
header_legth = field('header_length')
total_no_of_tracks = field('total_no_of_tracks')
total_no_of_playlists = field('total_no_of_playlists')
max_volume = field('max_volume')
voiceover_enabled = field('voiceover_enabled')
total_no_of_tracks2 = field('total_no_of_tracks2')
track_header_chunk_offset = field('track_header_chunk_offset')
playlist_header_chunk_offset = field('track_header_chunk_offset')

bdhs_items = (
    {K_NAME: header_id,                    K_SIZE: 4,  K_MUST_BE: b'bdhs'},
    {K_NAME: unknown_1,                    K_SIZE: 4,  K_SEEMS_BE: b'\x01\x00\x01\x02'},
    {K_NAME: header_legth,                 K_SIZE: 4,  K_TYPE: T_INT},
    {K_NAME: total_no_of_tracks,           K_SIZE: 4,  K_TYPE: T_INT},
    {K_NAME: total_no_of_playlists,        K_SIZE: 4,  K_TYPE: T_INT},
    {K_NAME: unknown_2,                    K_SIZE: 8,  K_TYPE: T_UNKNOWN},
    {K_NAME: max_volume,                   K_SIZE: 1,  K_TYPE: T_INT},
    {K_NAME: voiceover_enabled,            K_SIZE: 1,  K_TYPE: T_INT},
    {K_NAME: unknown_3,                    K_SIZE: 2,  K_TYPE: T_UNKNOWN},
    {K_NAME: total_no_of_tracks2,          K_SIZE: 4,  K_TYPE: T_INT},
    {K_NAME: track_header_chunk_offset,    K_SIZE: 4,  K_TYPE: T_INT},
    {K_NAME: playlist_header_chunk_offset, K_SIZE: 4,  K_TYPE: T_INT},
    {K_NAME: unknown_4,                    K_SIZE: 20, K_TYPE: T_UNKNOWN})
bdhs_items_size = sum([i[K_SIZE] for i in bdhs_items])


total_length = field('total_legth')
number_of_tracks = field('number_of_tracks')

hths_items = (
    {K_NAME: header_id,        K_SIZE: 4, K_MUST_BE: b'hths'},
    {K_NAME: total_length,     K_SIZE: 4, K_TYPE: T_INT},
    {K_NAME: number_of_tracks, K_SIZE: 4, K_TYPE: T_INT},
    {K_NAME: unknown_1,        K_SIZE: 8, K_TYPE: T_UNKNOWN},
    #offset_of_track_1  4
    #offset_of_track_2  4
    #......
)
hths_items_size = sum([i[K_SIZE] for i in hths_items])


start_at_pos_ms = field('start_at_pos_ms')
stop_at_pos_ms = field('stop_at_pos_ms')
volume_gain = field('volume_gain')
TYPE = field('type')
filetype = field('filetype')
filename = field('filename')
bookmark = field('bookmark')
dont_skip_on_shuffle = field('dont_skip_on_shuffle')
remember_playing_pos = field('remember_playing_pos')
part_of_uninterruptable_album = field('part_of_uninterruptable_album')
pregap = field('pregap')
postgap = field('postgap')
number_of_sampless = field('number_of_sampless')
unknown_file_related_data1 = field('unknown_file_related_data1')
gapless_data = field('gapless_data')
unknown_file_related_data2 = field('unknown_file_related_data2')
albumid = field('albumid')
track_number = field('track_number')
disc_number = field('disc_number')
dbid = field('dbid')
artistid = field('artistid')

rths_items = (
    {K_NAME: header_id,                     K_SIZE: 4,   K_MUST_BE: b'rths'},
    {K_NAME: total_length,                  K_SIZE: 4,   K_TYPE: T_INT},
    {K_NAME: start_at_pos_ms,               K_SIZE: 4,   K_TYPE: T_INT},
    {K_NAME: stop_at_pos_ms,                K_SIZE: 4,   K_TYPE: T_INT},
    {K_NAME: volume_gain,                   K_SIZE: 4,   K_TYPE: T_INT},
    {K_NAME: filetype,                      K_SIZE: 4,   K_TYPE: T_INT},
    {K_NAME: filename,                      K_SIZE: 256, K_TYPE: T_STR},
    {K_NAME: bookmark,                      K_SIZE: 4,   K_TYPE: T_INT},
    {K_NAME: dont_skip_on_shuffle,          K_SIZE: 1,   K_TYPE: T_INT},
    {K_NAME: remember_playing_pos,          K_SIZE: 1,   K_TYPE: T_INT},
    {K_NAME: part_of_uninterruptable_album, K_SIZE: 1,   K_TYPE: T_BOOL},
    {K_NAME: unknown_1,                     K_SIZE: 1,   K_TYPE: T_UNKNOWN},
    {K_NAME: pregap,                        K_SIZE: 4,   K_TYPE: T_INT},
    {K_NAME: postgap,                       K_SIZE: 4,   K_TYPE: T_INT},
    {K_NAME: number_of_sampless,            K_SIZE: 4,   K_TYPE: T_INT},
    {K_NAME: unknown_file_related_data1,    K_SIZE: 4,   K_TYPE: T_UNKNOWN},
    {K_NAME: gapless_data,                  K_SIZE: 4,   K_TYPE: T_INT},
    {K_NAME: unknown_file_related_data2,    K_SIZE: 4,   K_TYPE: T_UNKNOWN},
    {K_NAME: albumid,                       K_SIZE: 4,   K_TYPE: T_INT},
    {K_NAME: track_number,                  K_SIZE: 2,   K_TYPE: T_INT},
    {K_NAME: disc_number,                   K_SIZE: 2,   K_TYPE: T_INT},
    {K_NAME: unknown_2,                     K_SIZE: 8,   K_TYPE: T_UNKNOWN},
    {K_NAME: dbid,                          K_SIZE: 8,   K_TYPE: T_INT},
    {K_NAME: artistid,                      K_SIZE: 4,   K_TYPE: T_INT},
    {K_NAME: unknown_3,                     K_SIZE: 32,  K_TYPE: T_UNKNOWN},
)
rths_items_size = sum([i[K_SIZE] for i in rths_items])


number_of_all_playlists = field('number_of_all_playlists')

playlist_flag_normal = field('playlist_flag_normal')
number_of_normal_playlists = field('number_of_normal_playlists')

playlist_flag_audiobook = field('playlist_flag_audiobook')
number_of_audiobook_playlists = field('number_of_audiobook_playlists')

playlist_flag_podcast = field('playlist_flag_podcast')
number_of_podcast_playlists = field('number_of_podcast_playlists')

hphs_items = (
    {K_NAME: header_id,                    K_SIZE: 4, K_MUST_BE: b'hphs'},
    {K_NAME: total_length,                 K_SIZE: 4, K_TYPE: T_INT},
    {K_NAME: number_of_all_playlists,      K_SIZE: 4, K_TYPE: T_INT},

    {K_NAME: playlist_flag_normal,         K_SIZE: 4, K_TYPE: T_INT},  # \xFF if normal pls is 0 else 1
    {K_NAME: number_of_normal_playlists,   K_SIZE: 4, K_TYPE: T_INT},

    {K_NAME: playlist_flag_audiobook,      K_SIZE: 4, K_TYPE: T_INT},  # \xFF if audiobook pls is 0, or master + normal + podcast
    {K_NAME: number_of_audiobook_playlists,K_SIZE: 4, K_TYPE: T_INT},

    {K_NAME: playlist_flag_podcast,        K_SIZE: 4, K_TYPE: T_INT},  # \xFF if podcast pls is 0, or master + normal
    {K_NAME: number_of_podcast_playlists,  K_SIZE: 4, K_TYPE: T_INT},

    {K_NAME: unknown_1,                    K_SIZE: 4, K_SEEMS_BE: b'\xFF'*4},
    {K_NAME: unknown_2,                    K_SIZE: 4, K_TYPE: T_UNKNOWN},
    {K_NAME: unknown_3,                    K_SIZE: 4, K_SEEMS_BE: b'\xFF'*4},
    {K_NAME: unknown_4,                    K_SIZE: 20, K_TYPE: T_UNKNOWN},
    # offset_of_playlist_1                 4
    # ....
)

hphs_items_size = sum([i[K_SIZE] for i in hphs_items])


PL_TYPE_MASTER = 1
PL_TYPE_NORMAL = 2
PL_TYPE_PODCAST = 3
PL_TYPE_AUDIOBOOK = 4

number_of_all_sound = field('number_of_all_sound')
number_of_normal_sound = field('number_of_normal_sound')
lphs_items = (
    {K_NAME: header_id,                 K_SIZE: 4,  K_MUST_BE: b'lphs'},
    {K_NAME: total_length,              K_SIZE: 4,  K_TYPE: T_INT},
    {K_NAME: number_of_all_sound,       K_SIZE: 4,  K_TYPE: T_INT},
    {K_NAME: number_of_normal_sound,    K_SIZE: 4,  K_TYPE: T_INT},
    {K_NAME: dbid,                      K_SIZE: 8,  K_TYPE: T_INT},
    {K_NAME: TYPE,                      K_SIZE: 4,  K_TYPE: T_INT},
    {K_NAME: unknown_1,                 K_SIZE: 16, K_TYPE: T_UNKNOWN},
    # playlist_track_1                  4
    # ....
)

lphs_items_size = sum([i[K_SIZE] for i in lphs_items])


def split_xxhs(data, xxhs):
    dic = {}
    i = 0
    for item in xxhs:
        dic[item[K_NAME]] = data[i:i+item[K_SIZE]]
        i += item[K_SIZE]
    return dic


def join_xxhs(dic, xxhs):
    data = b''
    for key in [item[K_NAME] for item in xxhs]:
        data += dic[key]
    return data


def check_xxhs(dic, xxhs):
    is_ok = True
    for item in xxhs:
        if K_MUST_BE in item.keys() and dic[item[K_NAME]] != item[K_MUST_BE]:
            is_ok = False
            break
    return is_ok


def convert_dic(dic, xxhs_items, to_bytes=True):  # bytes items to converted value like: bool, int, str etc
    new_dic = {}

    for item in xxhs_items:
        k = item[K_NAME]
        v = None

        if k not in dic.keys():
            continue

        if K_TYPE in item.keys():
            if item[K_TYPE] == T_INT:
                if to_bytes:
                    v = itb(dic[k], length=item[K_SIZE])
                else:
                    v = ifb(dic[k])

            elif item[K_TYPE] == T_STR:
                if to_bytes:
                    v = dic[k].encode() + (item[K_SIZE] - len(dic[k].encode())) * b'\x00'
                else:
                    v = dic[k].decode()

            elif item[K_TYPE] == T_BOOL:
                if to_bytes:
                    v = itb(int(dic[k]), length=item[K_SIZE])
                else:
                    v = bool(ifb(dic[k]))

            elif item[K_TYPE] == T_UNKNOWN:
                if to_bytes:
                    v = dic[k] + b'\x00' * (item[K_SIZE] - len(dic[k]))
                else:
                    v = dic[k]

        elif K_MUST_BE in item.keys():
            if dic[k] != item[K_MUST_BE]:
                raise()  # May be I should Delete the function check_xxhs
            else:
                v = item[K_MUST_BE]

        elif K_SEEMS_BE in item.keys():
            v = dic[k]

        new_dic[k] = v
    return new_dic
