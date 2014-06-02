from pprint import pprint

import q3.bsp
import q3.fs


fs = q3.fs.FileSystem.from_dir("../q3data/")

with fs.open("maps/q3dm7.bsp") as bsp_file:
    bsp = q3.bsp.Bsp(bsp_file)

    #pprint(bsp.faces)
    pprint(list(bsp.entities))

