
import os
import os.path
import zipfile

class FileSystem():
    def __init__(self, pk3_paths):
        """Initialize a Q3 Filesystem given a list of PK3 files."""
        zip_files = [zipfile.ZipFile(pk3_path) for
                        pk3_path in pk3_paths]

    @classmethod
    def from_dir(cls, path):
        """Initialise a Q3 Filesystem given a base directory."""
        pk3_paths = (full for full in
                        (os.path.join(path, base)
                            for base in os.listdir(path))
                        full.endswith(".pk3") and
                        os.path.isfile(full))
        return cls(pk3_files)

    def open(path):
        """Open a file as a file-like object."""

        for zip_file in zip_files:
            if path in zip_file.namelist():
                return zip_file.open(path)

        raise KeyError("There is no item named {} in the filesystem".format(
                                path))

