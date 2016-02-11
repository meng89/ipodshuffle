import json
import os
import shutil
from abc import abstractmethod

from . import audio
from .utils import get_checksum


class Log:
    def __init__(self, logs_path):
        self._logs_path = logs_path

        self._original_logs_str = '{}'
        self._log = {}
        os.makedirs(os.path.split(self._logs_path)[0], exist_ok=True)

        try:
            with open(self._logs_path) as f:
                self._original_logs_str = f.read()
        except FileNotFoundError:
            pass
        self._log = json.loads(self._original_logs_str, )

    def write_log(self):
        new_logs_str = json.dumps(self._log, sort_keys=True, indent=4, ensure_ascii=False)
        if new_logs_str != self._original_logs_str:
            open(self._logs_path, 'w').write(new_logs_str)
            self._original_logs_str = new_logs_str


class VoiceDB(Log):
    def __init__(self, logs_path, stored_dir):
        super().__init__(logs_path)
        self._stored_dir = stored_dir

        os.makedirs(self._stored_dir, exist_ok=True)

    def del_not_exists(self):
        no_exists_files = []
        for path, info in self._log.items():
            full_path = self._stored_dir + '/' + path
            if not os.path.exists(full_path) or not os.path.isfile(full_path):
                no_exists_files.append(path)

        for path in no_exists_files:
            del self._log[path]

    def del_wrong_logs(self):
        pass
        dbids_to_del = []
        for filename, info in self._log.items():
            voice_path = self.get_full_path(filename)
            if info['mtime'] != os.path.getmtime(voice_path) or info['size'] != os.path.getsize(voice_path):
                dbids_to_del.append(filename)

        for dbid in dbids_to_del:
            del self._log[dbid]

    def clean(self):
        self.del_not_exists()
        self.del_wrong_logs()

    @abstractmethod
    def get_random_name(self):
        pass

    def get_new_filename(self):
        file_name = None
        while True:
            file_name = self.get_random_name()
            if file_name not in self._log.keys() and not os.path.exists(self.get_full_path(file_name)):
                break
        return file_name

    def add(self, path, text, lang, checksum=None, user_defined=None):
        if not audio.get_type(path) == audio.WAV:
            raise TypeError

        checksum = checksum or get_checksum(path)

        for file_in_dir, info in self._log.items():
            if info['checksum'] == checksum:
                print(lang, text, path)
                raise FileExistsError

        filename = self.get_new_filename() + '.wav'
        full_path = self.get_full_path(filename)

        shutil.copyfile(path, full_path)

        self._log[filename] = {
            'text': text,
            'lang': lang,
            'checksum': checksum,
            'mtime': os.path.getmtime(full_path),
            'size': os.path.getsize(full_path),
            'user_defined': user_defined
        }

        self.write_log()

        return filename

    def _get_filename_by_text_lang(self, text, lang):
        filename = None
        for _filename, info in self._log.items():
            if info['text'] == text and info['lang'] == lang:
                filename = _filename
        return filename

    def _get_filename_by_checksum(self, checksum):
        filename = None
        for _filename, info in self._log.items():
            if info['checksum'] == checksum:
                filename = _filename
        return filename

    def remove(self, filename):
        os.remove(self.get_full_path(filename))
        del self._log[filename]

    def get_full_path(self, filename):
        return os.path.join(self._stored_dir, filename)
