
import abc
import collections
import struct

Face = collections.namedtuple('Face',
    ['verts',
    ]

Vert = collections.namedtuple('Vert',
    ['x', 'y', 'z',
    ]

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
        rec_size = struct.calcsize(self._struct_fmt)
        assert self._size % rec_size == 0
        for idx in range(self._size // rec_size):
            out = self._bsp_file.read(self._size)
            assert len(out) == self._size
            yield out
    
    @abstractmethod
    def _rec_from_internal_tuple(internal_tuple):
        raise NotImplementedError

    def _read_rec(rec_bytes):
        """
        Read a record from the lump.

        Update self._bsp_file with the data from the lump.

        """
        unpacked = struct.unpack(self._struct_fmt, rec_bytes)

        self._read_from_unpacked(unpacked)

    def read():
        """
        Read the lump.

        Update self._bsp_file with the data from the lump.
        
        """
        for rec_bytes in self._records:
            self._read_rec(rec_bytes)

@_lump_class(_LumpEnum.VERTEXES)
class _VertexLump(_Lump):
    """
    The vertexes lump stores lists of vertices used to describe faces. There
    are a total of length / sizeof(vertex) records in the lump, where length is
    the size of the lump itself, as specified in the lump directory.

    0 float[3] position   Vertex position.
    3 float[2][2] texcoord    Vertex texture coordinates. 0=surface, 1=lightmap.
    7 float[3] normal Vertex normal.
    10 ubyte[4] color  Vertex color. RGBA.

    """

    _struct_fmt = "<f<f<f<f<f<f<f<f<f<fBBBB"

    def _start_read(self):
        self._bsp_file.verts = []

    def _read_from_unpacked(self, unpacked): 
        self._bsp_file.verts.append(
            Vert(x=unpacked[0],
                 y=unpacked[1],
                 z=unpacked[2]))


@_lump_class(_LumpEnum.FACES)
class _FaceLump(_Lump):
    """
    The faces lump stores information used to render the surfaces of the map.

    0  int texture Texture index.
    1  int effect  Index into lump 12 (Effects), or -1.
    2  int type    Face type. 1=polygon, 2=patch, 3=mesh, 4=billboard
    3  int vertex  Index of first vertex.
    4  int n_vertexes  Number of vertices.
    5  int meshvert    Index of first meshvert.
    6  int n_meshverts Number of meshverts.
    7  int lm_index    Lightmap index.
    8  int[2] lm_start Corner of this face's lightmap image in lightmap.
    10 int[2] lm_size  Size of this face's lightmap image in lightmap.
    12 float[3] lm_origin  World space origin of lightmap.
    15 float[2][3] lm_vecs World space lightmap s and t unit vectors.
    21 float[3] normal Surface normal.
    24 int[2] size Patch dimensions.

    """

    _struct_fmt = "<I<I<I<I<I<I<I<I<I<I<I<I<f<f<f<f<f<f<f<f<f<f<f<f<I<I"

    def _start_read(self):
        self._bsp_file.faces = []

    def _read_from_unpacked(self, unpacked): 
        vert_indices = range(unpacked[3], unpacked[3] + unpacked[4])
        self._bsp_file.faces.append(
            Face(verts=[self._bsp_file.verts[i] for i in vert_indices])) 


class Bsp():
    def __init__(self, bsp_file): 
    def faces():


