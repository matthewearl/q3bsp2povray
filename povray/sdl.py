
"""
Scene object attributes:
    .. tris::  An iterable of triangle objects (see below).
    .. camera:: A camera object (see below).
    .. lights:: An iterable of light objects (see below).

A triangle object is a triple of vertices (vertex objects). A vertex object is
a triple of coordinates.

A camera object has the following attributes::
    .. type:: (Optional.) An instance of `CameraType` describing the camera type.
    .. up:: (Optional.) One of 'x', 'y', or 'z'
    .. location:: (Optional.) Indicates the location of the camera.
    .. direction:: (Optional.) Indicates the direction of the camera.
    .. look_at:: (Optional.) Indicates an object that the camera is looking at.

A light object has the following attributes::
    .. location:: Coordinates of the light.
    .. color:: A triple representing an RGB value.
    .. intensity:: A float representing the light's intensity.

"""


__all__ = (
    'write',
    'CameraType',
)


import contextlib
import random


def _random_color():
    return (random.random(), random.random(), random.random(),)


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
        meth(self, element)

    return _wrapped


class _SdlWriter():
    def __init__(self, sdl_file, scene):
        self._scene = scene
        self._sdl_file = sdl_file
        self._indent = 0

    def _output_line(self, line):
        self._sdl_file.write("  " * self._indent + line + "\n")

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
        if hasattr(element, "comment"):
            self._output_lines("// {}".format(line)
                    for line in element.comment.splitlines())

    def _vert_to_str(self, vert):
        return "<{}>".format(", ".join(str(x) for x in vert))

    @_element_writer
    def _write_tri(self, tri):
        with self._block("triangle"):
            assert len(tri) == 3
            self._output_line(", ".join(self._vert_to_str(v) for v in tri))

            #@@@ Here so that triangles can be differentiated under uniform
            # (or no) lighting.
            #self._output_line("pigment {{ color rgb {} }}".format(
            # self._vert_to_str(_random_color())))
            with self._block("texture"):
                self._output_line("pigment { color <1., 1., 1.> }")
                self._output_line("finish { ambient .0 diffuse 1. }") 

    @_element_writer
    def _write_camera(self, cam):
        with self._block("camera"):
            if hasattr(cam, "type"):
                self._output_line(CameraType.to_str(cam.type))

            if hasattr(cam, "up"):
                assert cam.up in ("x", "y", "z")
                self._output_line("up {}".format(cam.up))
            if hasattr(cam, 'location'):
                self._output_line("location {}".format(
                    self._vert_to_str(cam.location)))

            if hasattr(cam, 'direction'):
                self._output_line("direction {}".format(
                    self._vert_to_str(cam.direction)))

            if hasattr(cam, 'look_at'):
                self._output_line("look_at {}".format(
                    self._vert_to_str(cam.look_at)))

    @_element_writer
    def _write_light(self, light):
        with self._block("light_source"):
            self._output_line(self._vert_to_str(light.location))
            color = getattr(light, "color", (1., 1., 1.))
            color = tuple(x * 0.0001 * light.intensity for x in color)

            self._output_line("color {}".format(
                self._vert_to_str(color)))

    def write(self):
        self._write_camera(self._scene.camera)
        for light in self._scene.lights:
            self._write_light(light)
        for tri in self._scene.tris:
            self._write_tri(tri)

def write(sdl_file, scene):
    """
    Write a scene to a SDL file

    """

    sdl_writer = _SdlWriter(sdl_file, scene)
    sdl_writer.write()

