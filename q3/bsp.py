import abc
import collections
import struct

from . import ents

"""
Read a BSP file.

Please see http://www.mralligator.com/q3/ for details of the file format.

"""

__all__ = (
    'Bsp',
)
    

Face = collections.namedtuple('Face',
    ['verts',
    ]) 

Vert = collections.namedtuple('Vert',
    ['x', 'y', 'z',
    ])

Texture = collections.namedtuple('Texture',
    ['name', 'flags', 'contents'])

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
    
    COUNT = 17

class _FaceType:
    POLYGON = 1
    PATCH = 2
    MESH = 3
    BILLBOARD = 4

_lump_classes = {}


def _lump_class(lump_num):
    def decorator(cls):
        _lump_classes[lump_num] = cls
        return cls
    return decorator
    

class _Lump(metaclass=abc.ABCMeta):
    """
    Abstract base class for all lump readers classes.

    """
    def __init__(self, bsp, bsp_file, offset, length):
        """Initialize the lump."""
        self._bsp = bsp
        self._bsp_file = bsp_file
        self._offset = offset
        self._length = length

    @abc.abstractmethod
    def _read(self):
        """
        Read the lump.

        Update with the data from the lump.
        
        """
        raise NotImplementedError

class _StructLump(_Lump):
    """
    A lump that is a sequence of fixed length records, each of which can be
    decoded with a `struct` module format string.

    """

    def _records(self):
        """
        Generate bytes objects, each one containing the data for a record from
        this chunk.
        
        """
        self._bsp_file.seek(self._offset)
        rec_size = struct.calcsize(self._struct_fmt)
        assert self._length % rec_size == 0
        for idx in range(self._length // rec_size):
            out = self._bsp_file.read(rec_size)
            assert len(out) == rec_size, "{} != {}".format(
                len(out), rec_size)
            yield out
    
    @abc.abstractmethod
    def _start_lump(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _read_from_unpacked(self, unpacked):
        raise NotImplementedError

    def _read_rec(self, rec_bytes):
        """
        Read a record from the lump.

        Update `self._bsp` with the data from the lump.

        """
        unpacked = struct.unpack(self._struct_fmt, rec_bytes)

        self._read_from_unpacked(unpacked)

    def _read(self):
        """
        Read the lump.

        Update with the data from the lump.
        
        """
        self._start_lump()
        for rec_bytes in self._records():
            self._read_rec(rec_bytes)

@_lump_class(_LumpEnum.VERTEXES)
class _VertexLump(_StructLump):
    """
    Please see http://www.mralligator.com/q3/#Vertexes for details of this
    lump.

    """

    _struct_fmt = "<ffffffffffBBBB"

    def _start_lump(self):
        self._bsp.verts = []

    def _read_from_unpacked(self, unpacked): 
        # Backwards ordering due to Quake 3 treating Z as up.
        self._bsp.verts.append(
            Vert(x=unpacked[0],
                 y=unpacked[2],
                 z=unpacked[1]))


@_lump_class(_LumpEnum.MESHVERTS)
class _MeshVertexLump(_StructLump):
    """
    Please see http://www.mralligator.com/q3/#Meshverts for details of this
    lump.

    """

    _struct_fmt = "<I"

    def _start_lump(self):
        self._bsp.meshverts = []

    def _read_from_unpacked(self, unpacked): 
        self._bsp.meshverts.append(unpacked[0])


@_lump_class(_LumpEnum.FACES)
class _FaceLump(_StructLump):
    """
    Please see http://www.mralligator.com/q3/#Faces for details of this
    lump.

    """

    _struct_fmt = "<IIIIIIIIIIIIffffffffffffII"

    def _start_lump(self):
        self._bsp.faces = []

    def _read_from_unpacked(self, unpacked): 
        face_type = unpacked[2]
        vertex = unpacked[3]
        n_vertexes = unpacked[4]
        meshvert = unpacked[5]
        n_meshverts = unpacked[6]
        patch_size = (unpacked[24], unpacked[25])

        if face_type in (_FaceType.POLYGON, _FaceType.MESH): 
            # `vertex` and `n_vertex` describe the vertices of the mesh/poly.
            # `meshverts` and `n_meshverts` describe the triangulation of these
            # verts.
            vert_indices = range(vertex, vertex + n_vertexes)
            verts = [self._bsp.verts[i] for i in vert_indices]

            assert n_meshverts % 3 == 0
            for idx in range(meshvert, meshvert + n_meshverts, 3):
                self._bsp.faces.append(
                        Face(verts=[verts[self._bsp.meshverts[idx + i]]
                                        for i in range(3)]))
        if face_type == _FaceType.PATCH:
            # `vertex` and `n_vertex` describe the control points of the patch.
            # The control points are a grid of size `patch_size`.
            assert patch_size[0] * patch_size[1] == n_vertexes

            verts = { (i, j):
                         self._bsp.verts[vertex + i + j * patch_size[0]]
                            for j in range(patch_size[1])
                                for i in range(patch_size[0])
                    }

            # No interpolation yet, just triangulate the control points.
            for j in range(patch_size[1] - 1):
                for i in range(patch_size[0] - 1):
                    self._bsp.faces.append(
                        Face(verts=[verts[i, j],
                                    verts[i + 1, j],
                                    verts[i + 1, j + 1]]))
                    self._bsp.faces.append(
                        Face(verts=[verts[i, j],
                                    verts[i + 1, j + 1],
                                    verts[i, j + 1]]))
        else:
            pass


@_lump_class(_LumpEnum.ENTITIES)
class _EntitiesLump(_Lump):
    """
    Please see http://www.mralligator.com/q3/#Entities for details of this
    lump.

    """
    def _read(self):
        self._bsp_file.seek(self._offset)
        ents_str = self._bsp_file.read(self._length).decode('ascii')
        self._bsp.entities = ents.parse(ents_str)


@_lump_class(_LumpEnum.TEXTURES)
class _TextureLump(_StructLump):
    """
    Please see http://www.mralligator.com/q3/#Textures for details of this
    lump.

    """

    _struct_fmt = "<64sII"

    def _start_lump(self):
        self._bsp.textures = []

    def _read_from_unpacked(self, unpacked): 
        name = unpacked[0].decode('ascii')
        null_term_idx = name.find('\x00')
        if null_term_idx != -1:
            name = name[:null_term_idx]
        self._bsp.textures.append(Texture(
            name=name,
            flags=unpacked[1],
            contents=unpacked[2]))


_LumpEntry = collections.namedtuple('_LumpEntry', ['offset', 'length'])

class Bsp():
    """
    Represents a BSP file.

    """

    def _read_lump_entry(self):
        fmt = "<II"
        unpacked = struct.unpack(fmt,
                    self._bsp_file.read(struct.calcsize(fmt)))
        return _LumpEntry._make(unpacked)

    def _read_lump_dir(self):
        self._bsp_file.seek(8)
            
        self._lump_dir = {}
        for lump_num in range(_LumpEnum.COUNT):
            self._lump_dir[lump_num] = self._read_lump_entry()
        
    def __init__(self, bsp_file): 
        self._bsp_file = bsp_file

        self._read_lump_dir()

        _lump_readers = {
            lump_num: cls(bsp=self,
                          bsp_file=self._bsp_file,
                          offset=self._lump_dir[lump_num].offset,
                          length=self._lump_dir[lump_num].length)
            for lump_num, cls in _lump_classes.items()
        }

        _lump_readers[_LumpEnum.TEXTURES]._read()
        _lump_readers[_LumpEnum.VERTEXES]._read()
        _lump_readers[_LumpEnum.MESHVERTS]._read()
        _lump_readers[_LumpEnum.FACES]._read()
        _lump_readers[_LumpEnum.ENTITIES]._read()


