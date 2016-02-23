"""
Shuffle for scripts
"""
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

from ipodshuffle.storage.voice import VoiceOverDB

from ipodshuffle.storage.log import Storage

from ipodshuffle.utils import get_checksum

from ipodshuffle import audio


from ipodshuffle.storage.log import FileAlreadyInError


class AudioFileTypeError(Exception):
    pass


class Shuffle:
    def __init__(self, base, voice_path_func=None):
        self.base = os.path.realpath(os.path.normpath(base))
        self.voice_path_func = voice_path_func

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

        self.__dict__['tracks_voicedb'] = \
            VoiceOverDB(log_path=os.path.join(self.base, self._ctrl, 'tracks_voices_log.json'),
                        stored_dir=os.path.join(self.base, self._ctrl, 'Speakable', 'Tracks'),
                        )

        self.__dict__['playlists_voicedb'] = \
            VoiceOverDB(log_path=os.path.join(self.base, self._ctrl, 'playlists_voices_log.json'),
                        stored_dir=os.path.join(self.base, self._ctrl, 'Speakable', 'Playlists'),
                        )

        self.__dict__['playlists'] = _Playlists(shuffle=self)

        for playlistdb in shuffledb.playlists:

            pl = pl_type_class_map[playlistdb.type](self, playlistdb)

            for i in playlistdb.indexes_of_tracks:
                pl.tracks.append(Track(self, trackdb=copy.copy(shuffledb.tracks[i])))

            self.__dict__['playlists'].append(pl)

    def write(self):
        shuffledb = ShuffleDB()

        shuffledb.enable_voiceover = self.enable_voiceover
        shuffledb.max_volume = self.max_volume

        for playlist in self.playlists:

            pldb = copy.copy(playlist.lldb)
            pldb.type = [k for k, v in pl_type_class_map.items() if isinstance(playlist, v)][0]
            pldb.indexes_of_tracks.clear()

            shuffledb.playlists.append(pldb)

            for trdb in playlist.trackdbs():
                print('here', trdb.dbid)
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

    def path_in_ipod(self, path):
        realpath = os.path.realpath(path)
        path = None
        if realpath[0:len(self.base)] == self.base:
            path = realpath[len(self.base) + 1:]
        return path

    @property
    def playlists(self):
        return self.__dict__['playlists']

    @property
    def audiodb(self):
        return self.__dict__['audiodb']

    @property
    def tracks_voicedb(self):
        return self.__dict__['tracks_voicedb']

    @property
    def playlists_voicedb(self):
        return self.__dict__['playlists_voicedb']

    def create_track(self, path_in_ipod=None, checksum=None):
        if bool(path_in_ipod) == bool(checksum):
            raise Exception

        if not path_in_ipod:
            path_in_ipod = self.audiodb.get_filename(checksum)

        track = Track(self, path_in_ipod=path_in_ipod)

        return track

    def create_playlist(self, pl_type=None):
        pldb = PlaylistDB()
        pl = pl_type_class_map[pl_type](self, pldb)

        return pl

    @staticmethod
    def check_audio(path):
        if not audio.get_type(path):
            raise TypeError('The type of this file is not supported.')

######################################################################################


class _Voice:
    @abstractmethod
    def __init__(self, shuffle=None, lldb=None, voicedb=None):
        self._shuffle = shuffle
        self.lldb = lldb
        self._voicedb = voicedb

    @property
    def voice(self):
        dbid = self.lldb.dbid
        text, lang = self._voicedb.get_text_lang(dbid)
        return text, lang

    @voice.setter
    def voice(self, value):
        if value is None:
            self.lldb.dbid = '0000000000000000'
            return

        text, lang = value

        dbid = self._voicedb.get_dbid(text, lang)

        if not dbid and bool(self._shuffle.voice_path_func):

            self._voicedb.add(self._shuffle.voice_path_func(text=text, lang=lang), text=text, lang=lang)

            dbid = self._voicedb.get_dbid(text, lang)

        self.lldb.dbid = dbid

##################################################################################


class Track(_Voice):
    def __init__(self, shuffle, trackdb=None, path_in_ipod=None):
        # super().__init__()

        self._shuffle = shuffle

        if not trackdb:
            trackdb = TrackDB('/' + path_in_ipod)

            trackdb.type = audio.get_type(os.path.join(self._shuffle.base, path_in_ipod))

        super().__init__(shuffle, trackdb, self._shuffle.tracks_voicedb)

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


class _Playlist(_Voice):
    def __init__(self, shuffle, pldb=None):
        self._shuffle = shuffle
        if not pldb:
            pldb = PlaylistDB()

        super().__init__(shuffle, pldb, self._shuffle.playlists_voicedb)

        self._shuffle = shuffle

        self.__dict__['tracks'] = _Tracks(self._shuffle)

    @property
    def tracks(self):
        return self.__dict__['tracks']

    @abstractmethod
    def trackdbs(self):
        return [track.lldb for track in self.tracks]


class Master(_Playlist):
    def __init__(self, shuffle, pldb):
        super().__init__(shuffle, pldb)
        self.lldb.type = MASTER

    def trackdbs(self):
        return [track.lldb for track in self.tracks]


class Normal(_Playlist):
    def __init__(self, shuffle, pldb):
        super().__init__(shuffle, pldb)
        self.lldb.type = NORMAL

    def trackdbs(self):
        for track in self.tracks:
            track.lldb.dont_skip_on_shuffle = True
            track.lldb.remember_playing_pos = False

        return [track.lldb for track in self.tracks]


class Podcast(_Playlist):
    def __init__(self, shuffle, pldb):
        super().__init__(shuffle, pldb)
        self.lldb.type = PODCAST

    def trackdbs(self):
        for track in self.tracks:
            track.lldb.dont_skip_on_shuffle = False
            track.lldb.remember_playing_pos = True

        return [track.lldb for track in self.tracks]


class Audiobook(_Playlist):
    def __init__(self, shuffle, pldb):
        super().__init__(shuffle, pldb)
        self.lldb.type = AUDIOBOOK

    def trackdbs(self):
        for track in self.tracks:
            track.lldb.dont_skip_on_shuffle = False
            track.lldb.remember_playing_pos = True

        return [track.lldb for track in self.tracks]


pl_type_class_map = {
    MASTER: Master,
    NORMAL: Normal,
    PODCAST: Podcast,
    AUDIOBOOK: Audiobook
}

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

    def add(self, src, checksum=None):
        if not audio.get_type(src):
            raise TypeError('The type of this file is not supported.')
        checksum = checksum or get_checksum(src)

        try:
            super().add(src, checksum)
        except FileAlreadyInError:
            pass
