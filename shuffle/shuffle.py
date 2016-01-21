import os
import json
import hashlib
from . import itunessd
from . import baseclasses

MUSIC = 'music'
AUDIOBOOK = 'audiobook'


class Shuffle:
    def __init__(self, directory):
        self.directory = directory

        itunessd_name = 'iTunesSD'

        ipod_control_folder = '/iPod_Control'

        itunessd_path = directory + '/iPod_Control/iTunes/iTunesSD'
        self.sounds_logs_path = directory + '/iPod_Control/sounds_logs.json'

        # speakable_folder = 'Speakable'

        # self.default_sound_dir = os.path.join(self.directory, ipod_control_folder, 'sound')

        # self.sounds_voice_folder = os.path.join(self.directory, ipod_control_folder, speakable_folder, 'Tracks')

        # self.playlists_voice_folder = os.path.join(self.directory, ipod_control_folder, speakable_folder, 'Playlists')

        # self._sounds_log = {}

        # self._tracks_add_info_file = self.directory + '/iTunes' + '/tracks_add_info.json'
        # try:
        #    self._tracks_add_info = json.load(open(self._tracks_add_info_file))
        # except(FileNotFoundError, ValueError):
        #    self._tracks_add_info = {}

        if os.path.exists(itunessd_path):
            if os.path.isfile(itunessd_path):
                self.itunessd = itunessd.Itunessd(open(itunessd_path, 'rb').read())
            else:
                raise Exception
        else:
            self.itunessd = itunessd.Itunessd()

        self.sounds_logs = json.loads(open(self.sounds_logs_path))

    def get_metadata(self, path):
        log = {
            'md5': hashlib.md5().update(open(path, 'rb').read()).hexdigest(),
            'mtime': os.path.getmtime(path),
            'size': os.path.getsize(path)
        }
        return log

    def clean_sounds_logs(self):
        cleand_logs = {}

        for path, metadata in self.sounds_logs.items():
            os_path = self.directory + os.sep + path

            if not os.path.exists(path):
                continue
            if not os.path.isfile(path):
                continue

            if (os.path.getmtime(os_path) != metadata['mtime']) or\
                    (os.path.getsize(os_path) != metadata['size']):

                cleand_logs[path] = self.get_metadata(os_path)

            else:
                cleand_logs[path] = metadata




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

