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


import argparse
import sys

from PIL import Image

import q3.bsp
import q3.fs

def _open_tex_file(fs, tex_name):
    def match(path):
        return path.lower() in (
                tex_name.lower() + ".jpg", tex_name.lower() + ".tga")

    match_iter = iter(path for path in fs.paths if match(path))
    try:
        tex_path = next(match_iter)
    except StopIteration:
        raise KeyError("Texture {} not found within FS".format(tex_name))

    return fs.open(tex_path)


def calculate_color(fs, tex_name):
    """
    Calculate the average color of a texture.

    Arguments:
        fs: Filesystem to find the texture.
        tex_name: Name of the texture to find (without extension).

    Returns:
        An RGB triple representing the average color.

    """
    tex_file = _open_tex_file(fs, tex_name)
    
    im = Image.open(tex_file)

    # This seems like an efficient method in terms of offloading as much work
    # as possible to C: Calculate the histogram, and then sum the respective
    # components. Finally, each sum by the number of pixels to obtain the
    # average.

    im = im.convert("RGB")
    hist = im.histogram()
    def _component_average(comp_hist):
        return float(sum(val * count
                    for val, count in enumerate(comp_hist))) / (
                                256. * im.size[0] * im.size[1])
    return tuple(_component_average(hist[(256 * c):(256 * (c + 1))])
                    for c in range(3))


def _parse_args(in_args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseq3", "-b",
            help="Directory containing pk3 files", required=True)
    parser.add_argument("--map", "-m", 
                        help="The map whose textures are to be cached",
                        required=True)

    return parser.parse_args(in_args)

def _color_to_hex(color):
    return "#{}".format("".join("%02X" % int(255. * c) for c in color))

def main(argv):
    args = _parse_args(argv)

    fs = q3.fs.FileSystem.from_dir(args.baseq3)

    with fs.open("maps/{}.bsp".format(args.map)) as bsp_file:
        bsp = q3.bsp.Bsp(bsp_file)
        for tex_name in (tex.name for tex in bsp.textures):
            try:
                color = calculate_color(fs, tex_name)
            except KeyError as e:
                print("!! {}".format(e))
            else:
                print(color)
                print('<span style="background-color:{};width:40;float:left;">'
                        .format(_color_to_hex(color)))
                print('x</span>')
                print("<p>{} {}</p>".format(color, tex_name))


if __name__ == "__main__":
    main(sys.argv[1:])
