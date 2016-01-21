import os
import copy

from .shuffle_old import format_dbid
from . import fields as f
from . import utils
from .track import Track


class Playlist:
    def __init__(self, shuffle, offset=None, add_info=None):
        self._shuffle = shuffle
        self._tracks = []
        self._data = {}

        if add_info is not None:
            self._add_info = add_info

        if offset:
            data = self._shuffle.iTunesSD[offset:]

            dic = f.convert_dic(f.split_xxhs(data, f.lphs_items), f.lphs_items, to_bytes=False)

            self._data = dic

            for index_of_tracks_bytes in utils.split_by_step(data[f.lphs_items_size:self._data[f.total_length]], 4):
                self._tracks.append(self._shuffle.get_all_tracks()[utils.ifb(index_of_tracks_bytes)])

        else:
            self._data[f.dbid] = self._shuffle.get_new_dbid()

    def __setattr__(self, key, value):
        if key == 'type':

            self._data[key] = value

    def __getattr__(self, key):
            if key == 'voiceover_file':
                return self._shuffle.pl_speakable_dir+os.sep+format_dbid(self.dbid)+'.wav'
            else:
                return self._data[key]

    def make_voiceover(self):
        utils.tts(self.voice_string, self.voice_lang, self.voiceover_file)

    def get_all_tracks(self):
        return copy.copy(self._tracks)

    def add_track(self, track):
        """Put a Track into playlist, Track must be a Class Track"""
        if not isinstance(track, Track):
            raise ()

        if track not in self._shuffle.get_all_tracks():
            self._tracks.append(track)

    def del_track(self, track):
        """Delete a Track from this playlist.
        You should use Shuffle.del_track() if you want to delete a Track and it's sound file from your iPod Shuffle
        """

        self._tracks.remove(track)

    def get_chunk2(self):
        self._data[f.total_length] = f.lphs_items_size + len(self._tracks) * 4
        self._data[f.number_of_all_sound]

    def get_chunk(self):
        """Return a Bytes can be use to write to iTunesSD in iPod Shuffle"""

        data = bytes()
        place_to_insert_total_length = None
        total_length_size = None

        for one in f.lphs_items:
            if f.K_DEFAULT in one.keys():
                data += one[f.K_DEFAULT]

            elif one[f.K_NAME] is f.total_length:
                total_length_size = one[f.K_SIZE]
                place_to_insert_total_length = len(data)

            elif one[f.K_NAME] is f.number_of_all_sound or f.number_of_normal_sound:
                data += utils.itb(len(self._tracks), one[f.K_SIZE])

            elif one[f.K_NAME] is f.dbid:
                data += self._data[f.dbid].encode()

            else:
                data += b'\00' * one[f.K_SIZE]

        data = data[:place_to_insert_total_length] +\
            utils.itb(len(data) + total_length_size, total_length_size) +\
            data[place_to_insert_total_length:]

        return data

    def get_add_info(self):
        return self._add_info