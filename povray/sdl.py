
"""
Scene object attributes:
    .. tris::  An iterable of triangle objects (see below).
    .. camera:: A camera object (see below).

A triangle object is a triple of vertices (vertex objects). A vertex object is
a triple of coordinates.

A camera object has the following attributes::
    .. type:: (Optional.) An instance of `CameraType` describing the camera type.
    .. up:: (Optional.) One of 'x', 'y', or 'z'
    .. location:: (Optional.) Indicates the location of the camera.
    .. direction:: (Optional.) Indicates the direction of the camera.

"""

__all__ = ( 
    'write',
    'CameraType',
)

import contextlib

#@@@ Replace with enums
class CameraType:
    PERSPECTIVE = 1
    ORTHOGRAPHIC = 2
    FISHEYE = 3
    ULTRA_WIDE_ANGLE = 4
    OMNIMAX  = 5
    PANORAMIC  = 6
    CYLINDER = 7
    SPHERICAL = 8

    @staticmethod
    def to_str(c):
        return {
            1: "perspective",
            2: "orthographic",
            3: "fisheye",
            4: "ultra_wide_angle",
            5: "omnimax",
            6: "panoramic",
            7: "cylinder",
            8: "spherical",
        }[c]


def _element_writer(meth):
    """
    Decoroator for elements within a scene.

    An element roughly corresponds with a construct that can have curly braces
    in an SDL file, although all this decorator currently does is output any
    comments for the object, should any exist.

    """
    def _wrapped(self, element):
        self._write_comment(element)
        self.meth(element)

    return _wrapped

class _SdlWriter():
    def __init__(self, sdl_file, scene):
        self._scene = scene
        self._sdl_file = sdl_file
        self._indent = 0

    def _output_line(self, line):
        self._sdl_file.write("  " * indent + line + "\n")

    @contextlib.contextmanager
    def _block(self, name):
        """Context manager to print a block."""
        self._output_line(name)
        self._output_line("{")
        self._indent += 1
        yield
        self._indent -= 1
        self._output_line("}")

    def _output_lines(self, lines):
        for line in lines:
            self._output_line(line)

    def _write_comment(self, element):
        if hasattr(obj, "comment"):
            self._output_lines("// {}".format(line)
                    for line in obj.comment.splitlines())

    def _vert_to_str(self, vert):
        return "<{}>,".format(", ".join(x for x in vert))

    @_element_writer
    def _write_tri(self, tri):
        with self._block("triangle"):
            assert len(tri) == 3
            self._output_line(", ".join(self._vert_to_str(v) for v in tri))

    def _write_cam_type(self, cam):
        if hasattr(cam, "type")
            
    @_element_writer
    def _write_camera(self, cam):
        with self._block("camera"):
            
            self._output_line("up z")
            self._output_line("location {}".format(
            self._output_line("look_at {}".format(self._vert_to_strcam.get_target())

    def write(self):
        for tri in self.scene.tris:
            self._write_triangles(tri)


def write(sdl_file, scene):
    """
    Write a scene to a .sdl file

    """

    sdl_writer = _SdlWriter(sdl_file, scene)
    sdl_writer.write()

