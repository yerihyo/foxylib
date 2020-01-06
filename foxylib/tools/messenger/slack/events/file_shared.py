import logging

from foxylib.tools.log.foxylib_logger import FoxylibLogger


class FileSharedEvent:
    NAME = "file_shared"

    @classmethod
    def j_event2j_file_list(cls, j_event):
        logger = FoxylibLogger.func_level2logger(cls.j_event2j_file_list, logging.DEBUG)
        logger.debug({"j_event": j_event})

        j_file_list = j_event.get("files", [])
        return j_file_list


"""
{
  "type": "message",
  "data": {
    "text": "this is user input content",
    "files": [
      {
        "id": "FS9774SEL",
        "created": 1578118981,
        "timestamp": 1578118981,
        "name": "20181113.txt",
        "title": "20181113.txt",
        "mimetype": "text/plain",
        "filetype": "text",
        "pretty_type": "Plain Text",
        "user": "URGTKN3R7",
        "editable": true,
        "size": 6617,
        "mode": "snippet",
        "is_external": false,
        "external_type": "",
        "is_public": false,
        "public_url_shared": false,
        "display_as_bot": false,
        "username": "",
        "url_private": "https://files.slack.com/files-pri/TRT5T32CQ-FS9774SEL/20181113.txt",
        "url_private_download": "https://files.slack.com/files-pri/TRT5T32CQ-FS9774SEL/download/20181113.txt",
        "permalink": "https://napoleonbakery.slack.com/files/URGTKN3R7/FS9774SEL/20181113.txt",
        "permalink_public": "https://slack-files.com/TRT5T32CQ-FS9774SEL-d625ef053c",
        "edit_link": "https://napoleonbakery.slack.com/files/URGTKN3R7/FS9774SEL/20181113.txt/edit",
        "preview": "##### NEW BOTLET: report item missing\n\n\n# botlet\n[cortex-local:5beb53c051a13d08e923d22d]",
        "preview_highlight": "<div class=\"CodeMirror cm-s-default CodeMirrorServer\" oncopy=\"if(event.clipboardData){event.clipboardData.setData('text/plain',window.getSelection().toString().replace(/\\u200b/g,''));event.preventDefault();event.stopPropagation();}\">\n<div class=\"CodeMirror-code\">\n<div><pre>##### NEW BOTLET: report item missing</pre></div>\n<div><pre></pre></div>\n<div><pre></pre></div>\n<div><pre># botlet</pre></div>\n<div><pre>[cortex-local:5beb53c051a13d08e923d22d]</pre></div>\n</div>\n</div>\n",
        "lines": 233,
        "lines_more": 228,
        "preview_is_truncated": true,
        "is_starred": false,
        "has_rich_preview": false
      }
    ],
    "upload": true,
    "blocks": [
      {
        "type": "rich_text",
        "block_id": "oT0wd",
        "elements": [
          {
            "type": "rich_text_section",
            "elements": [
              {
                "type": "text",
                "text": "this is user input content"
              }
            ]
          }
        ]
      }
    ],
    "user": "URGTKN3R7",
    "display_as_bot": false,
    "team": "TRT5T32CQ",
    "client_msg_id": "35a2a1e1-3ee8-4008-a5b5-b5039b523de4",
    "user_team": "TRT5T32CQ",
    "source_team": "TRT5T32CQ",
    "channel": "CRT63AUER",
    "event_ts": "1578118982.000100",
    "ts": "1578118982.000100"
  }
}
"""
