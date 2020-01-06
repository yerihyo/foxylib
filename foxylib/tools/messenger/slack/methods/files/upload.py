import os

from foxylib.tools.file.file_tool import FileTool
from foxylib.tools.messenger.slack.slack_tool import SlackFiletype

# https://api.slack.com/methods/files.upload
class FilesUploadMethod:
    @classmethod
    def invoke(cls, web_client, channel, filepath):
        mimetype = FileTool.filepath2mimetype(filepath)
        filetype = SlackFiletype.mimetype2filetype(mimetype)

        j_files_upload_in = {"channels": channel,
                             "file": filepath,
                             "filename": os.path.basename(filepath),
                             "filetype": filetype,
                             }

        response = web_client.files_upload(**j_files_upload_in)
        return response

    @classmethod
    def j_response2j_file(cls, j_response):
        return j_response.get("file")