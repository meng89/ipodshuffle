
import uuid

from ipodshuffle.log import VoiceDB


def get_uuid1_hex():
    return uuid.uuid1().hex


class LocalVoiceDB(VoiceDB):
    def __init__(self, log_path, stored_dir):
        super().__init__(log_path, stored_dir, random_name_fun=get_uuid1_hex)

    def get_path(self, text, lang):
        realpath = None
        filename = self.get_filename(text, lang)
        if filename:
            realpath = self.realpath(filename)
        return realpath
