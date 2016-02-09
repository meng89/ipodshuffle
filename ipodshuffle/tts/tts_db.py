from ipodshuffle.shuffle import Voicedb, get_dbid2


class Db(Voicedb):
    def __init__(self, logs_path, stored_dir):
        super().__init__(logs_path, stored_dir)

    def get_random_name(self):
        return get_dbid2()

    def get_path_by_text_lang(self, text, lang):
        return self._stored_dir + self.get_filename_by_text_lang(text, lang)
