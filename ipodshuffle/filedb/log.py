import json
import os
import shutil
import uuid

from ipodshuffle.utils import get_checksum


class FileNotInLogError(Exception):
    pass


class FileAlreadyInError(Exception):
    pass


class JsonLog:
    """
    only read and write json file to log_path
    """
    def __init__(self, log_path):

        self._log_path = os.path.realpath(log_path)

        os.makedirs(os.path.split(self._log_path)[0], exist_ok=True)

        try:
            f = open(self._log_path)
            self._original_logs_str = f.read()
            f.close()

        except FileNotFoundError:
            self._original_logs_str = '{}'

        try:
            self._log = json.loads(self._original_logs_str)
        except ValueError:
            self._log = {}

    def write_log(self):

        new_logs_str = json.dumps(self._log, sort_keys=True, indent=4, ensure_ascii=False)

        if new_logs_str != self._original_logs_str:
            f = open(self._log_path, 'w')
            f.write(new_logs_str)
            f.flush()
            f.close()
            self._original_logs_str = new_logs_str


########################################################################################################################
########################################################################################################################


class Storage(JsonLog):
    """
    storage files, use random_name_fun to create name for new file.
    """
    def __init__(self, log_path, storage_dir, random_name_fun=None):
        super().__init__(log_path)
        self._storage_dir = storage_dir

        os.makedirs(self._storage_dir, exist_ok=True)

        self._get_random_name = random_name_fun or uuid.uuid1().hex

    def realpath(self, filename):
        return os.path.join(self._storage_dir, filename)

    # ------------------------------------------------------------------------------

    def del_log_if_file_no_exist(self):
        no_exist_in_fs_filenames = []

        for filename, info in self._log.items():
            realpath = self.realpath(filename)

            if not os.path.exists(realpath) or not os.path.isfile(realpath):
                no_exist_in_fs_filenames.append(filename)

        for filename in no_exist_in_fs_filenames:
            del self._log[filename]

        self.write_log()

    def del_log_if_file_wrong(self):
        wrong_filenames = []
        for filename, info in self._log.items():
            full_path = self.realpath(filename)

            now_mtime = os.path.getmtime(full_path)

            if info['size'] != os.path.getsize(full_path) or abs(info['mtime'] - now_mtime) > 2:
                wrong_filenames.append(filename)
                continue

            if 0 < abs(info['mtime'] - now_mtime) <= 2:
                pass
                # print("\nFile MTIMEs don't match, but very close: ", full_path)
                # print('log: {}, now: {}'.format(repr(info['mtime']), repr(os.path.getmtime(full_path))))
                # print('Just notice, nothing to do')
                # print("Interesting! I dont know why.")

        for filename in wrong_filenames:
            del self._log[filename]

        self.write_log()

    def remove_file_if_not_logged(self):
        pass

    def clean(self):
        self.del_log_if_file_no_exist()
        self.del_log_if_file_wrong()

    # ------------------------------------------------------------------------------

    def _get_new_name(self):
        new_name = None
        while True:
            new_name = self._get_random_name()
            if new_name not in self._log.keys():
                break
        return new_name

    # ------------------------------------------------------------------------------

    def get_filename(self, checksum):
        filename = None
        for _filename, metadata in self._log.items():
            if metadata['checksum'] == checksum:
                filename = _filename
                break
        return filename

    def add(self, src, checksum=None):

        checksum = checksum or get_checksum(src)

        filename = self.get_filename(checksum)
        if filename:
            raise FileAlreadyInError('file: {}'.format(filename))

        new_name = self._get_new_name()
        new_realpath = self._storage_dir + '/' + new_name

        shutil.copyfile(src, new_realpath)

        self._log[new_name] = {
            'checksum': checksum,
            'mtime': os.path.getmtime(new_realpath),
            'size': os.path.getsize(new_realpath)
        }

        self.write_log()

    # ------------------------------------------------------------------------------

    def remove(self, filename):
        os.remove(self.realpath(filename))
        del self._log[filename]

        self.write_log()
    # ------------------------------------------------------------------------------

    def get_filenames(self):
        return self._log.keys()

    def get_extra(self, filename):
        return self._log[filename].setdefault('extra', {})

    def set_extra(self, filename, extra):
        self._log[filename]['extra'] = extra

        self.write_log()
