
from . import itunessd, itunesstats

from collections import UserList as List

from .itunessd import MASTER, NORMAL, PODCAST, AUDIOBOOK


"""
Class Shuffle, Playlists, playlist, Tracks, Track, is more like wrapper of iTunesSD and iTunesStats,
should use AudioDB and VoiceDB to store audio and tts voice files.
"""

PL_MAP = {
    MASTER: 'MASTER',
    NORMAL: 'NORMAL',
    PODCAST: 'PODCAST',
    AUDIOBOOK: 'AUDIOBOOK'
}


class Shuffle:
    def __init__(self, itunessd_chunk=None, itunesstats_chunk=None):

        self._dic = {}

        if itunessd_chunk and itunesstats_chunk:

                header_dic, tracks_dics, playlists_dics_and_indexes = itunessd.itunessd_to_dics(itunessd_chunk)
                tracks_play_count_dics = itunesstats.itunesstats_to_dics(itunesstats_chunk)

                self._dic = header_dic

                self.__dict__['tracks'] = Tracks(tracks_dics, tracks_play_count_dics)
                self.__dict__['playlists'] = Playlists(playlists_dics_and_indexes)

        else:
            self.enable_voiceover = False
            self.max_volume = 0

            self.__dict__['tracks'] = Tracks()
            self.__dict__['playlists'] = Playlists()

    def get_chunks(self):

        db_dic = self._dic.copy()

        tracks_dics, tracks_play_count_dics = self.tracks.tracks_dics_and_tracks_play_count_dics()
        playlists_dics_and_indexes = self.playlists.get_dics_and_indexes()

        itunessd_chunk = itunessd.dics_to_itunessd(db_dic, tracks_dics, playlists_dics_and_indexes)
        itunesstats_chunk = itunesstats.dics_to_itunesstats(tracks_play_count_dics)

        return itunessd_chunk, itunesstats_chunk

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


class Tracks(List):
    """ this should be db.tracks not db.playaylist.tracks
    """
    def __init__(self, tracks_dics=None, tracks_play_count_dics=None):
        super().__init__()

        tracks_with_play_count_dics_zip = []

        if tracks_dics:
            tracks_play_count_dics = tracks_play_count_dics or []
            if len(tracks_dics) != len(tracks_play_count_dics):
                tracks_play_count_dics = [None] * len(tracks_dics)

            tracks_with_play_count_dics_zip = zip(tracks_dics, tracks_play_count_dics)

        for dic, count_dic in tracks_with_play_count_dics_zip:
            self.append(Track(dic=dic, count_dic=count_dic))

    # def add(self, path_in_ipod):
    #    # if path_in_ipod not in self._shuffle.sounds:
    #    #    raise Exception

    #    track = Track(self._shuffle, path_in_ipod)
    #    self.append(track)
    #    return track

    def tracks_dics_and_tracks_play_count_dics(self):

        tracks_dics = []
        play_count_dics = []

        for track in self:
            dic, play_count_dic = track.get_dics()
            tracks_dics.append(dic)
            play_count_dics.append(play_count_dic)

        return tracks_dics, play_count_dics


class Track:
    def __init__(self, path_in_ipod=None, dic=None, count_dic=None):

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
            self._dic['filename'] = path_in_ipod
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

    # @property
    # def fullpath(self):
    #    return self._shuffle.base + self.filename

    # @property
    # def path_in_ipod(self):
    #    return self.filename[1:]
    ###################################################
    ###################################################

    @property
    def start_at_pos_ms(self):
        return self._dic['start_at_pos_ms']

    @start_at_pos_ms.setter
    def start_at_pos_ms(self, value):
        self._dic['start_at_pos_ms'] = value

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
    ########################################################

    def __eq__(self, other):
        if isinstance(other, self.__class__) and self.get_dics() == other.get_dics():
            return True
        else:
            return False

    ########################################################
    ########################################################

    def get_dics(self):
        return self._dic, self._count_dic


class Playlists(List):
    def __init__(self, lphs_dics_indexes=None):
        super().__init__()

        lphs_dics_indexes = lphs_dics_indexes or []
        for lphs_dic, indexes in lphs_dics_indexes:
            self.append(Playlist(lphs_dic, indexes))

    def get_dics_and_indexes(self):
        dic_indexes_s = []
        for playlist in self:
            dic_indexes_s.append(playlist.get_dic_indexes())

        return dic_indexes_s


class Playlist:
    def __init__(self, dic=None, indexes_of_tracks=None):
        super().__init__()

        self.__dict__['tracks'] = []

        self._dic = dic or {}

        if not self._dic:
            self.dbid = '0000000000000000'

        self.__dict__['indexes_of_tracks'] = indexes_of_tracks or []

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

    #####################################################################
    @property
    def indexes_of_tracks(self):
        return self.__dict__['indexes_of_tracks']

    def get_dic_indexes(self):
        return self._dic, self.indexes_of_tracks
