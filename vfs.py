import zipfile
import os

class VirtualFileSystem:
    def __init__(self, archive_path):
        self.archive = zipfile.ZipFile(archive_path, 'r')

    def exists(self, path):
        return any(info.filename == path for info in self.archive.infolist())

    def is_directory(self, path):
        return any(info.filename.startswith(f"{path}/") for info in self.archive.infolist())

    def is_regular_file(self, path):
        return self.exists(path) and not self.is_directory(path)

    def list_dir(self, path):
        if not self.is_directory(path):
            raise NotADirectoryError(f"'{path}' is not a directory.")
        entries = [info.filename[len(path):].lstrip("/") for info in self.archive.infolist() if info.filename.startswith(path)]
        return sorted(set(entries))

    def open(self, path, mode='r'):
        if 'b' in mode:
            return self.archive.open(path, mode)
        else:
            return self.archive.open(path, mode).read().decode('utf-8')
