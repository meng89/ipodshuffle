sync
====

.. program-output:: tools/teresa sync --help


TTS engines
-----------

Program use `langid <https://github.com/saffsd/langid.py>`_ to identify title text langguage of track and playlist,
but not work perfectly, It is suggested that you use "langs=lang1,lang2…" to specify languages range.

For now, have two TTS engine wrapper:

sovx
^^^^

CLI command is "pico2wave", make sure you have already installed it.


voicerss
^^^^^^^^

An http engine. It supports lot of languages(include CJK).
For now, dayily request is free for 350 times, but need to register on the website to get an API key,
website: http://www.voicerss.org


source folder structure
-----------------------

all folders and audio files can be symbolic(soft) links.

"source" is just a example, you can use another name whatever you want.
In source folder,
only three folders will be scanned: "music", "podcasts" and "audiobooks".

Under "music", all folders(include children folders and children's children folders and so on) are NORMAL playlists.
NORMAL playlist also caontain their child folder tracks.
MASTER playlist contain all tracks of all NORMAL playlists

Under "podcasts", only folders will be PODCAST playlists.

Under "audiobooks", files and folders will be AUDIOBOOK playlists, but folder's child folder wouldn't.

See example folders structure following and notice the IGNORED folders and IGNORED audio files::

    source
       ├── music
       │      ├── English songs
       │      │      ├── Bob Dylan
       │      │      │      ├── Bob Dylan - Farewell.mp31
       │      │      │      └── Bob Dylan - Mr. Tambourine Man.mp3
       │      │      │
       │      │      └── Mariah Carey
       │      │             ├── Mariah Carey - Bye Bye.mp3
       │      │             └── Mariah Carey - Hero.mp3
       │      │
       │      ├── 邓丽君
       │      │      ├── 邓丽君 - 小城故事多.mp3
       │      │      ├── 邓丽君 - 何日君再来.mp3
       │      │      └── 邓丽君 - 恰似你的温柔.mp3
       │      │
       │      ├── The Clash - Bankrobber.mp3
       │      ├── The Weepies - Gotta Have You.mp3
       │      ├── 梁静茹 - 小手拉大手.mp3
       │      ├── 卢冠廷 - 一生所爱.mp3
       │      └── 喜納昌吉 - 花~すべての人の心に花を.mp3
       │
       │
       ├── podcasts
       │      ├── 6 Minute English
       │      │      ├── p03fgnf9.mp3
       │      │      ├── p03g4kll.mp3
       │      │      ├── p03gtsz8.mp3
       │      │      └── p03hj7dq.mp3
       │      │
       │      ├── The English We Speak
       │      │      ├── p03gmjw3.mp3
       │      │      ├── p03hb15j.mp3
       │      │      └── p03j16wv.mp3
       │      │
       │      ├── Luk's ENGLISH Podcast
       │      │      ├── FOLDER_IN_THIS_LEVEL_WILL_BE_IGNORED
       │      │      │      └── THIS_AUDIO_WILL_BE_IGNORED.mp3
       │      │      │
       │      │      ├── 326-catching-up-with-oli-future-predictions-part-2.mp3
       │      │      ├── 327-the-lep-photo-competition-please-check-out-the-photos-and-vote.mp3
       │      │      └── 328-cooking-with-luke-verbs-and-expressions-in-the-kitchen.mp3
       │      │
       │      │
       │      └── AUDIO_IN_THIS_LEVEL_WILL_BE_IGNORED.mp3
       │
       │
       └── audiobooks
              ├── 01.Love Or Money
              │      ├── 01.mp3
              │      ├── 02.mp3
              │      ├── 03.mp3
              │      ├── 04.mp3
              │      ├── 05.mp3
              │      ├── 06.mp3
              │      └── 07.mp3
              │
              │
              ├── 02.Mary Queen Of Scots
              │      ├── FOLDER_IN_THIS_LEVEL_WILL_BE_IGNORED
              │      │      └── THIS_AUDIO_WILL_BE_IGNORED.mp3
              │      │
              │      ├── 01.Fotheringhay.mp3
              │      ├── 02.France.mp3
              │      ├── 03.Darnley and Riccio.mp3
              │      ├── 04.The death of David Riccio.mp3
              │      ├── 05.My son is born.mp3
              │      ├── 06.Kirk O'Field.mp3
              │      ├── 07.Bothwell.mp3
              │      ├── 08.England.mp3
              │      └── 09.A Death.mp3
              │
              ├── a book in single audio.mp3
              └── another book in single audio.mp3

