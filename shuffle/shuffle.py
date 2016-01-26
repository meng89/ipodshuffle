import os
import json
import hashlib

import mutagen
# import pydub
# import av
# import magic


from . import itunessd
from .baseclasses import List

MUSIC = 'music'
AUDIOBOOK = 'audiobook'





def isablefile(path):
    if

def get_metadata(path):
    log = {
        'md5': hashlib.md5().update(open(path, 'rb').read()).hexdigest(),
        'mtime': os.path.getmtime(path),
        'size': os.path.getsize(path)
    }
    return log


class Shuffle:
    def __init__(self, directory):
        self.directory = directory

        itunessd_name = 'iTunesSD'

        ipod_control_folder = '/iPod_Control'

        itunessd_path = directory + '/iPod_Control/iTunes/iTunesSD'
        sounds_logs_path = directory + '/iPod_Control/sounds_logs.json'

        if os.path.exists(itunessd_path):
            if os.path.isfile(itunessd_path):
                self.itunessd = itunessd.Itunessd(open(itunessd_path, 'rb').read())
            else:
                raise Exception
        else:
            self.itunessd = itunessd.Itunessd()

        self.sounds_logs = json.loads(open(sounds_logs_path))

        self.sounds = Sounds(self)

    def __logs_del_iffilenotexists(self):
        new_logs = {}
        for path, metadata in self.sounds_logs.items():
            full_path = self.directory + os.sep + path

            if os.path.exists(full_path) and os.path.isfile(full_path):
                new_logs[path] = metadata

        self.sounds_logs = new_logs

    def __logs_updata_ifsizeormtimechanged(self):
        new_logs = {}
        for path, metadata in self.sounds_logs.items():
            full_path = self.directory + os.sep + path

            if os.path.getsize(full_path) == metadata['size'] and os.path.getmtime(full_path) == metadata['mtime']:
                new_logs[path] = metadata
            else:
                new_logs[path] = get_metadata(full_path)

    def __logs_add_fromtracks(self):
        tracks_logs_notinlogs = {}
        for track in self.itunessd.tracks:
            if not [path for path in self.sounds_logs.keys()
                    if os.path.samefile(self.directory + os.sep + path, self.directory + os.sep + track.filename)]:

                tracks_logs_notinlogs[track.filename] = get_metadata(self.directory + os.sep + track.filename)

        self.sounds_logs.update(tracks_logs_notinlogs)


    def fix(self, deeply=False):
        pass


class Sounds:
    def filelist(self):
        


class Tracks(List):
    pass


class Track:
    pass

class Playlists(List):
    def __init__(self):
        super().__init__()


class Playlist(List):
    def __init__(self):
        super().__init__()
