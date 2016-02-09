import os
import json
import hashlib
import random
import string
import shutil

from abc import abstractmethod

from . import itunessd, itunesstats, audio, tools

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
    return os.path.getmtime(path), os.path.getsize(path)


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
        self.ctrl_folder = 'iPod_Control'

        self._itunessd_path = self.base + '/' + self.ctrl_folder + '/iTunes/iTunesSD'
        self._itunesstats_path = self.base + '/' + self.ctrl_folder + '/iTunes/iTunesStats'

        self._dic = {}

        def read(path, fun):
            if os.path.exists(path):
                if os.path.isfile(path):
                    chunk = open(path, 'rb').read()
                    return fun(chunk)
                else:
                    raise Exception

        if os.path.exists(self._itunessd_path):
            header_dic, tracks_dics, playlists_dics_and_indexes = read(self._itunessd_path, itunessd.itunessd_to_dics)

            tracks_play_count_dics = []
            if os.path.exists(self._itunesstats_path):
                tracks_play_count_dics = read(self._itunesstats_path, itunesstats.itunesstats_to_dics)

            if len(tracks_dics) != len(tracks_play_count_dics):
                tracks_play_count_dics = [None] * len(tracks_dics)

            tracks_with_play_count_dics_zip = zip(tracks_dics, tracks_play_count_dics)

            self._dic = header_dic

            self.__dict__['tracks'] = Tracks(self, tracks_with_play_count_dics_zip)

            self.__dict__['playlists'] = Playlists(self, playlists_dics_and_indexes)

        else:
            self.enable_voiceover = 0
            self.max_volume = 0
            self.__dict__['tracks'] = Tracks(self)
            self.__dict__['playlists'] = Playlists(self)

        self.__dict__['sounds'] = SoundsDB(self,
                                           logs_path=os.path.join(self.base, self.ctrl_folder, 'sounds_logs.json'),
                                           stored_dir=os.path.join(self.base, self.ctrl_folder, 'sounds'))

        self.__dict__['tracks_voicedb'] = \
            IpodVoice(logs_path=os.path.join(self.base, self.ctrl_folder, 'tracks_voice_logs.json'),
                      stored_dir=os.path.join(self.base, self.ctrl_folder, 'Speakable', 'Tracks'),
                      users=self.tracks)

        self.__dict__['playlists_voicedb'] = \
            IpodVoice(logs_path=os.path.join(self.base, self.ctrl_folder, 'playlists_voice_logs.json'),
                      stored_dir=os.path.join(self.base, self.ctrl_folder, 'Speakable', 'Playlists'),
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

        itunessd_chunk = itunessd.dics_to_itunessd(db_dic, tracks_dics, playlists_dics_and_indexes)

        os.makedirs(os.path.split(self._itunessd_path)[0], exist_ok=True)
        with open(self._itunessd_path, 'wb') as f:
            f.write(itunessd_chunk)

    def get_path_in_ipod(self, path):

        path_in_pod = None
        if path[0:len(self.base)] == self.base:
            path_in_pod = path[len(self.base)+1:]

        return path_in_pod


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

    def add(self):
        pl = Playlist(self._shuffle)
        return pl


class Playlist(List):
    def __init__(self, shuffle, dic=None, indexes_of_tracks=None):
        super().__init__()
        self._shuffle = shuffle
        self._dic = dic or {}

        self.__dict__['tracks'] = []

        indexes_of_tracks = indexes_of_tracks or []

        for index in indexes_of_tracks:
            self.tracks.append(shuffle.tracks[index])

    @property
    def type(self):
        return self._dic['type']

    @type.setter
    def type(self, value):
        self._dic['type'] = value

    @property
    def dbid(self):
        return self._dic['dbid']

    @property
    def tracks(self):
        return self.__dict__['tracks']

    def get_dic_indexes(self):
        return self._dic, (self._shuffle.tracks.index(track) for track in self)


class JsonLog:
    def __init__(self, logs_path):
        self._logs_path = logs_path

        self._original_logs_str = '{}'
        self._logs = {}
        os.makedirs(os.path.split(self._logs_path)[0], exist_ok=True)
        try:
            with open(self._logs_path) as f:
                self._original_logs_str = f.read()
        except FileNotFoundError:
            pass
        self._logs = json.loads(self._original_logs_str)

    def write_logs(self):
        new_logs_str = json.dumps(self._logs, sort_keys=True, indent=4)
        if new_logs_str != self._original_logs_str:
            open(self._logs_path, 'w').write(new_logs_str)
            self._original_logs_str = new_logs_str


class SoundsDB(JsonLog):
    def __init__(self, shuffle, logs_path, stored_dir):
        super().__init__(logs_path)

        self._shuffle = shuffle

        self._stored_dir = stored_dir

    def del_not_exists(self):
        no_exists_files = []
        for path_in_ipod, metadata in self._logs.items():
            full_path = self._shuffle.base + '/' + path_in_ipod
            if not os.path.exists(full_path) or not os.path.isfile(full_path):
                no_exists_files.append(path_in_ipod)

        for path in no_exists_files:
            del self._logs[path]

    def updata_changed(self):
        changed_logs = {}
        for path_in_ipod, metadata in self._logs.items():
            path_in_os = self._shuffle.base + '/' + path_in_ipod

            if os.path.getsize(path_in_os) != metadata['size'] or os.path.getmtime(path_in_os) != metadata['mtime']:
                changed_logs[path_in_ipod] = {
                    'mtime': os.path.getmtime(path_in_os),
                    'size': os.path.getsize(path_in_os),
                    'checksum': get_checksum(path_in_os)
                }

        self._logs.update(changed_logs)

    def update_from_tracks(self):
        not_log_tracks_filenames = []
        for track in self._shuffle.tracks:
            if track.filename[1:] not in self._logs.keys():
                not_log_tracks_filenames.append(track.filename[1:])

        tracks_logs_notinlogs = {}
        for path_in_ipod in not_log_tracks_filenames:
            path_in_os = self._shuffle.base + '/' + path_in_ipod
            tracks_logs_notinlogs[path_in_ipod] = {
                    'mtime': os.path.getmtime(path_in_os),
                    'size': os.path.getsize(path_in_os),
                    'checksum': get_checksum(path_in_os)
                }
        self._logs.update(tracks_logs_notinlogs)

    def updata_from_stored_dir(self):
        for file in [file for file in tools.get_all_files(self._stored_dir) if audio.get_type(file)]:
            if self._shuffle.get_path_in_ipod(file) not in self._logs.keys():
                self.add(file)

    def rebuilt_logs_from_stored_dir(self):
        pass

    def remove_not_in_logs_files(self):
        pass

    def clean_logs(self):
        self.del_not_exists()
        self.updata_changed()
        self.update_from_tracks()

        self.updata_from_stored_dir()

        self.write_logs()

    def filelist(self):
        return tuple(self._logs.keys())

    def get(self, checksum):
        path = None
        for key, info in self._logs.items():
            if info['checksum'] == checksum:
                path = key
                break
        return path

    def add(self, path, checksum=None):
        if not audio.get_type(path):
            raise TypeError('The type of this file is not supported.')

        checksum = checksum or get_checksum(path)

        path_in_ipod = None

        path_in_ipod_but_not_in_logs = self._shuffle.get_path_in_ipod(path)

        if path_in_ipod_but_not_in_logs:
            path_in_ipod = path_in_ipod_but_not_in_logs

            self._logs[path_in_ipod] = {
                'checksum': checksum,
                'mtime': os.path.getmtime(path),
                'size': os.path.getsize(path)
            }

        for PATH, metadata in self._logs.items():
            if metadata['checksum'] == checksum:
                path_in_ipod = PATH
                break

        if not path_in_ipod:  # Mean this file is not in ipod.

            target_path = None

            # 1. get random filename which not use.
            while True:
                # at most 65533 files in one folder
                target_path = os.path.join(self._stored_dir, ''.join(random.sample(string.ascii_uppercase, 6)))

                path_in_ipod = self._shuffle.get_path_in_ipod(target_path)

                if not os.path.exists(target_path) and path_in_ipod not in self._logs.keys():
                    break

            # 2. copy file
            # target_path = self._shuffle.base_dir + '/' + path_in_ipod
            os.makedirs(os.path.split(target_path)[0], exist_ok=True)
            shutil.copyfile(path, target_path)

            # 3. update logs
            self._logs[path_in_ipod] = {
                'checksum': checksum,
                'mtime': os.path.getmtime(target_path),
                'size': os.path.getsize(target_path)
            }

        self.write_logs()

        return path_in_ipod

    def remove(self, path):
        os.remove(self._shuffle.base_dir + '/' + path)
        del self._shuffle.sounds_logs[path]


class Voicedb(JsonLog):
    def __init__(self, logs_path, stored_dir):
        super().__init__(logs_path)

        self._stored_dir = stored_dir

        self._ramdom_name = get_dbid2

    def _fullpath(self, filename):
        return os.path.join(self._stored_dir, filename)

    @abstractmethod
    def get_random_name(self):
        pass

    def del_wrong_logs(self):
        pass
        dbids_to_del = []
        for filename, info in self._logs.items():
            voice_path = self._fullpath(filename)
            if info['mtime'] != os.path.getmtime(voice_path) or info['size'] != os.path.getsize(voice_path):
                dbids_to_del.append(filename)

        for dbid in dbids_to_del:
            del self._logs[dbid]

    def clean(self):
        pass

    def get_new_filename(self):
        file_name = None
        while True:
            file_name = self._ramdom_name()
            if file_name not in self._logs.keys() and not os.path.exists(self._fullpath(file_name)):
                break
        return file_name

    def add(self, path, text, lang, checksum=None, user_defined=None):
        if not audio.get_type(path) == audio.WAV:
            raise TypeError

        checksum = checksum or get_checksum(path)

        for file_in_dir, info in self._logs.items():
            if info['checksum'] == checksum:
                raise FileExistsError

        filename = self.get_new_filename() + '.wav'
        shutil.copyfile(path, self._stored_dir + '/' + filename)

        self._logs[filename] = {
            'text': text,
            'lang': lang,
            'checksum': checksum,
            'mtime': os.path.getmtime(filename),
            'size': os.path.getsize(filename),
            'user_defined': user_defined
        }

        self.write_logs()

        return filename

    def get_filename_by_text_lang(self, text, lang):
        filename = None
        for _filename, info in self._logs.items():
            if info['text'] == text and lang == lang:
                filename = _filename
        return filename

    def get_filename_by_checksum(self, checksum):
        filename = None
        for _filename, info in self._logs.items():
            if info['checksum'] == checksum:
                filename = _filename
        return filename

    def remove(self, filename):
        os.remove(self._stored_dir + '/' + filename)
        del self._logs[filename]


class IpodVoice(Voicedb):
    def __init__(self, logs_path, stored_dir, users):
        super().__init__(logs_path, stored_dir)
        self._users = users

    def get_random_name(self):
        return get_dbid2()

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
        self.del_wrong_logs()
        self.clean_store_dir()

    def get_dbid(self, text=None, lang=None, checksum=None):
        if text and lang:
            return os.path.splitext(self.get_filename_by_text_lang(text, lang))[0]
        elif checksum:
            return os.path.splitext(self.get_filename_by_checksum(checksum))[0]
        else:
            raise Exception


class SystemVoice:
    pass


class MassagesVoice:
    pass
