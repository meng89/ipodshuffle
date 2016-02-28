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

svox (if you use this tts engine)

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

If you use svox engine, try install svox package in your Linux distribution

Usage & Modules API
===================

see http://ipodshuffle.readthedocs.org/ 


note
====

This program not compatible with iTunes.
