#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import shuffle.tts


def test_tts():
    import sys
    print(sys.argv[1])
    print(sys.argv[2])
    mp3fp = shuffle.tts.tts(sys.argv[1], sys.argv[2])
    wavfp = shuffle.tts.mp3_to_wav(mp3fp)
    open('1.wav', 'wb').write(wavfp.read())


def test_gtts():
    from gtts import gTTS
    tts = gTTS(text='hello world', lang='zh-cn')
    tts.save("hello.mp3")


if __name__ == '__main__':
    # test_tts()
    test_gtts()
