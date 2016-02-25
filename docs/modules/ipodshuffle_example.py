import shutil
import os
import tempfile

from ipodshuffle import Shuffle
from ipodshuffle import MASTER, NORMAL, PODCAST, AUDIOBOOK


# for VoiceOver, make sure you have already installed sovx TTS softwave
def voice_path_func(text, lang):
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_file_name = tmp_file.name + '.wav'
    tmp_file.close()

    cmd = 'pico2wave --wave={} --lang={} {}'.format(tmp_file_name, lang, repr(text))
    # print('\n\n', cmd, '\n')
    os.system(cmd)

    return tmp_file_name

base = '/media/data/ipod_base_doc_text'

ipod = Shuffle(base)

ipod.playlists.clear()

# enable VoiceOver
ipod.enable_voiceover = True

# when track or playlist set "voice = 'text', 'lang code'",  will call this funcition
ipod.voice_path_func = voice_path_func


# create a master playlist, it's the "All songs" in ipod
master_playlist = ipod.playlists.append_one(pl_type=MASTER)


# create a normal playlist
normal_playlist = ipod.playlists.append_one(pl_type=NORMAL)
normal_playlist.voice = 'Bob Dylan', 'en-US'


# copy file to ipod
track1_pathinipod = 'Bob Dylan - Farewell.mp3'
shutil.copyfile('/media/data/music/Bob Dylan/Bob Dylan - Farewell.mp3',
                ipod.base + '/' + track1_pathinipod)
track1 = ipod.create_track(path_in_ipod=track1_pathinipod)
track1.voice = 'Farewell', 'en-US'
normal_playlist.tracks.append(track1)


# use AudioDB copy file to ipod
track2_checksum = ipod.audiodb.add('/media/data/music/Bob Dylan/Bob Dylan - Mr. Tambourine Man.mp3')
track2_pathinipod = ipod.audiodb.get_filename(track2_checksum)
track2 = ipod.create_track(path_in_ipod=track2_pathinipod)
track2.voice = 'Mr. Tambourine Man', 'en-US'
normal_playlist.tracks.append(track2)


# tracks can use same file, and you can set different voices for tracks
track3 = ipod.create_track(path_in_ipod=track1_pathinipod)
track3.voice = 'Farewell, Bob Dylan'
master_playlist.tracks.append(track3)

track4 = ipod.create_track(path_in_ipod=track2_pathinipod)
track4.voice = 'Mr. Tambourine Man, Bob Dylan'
master_playlist.tracks.append(track4)


track5_checksum = ipod.audiodb.add('/media/data/music/Goo Goo Dolls - Name.mp3')
track5_pathinipod = ipod.audiodb.get_filename(track5_checksum)
track5 = ipod.create_track(path_in_ipod=track5_pathinipod)
track5.voice = 'Name, Goo Goo Dolls', 'en-US'
master_playlist.tracks.append(track5)


ipod.write_db()
