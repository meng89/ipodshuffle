ipodshuffle
===========

ipodshuffle is a Python Project to manage iPod Shuffle 4th generation.

It contain a few modules to handle "iTunesSD"

And a cli tool "teresa" for sync audio files,
with TTS engine "voicerss", it can speak lot of languages naturally, include English, Chinese, Japanese and Korean.

Dependencies:
=============

Python 3

`mutagen <https://bitbucket.org/lazka/mutagen>`_ >= 1.27

`langid <https://github.com/saffsd/langid.py>`_

`svox(PicoSpeaker) <http://picospeaker.tk/readme.php>`_

Installation
============

Gentoo/Linux
------------

app-accessibility/svox in Overlay "ikelos"

dev-python/ipodshuffle in Overlay "observer"

PyPi
----
::

    pip3 install ipodshuffle

if you use svox engine, try install svox package in the distribution

Usage & Modules API
===================
see http://ipodshuffle.readthedocs.org/ 
