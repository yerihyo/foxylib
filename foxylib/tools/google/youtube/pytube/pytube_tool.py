# importing the module
# from pytube import YouTube, StreamQuery


"""
Not working as of 2022.01.19
"""
import os

import ffmpeg
from pytube import YouTube


class PytubeTool:
    # @classmethod
    # def url2youtube(cls, url):
    #     try:
    #         # object creation using YouTube
    #         # which was imported in the beginning
    #         return YouTube(url)
    #     except:
    #         print("Connection Error")  # to handle exception

    @classmethod
    def url2videofile(cls, url, outdir, tmp_prefix=None):
        # https://www.geeksforgeeks.org/pytube-python-library-download-youtube-videos/

        # where to save
        # SAVE_PATH = "E:/"  # to_do

        # link of the video to be downloaded
        # link = "https://www.youtube.com/watch?v=xWOoBJUqlbI"

        # object creation using YouTube
        # which was imported in the beginning
        youtube = YouTube(url)

        if not tmp_prefix:
            tmp_prefix = '/tmp/foxylib/pytube/video'

        if not os.path.exists(os.path.dirname(tmp_prefix)):
            os.makedirs(os.path.dirname(tmp_prefix))

        if not os.path.exists(outdir):
            os.makedirs(outdir)
        # pprint({'youtube.js':youtube.js})

        # ofolder_path = '/Users/moonyoungkang/Downloads/표전/climatechange/series/5_carbon_neutral_2050_car/video'
        # ofile_prefix = f'{ofolder_path}/youtube_download'
        tmpfile_video = f'{tmp_prefix}.video.mp4'
        tmpfile_audio = f'{tmp_prefix}.audio.mp4'
        tmp_final = f'{tmp_prefix}.mp4'

        video = youtube.streams.filter(adaptive=True, file_extension='mp4') \
            .order_by('resolution') \
            .desc() \
            .first()

        # if not ofilepath:
        if os.path.exists(tmpfile_video):
            os.unlink(tmpfile_video)
        video.download(filename=tmpfile_video)

        if os.path.exists(tmpfile_audio):
            os.unlink(tmpfile_audio)
        youtube.streams.filter(only_audio=True, file_extension='mp4') \
            .first().download(filename=tmpfile_audio)

        if os.path.exists(tmp_final):
            os.unlink(tmp_final)
        input_video = ffmpeg.input(tmpfile_video)
        input_audio = ffmpeg.input(tmpfile_audio)
        ffmpeg.concat(input_video, input_audio, v=1, a=1).output(tmp_final).run()

        ofilepath = os.path.join(outdir, video.default_filename)
        if os.path.exists(ofilepath):
            os.unlink(ofilepath)
        os.rename(tmp_final, ofilepath)
