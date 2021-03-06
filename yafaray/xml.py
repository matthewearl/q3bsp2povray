
__all__ = (
    'write',
)

import contextlib

#@@@ Make these more general and not hardcoded.
_OUTPUT_SIZE = (800, 600)
_CAMERA_FOCAL = 0.5
_INTEGRATOR = "photon"

class _Tag():
    def __init__(self, _tag_name, **params):
        self.name = _tag_name
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
        num_tris = len(list(self._scene.tris))
        with self._in_tag(_Tag("mesh",
                               vertices=(3 * num_tris),
                               faces=num_tris)):
            for tri in self._scene.tris:
                for point in tri:
                    self._output_line(_Tag("p",
                                      x=point[0],
                                      y=point[1],
                                      z=point[2]))

            for idx, tri in enumerate(self._scene.tris):
                self._output_line(_Tag("set_material", sval=tri.material.name))
                self._output_line(_Tag("f",
                                  a=(3 * idx),
                                  b=(3 * idx + 1),
                                  c=(3 * idx + 2)))

    def _write_lights(self):
        for idx, light in enumerate(self._scene.lights):
            with self._in_tag(_Tag("light",
                                   name="light{}".format(idx))):
                self._output_line(_Tag("type",
                                       sval="pointlight"))
                self._output_line(_Tag("from",
                                       x=light.location[0],
                                       y=light.location[1],
                                       z=light.location[2]))

                # Multiplicand chosen to "look right"
                self._output_line(_Tag("power",
                                       fval=(30. * light.intensity)))

                if hasattr(light, "color"):
                    self._output_line(_Tag("color",
                                           r=light.color[0],
                                           g=light.color[1],
                                           b=light.color[2]))

    def _write_camera(self):
        with self._in_tag(_Tag("camera", name="cam")):
            self._output_line(_Tag("type", sval="perspective"))
            self._output_line(_Tag("up",
                                   x=self._scene.camera.location[0],
                                   y=(1. + self._scene.camera.location[1]),
                                   z=self._scene.camera.location[2]))
            self._output_line(_Tag("from",
                                   x=self._scene.camera.location[0],
                                   y=self._scene.camera.location[1],
                                   z=self._scene.camera.location[2]))
            self._output_line(_Tag("to",
                                   x=self._scene.camera.look_at[0],
                                   y=self._scene.camera.look_at[1],
                                   z=self._scene.camera.look_at[2]))
            self._output_line(_Tag("resx",
                                   ival=_OUTPUT_SIZE[0]))
            self._output_line(_Tag("resy",
                                   ival=_OUTPUT_SIZE[1]))
            self._output_line(_Tag("focal",
                                   fval=_CAMERA_FOCAL))

    def _write_materials(self):
        for mat in self._scene.materials.values():
            with self._in_tag(_Tag("material", name=mat.name)):
                self._output_line(_Tag("type",
                                       sval="shinydiffusemat"))
                self._output_line(_Tag("color",
                                       r=mat.color[0],
                                       g=mat.color[1],
                                       b=mat.color[2],
                                       a=1))

    def _write_render(self):
        self._xml_file.write(""" 
<background name="world_background">
	<color r="0.437557" g="0.546283" b="1" a="1"/>
	<power fval="1"/>
	<type sval="constant"/>
</background>

<integrator name="photon">
	<bounces ival="3"/>
	<caustic_mix ival="5"/>
	<diffuseRadius fval="1"/>
	<fg_bounces ival="3"/>
	<fg_samples ival="32"/>
	<finalGather bval="true"/>
	<photons ival="200000"/>
	<raydepth ival="4"/> <search ival="150"/>
	<shadowDepth ival="2"/>
	<show_map bval="true"/>
	<transpShad bval="false"/>
	<type sval="photonmapping"/>
	<use_background bval="false"/>
</integrator>

<integrator name="direct">
	<raydepth ival="0"/>
	<type sval="directlighting"/>
</integrator>

<integrator name="volintegr">
	<type sval="none"/>
</integrator>

<render>
	<AA_inc_samples ival="2"/>
	<AA_minsamples ival="4"/>
	<AA_passes ival="2"/>
	<AA_pixelwidth fval="1.5"/>
	<AA_threshold fval="0.05"/>
	<background_name sval="world_background"/>
	<camera_name sval="cam"/>
	<clamp_rgb bval="true"/>
	<filter_type sval="mitchell"/>
	<gamma fval="2.2"/>
	<integrator_name sval="{integrator}"/>
	<threads ival="8"/>
	<volintegrator_name sval="volintegr"/>
	<width ival="{width}"/>
	<height ival="{height}"/>
	<xstart ival="0"/>
	<ystart ival="0"/>
	<z_channel bval="true"/>
</render>
""".format(width=_OUTPUT_SIZE[0],
           height=_OUTPUT_SIZE[1],
           integrator=_INTEGRATOR))
            
    def write(self):
        with self._in_tag(_Tag("scene", type="triangle")):
            self._write_materials()
            self._write_camera()
            self._write_lights()
            self._write_render()
            self._write_mesh()

def write(xml_file, scene):
    """
    Write a scene to an XML file

    """

    xml_writer = _XmlWriter(xml_file, scene)
    xml_writer.write()


