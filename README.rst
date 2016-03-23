ipodshuffle
===========

ipodshuffle is a Python Project for iPod Shuffle 4th generation.

It contain a few modules to handle "iTunesSD".

And a cli tool "teresa" for sync audio files.

With TTS engine "voicerss", it can speak lot of languages naturally, include English, Chinese, Japanese and Korean.


Installation
============

Dependencies
------------

Python 3

`mutagen <https://bitbucket.org/lazka/mutagen>`_

`langid <https://github.com/saffsd/langid.py>`_

`Babel <http://babel.pocoo.org/>`_

svox (only if you want to use this TTS engline)

Gentoo/Linux
------------

app-accessibility/svox in overlay 'ikelos'

dev-python/ipodshuffle in overlay 'observer'

PyPi
----
::

    pip3 install ipodshuffle


Easy to use
===========
::

    # enable "voiceover" first
    teresa set -b ipod_test -v true

    # sync audio files. I got Chinese, Japenese and English id3 title, and use "voicerss" TTS engine.
    teresa sync -b ipod_test -s ipod_src -l zh-cn,ja-jp,en-gb -e voicerss -k d279f919f7384d3bafa5c6caad0eae56


`ipod_src structure <http://ipodshuffle.readthedocs.org/en/latest/teresa/index.html#source-path-folder-structure>`_


Read the docs
=============

http://ipodshuffle.readthedocs.org/


Note
====

This program not compatible with iTunes, and it may destroy data on your iPod.