"""
Shuffle for scritps writer,
"""
import os
import random
import string

# from hooky import List, Hook

from ipodshuffle.device.device import Shuffle as ShuffleDB
from ipodshuffle.device.device import Track as TrackDB
from ipodshuffle.device.device import MASTER, NORMAL, PODCAST, AUDIOBOOK

from ipodshuffle.filedb.filedb import VoiceOverDB

from ipodshuffle.filedb.log import Storage

from ipodshuffle.utils import get_checksum

from ipodshuffle import audio


from ipodshuffle.filedb.log import FileAlreadyInError

from collections import UserList as List

class AudioFileTypeError(Exception):
    pass


class Shuffle:
    def __init__(self, base, tts_fun=None):
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
                                           os.path.join(self.base, self._ctrl, 'audio'))

        self.__dict__['tracks_voicedb'] = \
            VoiceOverDB(log_path=os.path.join(self.base, self._ctrl, 'tracks_voices_log.json'),
                        stored_dir=os.path.join(self.base, self._ctrl, 'Speakable', 'Tracks'),
                        )

        self.__dict__['playlists_voicedb'] = \
            VoiceOverDB(log_path=os.path.join(self.base, self._ctrl, 'playlists_voices_log.json'),
                        stored_dir=os.path.join(self.base, self._ctrl, 'Speakable', 'Playlists'),
                        )

        self.__dict__['playlists'] = Playlists(shuffle=self)

        pl_map = {MASTER: Master, NORMAL: Normal, PODCAST:Podcast, AUDIOBOOK: Audiobook}
        for playlistdb in shuffledb.playlists:
            pl = pl_map[playlistdb.type](playlistdb, [shuffledb.tracks[i].copy() for i in playlistdb.indexes_of_tracks])
            self.__dict__['playlists'].appent(pl)


    def write_devicedb(self):
        shuffledb = ShuffleDB()

        shuffledb.enable_voiceover = self.enable_voiceover
        shuffledb.max_volume = self.max_volume

        for _pl in self.playlists:
            shuffledb.playlists.append(_pl.lldb)

            for track in _pl.tracks:
                if track.lldb not in shuffledb.tracks:
                    shuffledb.tracks.append(track.lldb)

                _pl.lldb.indexes_of_tracks.append(shuffledb.tracks.index(track.lldb))


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

    def tracks_from_checksum(self, checksum):
        pass

    def add_audio(self, src, checksum=None):
        self.audiodb.add(src, checksum)

    def get_audio_path(self, checksum):
        pass

    def get_tracks_by_checksum(self):
        pass

    def make_track(self, path_in_ipod=None, checksum=None):
        if bool(path_in_ipod) == bool(checksum):
            raise Exception

    @staticmethod
    def check_audio(path):
        if not audio.get_type(path):
            raise TypeError('The type of this file is not supported.')


class _Voice:
    def __init__(self, lldb, voicedb):
        self.lldb = lldb
        self._voicedb = voicedb

    @property
    def voice(self):
        dbid = self.lldb.dbid
        text, lang = self._voicedb.get_text_lang(dbid + '.wav')
        return text, lang

    @voice.setter
    def voice(self, value):
        if value is None:
            self.lldb.dbid= '0000000000000000'
            return

        text, lang = value
        dbid = self._voicedb.get_dbid(text, lang)
        self.lldb.dbid = dbid


class Track(_Voice):
    def __init__(self, shuffle, trackdb=None, path_in_ipod=None):

        self._shuffle = shuffle

        if not trackdb:
            trackdb = TrackDB('/' + path_in_ipod)

        super().__init__(trackdb, self._shuffle.tracks_voicedb)

    @property
    def path_in_ipod(self):
        return self.lldb.filename[0:]

###################################################################################
###################################################################################


class Playlists(List):
    def __init__(self, shuffle):
        super().__init__()
        self._shuffle = shuffle


###################################################################################

class _Playlist(_Voice):
    def __init__(self, shuffle, pldb):
        self._shuffle = shuffle
        super().__init__(pldb, self._shuffle.playlists_voicedb)

        self._shuffle = shuffle

        self.tracks = []

    def add_track(self, path_in_ipod):
        self.tracks.append(Track(self._shuffle, path_in_ipod=path_in_ipod))


class Master(_Playlist):
    def __init__(self, shuffle, pldb):
        super().__init__(shuffle, pldb)
        self.lldb.type = MASTER


class Normal(_Playlist):
    def __init__(self, shuffle, pldb):
        super().__init__(shuffle, pldb)
        self.lldb.type = NORMAL


class Podcast(_Playlist):
    def __init__(self, shuffle, pldb):
        super().__init__(shuffle, pldb)
        self.lldb.type = PODCAST


class Audiobook(_Playlist):
    def __init__(self, shuffle, pldb):
        super().__init__(shuffle, pldb)
        self.lldb.type = AUDIOBOOK


####################################################################################
####################################################################################

def get_random_name():
    return ''.join(random.sample(string.ascii_uppercase, 6))


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

        return self.get_path_in_ipod(checksum)
