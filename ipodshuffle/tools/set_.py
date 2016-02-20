from ipodshuffle.shuffle import Shuffle


description = "Set enable_voiceover and max_volume"


def set_(base, enable_voiceover=None, max_volume=None):
    ipod = Shuffle(base)

    if enable_voiceover is not None:
        ipod.enable_voiceover = enable_voiceover

    if max_volume is not None:
        ipod.max_volume = max_volume

    ipod.write()

fun = set_


def get_help_strings(indet=None):
    indet = indet or 0

    s = ' ' * indet + 'usage:  base=<path> enable_voiceover=[true|false] max_volume=[0-17]\n'

    return s
