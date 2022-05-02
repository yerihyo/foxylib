import logging
from dataclasses import dataclass
from pprint import pformat, pprint
from typing import Iterable, List

from future.utils import lmap

from foxylib.tools.collections.collections_tool import smap
from foxylib.tools.json.json_tool import JsonTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.log.logger_tool import LoggerTool


class YoutubeCommentthreadTool:
    @classmethod
    def hdoc2id(cls, hdoc):
        return hdoc.get('id') if hdoc else None

    # @classmethod
    # def hdoc2replies(cls, hdoc):
    #     return hdoc.get('replies') if hdoc else None

    @classmethod
    def video_id2items(cls, video_id, service, next_page_token_init=None) -> Iterable[dict]:
        # https://developers.google.com/youtube/v3/docs/commentThreads/list

        logger = FoxylibLogger.func_level2logger(cls.video_id2items, logging.DEBUG)

        # if not part:
        #     part = "snippet"

        next_page_token = next_page_token_init
        page_index = -1
        id_set = set([])

        while page_index < 0 or next_page_token:
            page_index += 1

            request = service.commentThreads().list(
                part='snippet,replies',
                videoId=video_id,
                pageToken=next_page_token,
            )
            response = request.execute()

            # logger.debug(pformat({
            #     "response": response
            # }))

            next_page_token = response.get('nextPageToken')
            items = response.get("items")

            id_set_this = smap(cls.hdoc2id, items)
            id_set_duplicate = id_set & id_set_this
            if id_set_duplicate:
                raise Exception({
                    'page_index': page_index,
                    'id_set': id_set,
                    'id_set_this': id_set_this,
                    'id_set_duplicate': id_set_duplicate,
                })
            id_set |= id_set_this

            logger.debug(pformat({
                'page_index': page_index,
                'next_page_token': next_page_token,
                'len(items)': len(items),
            }))
            # LoggerTool.logger2flush_handlers(logger)

            if not items:
                return

            yield from items

    class Item:
        # @classmethod
        # def jdoc2id(cls, jdoc):
        #     return jdoc.get('id') if jdoc else None

        # @classmethod
        # def jdoc2text(cls, jdoc):
        #     jdoc_comment = cls.jdoc2topLevelComment(jdoc)
        #     return YoutubeCommentthreadTool.Comment.jdoc2textOriginal(jdoc_comment)

        @classmethod
        def jdoc2topLevelComment(cls, jdoc) -> dict:
            logger = FoxylibLogger.func_level2logger(cls.jdoc2topLevelComment, logging.DEBUG)

            try:
                return JsonTool.down(jdoc, ['snippet', 'topLevelComment'])
            except:
                logger.debug(pformat({'item': jdoc}))
                raise

        @classmethod
        def jdoc2replyComments(cls, jdoc) -> List[dict]:
            logger = FoxylibLogger.func_level2logger(cls.jdoc2replyComments, logging.DEBUG)

            try:
                return JsonTool.down(jdoc, ['snippet', 'replies', 'comments'])
            except:
                logger.debug(pformat({'item': jdoc}))
                raise

        # @classmethod
        # def jdoc2publishedAt(cls, jdoc) -> str:
        #     topLevelComment = cls.jdoc2topLevelComment(jdoc)
        #     return YoutubeCommentthreadTool.Comment.jdoc2publishedAt(topLevelComment)

        # @classmethod
        # def jdoc2likeCount(cls, jdoc) -> int:
        #     comment = cls.jdoc2topLevelComment(jdoc)
        #     return YoutubeCommentthreadTool.Comment.jdoc2likeCount(comment)

        @classmethod
        def jdoc2comments(cls, jdoc_in) -> List[dict]:
            return [
                cls.jdoc2topLevelComment(jdoc_in),
                *(cls.jdoc2replyComments(jdoc_in) or []),
            ]

    class Comment:
        @classmethod
        def jdoc2id(cls, comment) -> str:
            return comment.get('id') if comment else None

        @classmethod
        def jdoc2parentId(cls, comment) -> str:
            return JsonTool.down(comment, ['snippet', 'parentId'])

        @classmethod
        def jdoc2publishedAt(cls, comment) -> str:
            return JsonTool.down(comment, ['snippet', 'publishedAt'])

        @classmethod
        def jdoc2likeCount(cls, comment) -> int:
            return JsonTool.down(comment, ['snippet', 'likeCount'])

        @classmethod
        def jdoc2textOriginal(cls, jdoc) -> str:
            return JsonTool.down(jdoc, ['snippet', 'textOriginal'])

