import ipodshuffle.shuffle


def set_(ipod, enable_voiceover=None, max_volume=None):
    ipod = ipodshuffle.shuffle.Shuffle(ipod)

    if enable_voiceover is not None:
        ipod.enable_voiceover = bool(enable_voiceover)

    if max_volume is not None:
        ipod.max_volume = int(max_volume)
