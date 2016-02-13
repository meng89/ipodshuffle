import os
import random
import string

from . import itunessd, itunesstats, audio

from .utils import get_checksum

from .log import VoiceDB, Storage, FileAlreadyInError

from collections import UserList as List

from .itunessd import ChunkError, MASTER, NORMAL, PODCAST, AUDIOBOOK

PL_MAP = {
    MASTER: 'MASTER',
    NORMAL: 'NORMAL',
    PODCAST: 'PODCAST',
    AUDIOBOOK: 'AUDIOBOOK'
}


def make_dbid1():
    return ''.join(random.sample('ABCDEF' + string.digits, 16))


def make_dbid2():
    dbid_string = ''
    for x in random.sample(range(0, 255), 8):
        s = hex(x)[2:]
        if len(s) == 1:
            s = '0' + s
        dbid_string += s.upper()
    return dbid_string

make_dbid = make_dbid2


def make_dbid_name():
    return make_dbid() + '.wav'


class Shuffle:
    def __init__(self, directory):
        self.base = os.path.realpath(os.path.normpath(directory))
        self.ctrl_folder = 'iPod_Control'

        self._itunessd_path = self.base + '/' + self.ctrl_folder + '/iTunes/iTunesSD'
        self._itunesstats_path = self.base + '/' + self.ctrl_folder + '/iTunes/iTunesStats'

        self._itunessd_chunk = b''
        self._itunesstats_chunk = b''

        self._dic = {}

        try:
            if os.path.exists(self._itunessd_path):
                self._itunessd_chunk = open(self._itunessd_path, 'rb').read()

            header_dic, tracks_dics, playlists_dics_and_indexes = itunessd.itunessd_to_dics(self._itunessd_chunk)

            tracks_play_count_dics = []

            if os.path.exists(self._itunesstats_path):
                self._itunesstats_chunk = open(self._itunesstats_path, 'rb').read()
                tracks_play_count_dics = itunesstats.itunesstats_to_dics(self._itunesstats_chunk)

            else:
                pass

            self._dic = header_dic
            self.__dict__['tracks'] = Tracks(self, tracks_dics, tracks_play_count_dics)
            self.__dict__['playlists'] = Playlists(self, playlists_dics_and_indexes)

        except ChunkError:

            print('iTunesSD is wrong, start as empty now!')

            self.enable_voiceover = True
            self.max_volume = 12
            self.__dict__['tracks'] = Tracks(self)
            self.__dict__['playlists'] = Playlists(self)

        self.__dict__['sounds'] = SoundDB(self,
                                          os.path.join(self.base, self.ctrl_folder, 'sounds_log.json'),
                                          os.path.join(self.base, self.ctrl_folder, 'sounds'))

        self.__dict__['tracks_voicedb'] = \
            VoiceOverDB(log_path=os.path.join(self.base, self.ctrl_folder, 'tracks_voices_log.json'),
                        stored_dir=os.path.join(self.base, self.ctrl_folder, 'Speakable', 'Tracks'),
                        users=self.tracks)

        self.__dict__['playlists_voicedb'] = \
            VoiceOverDB(log_path=os.path.join(self.base, self.ctrl_folder, 'playlists_voices_log.json'),
                        stored_dir=os.path.join(self.base, self.ctrl_folder, 'Speakable', 'Playlists'),
                        users=self.playlists)

    def write(self):
        db_dic = self._dic.copy()

        tracks_dics, tracks_play_count_dics = self.tracks.tracks_dics_and_tracks_play_count_dics()

        playlists_dics_and_indexes = self.playlists.get_dics_and_indexes()

        itunessd_chunk = itunessd.dics_to_itunessd(db_dic, tracks_dics, playlists_dics_and_indexes)
        itunesstats_chunk = itunesstats.dics_to_itunesstats(tracks_play_count_dics)

        os.makedirs(os.path.split(self._itunessd_path)[0], exist_ok=True)

        if self._itunessd_chunk != itunessd_chunk:
            with open(self._itunessd_path, 'wb') as f:
                f.write(itunessd_chunk)
            self._itunessd_chunk = itunessd_chunk

        if self._itunesstats_chunk != itunesstats_chunk:
            os.makedirs(os.path.split(self._itunesstats_path)[0], exist_ok=True)
            with open(self._itunesstats_path, 'wb') as f:
                f.write(itunesstats_chunk)
            self._itunesstats_chunk = itunesstats_chunk

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

    def get_path_in_ipod(self, realpath):

        path_in_pod = None
        if realpath[0:len(self.base)] == self.base:
            path_in_pod = realpath[len(self.base) + 1:]

        return path_in_pod


class Tracks(List):
    def __init__(self, shuffle, tracks_dics=None, tracks_play_count_dics=None):
        super().__init__()

        self._shuffle = shuffle

        tracks_with_play_count_dics_zip = []

        if tracks_dics:
            tracks_play_count_dics = tracks_play_count_dics or []
            if len(tracks_dics) != len(tracks_play_count_dics):
                tracks_play_count_dics = [None] * len(tracks_dics)

            tracks_with_play_count_dics_zip = zip(tracks_dics, tracks_play_count_dics)

        for dic, count_dic in tracks_with_play_count_dics_zip:
            self.append(Track(self._shuffle, dic=dic, count_dic=count_dic))

    def add(self, path_in_ipod):
        # if path_in_ipod not in self._shuffle.sounds:
        #    raise Exception

        track = Track(self._shuffle, path_in_ipod)
        self.append(track)
        return track

    def tracks_dics_and_tracks_play_count_dics(self):

        tracks_dics = []
        play_count_dics = []

        for track in self:
            dic, play_count_dic = track.get_dics()
            tracks_dics.append(dic)
            play_count_dics.append(play_count_dic)

        return tracks_dics, play_count_dics


class Track:
    def __init__(self, shuffle, path_in_ipod=None, dic=None, count_dic=None):
        self._shuffle = shuffle
        # self._dbid = dic['dbid']

        if count_dic:
            self._count_dic = count_dic
        else:
            self._count_dic = {}

            self.bookmark_time = 0
            self.play_count = 0
            self.skip_count = 0
            self.time_of_last_skip = 0
            self.time_of_last_play = 0

        if dic:
            self._dic = dic

        elif path_in_ipod:
            self._dic = {}

            self.start_at_pos_ms = 0
            self.stop_at_pos_ms = 0
            self.volume_gain = 0
            self._dic['filename'] = '/' + path_in_ipod
            self.dont_skip_on_shuffle = 0
            self.remember_playing_pos = 0
            self.part_of_uninterruptable_album = 0
            self.pregap = 0
            self.postgap = 0
            self.number_of_sampless = 0
            self.gapless_data = 0
            self.album_id = 0
            self.track_number = 0
            self.disc_number = 0
            self.dbid = '0000000000000000'
            self.artist_id = 0
        else:
            raise Exception

    @property
    def fullpath(self):
        return self._shuffle.base + self.filename

    @property
    def path_in_ipod(self):
        return self.filename[1:]
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
        return audio.get_type(self.fullpath)

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
        return self._count_dic['bookmark_time']

    @bookmark_time.setter
    def bookmark_time(self, value):
        self._count_dic['bookmark_time'] = value

    @property
    def play_count(self):
        return self._count_dic['play_count']

    @play_count.setter
    def play_count(self, value):
        self._count_dic['play_count'] = value

    @property
    def time_of_last_play(self):
        return self._count_dic['time_of_last_play']

    @time_of_last_play.setter
    def time_of_last_play(self, value):
        self._count_dic['time_of_last_play'] = value

    @property
    def skip_count(self):
        return self._count_dic['skip_count']

    @skip_count.setter
    def skip_count(self, value):
        self._count_dic['skip_count'] = value

    @property
    def time_of_last_skip(self):
        return self._count_dic['time_of_last_skip']

    @time_of_last_skip.setter
    def time_of_last_skip(self, value):
        self._count_dic['time_of_last_skip'] = value

    ########################################################
    def get_dics(self):
        self._dic['type'] = self.type
        return self._dic, self._count_dic


class Playlists(List):
    def __init__(self, shuffle, lphs_dics_indexes=None):
        super().__init__()
        self._shuffle = shuffle

        lphs_dics_indexes = lphs_dics_indexes or []
        for lphs_dic, indexes in lphs_dics_indexes:
            self.append(Playlist(shuffle, lphs_dic, indexes))

    def add(self):
        pl = Playlist(self._shuffle)
        self.append(pl)
        return pl

    def get_dics_and_indexes(self):
        dic_indexes_s = []
        for playlist in self:
            dic_indexes_s.append(playlist.get_dic_indexes())

        return dic_indexes_s


class Playlist:  # not list
    def __init__(self, shuffle, dic=None, indexes_of_tracks=None):
        super().__init__()
        self._shuffle = shuffle

        self.__dict__['tracks'] = []

        self._dic = dic or {}

        indexes_of_tracks = indexes_of_tracks or []

        if self._dic:
            for index in indexes_of_tracks:
                self.tracks.append(shuffle.tracks[index])
        else:
            self.dbid = '0000000000000000'

    @property
    def type(self):
        return self._dic['type']

    @type.setter
    def type(self, value):
        self._dic['type'] = value

    @property
    def dbid(self):
        return self._dic['dbid']

    @dbid.setter
    def dbid(self, value):
        self._dic['dbid'] = value

    @property
    def tracks(self):
        return self.__dict__['tracks']

    def get_dic_indexes(self):
        indexes = [self._shuffle.tracks.index(track) for track in self.tracks]
        return self._dic, indexes


def get_name():
    return ''.join(random.sample(string.ascii_uppercase, 6))


class SoundDB(Storage):
    def __init__(self, shuffle, log_path, storage_dir):
        super().__init__(log_path, storage_dir, random_name_fun=get_name)

        self._shuffle = shuffle

        self.storage_dir = storage_dir

    def add(self, src, checksum=None):
        if not audio.get_type(src):
            raise TypeError('The type of this file is not supported.')
        checksum = checksum or get_checksum(src)

        try:
            super().add(src, checksum)
        except FileAlreadyInError:
            pass

        return self.get_path_in_ipod(checksum)

    def get_path_in_ipod(self, checksum):
        path_in_ipod = None

        filename = self.get_filename(checksum)
        realpath = self.realpath(filename)
        if filename:
            path_in_ipod = self._shuffle.get_path_in_ipod(realpath)

        return path_in_ipod

    def remove(self, path):
        os.remove(self._shuffle.base_dir + '/' + path)
        del self._shuffle.sounds_logs[path]


class VoiceOverDB(VoiceDB):
    def __init__(self, log_path, stored_dir, users=None):
        super().__init__(log_path, stored_dir, random_name_fun=make_dbid_name)

        self._storage_dir = stored_dir
        self._users = users

    def remove_not_in_use(self):
        files_to_remove = []

        for filename in os.listdir(self._storage_dir):
            dbid, ext = os.path.splitext(filename)

            if filename not in self.get_filenames() and dbid not in [user.dbid for user in self._users]:
                files_to_remove.append(self.realpath(filename))

        for path in files_to_remove:
            if os.path.isfile(path):
                os.remove(path)
            else:
                os.removedirs(path)

    def get_dbid(self, text, lang):
        dbid = None
        filename = self.get_filename(text, lang)
        if filename:
            dbid = os.path.splitext(filename)[0]
        return dbid

    def get_text_lang(self, filename):
        extra = self._Store.get_extra(filename)
        text, lang = extra['text'], extra['lang']
        return text, lang


class SystemVoice:
    pass


class MassagesVoice:
    pass
