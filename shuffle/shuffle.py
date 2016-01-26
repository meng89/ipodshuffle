import os
import json
import hashlib
import random
import string


from shuffle import audiorec


from . import itunessd
from .baseclasses import List

MUSIC = 'music'
AUDIOBOOK = 'audiobook'



def get_metadata(path):
    log = {
        # 'md5': hashlib.md5().update(open(path, 'rb').read()).hexdigest(),
        'mtime': os.path.getmtime(path),
        'size': os.path.getsize(path)
    }
    return log


class Shuffle:
    def __init__(self, directory):
        self.base_dir = directory

        itunessd_name = 'iTunesSD'

        self.control_folder = 'iPod_Control'

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
            full_path = self.base_dir + os.sep + path

            if os.path.exists(full_path) and os.path.isfile(full_path):
                new_logs[path] = metadata

        self.sounds_logs = new_logs

    def __logs_updata_ifsizeormtimechanged(self):
        new_logs = {}
        for path, metadata in self.sounds_logs.items():
            full_path = self.base_dir + os.sep + path

            if os.path.getsize(full_path) == metadata['size'] and os.path.getmtime(full_path) == metadata['mtime']:
                new_logs[path] = metadata
            else:
                new_logs[path] = get_metadata(full_path)

    def __logs_add_fromtracks(self):
        tracks_logs_notinlogs = {}
        for track in self.itunessd.tracks:
            if not [path for path in self.sounds_logs.keys()
                    if os.path.samefile(self.base_dir + os.sep + path, self.base_dir + os.sep + track.filename)]:

                tracks_logs_notinlogs[track.filename] = get_metadata(self.base_dir + os.sep + track.filename)

        self.sounds_logs.update(tracks_logs_notinlogs)


    def fix(self, deeply=False):
        pass


class Sounds:
    def __init__(self, _shuffle):
        self._def_dir = 'sounds'
        self._shuffle = _shuffle

    def get_files(self):
        return tuple(self._shuffle.sounds_logs.keys())

    def get_from_checksum(self, checksum):
        path = None
        for key, info in self._shuffle.sounds_logs.items():
            if info['checksum'] == checksum:
                path = key
                break
        return path

    def add(self, path):
        # at most 65533 files in one folder
        if not audiorec.get_filetype(path):
            raise TypeError('This file type is not supported.')

        full_path = None
        filename = None
        while True:
            filename = random.sample(string.ascii_uppercase, 6)
            full_path = os.path.join(self._shuffle.base_dir, self._shuffle.control_folder, self._def_dir, filename)
            if not os.path.exists(full_path):
                break

        source = open(path, 'rb')
        target = open(full_path, 'wb')
        m = hashlib.md5()

        while True:
            data = source.read(10240)
            if data:
                m.update(data)
                target.write(data)
            else:
                break

        source.close()
        target.close()

        checksum = m.hexdigest()
        key = self._shuffle.control_folder + '/' + self._def_dir + '/' + filename
        self._shuffle.sounds_logs[key]['checksum'] = checksum
        self._shuffle.sounds_logs[key]['size'] = get_metadata(path)

    def remove(self, path):
        pass

        


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
