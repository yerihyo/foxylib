import logging
import os
import sys

from future.utils import lfilter, lmap

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.env.env_tool import EnvTool
from foxylib.tools.jinja2.jinja2_tool import Jinja2Tool
from foxylib.tools.string.string_tool import str2strip


def main():
    logger = FoxylibLogger.func_level2logger(main, logging.DEBUG)

    # if len(sys.argv) < 2:
    #     print("usage: {} <listfile_filepath> <repo_dir>".format(sys.argv[0]))
    #     sys.exit(1)

    from foxylib.tools.file.file_tool import FileTool


    l = lfilter(bool, (map(str2strip,sys.stdin)))
    # tmplt_filepath = sys.argv[1]
    # env = sys.argv[2]
    # repo_dir = sys.argv[2]

    # l = lfilter(bool, map(str2strip, FileTool.filepath2utf8_lines(tmplt_filepath)))
    logger.debug({"l": l})

    h_env = dict(os.environ)

    filepath_list = lmap(lambda s:Jinja2Tool.tmplt_str2str(s.split(maxsplit=1)[1], data=h_env), l)

    # data = {"ENV": env, "REPO_DIR":repo_dir, "HOME_DIR":os.path.expanduser('~')}

    str_tmplt = "\n".join([Jinja2Tool.tmplt_file2str(fp, h_env)
                           for fp in filepath_list
                           if fp.endswith(".yaml") or fp.endswith(".yml")])

    envname_list = lfilter(bool, [h_env.get("ENV"), "_DEFAULT_"])
    kv_list = EnvTool.yaml_str2kv_list(str_tmplt, envname_list)

    str_export = "\n".join(['export {0}="{1}"'.format(k, v_yaml) for k, v_yaml in kv_list])
    print(str_export)

if __name__== "__main__":
    FoxylibLogger.attach_stderr2loggers(logging.DEBUG)
    main()