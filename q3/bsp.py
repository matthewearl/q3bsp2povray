
import abc
import collections
import struct

class _LumpEnum:
    ENTITIES = 0
    TEXTURES = 1
    PLANES = 2
    NODES = 3
    LEAFS = 4
    LEAFFACES = 5
    LEAFBRUSHES = 6
    MODELS = 7
    BRUSHES = 8
    BRUSHSIDES = 9
    VERTEXES = 10
    MESHVERTS = 11
    EFFECTS = 12
    FACES = 13
    LIGHTMAPS = 14
    LIGHTVOLS = 15
    VISDATA = 16

_lump_classes = {}

def _lump_class(lump_num):
    def decorator(cls):
        lump_classes[lump_num] = cls
        return cls
    
class _Lump(metaclass=abc.ABCMeta):
    @abstractmethod
    def __init__(self, bsp_file, offset, size):
        """Initialize the lump."""
        self._bsp_file = bsp_file
        self._offset = offset
        self._size = size

    def _records():
        """
        Generate bytes objects, each one containing the data for a record from
        this chunk.
        
        """
        self._bsp_file.seek(self._offset)
        assert self._size % self._record_size == 0
        for idx in range(self._size // self._record_size):
            out = self._bsp_file.read(self._size)
            assert len(out) == self._size
            yield out

    def _read_rec(rec_bytes):
        """
        Read a record from the lump.

        Update self._bsp_file with the data from the lump.

        """
        raise NotImplementedError

    @abstractmethod
    def read():
        """
        Read the lump.

        Update self._bsp_file with the data from the lump.
        
        """
        for rec_bytes in self._records:
            self._read_rec(rec_bytes)

Face = collections.namedtuple('Face',
    ['verts',
    ]

@_lump_class(_LumpEnum.FACES)
class _FaceLump(_Lump):
    _record_size = (26 * 4)
    def read_rec(rec_bytes):
        


class Bsp():
    def __init__(self, bsp_file):

    def faces():


