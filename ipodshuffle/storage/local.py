import os
import uuid

from .log import JsonLog, get_checksum
from .filedb import VoiceDB


def get_uuid1_hex():
    return uuid.uuid1().hex


class LocalFileLog(JsonLog):
    def __init__(self, log_path):
        super().__init__(log_path)

        self.clean_log()

    def clean_log(self):
        log_keys_to_del = []

        for realpath in self._log.keys():
            if not os.path.exists(realpath) or not os.path.isfile(realpath):
                log_keys_to_del.append(realpath)

        for key in log_keys_to_del:
            del self._log[key]

        self.write_log()

    def log_it(self, path):
        realpath = os.path.realpath(path)

        if realpath not in self._log.keys():
            self._log[realpath] = {
                'checksum': get_checksum(realpath),
                'mtime': os.path.getmtime(realpath),
                'size': os.path.getsize(realpath)
            }

        self.write_log()

    def get_checksum(self, path):
        checksum = None

        realpath = self.realpath(path)
        if realpath in self._log.keys():
            checksum = self._log[realpath]['checksum']
        return checksum

    @staticmethod
    def realpath(path):
        return os.path.realpath(path)


class LocalVoiceDB(VoiceDB):
    def __init__(self, log_path, stored_dir):
        super().__init__(log_path, stored_dir, random_name_fun=get_uuid1_hex)

    def get_path(self, text, lang):
        realpath = None
        filename = self.get_filename(text, lang)
        if filename:
            realpath = self.realpath(filename)
        return realpath
