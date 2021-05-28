import copy
import json
import logging
from pprint import pprint

from logzio.handler import LogzioHandler


# https://app.logz.io/#/dashboard/send-your-data/log-sources/python
class HdocFormatter(logging.Formatter):
    def format(self, record):
        """
        Automatically json.dumps object if message is dict or list
        :param record:
        :return:
        """
        def record_in2out(record_in):
            if not isinstance(record_in.msg, (list, dict)):
                return record_in

            pprint(record_in.msg)

            record_out = copy.deepcopy(record)
            # https://stackoverflow.com/a/15538391
            record_out.msg = json.dumps(record.msg, default=lambda o: o.__dict__)
            return record_out

        # raise Exception()
        return super(HdocFormatter, self).format(record_in2out(record))


class LogzioTool:
    @classmethod
    def formatter_default(cls):
        # formatter = logging.Formatter(validate=False)
        formatter = HdocFormatter(validate=False)
        return formatter

    @classmethod
    def level_default(cls):
        return logging.INFO

    @classmethod
    def token2handler(cls, token):
        handler = LogzioHandler(token, logs_drain_timeout=5)
        handler.setFormatter(cls.formatter_default())
        # handler.setLevel(level)
        return handler
