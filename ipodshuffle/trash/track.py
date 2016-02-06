#!/bin/env python3

import os

import mutagen

from shuffle import utils
from shuffle.trash import fields as f, utils
from shuffle.trash.shuffle_old import format_dbid


class Track:
    def __init__(self, shuffle, offset=None, filename=None, add_info=None):
        self._shuffle = shuffle
        self._data = {}
        if add_info:
            self._add_info = add_info

        if offset:
            data = self._shuffle.iTunesSD[offset:]
            dic = f.convert_dic(f.split_xxhs(data, f.rths_items), f.rths_items, to_bytes=False)
            if dic[f.header_id] != b'rths':
                raise()

            self._data = dic

        elif filename:
            if not utils.is_able_file(filename):
                raise ()

            a = os.path.splitext(filename)[1].lower()
            if a == 'mp3':
                self._data[f.filetype] = 1
            elif a in (".m4a", ".m4b", ".m4p", ".aa"):
                self._data[f.filetype] = 2
            elif a == 'wav':
                self._data[f.filetype] = 4

            self._data[f.filename] = filename
            self._data[f.dbid] = self._shuffle.get_new_dbid()
            self._data[f.stop_at_pos_ms] = int(mutagen.File(filename, easy=True).info.length * 1000)

        else:
            raise ()

    def __setattr__(self, key, value):
        if key in ('voice_string', 'voice_lang', 'original_name'):
            self._add_info[key] = value
        else:
            raise KeyError

    def __getattr__(self, key):

        if key in self._data.keys():
            return self._data[key]
        elif key in self._add_info.keys():
            return self._add_info[key]
        elif key == 'voiceover_file':
            return self._shuffle.base+'/Speakable/Tracks/'+format_dbid(self.dbid)+'.wav'
        else:
            raise ()

    def make_voiceover(self):
        utils.tts(self.voice_string, self.voice_lang, self.voiceover_file)

    def get_chunk(self):
        bytes_dic = f.convert_dic(self._data, f.rths_items, to_bytes=True)
        bytes_data = f.join_xxhs(bytes_dic, f.rths_items)
        return bytes_data

    def get_ext(self):
        return self._add_info
