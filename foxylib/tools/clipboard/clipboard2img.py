#!/usr/bin/env python

from PIL import ImageGrab
import sys
import os.path


def main():
    ofile = sys.argv[1]

    im = ImageGrab.grabclipboard()
    filename_ext = os.path.splitext(ofile)

    dirpath = os.path.dirname(ofile)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath)

    im.save(ofile, filename_ext[1][1:])


if __name__ == "__main__":
    main()
