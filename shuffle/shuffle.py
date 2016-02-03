import os
import json
import hashlib
import random
import string
import shutil


from shuffle import audiorec


from . import itunessd
from .baseclasses import List
# baseclasses ?  see https://github.com/meng89/epubuilder/blob/feature-rw/epubuilder/baseclasses.py

MUSIC = 'music'
AUDIOBOOK = 'audiobook'


def int_from_bytes(data):
    return int.from_bytes(data, byteorder='little')


def dbid_from_bytes(data):
    return '{:X}'.format(int_from_bytes(data))


def get_dbid1():
    return ''.join(random.sample('ABCDEF' + string.digits, 16))


def get_dbid2():
    dbid_string = ''
    for x in random.sample(range(0, 255), 8):
        s = hex(x)[2:]
        if len(s) == 1:
            s = '0' + s
        dbid_string += s.upper()
    return dbid_string

get_dbid = get_dbid2


def get_mtime_size(path):
    return {
        'mtime': os.path.getmtime(path),
        'size': os.path.getsize(path)
    }


def get_checksum(path):
    source = open(path, 'rb')
    m = hashlib.md5()
    while True:
        data = source.read(10240)
        if data:
            m.update(data)
        else:
            break
    source.close()
    checksum = m.hexdigest()
    return checksum


class Shuffle:
    def __init__(self, directory):
        self.base_dir = os.path.realpath(os.path.normpath(directory))
        self._ctrl_folder = 'iPod_Control'

        self._itunessd_path = self.base_dir + '/' + self._ctrl_folder + '/iTunes/iTunesSD'

        bdhs_dic = None
        rths_dics = None
        lphs_dic_indexes_s = None

        if os.path.exists(self._itunessd_path):
            if os.path.isfile(self._itunessd_path):
                bytes_data = open(self._itunessd_path, 'rb').read()
                bdhs_dic, rths_dics, lphs_dic_indexes_s = itunessd.itunessd_to_dics(bytes_data)
            else:
                raise Exception

        self._dic = bdhs_dic

        self.tracks = Tracks(self, rths_dics)

        self.playlists = Playlists(self, lphs_dic_indexes_s)

        self.sounds = Sounds(_shuffle=self)

        self.tracks_voicedb = Voicedb(logs_path=self.base_dir + '/' + 'tracks_voice_logs.json',
                                      stored_dir=self.base_dir + '/' + 'Speakable' + '/' + 'Tracks',
                                      users=self.tracks)

        self.playlists_voicedb = Voicedb(logs_path=self.base_dir + '/' + 'playlists_voice_logs.json',
                                         stored_dir=self.base_dir + '/' + 'Speakable' + '/' + 'Playlists',
                                         users=self.playlists)

    def write(self):
        bdhs_dic = self._dic.copy()
        rths_dics = self.tracks.get_dics()
        lphs_dic_indexes_s = self.playlists.get_dic_indexes_s()

        bytes_data = itunessd.dics_to_itunessd(bdhs_dic, rths_dics, lphs_dic_indexes_s)

        open(self._itunessd_path, 'wb').write(bytes_data)


class Tracks(List):
    def __init__(self, shuffle, rths_dics=None):
        super().__init__()

        self._shuffle = shuffle
        rths_dics = rths_dics or []
        for rths_dic in rths_dics:
            self.append(Track(self, rths_dic))

    def get_dics(self):
        dics = []
        for track in self:
            dics.append(track.get_dic())
        return dics


class Track:
    def __init__(self, shuffle, rths_dic=None, sound=None):
        self._shuffle = shuffle

        if rths_dic:
            self._dic = rths_dic
        elif sound:
            self.sound = sound
        else:
            raise Exception

    def get_dic(self):
        return self._dic

    def set_voice(self, text, lang, dbid):
        pass


class Playlists(List):
    def __init__(self, shuffle, lphs_dics_indexes=None):
        super().__init__()
        self._shuffle = shuffle

        lphs_dics_indexes = lphs_dics_indexes or []
        for lphs_dic, indexes in lphs_dics_indexes:
            self.append(Playlist(shuffle, lphs_dic, indexes))

    def get_dic_indexes_s(self):
        dic_indexes_s = []
        for playlist in self:
            dic_indexes_s.append(playlist.get_dic_indexes())

        return dic_indexes_s


class Playlist(List):
    def __init__(self, shuffle, lphs_dic=None, indexes_of_tracks=None):
        super().__init__()
        self._shuffle = shuffle
        self._dic = lphs_dic

        indexes_of_tracks = indexes_of_tracks or []
        for index in indexes_of_tracks:
            self.append(shuffle.tracks[index])

    def get_dic_indexes(self):
        return self._dic, [self._shuffle.tracks.index(track) for track in self]


class Sounds:
    def __init__(self, _shuffle):
        self._shuffle = _shuffle

        self._stored_dir = 'sounds'

        self._logs_path = self._shuffle.base_dir + '/' + self._shuffle.control_folder + '/' + 'sounds_logs.json'
        self._logs = json.loads(open(self._logs_path).read())

    def _del_not_exists(self):
        new_logs = {}
        for path, metadata in self._logs.items():
            full_path = self._shuffle.base_dir + os.sep + path

            if os.path.exists(full_path) and os.path.isfile(full_path):
                new_logs[path] = metadata

        self._logs = new_logs

    def _updata_metadata_changed(self):
        new_logs = {}
        for path, metadata in self._logs.items():
            full_path = self._shuffle.base_dir + os.sep + path

            if os.path.getsize(full_path) == metadata['size'] and os.path.getmtime(full_path) == metadata['mtime']:
                new_logs[path] = metadata
            else:
                new_logs[path] = get_mtime_size(full_path)

    def _update_from_tracks(self):
        not_log_tracks_filenames = []
        for track in self._shuffle.itunessd.tracks:
            if track.filename[1:] not in self._logs.keys():
                not_log_tracks_filenames.append(track.filename[1:])

        tracks_logs_notinlogs = {}
        for filename in not_log_tracks_filenames:
            tracks_logs_notinlogs[filename] = get_mtime_size(self._shuffle.base_dir + '/' + filename)

        self._logs.update(tracks_logs_notinlogs)

    def list(self):
        return tuple(self._logs.keys())

    def get_from_checksum(self, checksum):
        path = None
        for key, info in self._logs.items():
            if info['checksum'] == checksum:
                path = key
                break
        return path

    def add(self, path, checksum=None):
        if not audiorec.get_filetype(path):
            raise TypeError('This file type is not supported.')

        checksum = checksum or checksum(path)

        path_in_ipod = None
        for PATH, metadata in self._logs:
            if metadata['checksum'] == checksum:
                path_in_ipod = PATH
                break

        if not path_in_ipod:  # Mean this file is not in ipod.

            # 1. get random filename which not use.
            while True:
                # at most 65533 files in one folder
                path_in_ipod = os.path.join(self._shuffle.base_dir, self._shuffle.control_folder,
                                            self._stored_dir, random.sample(string.ascii_uppercase, 6))

                if not os.path.exists(path_in_ipod) and path_in_ipod not in self._logs.keys():
                    break

            # 2. copy file
            target_path = self._shuffle.base_dir + '/' + path_in_ipod
            shutil.copyfile(path, target_path)

            # 3. update logs
            self._logs[path_in_ipod] = {
                'checksum': checksum,
                'mtime': os.path.getmtime(target_path),
                'size': os.path.getsize(target_path)
            }

        return path_in_ipod

    def remove(self, path):
        os.remove(self._shuffle.base_dir + '/' + path)
        del self._shuffle.sounds_logs[path]

    def write_logs(self):
        open(self._logs_path, 'w').write(json.dumps(self._logs))


class Voicedb:
    def __init__(self, logs_path, stored_dir, users):
        self._logs_path = logs_path
        self._stored_dir = stored_dir
        self._users = users
        self._logs = json.loads(open(self._logs_path).read())

    def _path(self, dbid):
        return self._stored_dir + '/' + dbid + '.wav'

    def del_wrong_logs(self):
        pass
        dbids_to_del = []
        for DBID, info in self._logs.items():
            voice_path = self._path(DBID)
            if info['mtime'] != os.path.getmtime(voice_path) or info['size'] != os.path.getsize(voice_path):
                dbids_to_del.append(DBID)

        for dbid in dbids_to_del:
            del self._logs[dbid]

    def clean_store_dir(self):
        files_to_del = []
        for file in os.listdir(self._stored_dir):
            name, ext = os.path.splitext(file)
            if (name not in self._logs.keys() and name not in [user.dbid for user in self._users]) or ext != '.wav':
                files_to_del.append(file)

        for file in files_to_del:
            full_path = self._stored_dir + '/' + file

            if os.path.isfile(full_path):
                os.remove(full_path)
            else:
                os.removedirs(full_path)

    def clean(self):
        pass

    def add(self, path, text, lang, checksum):
        if not audiorec.get_filetype(path) == 'wav':
            raise TypeError

        checksum = checksum or get_checksum(path)

        dbid = None
        for DBID, info in self._logs.items():
            if info['text'] == text and info['lang'] == lang:
                if info['checksum'] == checksum:
                    dbid = DBID
                    break
                else:
                    shutil.copyfile(path, self._stored_dir + '/' + DBID + '.wav')

        if not dbid:
            while True:
                dbid = get_dbid()
                if dbid not in self._logs.keys():
                    break

            voice_in_ipod = self._stored_dir + '/' + dbid + '.wav'
            shutil.copyfile(path, voice_in_ipod)

            self._logs[dbid] = {
                'text': text,
                'lang': lang,
                'checksum': checksum,
                'mtime': os.path.getmtime(voice_in_ipod),
                'size': os.path.getsize(voice_in_ipod)
            }
        return dbid

    def remove(self, dbid):
        os.remove(self._stored_dir + '/' + dbid + '.wav')
        del self._logs[dbid]

    def get(self, text=None, lang=None, checksum=None):
        dbid = None
        for DBID, info in self._logs.items():
            if (info['text'] == text and info['lang'] == lang) or info['checksum'] == checksum:
                dbid = DBID
                break
        return dbid


class SystemVoice:
    pass


class MassagesVoice:
    pass
