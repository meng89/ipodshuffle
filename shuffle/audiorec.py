#  Audio formats supported:
#
# .m4a/.m4b         AAC (8 to 320 Kbps),
# .m4a              Protected AAC (from iTunes Store),

# .mp3              MP3 (8 to 320 Kbps),
# .mp3              MP3 VBR,

#                   Audible (formats 2, 3, 4, Audible Enhanced Audio, AAX, and AAX+),
# .m4a              Apple Lossless,
# .aiff/.aif/.aifc  AIFF,
# .wav              WAV

# mutagen.File(path).mime

# mp3 : ['audio/mp3', 'audio/x-mp3', 'audio/mpeg', 'audio/mpg', 'audio/x-mpeg', 'application/octet-stream']
# acc, alac : ['audio/mp4', 'audio/x-m4a', 'audio/mpeg4', 'audio/aac', 'application/octet-stream']
# flac : ['audio/x-flac', 'application/x-flac', 'application/octet-stream']
# aiff: ['audio/aiff', 'audio/x-aiff', 'application/octet-stream']

# wav : None!


#     http://www.apple.com/shop/buy-ipod/ipod-shuffle

# AAC (8 to 320 Kbps)
# Protected AAC (from iTunes Store)
# — (shuffle does not support HE-AAC)
# MP3 (8 to 320 Kbps)
# MP3 VBR
# Audible (formats 2, 3, 4, Audible Enhanced Audio, AAX, and AAX+)
# Apple Lossless
# AIFF
# WAV


import mutagen
import sndhdr

audio_types = {
    1: {'format': 'mp3',  'exts': ['mp3']},
    2: {'format': 'acc',  'exts': ['m4a', 'm4b']},
    # 3 ???
    4: {'format': 'wav',  'exts': ['wav']},
    5: {'format': 'alac', 'exts': ['m4a']},
    6: {'format': 'aiff', 'exts': ['aif']}
}


def get_filetype(path):
    file_type = None

    audio = mutagen.File(path)
    if audio:
        if 'audio/mp3' in audio.mime:
            file_type = 1
        elif 'audio/mp4' in audio.mime:
            if audio.info.codec == 'mp4a.40.2':
                file_type = 2
            elif audio.info.codec == 'alac':
                file_type = 5

    else:
        t = sndhdr.what(path)
        if t:
            if t[0] == 'wav':
                file_type = 4
            elif t[0] == 'aiff':
                file_type = 6

    return file_type