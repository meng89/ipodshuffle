ipodshuffle
===========

ipodshuffle is a Python Project for iPod Shuffle 4th generation.

It contain a few modules to handle "iTunesSD".

And a cli tool "teresa" for sync audio files.

With TTS engine "voicerss", it can speak lot of languages naturally, include English, Chinese, Japanese and Korean.

Easy to use
-----------
::

    teresa set -b ipod_test -v true
    teresa sync -b ipod_test -s ipod_src -l zh-cn,ja-jp,en-gb -e voicerss -k d279f919f7384d3bafa5c6caad0eae56


`ipod_src structure <http://ipodshuffle.readthedocs.org/en/latest/teresa/index.html#source-path-folder-structure>`_

Installation
============

Dependencies
------------

Python 3

`mutagen <https://bitbucket.org/lazka/mutagen>`_

`langid <https://github.com/saffsd/langid.py>`_

`Babel <http://babel.pocoo.org/>`_

svox

Gentoo/Linux
------------

app-accessibility/svox in overlay 'ikelos'

dev-python/ipodshuffle in overlay 'observer'

PyPi
----
::

    pip3 install ipodshuffle

install svox yourself if you want to use svox tts engine


Read the docs
=============

http://ipodshuffle.readthedocs.org/

note
====

This program not compatible with iTunes.
