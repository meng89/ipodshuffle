from ipodshuffle.shuffle import Voicedb, make_dbid2

# 1, 检查有没有 这个音频，有就返回，没有就添加。


class Db(Voicedb):
    def __init__(self, logs_path, stored_dir):
        super().__init__(logs_path, stored_dir)

    def get_random_name(self):
        return make_dbid2()

    def get_path_by_text_lang(self, text, lang):
        filename = self._get_filename_by_text_lang(text, lang)

        if filename:
            return self._fullpath(filename)
        else:
            return None
