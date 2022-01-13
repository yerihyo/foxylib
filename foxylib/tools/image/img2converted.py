#!/usr/bin/env python

from PIL import Image
import sys
import os.path


def main():
    infile = sys.argv[1]
    ofile = sys.argv[2]

    im = Image.open(infile).convert("RGB")

    filename_ext = os.path.splitext(ofile)
    dirpath = os.path.dirname(ofile)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath)

    im.save(ofile, filename_ext[1][1:])


if __name__ == "__main__":
    main()
