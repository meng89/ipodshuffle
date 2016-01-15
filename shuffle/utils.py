import os


def get_md5(file):
    import hashlib
    m = hashlib.md5()
    f = open(file, 'rb')
    while True:
        data = f.read(10240)
        if data:
            m.update(data)
        else:
            break
    return m.hexdigest
get_checksum = get_md5


def split_by_step(data, step):
    return [data[i:i+step] for i in range(0, len(data), step)]


def text_to_speech_from_google(text, lang, filename):
    import urllib.request
    import subprocess
    quote_text = urllib.request.quote(text)
    headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;"
                             " .NET CLR 1.0.3705; .NET CLR 1.1.4322; .NET CLR 1.2.30703)"}
    url = urllib.request.Request('https://translate.google.com/translate_tts?tl=' +
                                 lang+'&q='+quote_text, headers=headers)
    response = urllib.request.urlopen(url)
    p = subprocess.Popen(['/usr/bin/lame', '--decode', '--mp3input', '-', filename],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.stdin.write(response.read())
tts = text_to_speech_from_google


def ifb(data):
    return int.from_bytes(data, byteorder='little')


def itb(num, length):
    return num.to_bytes(length=length, byteorder='little')


def is_able_file(filename):
    extension = os.path.splitext(filename)[1]
    if extension.lower() in ('mp3', 'acc', 'm4b'):
        return extension
    else:
        return False