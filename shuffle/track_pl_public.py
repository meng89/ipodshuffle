from ipod_shuffle_4 import utils


class Public:
    def __init__(self):
        pass

    def make_voiceover(self):
        utils.tts(self.voice_string, self.voice_lang, self.voiceover_file)

    def get_ext(self):
        return self._ext