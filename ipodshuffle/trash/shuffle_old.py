#!/bin/env python3

import copy
import json
import os
import random
import shutil

from shuffle.trash import fields as f, utils
from shuffle.trash.playlist import Playlist
from shuffle.trash.track import Track


def format_dbid(dbid):
    return '{:X}'.format(dbid)


class FieldError(Exception):
    pass


class Shuffle:
    def __init__(self, directory):
        self.dir = directory
        self.tracks = []
        self.playlists = []

        itunessd_name = 'iTunesSD'
        ipod_control_dir_name = 'iPod_Control'
        speakable_dir_name = 'Speakable'

        self.default_sound_dir = os.path.join(self.dir, ipod_control_dir_name, 'sound')

        self.tracks_speakable_dir = os.path.join(self.dir, ipod_control_dir_name, speakable_dir_name, 'Tracks')

        self.pls_speakable_dir = os.path.join(self.dir, ipod_control_dir_name, speakable_dir_name, 'Playlists')

        self._sounds_log = {}

        try:
            os.makedirs(self.default_sound_dir)
        except FileExistsError:
            pass

        self.itunessd_file = os.path.join(self.dir, ipod_control_dir_name, itunessd_name)
        self.itunessd = open(self.itunessd_file, 'rb').read()

        dic = f.split_xxhs(self.itunessd[:f.bdhs_items_size], f.bdhs_items)
        if dic[f.header_id] != b'bdhs':
            raise FieldError

        self.voiceover = bool(utils.ifb(dic[f.voiceover_enabled]))

        self._track_header_chunk_offset = utils.ifb(dic[f.track_header_chunk_offset])
        self._playlists_header_chunk_offset = utils.ifb(dic[f.playlist_header_chunk_offset])

        self.voiceover_lang = 'zh_CN'
        self.max_volume = utils.ifb(dic[f.max_volume])

        self._tracks_add_info_file = self.dir + '/iTunes' + '/tracks_add_info.json'
        try:
            self._tracks_add_info = json.load(open(self._tracks_add_info_file))
        except(FileNotFoundError, ValueError):
            self._tracks_add_info = {}

        self._init_tracks()

        self._playlists_ext_info_file = self.dir + '/iTunes' + '/playlists_add_info.json'
        try:
            self._playlists_ext_info = json.load(open(self._playlists_ext_info_file))
        except(FileNotFoundError, ValueError):
            self._playlists_ext_info = {}

        self._init_playlists()

    def _init_tracks(self,):
        data = self.itunessd[self._track_header_chunk_offset:]

        dic = f.split_xxhs(data, f.hths_items)

        if dic[f.header_id] != b'hths':
            raise FieldError

        total_length = utils.ifb(dic[f.total_length])

        for offset_bytes in utils.split_by_step(data[f.hths_items_size:total_length], 4):
            track = Track(shuffle=self, offset=utils.ifb(offset_bytes))

            add_info = self._tracks_add_info[track.dbid]
            track.voice_string = add_info['voice_string']
            track.voice_lang = add_info['voice_lang']
            track.name = add_info['name']

            self.tracks.append(track)

    def _init_playlists(self):
        data = self.itunessd[self._playlists_header_chunk_offset:]
        dic = f.split_xxhs(data, f.hphs_items)
        if dic[f.header_id] != b'hphs':
            raise ()
        total_length = utils.ifb(dic[f.total_length])

        for offsets_bytes in utils.split_by_step(data[f.hphs_items_size:total_length], 4):
            playlist = Playlist(shuffle=self, offset=utils.ifb(offsets_bytes))

            add_info = self._playlists_ext_info[playlist.dbid]
            playlist.voice_string = add_info['voice_string']
            playlist.voice_lang = add_info['voice_lang']
            playlist.name = add_info['name']
            self.playlists.append(playlist)

    def _get_chunk_of_tracks(self):
        data = b''
        lenght_of_all_offset_of_track_chunk = len(self.tracks) * 4
        list_of_tracks_bytes = []
        for track in self.tracks:
            list_of_tracks_bytes.append(track.get_chunk())

        for one in f.hths_items:
            if f.K_DEFAULT in one.keys():
                data += one[f.K_DEFAULT]
            elif one[f.K_NAME] == f.total_length:
                data += utils.itb(f.hths_items_size + lenght_of_all_offset_of_track_chunk, one[f.K_SIZE])

        all_offsets_of_track_bytes = b''
        all_tracks_bytes = b''
        for track_bytes in list_of_tracks_bytes:
            all_offsets_of_track_bytes += utils.itb(self._track_header_chunk_offset +
                                                    f.hths_items_size +
                                                    lenght_of_all_offset_of_track_chunk +
                                                    len(all_tracks_bytes), 4)
            all_tracks_bytes += track_bytes

        data += all_offsets_of_track_bytes + all_tracks_bytes

        return data

    def _get_chunk_of_playlists(self):
        data = b''
        lenght_of_all_offset_of_playlist = len(self.playlists) * 4

        list_of_playlists_bytes = []
        for track in self.tracks:
            list_of_playlists_bytes.append(track.get_chunk())

        number_of_master_playlists = 0
        number_of_normal_playlists = 0
        number_of_audiobooks_playlists = 0
        number_of_podcast_playlists = 0
        for playlist in self.playlists:
            if playlist.type == f.PL_TYPE_NORMAL:
                number_of_normal_playlists += 1
            elif playlist.type == f.PL_TYPE_AUDIOBOOK:
                number_of_audiobooks_playlists += 1
            elif playlist.type == f.PL_TYPE_PODCAST:
                number_of_podcast_playlists += 1
            elif playlist.type == f.PL_TYPE_MASTER:
                number_of_master_playlists += 1
        if number_of_master_playlists >= 1:
            raise()

        for one in f.hphs_items:
            if f.K_DEFAULT in one.key():
                data += one[f.K_DEFAULT]
            elif one[f.K_NAME] == f.total_length:
                data += utils.itb(f.hphs_items_size + lenght_of_all_offset_of_playlist, one[f.K_SIZE])

            elif one[f.K_NAME] == f.number_of_all_playlists:
                data += utils.itb(number_of_master_playlists +
                                  number_of_normal_playlists +
                                  number_of_audiobooks_playlists +
                                  number_of_podcast_playlists, one[f.K_SIZE])

            elif one[f.K_NAME] == f.playlist_flag_normal:
                data += b'\xFF'*one[f.K_SIZE] if number_of_normal_playlists == 0\
                    else utils.itb(1, one[f.K_SIZE])

            elif one[f.K_NAME] == f.number_of_normal_playlists:
                data += utils.itb(number_of_normal_playlists, one[f.K_SIZE])

            elif one[f.K_NAME] == f.playlist_flag_audiobook:
                if number_of_audiobooks_playlists == 0:
                    data += b'\xFF'*one[f.K_SIZE]
                else:
                    utils.itb(number_of_master_playlists + number_of_normal_playlists +
                              number_of_podcast_playlists, one[f.K_SIZE])

            elif one[f.K_NAME] == f.number_of_audiobook_playlists:
                data += utils.itb(number_of_audiobooks_playlists, one[f.K_SIZE])

            elif one[f.K_NAME] == f.playlist_flag_podcast:
                data += b'\xFF'*one[f.K_SIZE] if number_of_podcast_playlists == 0\
                    else utils.itb(number_of_master_playlists + number_of_normal_playlists, one[f.K_SIZE])

        all_offsets_of_playlist_bytes = b''
        all_playlists_bytes = b''
        for playlist_bytes in list_of_playlists_bytes:
            all_offsets_of_playlist_bytes += utils.itb(self._playlists_header_chunk_offset +
                                                       f.hphs_items_size +
                                                       lenght_of_all_offset_of_playlist +
                                                       len(all_offsets_of_playlist_bytes), 4)
            all_playlists_bytes += playlist_bytes

        data += all_offsets_of_playlist_bytes + all_playlists_bytes

        return data

    def get_all_tracks(self):
        return copy.copy(self.tracks)

    def get_all_info_of_tracks(self):
        return copy.copy(self._tracks_add_info)

    def get_all_playlists(self):
        return copy.copy(self.playlists)

    def get_all_info_of_playlists(self):
        return copy.copy(self._playlists_ext_info)

    def get_tracks_of_master_playlist(self):
        master_playlist_tracks = []
        for playlist in self.playlists:
            if playlist.type == f.PL_TYPE_NORMAL:
                for track in playlist.tracks:
                    if track not in master_playlist_tracks:
                        master_playlist_tracks.append(track)
        return master_playlist_tracks

    def get_new_dbid(self):
        dbid = None
        while True:
            dbid = random.randint(1, 2**(8*8)-1)
            if dbid not in [track.dbid for track in self.tracks] and dbid not in [pl.dbid for pl in self.playlists]:
                break
        return dbid

    def add_track(self, file, checksum=None):
        if not utils.is_able_file(file):
            raise()

        exsit_track = None

        for track in self.tracks:
            if track.checksum == checksum:
                exsit_track = track
                break

        # 如果shuffle文件记录没有这个文件，就要拷过去
        if exsit_track is None:
            fullname = None
            while True:
                fullname = '%s/%s%s' % (self.default_sound_dir,
                                        random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 4),
                                        os.path.splitext(file)[1])
                if fullname not in [track.fullname for track in self.tracks]:
                    break

            shutil.copy(file, '%s%s%s' % (self.dir, os.sep, fullname))

            new_track = Track(shuffle=self, filename=fullname, add_info={'checksum': checksum})

            self.tracks.append(new_track)
            exsit_track = new_track

        return exsit_track

    def del_track(self, track):
        self.tracks.remove(track)
        track.remove_file()
        for playlist in self.playlists:
            playlist.remove(track)

    def add_playlist(self, playlist_name):
        for playlist in self.playlists:
            if playlist.name == playlist_name:
                return playlist
        new_playlist = Playlist(playlist_name)
        self.playlists.append(new_playlist)
        return new_playlist

    def del_playlist(self, playlist):
        os.remove(playlist['dbid_file'])
        self.playlists.remove(playlist)

    def get_master_playlist(self):
        tracks = []
        for playlist in self.playlists:
            if playlist.type == f.PL_TYPE_NORMAL:
                for track in playlist.tracks:
                    if track not in tracks:
                        tracks.append(track)
        pl = Playlist(self)
        pl.type = f.PL_TYPE_MASTER
        pl.dbid = self.get_new_dbid()

    def wirte_itunessd(self):
        data = b''
        index_of__track_header_offset = None
        size_of__track_header_offset = None
        index_of__playlist_header_offset = None
        size_of__playlist_header_offset = None

        bdhs_chunk_items = []
        items = bdhs_chunk_items

        for one in f.bdhs_items:
            if f.K_DEFAULT in one.keys():
                items += one[f.K_DEFAULT]
            elif one[f.K_NAME] == f.header_legth:
                items += f.bdhs_items_size
            elif one[f.K_NAME] == f.total_no_of_tracks:
                items += utils.itb(len(self.tracks), one[f.K_SIZE])
            elif one[f.K_NAME] == f.total_no_of_playlists:
                items += utils.itb(len(self.playlists), one[f.K_SIZE])
            elif one[f.K_NAME] == f.max_volume:
                items += utils.itb(self.max_volume, one[f.K_SIZE])
            elif one[f.K_NAME] == f.voiceover_enabled:
                items += utils.itb(int(self.voiceover), one[f.K_SIZE])
            elif one[f.K_NAME] == f.total_no_of_tracks2:
                items += utils.itb(len(self.get_tracks_of_master_playlist()), one[f.K_SIZE])
            elif one[f.K_NAME] == f.track_header_chunk_offset:
                size_of__track_header_offset = one[f.K_SIZE]
                index_of__track_header_offset = len(items)
                items += None  # placeholder
            elif one[f.K_NAME] == f.playlist_header_chunk_offset:
                size_of__playlist_header_offset = one[f.K_SIZE]
                index_of__playlist_header_offset = len(items)
                items += None  # placeholder

        self._track_header_chunk_offset = f.bdhs_items_size
        hths_chunk = self._get_chunk_of_tracks()

        self._playlists_header_chunk_offset = f.bdhs_items + len(hths_chunk)
        hphs_chunk = self._get_chunk_of_playlists()

        bdhs_chunk_items[index_of__track_header_offset] =\
            utils.itb(self._track_header_chunk_offset, size_of__track_header_offset)
        bdhs_chunk_items[index_of__playlist_header_offset] =\
            utils.itb(self._playlists_header_chunk_offset, size_of__playlist_header_offset)

        for item in bdhs_chunk_items:
            data += item

        data += hths_chunk + hphs_chunk

        itunessd = open(self.itunessd_file, 'wb')
        itunessd.write(data)
        itunessd.close()

    def write_add_info(self):
        track_add_info = {}
        playlist_add_info = {}
        for track in self.tracks:
            track_add_info[track.dbid] = track.get_add_info()
        for playlist in self.playlists:
            playlist_add_info[playlist.dbid] = playlist.get_add_info()


class PlayList:
    pass
