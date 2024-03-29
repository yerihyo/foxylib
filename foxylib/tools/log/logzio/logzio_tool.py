import copy
import json
import logging
from datetime import datetime
from pprint import pprint

from logzio.handler import LogzioHandler


# https://app.logz.io/#/dashboard/send-your-data/log-sources/python
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.log.logger_tool import LoggerTool


class HdocFormatter(logging.Formatter):
    def format(self, record):
        """
        Automatically json.dumps object if message is dict or list
        :param record:
        :return:
        """

        logger = FoxylibLogger.func_level2logger(self.format, logging.DEBUG)

        def dumps_default(o):
            if isinstance(o, datetime):
                return o.isoformat()

            return o.__dict__

        def record_in2out(record_in_):
            if not isinstance(record_in_.msg, (list, dict)):
                return record_in_

            # pprint(record_in_.msg)

            record_out_ = copy.deepcopy(record_in_)
            # https://stackoverflow.com/a/15538391
            record_out_.msg = json.dumps(record_in_.msg, default=dumps_default)
            return record_out_

        # raise Exception()
        record_out = record_in2out(record)
        # logger.debug({
        #     'record.msg': record.msg,
        #     'record_out.msg': record_out.msg,
        # })
        # LoggerTool.print_all_loggers()
        return super(HdocFormatter, self).format(record_out)


class LogzioTool:
    @classmethod
    def formatter_default(cls):
        # formatter = logging.Formatter(validate=False)
        formatter = HdocFormatter(validate=False)
        return formatter

    @classmethod
    def level_default(cls):
        return logging.INFO

    # @classmethod
    # def token2handler(cls, token, *_, **__):
    #     # handler = LogzioHandler(token, logs_drain_timeout=3, debug=True)
    #     handler = LogzioHandler(token, *_, **__)
    #     handler.setFormatter(cls.formatter_default())
    #     # handler.setLevel(level)
    #     return handler
