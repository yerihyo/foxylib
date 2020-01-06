import logging
import os
import sys

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.jinja2.jinja2_tool import Jinja2Tool


def main():
    logger = FoxylibLogger.func_level2logger(main, logging.DEBUG)

    str_in = sys.stdin.read()

    h_env = dict(os.environ)
    str_out = Jinja2Tool.tmplt_str2str(str_in, h_env)

    logger.debug({"str_in":str_in,
                  "str_out": str_out,
                  })

    print(str_out)

if __name__== "__main__":
    FoxylibLogger.attach_stderr2loggers(logging.DEBUG)
    main()