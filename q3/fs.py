
import os
import os.path
import zipfile

class _SeekableFile():
    """
    Wrap a ZipFile to support more file-like methods.

    This implementation reads the entire file into memory.

    """

    def __init__(self, f):
        self._data = f.read() 
        self._offs = 0

    def seek(self, offs):
        self._offs = offs

    def tell(self):
        return self._offs

    def read(self, count):
        new_offs = self._offs + count
        out = self._data[self._offs:new_offs]
        self._offs = new_offs

        return out

class FileSystem():
    def __init__(self, pk3_paths):
        """Initialize a Q3 Filesystem given a list of PK3 files."""
        pk3_paths = sorted(pk3_paths)

        self._zip_files = [zipfile.ZipFile(pk3_path) for
                           pk3_path in pk3_paths]

        # _dir_dict maps paths onto zip files.
        self._dir_dict = {}
        for zip_file in self._zip_files:
            self._dir_dict.update(
                { name: zip_file for name in zip_file.namelist() })


    @classmethod
    def from_dir(cls, path):
        """Initialise a Q3 Filesystem given a base directory."""
        pk3_paths = (full for full in
                        (os.path.join(path, base)
                            for base in os.listdir(path))
                        if full.endswith(".pk3") and
                            os.path.isfile(full))
        return cls(pk3_paths)


    @property
    def paths(self):
        """Return an iterable of paths in the filesystem."""

        return sorted(self._dir_dict.keys())

    def open(self, path):
        """Open a file as a file-like object."""

        try:
            zip_file = self._dir_dict[path]
        except KeyError:
            raise KeyError("There is no item named {} in the "
                           "filesystem".format(path))

        return _SeekableFile(zip_file.open(path))

