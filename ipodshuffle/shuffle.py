
import os
import random
import string

import copy

from abc import abstractmethod

from collections import UserList as List

# from hooky import List, Hook

from ipodshuffle.db import Shuffle as ShuffleDB
from ipodshuffle.db import Playlist as PlaylistDB
from ipodshuffle.db import Track as TrackDB
from ipodshuffle.db import MASTER, NORMAL, PODCAST, AUDIOBOOK

from ipodshuffle.storage.voice import VoiceDB

from ipodshuffle.storage.log import Storage

from ipodshuffle import audio


class AudioFileTypeError(Exception):
    pass


class Shuffle:
    def __init__(self, base):
        """
        :param base: iPod base path
        """
        self.base = os.path.realpath(os.path.normpath(base))

        self._ctrl = 'iPod_Control'

        self._itunessd_path = self.base + '/' + self._ctrl + '/iTunes/iTunesSD'
        self._itunesstats_path = self.base + '/' + self._ctrl + '/iTunes/iTunesStats'

        self._itunessd_chunk = None
        self._itunesstats_chunk = None

        if os.path.exists(self._itunessd_path):
            self._itunessd_chunk = open(self._itunessd_path, 'rb').read()

            if os.path.exists(self._itunesstats_path):
                self._itunesstats_chunk = open(self._itunesstats_path, 'rb').read()

        shuffledb = ShuffleDB(self._itunessd_chunk, self._itunesstats_chunk)

        self.enable_voiceover = shuffledb.enable_voiceover
        self.max_volume = shuffledb.max_volume

        self.__dict__['audiodb'] = AudioDB(self,
                                           os.path.join(self.base, self._ctrl, 'audio_log.json'),
                                           self.base)

        self.__dict__['tracks_voiceoverdb'] = \
            VoiceOverDB(log_path=os.path.join(self.base, self._ctrl, 'tracks_voices_log.json'),
                        stored_dir=os.path.join(self.base, self._ctrl, 'Speakable', 'Tracks'),
                        )

        self.__dict__['playlists_voiceoverdb'] = \
            VoiceOverDB(log_path=os.path.join(self.base, self._ctrl, 'playlists_voices_log.json'),
                        stored_dir=os.path.join(self.base, self._ctrl, 'Speakable', 'Playlists'),
                        )

        self.__dict__['playlists'] = _Playlists(shuffle=self)

        for pldb in shuffledb.playlists:

            pl = Playlist(self, playlistdb=pldb)

            for i in pldb.indexes_of_tracks:
                pl.tracks.append(Track(self, trackdb=copy.copy(shuffledb.tracks[i])))

            self.__dict__['playlists'].append(pl)

    def write_db(self):
        shuffledb = ShuffleDB()

        shuffledb.enable_voiceover = self.enable_voiceover
        shuffledb.max_volume = self.max_volume

        for playlist in self.playlists:

            pldb = copy.copy(playlist.lldb)
            pldb.type = playlist.type
            pldb.indexes_of_tracks.clear()

            shuffledb.playlists.append(pldb)

            for trdb in playlist.trackdbs():
                if not [_trackdb for _trackdb in shuffledb.tracks if _trackdb == trdb]:
                    shuffledb.tracks.append(trdb)

                pldb.indexes_of_tracks.append(shuffledb.tracks.index(trdb))

        itunessd_chunk, itunesstats_chunk = shuffledb.get_chunks()

        if self._itunessd_chunk != itunessd_chunk:
            os.makedirs(os.path.split(self._itunessd_path)[0], exist_ok=True)
            with open(self._itunessd_path, 'wb') as f:
                f.write(itunessd_chunk)
            self._itunessd_chunk = itunessd_chunk

        if self._itunesstats_chunk != itunesstats_chunk:
            os.makedirs(os.path.split(self._itunesstats_path)[0], exist_ok=True)
            with open(self._itunesstats_path, 'wb') as f:
                f.write(itunesstats_chunk)
            self._itunesstats_chunk = itunesstats_chunk

    @property
    def enable_voiceover(self):
        """
        boolean. enable or disable VoiceOver
        """
        return self.__dict__['enable_voiceover']

    @enable_voiceover.setter
    def enable_voiceover(self, value):
        if value in (True, False):
            self.__dict__['enable_voiceover'] = value
        else:
            raise TypeError('Must be a Boolean')

    @property
    def voice_path_func(self):
        """
        callable object or None. when set x.voice, will call it if it's Not None and enable_voiceover is True
        """
        return self.__dict__.setdefault('voice_path_func', None)

    @voice_path_func.setter
    def voice_path_func(self, value):
        if callable(value) or value is None:
            self.__dict__['voice_path_func'] = value
        else:
            raise ValueError('Must be a callable object or None')

    @property
    def max_volume(self):
        """
        integer. 0 do not limit, 3-20 is legal value to limit volume
        """
        return self.__dict__['max_volume']

    @max_volume.setter
    def max_volume(self, value):
        if value == 0 or 3 <= value <= 20:
            self.__dict__['max_volume'] = value
        else:
            raise ValueError('0, or 3 to 20')

    @property
    def playlists(self):
        """ list-like object, store all playlists
        """
        return self.__dict__['playlists']

    @property
    def audiodb(self):
        """
        store audio. if you don't want to copy file to ipod, you can use this

        is an instance of :class:`ipodshuffle.shuffle.AudioDB`
        """
        return self.__dict__['audiodb']

    @property
    def tracks_voiceoverdb(self):
        return self.__dict__['tracks_voiceoverdb']

    @property
    def playlists_voiceoverdb(self):
        return self.__dict__['playlists_voiceoverdb']

    def create_track(self, path_in_ipod=None, checksum=None):
        """
        :param path_in_ipod: the path of audio file in the iPod base
        :param checksum: CHECKSUM of the audio file in member audiodb
        :return: a new Track, you may want append it to the playlist.tracks
        """
        if bool(path_in_ipod) == bool(checksum):
            raise Exception

        if not path_in_ipod:
            path_in_ipod = self.audiodb.get_voice(checksum)

        track = Track(self, path_in_ipod=path_in_ipod)

        return track

    def create_playlist(self, pl_type=None):
        """
        :param pl_type: one in (MASTER, NORMAL, PODCAST, AUDIOBOOK)
        :return: a new PlayList, you may want append it to the playlists
        """

        pl = Playlist(self, playlist_type=pl_type)

        return pl

    @staticmethod
    def _check_audio(path):
        if not audio.get_type(path):
            raise TypeError('The type of this file is not supported.')

    def _path_in_ipod(self, path):
        realpath = os.path.realpath(path)
        path = None
        if realpath[0:len(self.base)] == self.base:
            path = realpath[len(self.base) + 1:]
        return path

######################################################################################


class _Voice:
    @abstractmethod
    def __init__(self, shuffle=None, lldb=None, voiceoverdb=None):
        self._shuffle = shuffle
        self.lldb = lldb
        self._voiceoverdb = voiceoverdb

    @property
    def voice(self):
        """tuple. contain text and lang code
        """
        dbid = self.lldb.dbid
        text, lang = self._voiceoverdb.get_text_lang(dbid)
        return text, lang

    @voice.setter
    def voice(self, value):
        if value is None:
            self.lldb.dbid = '0000000000000000'
            return

        text, lang = value

        dbid = self._voiceoverdb.get_dbid(text, lang)

        if dbid is None and self._shuffle.voice_path_func is not None:

            self._voiceoverdb.add_voice(self._shuffle.voice_path_func(text=text, lang=lang), text=text, lang=lang)

            dbid = self._voiceoverdb.get_dbid(text, lang)

        self.lldb.dbid = dbid

##################################################################################


class Track(_Voice):
    def __init__(self, shuffle, path_in_ipod=None, trackdb=None):

        self._shuffle = shuffle

        if not trackdb:
            trackdb = TrackDB('/' + path_in_ipod)

            trackdb.type = audio.get_type(os.path.join(self._shuffle.base, path_in_ipod))

        super().__init__(shuffle, trackdb, self._shuffle.tracks_voiceoverdb)

    @property
    def path_in_ipod(self):
        return self.lldb.filename[0:]

###################################################################################


class _Playlists(List):
    """
    for Shuffle.playlists
    """
    def __init__(self, shuffle):
        super().__init__()
        self._shuffle = shuffle

    def append_one(self, pl_type=None):
        pl = self._shuffle.create_playlist(pl_type)
        self.append(pl)
        return pl


class _Tracks(List):
    """
    for Playlist.tracks
    """
    def __init__(self, shuffle):
        super().__init__()
        self._shuffle = shuffle

    def append_one(self, path_in_ipod=None, checksum=None):
        track = self._shuffle.create_track(path_in_ipod, checksum)
        self.append(track)
        return track

###################################################################################


class Playlist(_Voice):
    def __init__(self, shuffle, playlist_type=None, playlistdb=None):
        if bool(playlist_type) == bool(playlistdb):
            raise Exception

        self._shuffle = shuffle
        if not playlistdb:
            playlistdb = PlaylistDB()
        else:
            playlist_type = playlistdb.type

        super().__init__(shuffle, playlistdb, self._shuffle.playlists_voiceoverdb)

        self._shuffle = shuffle
        self.__dict__['type'] = playlist_type

        self.__dict__['tracks'] = _Tracks(self._shuffle)

    @property
    def type(self):
        """
        MASTER, NORMAL, PODCAST or AUDIOBOOK. Can not change
        """
        return self.__dict__['type']

    @property
    def tracks(self):
        """
        list-like, store all tracks of this playlist
        """
        return self.__dict__['tracks']

    def trackdbs(self):
        if self.type == MASTER:
            self._do_master()
        elif self.type == NORMAL:
            self._do_normal()
        elif self.type == PODCAST:
            self._do_podcast()
        elif self.type == AUDIOBOOK:
            self._do_audiobook()

        return [track.lldb for track in self.tracks]

    def _do_master(self):
        pass

    def _do_normal(self):
        for track in self.tracks:
            track.lldb.dont_skip_on_shuffle = True
            track.lldb.remember_playing_pos = False

    def _do_podcast(self):
        for track in self.tracks:
            track.lldb.dont_skip_on_shuffle = False
            track.lldb.remember_playing_pos = True

    def _do_audiobook(self):
        for track in self.tracks:
            track.lldb.dont_skip_on_shuffle = False
            track.lldb.remember_playing_pos = True


####################################################################################
####################################################################################


def get_random_name():
    return 'iPod_Control/audio/' + ''.join(random.sample(string.ascii_uppercase, 6))


def get_ipodlike_random_name():
    """
    :return: F0[1-3]/XXXX.[mp3|m4a|m4b|...]
    """


class AudioDB(Storage):
    def __init__(self, shuffle, log_path, storage_dir):
        super().__init__(log_path, storage_dir, random_name_fun=get_random_name)
        self._shuffle = shuffle

        self.storage_dir = storage_dir

    def add(self, src):
        """ store an audio file to storage dir

        :param src: audio file path
        :return: checksum value
        """
        if not audio.get_type(src):
            raise TypeError('The type of this file is not supported.')

        return super().add(src)


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
        filename = self.get_voice(text, lang)
        if filename:
            dbid = os.path.splitext(filename)[0]

        return dbid

    def get_text_lang(self, dbid):
        text = None
        lang = None
        filename = dbid + '.wav'
        if filename in self.get_filenames():
            extra = self.get_extra(dbid + '.wav')
            text, lang = extra['text'], extra['lang']
        return text, lang


class SystemVoice:
    pass


class MassagesVoice:
    pass
