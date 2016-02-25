from ipodshuffle.utils import get_checksum

from ipodshuffle import audio

from .log import Storage


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

        self._Store.add(src)

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
        # print(self._Store._storage_dir, self._Store._log_path)
        # print('here', lang, filename, text)
        return filename

    def get_filenames(self):
        return self._Store.get_filenames()

    def realpath(self, filename):
        return self._Store.realpath(filename)
