import mutagen
import sndhdr

MP3 = 1
AAC = 2
# ? = 3
WAV = 4
ALAC = 5
AIFF = 6

AUDIO_MAP = {
    MP3: 'MP3',    # mp3
    AAC: 'AAC',    # m4a, m4b
    WAV: 'WAV',    # wav
    ALAC: 'ALAC',  # m4a
    AIFF: 'AIFF',  # aif
}


def get_type(path):
    file_type = None
    audio = mutagen.File(path)
    if audio:
        if 'audio/mp3' in audio.mime:
            file_type = MP3
        elif 'audio/mp4' in audio.mime:
            if audio.info.codec == 'mp4a.40.2':  # 'aac-lc'
                file_type = AAC
            elif audio.info.codec == 'alac':
                file_type = ALAC

    else:
        t = sndhdr.what(path)
        if t:
            if t[0] == 'wav':
                file_type = WAV
            elif t[0] == 'aiff':
                file_type = AIFF

    return file_type
