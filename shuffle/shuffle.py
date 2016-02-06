import os
import json
import hashlib
import random
import string
import shutil


from . import audio


from . import itunessd, itunesstats

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
        self.base = os.path.realpath(os.path.normpath(directory))
        self._ctrl_folder = 'iPod_Control'

        self._itunessd_path = self.base + '/' + self._ctrl_folder + '/iTunes/iTunesSD'
        self._itunesstats_path = self.base + '/' + self._ctrl_folder + '/iTunes/iTunesStats'

        def read(path, fun):
            if os.path.exists(path):
                if os.path.isfile(path):
                    chunk = open(path, 'rb').read()
                    return fun(chunk)
                else:
                    raise Exception

        header_dic, tracks_dics, playlists_dics_and_indexes = read(self._itunessd_path, itunessd.itunessd_to_dics)
        tracks_play_count_dics = read(self._itunesstats_path, itunesstats.itunesstats_to_dics)

        if len(tracks_dics) != len(tracks_play_count_dics):
            raise Exception

        tracks_with_play_count_dics_zip = zip(tracks_dics, tracks_play_count_dics)

        self._dic = header_dic

        self.__dict__['tracks'] = Tracks(self, tracks_with_play_count_dics_zip)

        self.__dict__['playlists'] = Playlists(self, playlists_dics_and_indexes)

        self.__dict__['sounds'] = Sounds(self,
                                         logs_path=os.path.join(self.base, self._ctrl_folder, 'sounds_logs.json'),
                                         stored_dir=os.path.join(self.base, self._ctrl_folder, 'sounds'))

        self.__dict__['tracks_voicedb'] = \
            Voicedb(logs_path=os.path.join(self.base, self._ctrl_folder, 'tracks_voice_logs.json'),
                    stored_dir=os.path.join(self.base, self._ctrl_folder, 'Speakable', 'Tracks'),
                    users=self.tracks)

        self.__dict__['playlists_voicedb'] = \
            Voicedb(logs_path=os.path.join(self.base, self._ctrl_folder, 'playlists_voice_logs.json'),
                    stored_dir=os.path.join(self.base, self._ctrl_folder, 'Speakable', 'Playlists'),
                    users=self.playlists)

    @property
    def max_volume(self):
        return self._dic['max_volume']

    @max_volume.setter
    def max_volume(self, value):
        self._dic['max_volume'] = value

    @property
    def enable_voiceover(self):
        return self._dic['enable_voiceover']

    @enable_voiceover.setter
    def enable_voiceover(self, value):
        self._dic['enable_voiceover'] = value

    @property
    def tracks(self):
        return self.__dict__['tracks']

    @property
    def playlists(self):
        return self.__dict__['playlists']

    @property
    def sounds(self):
        return self.__dict__['sounds']

    @property
    def tracks_voicedb(self):
        return self.__dict__['tracks_voicedb']

    @property
    def playlists_voicedb(self):
        return self.__dict__['playlists_voicedb']

    def write(self):
        db_dic = self._dic.copy()
        tracks_dics = self.tracks.get_dics()
        playlists_dics_and_indexes = self.playlists.get_dics_and_indexes()

        bytes_data = itunessd.dics_to_itunessd(db_dic, tracks_dics, playlists_dics_and_indexes)

        open(self._itunessd_path, 'wb').write(bytes_data)


class Tracks(List):
    def __init__(self, shuffle, tracks_with_play_count_dics_zip=None):
        super().__init__()

        self._shuffle = shuffle
        tracks_with_play_count_dics_zip = tracks_with_play_count_dics_zip or []

        for dic, play_count_dic in tracks_with_play_count_dics_zip:
            self.append(Track(self, dic=dic, play_count_dic=play_count_dic))

    def get_dics(self):
        dics = []
        for track in self:
            dics.append(track.get_dic())
        return dics


class Track:
    def __init__(self, shuffle, sound=None, dic=None, play_count_dic=None):
        self._is_inited = False
        self._resetable_keys = []
        self._shuffle = shuffle

        self._dbid = dic['dbid']

        if dic and play_count_dic:
            self._dic = dic
            self._play_count_dic = play_count_dic
        elif sound:
            self.sound = sound
        else:
            raise Exception

        self._is_inited = True

    # def __setattr__(self, key, value):
    #    if self._is_inited and key not in self._resetable_keys:
    #        raise AttributeError
    #    else:
    #        self.__dict__[key] = value

    # def __getattr__(self, key):
    #   if key == 'type':
    #       return audio.get_type(self.shuffle.base_dir + '/' + self.filename)
    #   else:
    #       return self.__dict__[key]

    ###################################################

    @property
    def start_at_pos_ms(self):
        return self._dic['start_at_pos_ms']

    @start_at_pos_ms.setter
    def start_at_pos_ms(self, value):
        self._dic['start_at_pos_ms'] = value

    ###################################################

    @property
    def stop_at_pos_ms(self):
        return self._dic['stop_at_pos_ms']

    @stop_at_pos_ms.setter
    def stop_at_pos_ms(self, value):
        self._dic['stop_at_pos_ms'] = value

    @property
    def volume_gain(self):
        return self._dic['volume_gain']

    @volume_gain.setter
    def volume_gain(self, value):
        self._dic['volume_gain'] = value

    @property
    def type(self):
        return self._dic['type']

    @type.setter
    def type(self, value):
        self._dic['type'] = value

    @property
    def filename(self):
        return self._dic['filename']

    @property
    def dont_skip_on_shuffle(self):
        return self._dic['dont_skip_on_shuffle']

    @dont_skip_on_shuffle.setter
    def dont_skip_on_shuffle(self, value):
        self._dic['dont_skip_on_shuffle'] = value

    @property
    def remember_playing_pos(self):
        return self._dic['remember_playing_pos']

    @remember_playing_pos.setter
    def remember_playing_pos(self, value):
        self._dic['remember_playing_pos'] = value

    @property
    def part_of_uninterruptable_album(self):
        return self._dic['part_of_uninterruptable_album']

    @part_of_uninterruptable_album.setter
    def part_of_uninterruptable_album(self, value):
        self._dic['part_of_uninterruptable_album'] = value

    @property
    def pregap(self):
        return self._dic['pregap']

    @pregap.setter
    def pregap(self, value):
        self._dic['pregap'] = value

    @property
    def postgap(self):
        return self._dic['postgap']

    @postgap.setter
    def postgap(self, value):
        self._dic['postgap'] = value

    @property
    def number_of_sampless(self):
        return self._dic['number_of_sampless']

    @number_of_sampless.setter
    def number_of_sampless(self, value):
        self._dic['number_of_sampless'] = value

    @property
    def gapless_data(self):
        return self._dic['gapless_data']

    @gapless_data.setter
    def gapless_data(self, value):
        self._dic['gapless_data'] = value

    @property
    def album_id(self):
        return self._dic['album_id']

    @album_id.setter
    def album_id(self, value):
        self._dic['album_id'] = value

    @property
    def track_number(self):
        return self._dic['track_number']

    @track_number.setter
    def track_number(self, value):
        self._dic['track_number'] = value

    @property
    def disc_number(self):
        return self._dic['disc_number']

    @disc_number.setter
    def disc_number(self, value):
        self._dic['disc_number'] = value

    @property
    def dbid(self):
        return self._dic['dbid']

    @dbid.setter
    def dbid(self, value):
        self._dic['dbid'] = value

    @property
    def artist_id(self):
        return self._dic['artist_id']

    @artist_id.setter
    def artist_id(self, value):
        self._dic['artist_id'] = value

    # ======================================================

    @property
    def bookmark_time(self):
        return self._play_count_dic['bookmark_time']

    @bookmark_time.setter
    def bookmark_time(self, value):
        self._play_count_dic['bookmark_time'] = value

    @property
    def play_count(self):
        return self._play_count_dic['play_count']

    @play_count.setter
    def play_count(self, value):
        self._play_count_dic['play_count'] = value

    @property
    def time_of_last_play(self):
        return self._play_count_dic['time_of_last_play']

    @time_of_last_play.setter
    def time_of_last_play(self, value):
        self._play_count_dic['time_of_last_play'] = value

    @property
    def skip_count(self):
        return self._play_count_dic['skip_count']

    @skip_count.setter
    def skip_count(self, value):
        self._play_count_dic['skip_count'] = value

    @property
    def time_of_last_skip(self):
        return self._play_count_dic['time_of_last_skip']

    @time_of_last_skip.setter
    def time_of_last_skip(self, value):
        self._play_count_dic['time_of_last_skip'] = value

    ########################################################
    def get_dics(self):
        return self._dic, self._play_count_dic


class Playlists(List):
    def __init__(self, shuffle, lphs_dics_indexes=None):
        super().__init__()
        self._shuffle = shuffle

        lphs_dics_indexes = lphs_dics_indexes or []
        for lphs_dic, indexes in lphs_dics_indexes:
            self.append(Playlist(shuffle, lphs_dic, indexes))

    def get_dics_and_indexes(self):
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

    @property
    def type(self):
        return self._dic['type']

    @type.setter
    def type(self, value):
        self._dic['type'] = value

    @property
    def dbid(self):
        return self._dic['dbid']

    def get_dic_indexes(self):
        return self._dic, (self._shuffle.tracks.index(track) for track in self)


class Sounds:
    def __init__(self, shuffle, logs_path, stored_dir):
        self._shuffle = shuffle

        self._logs_path = logs_path
        self._stored_dir = stored_dir
        try:
            self._logs = json.loads(open(self._logs_path).read())
        except FileNotFoundError:
            self._logs = {}

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
        if not audio.get_type(path):
            raise TypeError('The type of this file is not supported.')

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
        try:
            self._logs = json.loads(open(self._logs_path).read())
        except FileNotFoundError:
            self._logs = {}

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
        if not audio.get_type(path) == audio.WAV:
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
