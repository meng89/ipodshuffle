import os


def get_all_files(dire):
    files = []
    for top, sub_dirs, names in os.walk(dire, followlinks=True):
        files.extend([os.path.join(top, name) for name in names])
    return files
