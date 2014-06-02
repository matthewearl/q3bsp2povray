
"""
Scene object attributes:
    .. tris::  An iterable of triangle objects (see below).
    .. camera:: A camera object (see below).

A triangle object is a triple of vertices (vertex objects). A vertex object is
a triple of coordinates.

A camera is ... ?

"""

__all__ = ( 
    'write',
)

import contextlib

def element_writer(meth):
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

    @contextmanager
    def _indented(self):
        """Context manager to increase the indentation level."""
        self._indent += 1
        yield
        self._indent += -1

    def _output_line(self, line):
        self._sdl_file.write("  " * indent + line + "\n")

    def _output_lines(self, lines):
        for line in lines:
            self._output_line(line)

    def _write_comment(self, element):
        if hasattr(obj, "comment"):
            self._output_lines("// {}".format(line)
                    for line in obj.comment.splitlines())
    @element_writer
    def _write_tri(self, tri):
        self._output_line("triangle")
        self._output_line("{")
        self._indent += 1
        self


        


    def write(self):
        for tri in self.scene.tris:
            self._write_triangles(tri)


def write(sdl_file, scene):
    """
    Write a scene to a .sdl file

    """

    sdl_writer = _SdlWriter(sdl_file, scene)
    sdl_writer.write()

