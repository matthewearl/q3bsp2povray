
__all__ = (
    'write',
)


class _Tag():
    def __init__(self, name, *, **params):
        self.name = name
        self.params = params

    @property
    def opening_tag(self):
        return "<{} {}>".format(
            self.name,
            " ".join("{}={!r}".format(k,str(v))
                for k, v in self.params.items()))
        
    @property
    def closing_tag(self):
        return "</{}>".format(self.name)

    def __str__(self):
        return self.opening_tag + self.closing_tag

class _XmlWriter():
    def __init__(self, xml_file, scene):
        self._scene = scene
        self._xml_file = xml_file
        self._indent = 0

    def _output_line(self, line):
        self._xml_file.write("  " * self._indent + str(line) + "\n")

    def _output_lines(self, lines):
        for line in lines:
            self._output_line(line)

    @contextlib.contextmanager
    def _in_tag(self, tag):
        self._output_line(tag.opening_tag)
        self._indent += 1
        yield
        self._indent -= 1
        self._output_line(tag.closing_tag)

    def _write_mesh(self):
        with self._in_tag(_Tag("mesh")):
            for tri in self._scene.tris:
                for point in tri:
                    self._output_line(_Tag("p",
                                      x=point[0],
                                      y=point[1],
                                      z=point[2])):

            for idx, tri in scene.tris:
                self._output_line(_Tag("f",
                                  a=(3 * idx),
                                  b=(3 * idx + 1),
                                  c=(3 * idx + 2)))

    def _write_lights(self):
        for light in self._scene.lights:
            with self._in_tag(_Tag("light")):
                self._output_line(_Tag("from",
                                       x=light.location[0],
                                       y=light.location[1],
                                       z=light.location[2]))

                self._output_line(_Tag("power",
                                       fval=light.intensity,

                if hasattr(light, "color"):
                    self._output_line(_Tag("color",
                                           r=light.color[0],
                                           g=light.color[1],
                                           b=light.color[2]))



    def _write(self):

        self._write_mesh()
        self._write_camera()
        self._write_render()
        self._write_lights()





def write(xml_file, scene):
