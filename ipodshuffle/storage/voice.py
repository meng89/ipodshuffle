from ipodshuffle.utils import get_checksum

from ipodshuffle import audio

from .log import Storage


class VoiceDB(Storage):
    def __init__(self, log_path, storage_dir, random_name_fun):
        super().__init__(log_path, storage_dir, random_name_fun)

    def clean(self):
        super().clean()

    def add_voice(self, src, text, lang, checksum=None):

        checksum = checksum or get_checksum(src)

        if not audio.get_type(src) == audio.WAV:
            raise TypeError

        filename = self.get_voice(text, lang)

        if filename:
            raise Exception

        self.add(src)

        filename = self.get_filename(checksum)
        extra = {
            'text': text,
            'lang': lang
        }
        self.set_extra(filename, extra)

    def get_voice(self, text, lang):
        filename = None
        for _filename in self.get_filenames():
            _extra = self.get_extra(_filename)
            _text, _lang = _extra.setdefault('text', None), _extra.setdefault('lang', None)
            if _text == text and _lang == lang:
                filename = _filename
                break
        return filename

