
import os
import os.path

class FileSystem():
    def __init__(self, pk3_files):
        pass

    @classmethod
    def from_dir(cls, path):
        pk3_files = (full for full in
                        (os.path.join(path, base)
                            for base in os.listdir(path))

                        os.path.isfile(full) and

