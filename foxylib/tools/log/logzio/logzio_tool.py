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
        def record_in2out(record_in_):
            if not isinstance(record_in_.msg, (list, dict)):
                return record_in_

            # pprint(record_in_.msg)

            record_out_ = copy.deepcopy(record_in_)
            # https://stackoverflow.com/a/15538391
            record_out_.msg = json.dumps(record_in_.msg, default=lambda o: o.__dict__)
            return record_out_

        # raise Exception()
        record_out = record_in2out(record)
        # pprint({
        #     'record.msg': record.msg,
        #     'record_out.msg': record_out.msg,
        # })
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

    @classmethod
    def token2handler(cls, token):
        handler = LogzioHandler(token, logs_drain_timeout=3)
        handler.setFormatter(cls.formatter_default())
        # handler.setLevel(level)
        return handler
