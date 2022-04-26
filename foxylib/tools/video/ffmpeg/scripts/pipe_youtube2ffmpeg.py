import os
import subprocess
from unittest import TestCase

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)


def main():
    # https://flashphoner.com/how-to-grab-a-video-from-youtube-and-share-it-via-webrtc-in-real-time/
    # https://gist.github.com/olasd/9841772
    url = 'https://www.youtube.com/watch?v=9cQT4urTlXM'
    stream_id = 'stream1'
    key = 'ff7y-axck-03re-khyf-4fjb'
    destination = 'rtmp://a.rtmp.youtube.com/live2'

    _youtube_process = subprocess.Popen(('youtube-dl', '-f', '', '--prefer-ffmpeg', '--no-color', '--no-cache-dir',
                                         '--no-progress', '-o', '-', '-f', '22/18', url, '--reject-title',
                                         stream_id), stdout=subprocess.PIPE)
    _ffmpeg_process = subprocess.Popen(('ffmpeg', '-re', '-i', '-', '-preset', 'ultrafast', '-vcodec', 'copy',
                                        '-acodec', 'copy', '-threads', '1', '-f', 'flv',
                                        destination + "/" + key), stdin=_youtube_process.stdout)

if __name__ == '__main__':
    main() # python -m foxylib.tools.flask.foxylib_flask
