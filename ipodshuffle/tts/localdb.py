from ipodshuffle.shuffle import make_dbid2
from ipodshuffle.log import VoiceDB


class LocalDB(VoiceDB):
    def __init__(self, logs_path, stored_dir):
        super().__init__(logs_path, stored_dir)

    def get_random_name(self):
        return make_dbid2()

    def get_path_by_text_lang(self, text, lang):
        filename = self._get_filename_by_text_lang(text, lang)

        if filename:
            return self.get_full_path(filename)
        else:
            return None
