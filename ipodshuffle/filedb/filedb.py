import os
import random
import string

from ipodshuffle.utils import get_checksum

from ipodshuffle import audio

from .log import Storage, FileAlreadyInError


def get_random_name():
    return ''.join(random.sample(string.ascii_uppercase, 6))


def get_ipodlike_random_name():
    """
    :return: F0[1-3]/XXXX.[mp3|m4a|m4b|...]
    """


class AudioDB(Storage):
    def __init__(self, shuffle, log_path, storage_dir):
        super().__init__(log_path, storage_dir, random_name_fun=get_random_name)

        self._shuffle = shuffle

        self.storage_dir = storage_dir

    def add(self, src, checksum=None):
        if not audio.get_type(src):
            raise TypeError('The type of this file is not supported.')
        checksum = checksum or get_checksum(src)

        try:
            super().add(src, checksum)
        except FileAlreadyInError:
            pass

        return self.get_path_in_ipod(checksum)

    # def get_path_in_ipod(self, checksum):
    #    path_in_ipod = None

    #    filename = self.get_filename(checksum)
    #    realpath = self.realpath(filename)
    #    if filename:
    #        path_in_ipod = self._shuffle.get_path_in_ipod(realpath)

    #    return path_in_ipod

    # def remove(self, path):
    #    os.remove(self._shuffle.base_dir + '/' + path)
    #    del self._shuffle.sounds_logs[path]


class VoiceDB:
    def __init__(self, log_path, storage_dir, random_name_fun):
        self._Store = Storage(log_path, storage_dir, random_name_fun)

    def clean(self):
        self._Store.clean()

    def add(self, src, text, lang, checksum=None):

        checksum = checksum or get_checksum(src)

        if not audio.get_type(src) == audio.WAV:
            raise TypeError

        filename = self.get_filename(text, lang)

        if filename:
            raise Exception

        try:
            self._Store.add(src, checksum)

        except FileAlreadyInError:
            pass

        filename = self._Store.get_filename(checksum)
        extra = {
            'text': text,
            'lang': lang
        }
        self._Store.set_extra(filename, extra)

    def get_filename(self, text, lang):
        filename = None
        for _filename in self.get_filenames():
            _extra = self._Store.get_extra(_filename)
            _text, _lang = _extra.setdefault('text', None), _extra.setdefault('lang', None)
            if _text == text and _lang == lang:
                filename = _filename
                break

        return filename

    def get_filenames(self):
        return self._Store.get_filenames()

    def realpath(self, filename):
        return self._Store.realpath(filename)


def make_dbid1():
    return ''.join(random.sample('ABCDEF' + string.digits, 16))


def make_dbid2():
    dbid_string = ''
    for x in random.sample(range(0, 255), 8):
        s = hex(x)[2:]
        if len(s) == 1:
            s = '0' + s
        dbid_string += s.upper()
    return dbid_string

make_dbid = make_dbid2


def make_dbid_name():
    return make_dbid() + '.wav'


class VoiceOverDB(VoiceDB):
    def __init__(self, log_path, stored_dir, users=None):
        super().__init__(log_path, stored_dir, random_name_fun=make_dbid_name)

        self._storage_dir = stored_dir
        self._users = users

    def remove_not_in_use(self):
        files_to_remove = []

        for filename in os.listdir(self._storage_dir):
            dbid, ext = os.path.splitext(filename)

            if filename not in self.get_filenames() and dbid not in [user.dbid for user in self._users]:
                files_to_remove.append(self.realpath(filename))

        for path in files_to_remove:
            if os.path.isfile(path):
                os.remove(path)
            else:
                os.removedirs(path)

    def get_dbid(self, text, lang):
        dbid = None
        filename = self.get_filename(text, lang)
        if filename:
            dbid = os.path.splitext(filename)[0]
        return dbid

    def get_text_lang(self, filename):
        extra = self._Store.get_extra(filename)
        text, lang = extra['text'], extra['lang']
        return text, lang


class SystemVoice:
    pass


class MassagesVoice:
    pass
