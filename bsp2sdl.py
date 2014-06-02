__all__ = (
    'main',
    'BspScene',
)

from pprint import pprint
import argparse 
import pprint
import sys

import povray.sdl
import q3.bsp
import q3.fs


class _BspCamera():
    VIEW_CLASS = 'info_player_intermission'

    def _get_entity(field, val):
        ents = [ent for ent in bsp.entities
                if ent[field] == val]
        assert len(ents) == 1
        return ents[0]

    def __init__(self, bsp):
        self.up = "z"
        
        view_ent = self._get_entity('classname', VIEW_CLASS)
        target_ent = self._get_entity('targetname', view_ent["target"])

        self.comment = "view_ent:\n"
        self.commant += pprint.pformat(view_ent, 4)
        self.comment += "target_ent:\n"
        self.comment += pprint.pformat(target_ent, 4)

        self.location = view_ent["origin"]
        self.direction = tuple(a - b for a, b in zip(target_ent["origin"],
                                                     view_ent["origin"]))

class BspScene():
    """
    An SDL scene, constructed from a `q3.bsp.Bsp` instance.

    This satifies the definition of a scene, described in `povray.sdl`.

    """
    @property
    def tris(self):
        """
        Generate triangles by using a polygon fan approach on each face.

        """
        for face in self.faces:
            assert len(face.verts) > 3
            first_vert = face.verts[0]
            for vert_idx in range(2, len(face.verts)):
                yield (first_vert,
                       face.verts[vert_idx - 1],
                       face.verts[vert_idx])

    @property
    def camera(self):



    def __init__(self, bsp):
        self._bsp = bsp




def _parse_args(in_args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseq3", "-b",
            help="Directory containing pk3 files", required=True)
    parser.add_argument("--map", "-m", help="The map to view", required=True)
    parser.add_argument("--output-file", "-o", help="SDL output file")

    args = parser.parse_args(args)
    

def main(argv):
    args = _parse_args(argv)

    sdl_file = open(args.output_file, "w") if args.output_file else sys.stdout

    fs = q3.fs.FileSystem.from_dir(args.baseq3)

    with fs.open("maps/{}.bsp".format(args.map)) as bsp_file:
        bsp = q3.bsp.Bsp(bsp_file)
        scene = BspScene(bsp)
        povray.sdl.write(sdl_file, scene)

if __name__ == "__main__":
    main(sys.argv)
