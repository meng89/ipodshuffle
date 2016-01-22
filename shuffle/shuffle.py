import os
import json
import hashlib
from . import itunessd
from . import baseclasses

MUSIC = 'music'
AUDIOBOOK = 'audiobook'

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
        self.sounds_logs_path = directory + '/iPod_Control/sounds_logs.json'

        if os.path.exists(itunessd_path):
            if os.path.isfile(itunessd_path):
                self.itunessd = itunessd.Itunessd(open(itunessd_path, 'rb').read())
            else:
                raise Exception
        else:
            self.itunessd = itunessd.Itunessd()

        self.sounds_logs = json.loads(open(self.sounds_logs_path))

    def __logs_del_iffilenotexists(self):
        new_logs = {}
        for path, metadata in self.sounds_logs.items():
            full_path = self.directory + os.sep + path

            if os.path.exists(full_path) and os.path.isfile(full_path):
                new_logs[path] = metadata

        self.sounds_logs = new_logs

    def __logs_update_ifsizeormtimechanged(self):
        new_logs = {}
        for path, metadata in self.sounds_logs.items():
            full_path = self.directory + os.sep + path

            if os.path.getsize(full_path) == metadata['size'] and os.path.getmtime(full_path) == metadata['mtime']:
                new_logs[path] = metadata
            else:
                new_logs[path] = get_metadata(full_path)


class Sounds(baseclasses.List):
    def __init__(self):
        super().__init__()

    def add_from_file(self, path):
        sound = Sound(path)
        self.append(sound)


class Sound:
    def __init__(self, path):

        self.original_name = None
        self.path = None
        self.md5 = None
        self.size = None
        self.mtime = None

