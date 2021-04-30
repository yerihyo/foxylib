from contextlib import contextmanager

from werkzeug.datastructures import FileStorage


class FilestorageTool:
    @classmethod
    @contextmanager
    def filepath2filestorage(cls, filepath):
        with open(filepath, 'rb') as fp:
            storage = FileStorage(fp)
            yield storage
