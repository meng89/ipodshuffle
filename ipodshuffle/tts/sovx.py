from tempfile import TemporaryDirectory


def tts(text, lang):
    path = None

    cmd = 'pico2wave --wave={} --lang={} {}'.format(path, lang, text)

    return


langs = [
    ['en-US'],
    ['en-GB'],
    ['de-DE'],
    ['es-ES'],
    ['fr-FR'],
    ['it-IT'],
]
