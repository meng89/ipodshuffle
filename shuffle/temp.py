import os
import json
import uuid


import gtts
import tempfile
import pydub

voice_info_filename = 'voice_info.json'

home = os.path.expanduser("~")

voice_info_fullpath = home + os.sep + '.'


def voicedb(text, lang):

    voice_info = json.load(open(voice_info_fullpath))

    filename = None

    for one in voice_info:
        if one['text'] == text and one['lang'] == lang:
            filename = one['filename']
            break

    if filename is None:
        while True:
            filename = uuid.uuid1()
            if filename not in [info['filename'] for info in voice_info]:
                break

    s = gtts.gTTS(text=text, lang=lang)
    mp3_fp = tempfile.TemporaryFile()
    s.write_to_fp(mp3_fp)
    mp3_audio = pydub.AudioSegment.from_mp3(mp3_fp)

    wav_fp = tempfile.TemporaryFile()
    mp3_audio.export(wav_fp)

