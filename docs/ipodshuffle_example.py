import shutil
import copy
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
normal_playlist1 = ipod.playlists.append_one(pl_type=NORMAL)
# set playlist VoiceOver, will call ipod.voice_path_func to get voice path and will auto copy in ipod
normal_playlist1.voice = 'Mariah Carey', 'en-US'
# copy audio file to ipod
shutil.copyfile('/media/data/music/Mariah Carey/Mariah Carey - Bye Bye.mp3',
                base + '/' + 'Mariah Carey - Bye Bye.mp3')
# add a track
track1 = normal_playlist1.tracks.append_one(path_in_ipod='Mariah Carey - Bye Bye.mp3')
# set track voice
track1.voice = 'Bye Bye', 'en-US'

shutil.copyfile('/media/data/music/Mariah Carey/Mariah Carey - Hero.mp3',
                base + '/' + 'Mariah Carey - Hero.mp3')
track2 = normal_playlist1.tracks.append_one(path_in_ipod='Mariah Carey - Hero.mp3')
track2.voice = 'Hero', 'en-US'


normal_playlist2 = ipod.playlists.append_one(pl_type=NORMAL)
normal_playlist2.voice = 'Bob Dylan', 'en-US'

shutil.copyfile('/media/data/music/Bob Dylan/Bob Dylan - Farewell.mp3',
                base + '/' + 'Bob Dylan - Farewell.mp3')
track3 = normal_playlist2.tracks.append_one(path_in_ipod='Bob Dylan - Farewell.mp3')
track3.voice = 'Bye Bye', 'en-US'

shutil.copyfile('/media/data/music/Bob Dylan/Bob Dylan - Mr. Tambourine Man.mp3',
                base + '/' + 'Bob Dylan - Mr. Tambourine Man.mp3')
track4 = normal_playlist2.tracks.append_one(path_in_ipod='Bob Dylan - Mr. Tambourine Man.mp3')
track4.voice = 'Hero', 'en-US'


shutil.copyfile('/media/data/music/Goo Goo Dolls - Name.mp3',
                base + '/' + 'Goo Goo Dolls - Name.mp3')

track5 = master_playlist.tracks.append_one(path_in_ipod='Goo Goo Dolls - Name.mp3')
track5.voice = 'Name, Goo Goo Dolls', 'en-US'

# tracks can use same file, and you can set different voices for tracks
track6 = copy.deepcopy(track1)
track6.voice = 'Bye Bye, Mariah Carey', 'en-US'
master_playlist.tracks.append(track6)

track7 = copy.deepcopy(track2)
track7.voice = 'Hero, Mariah Carey', 'en-US'
master_playlist.tracks.append(track7)

track8 = copy.deepcopy(track3)
track8.voice = 'Farewell, Bob Dylan', 'en-US'
master_playlist.tracks.append(track8)

track9 = copy.deepcopy(track4)
track9.voice = 'Mr. Tambourine Man, Bob Dylan', 'en-US'
master_playlist.tracks.append(track9)

# finish it
ipod.write()
