
import hashlib
import os


def get_all_files(dire):
    files = []
    for top, sub_dirs, names in os.walk(dire, followlinks=True):
        files.extend([os.path.join(top, name) for name in names])
    return files


def get_checksum(path):
    source = open(path, 'rb')
    m = hashlib.md5()
    while True:
        data = source.read(10240)
        if data:
            m.update(data)
        else:
            break
    source.close()
    checksum = m.hexdigest()
    return checksum


def get_mtime_size(path):
    return os.path.getmtime(path), os.path.getsize(path)
