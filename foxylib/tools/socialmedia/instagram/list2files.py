#!/usr/bin/env python

# https://pencilprogrammer.com/download-instagram-image-using-python/
# python script to download instagram image
import sys
import time

from foxylib.tools.socialmedia.instagram.instagram_tool import InstagramTool


def main():
    ''' ask user to input the instagram post url '''
    # link = input("Enter Instagram Image URL: ")
    listfile = sys.argv[1]

    def file2urls():
        with open(listfile) as f:
            for s in f:
                yield s.strip()

    for url in file2urls():
        ofilepath = "instagram" + str(time.time()) + ".png"

        url_image = InstagramTool.url2url_image(url)
        InstagramTool.url_image2file(url_image, ofilepath)

    print('=== DONE ===')


if __name__ == "__main__":
    main()
