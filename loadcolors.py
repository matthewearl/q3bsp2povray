#!/usr/bin/env python3

"""
Load Colors

Read texture data for a Quake 3 BSP and calculate the average color for each
texture.

The output can be used as input to bsp2sdl.

Note this script requires pillow (or equivalent) to be installed.

"""

__all__ = (
    'calculate_color',
    'main'
)

import PIL


def calculate_color(fs, tex_name):
    def match(path):
        return path.lower() in (
                tex_name.lower() + ".jpg", tex_name.lower() + ".tga")

    match_iter = iter(path for path in fs.paths if match(path))
    try:
        img_path = next(match_iter)
    except StopIteration:
        raise 


def _parse_args(in_args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseq3", "-b",
            help="Directory containing pk3 files", required=True)
    parser.add_argument("--map", "-m", 
                        help="The map whose textures are to be cached",
                        required=True)

    return parser.parse_args(in_args)


def main(argv):
    args = _parse_args(argv)

    with fs.open("maps/{}.bsp".format(args.map)) as bsp_file:
        bsp = q3.bsp.Bsp(bsp_file)
        for tex_name in (tex.name for tex in bsp.textures):
            print("{} {}".format(
                calculate_color(fs, tex_name),
                name))


if __name__ == "__main__":
    main(sys.argv[1:])
