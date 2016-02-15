"""
Shuffle should be
"""
import os

from ipodshuffle.device.device import OOwrapper as DeviceDB

from ipodshuffle.filedb.filedb import AudioDB, VoiceOverDB

from ipodshuffle.audio import get_type


class AudioFileTypeError(Exception):
    pass


class Shuffle:
    def __init__(self, base):
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

        self.db = DeviceDB(self._itunessd_chunk, self._itunesstats_chunk)

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

    def write_devicedb(self):
        itunessd_chunk, itunesstats_chunk = self.db.get_chunks()

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

    def get_path_in_ipod(self, path):

        realpath = os.path.realpath(path)
        path_in_pod = None
        if realpath[0:len(self.base)] == self.base:
            path_in_pod = realpath[len(self.base) + 1:]
        return path_in_pod

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

    def add_audio(self, path, checksum):
        audio_type = get_type(path)
        if not audio_type:
            raise AudioFileTypeError(audio_type)

        pass

    def get_tracks_by_checksum(self):

        pass


# ipod = Shuffle('/run/media/IPOD1')
# checksum = ipod.add_audio('xxx/xxx.mp3')
#
# for track in ipod.tracks_from_checksum(checksum)
#     if track.title !=

# ipod.add_voice(text='bye bye', lang='en-gb', default=track)
# pl.set_voice(text='bye bye', lang='en-gb')
#
