import logging
from collections import Iterable
from dataclasses import dataclass

from foxylib.tools.log.foxylib_logger import FoxylibLogger


class YoutubeCommentTool:
    @dataclass(frozen=True)
    class Schema:
        pass

    @classmethod
    def video_id2hdocs(cls, video_id, service,) -> Iterable:
        # https://developers.google.com/youtube/v3/docs/commentThreads/list

        logger = FoxylibLogger.func_level2logger(cls.video_id2hdocs, logging.DEBUG)

        # if not part:
        #     part = "snippet"

        next_page_token = None
        is_first = True

        while is_first or next_page_token:
            is_first = False

            request = service.commentThreads().list(part='snippet,replies', videoId=video_id,)
            response = request.execute()

            logger.debug({"response": response})

            next_page_token = response.get('next_page_token')
            items = response.get("items")
            if not items:
                return

            yield from items


        #
        # item = l_singleton2obj(items)
        #
        # return item.get("liveStreamingDetails")

