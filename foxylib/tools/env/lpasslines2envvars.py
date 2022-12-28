#!/usr/bin/env python

import logging
import os
import sys
from argparse import ArgumentParser
from pprint import pformat

import yaml
from future.utils import lfilter, lmap

from foxylib.tools.collections.collections_tool import lchain, DictTool
from foxylib.tools.env.env_tool import EnvTool
from foxylib.tools.env.yaml.filepath2envvars import Filepath2Envvar
from foxylib.tools.env.yaml.yaml_env_tool import Yaml2EnvTool, Lpassline
from foxylib.tools.jinja2.jinja2_tool import Jinja2Renderer
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.string.string_tool import str2stripped


def lpasslines_context2envvars(lpasslines, h_context, value_wrapper):
    for lpassline in lpasslines:
        filepath = Lpassline.lpassline_context2filepath(lpassline, h_context)

        yield from Filepath2Envvar.filepath_context2envvars(filepath, h_context, value_wrapper)


def main():
    logger = FoxylibLogger.func_level2logger(main, logging.DEBUG)

    h_context = dict(os.environ)
    assert "ENV" in h_context

    logger.debug(pformat({
        'h_context_major': DictTool.filter_keys(h_context, {"REPO_DIR", "HOME_DIR", "ENV"}),
    }))

    # how to output bash pipe friendly in python
    # reference: https://stackoverflow.com/q/34459274/1902064
    value_wrapper = Filepath2Envvar.args2value_wrapper(sys.argv[1:])
    for envvar in lpasslines_context2envvars(sys.stdin, h_context, value_wrapper):
        # logger.debug(pformat({'envvar':envvar}))
        print(envvar)


def main_old():
    logger = FoxylibLogger.func_level2logger(main, logging.DEBUG)

    # if len(sys.argv) < 2:
    #     print("usage: {} <listfile_filepath> <repo_dir>".format(sys.argv[0]))
    #     sys.exit(1)

    l = lfilter(bool, (map(str2stripped, sys.stdin)))
    # tmplt_filepath = sys.argv[1]
    # env = sys.argv[2]
    # repo_dir = sys.argv[2]

    # l = lfilter(bool, map(str2stripped, FileTool.filepath2utf8_lines(tmplt_filepath)))
    logger.debug({"l": l})

    h_env = dict(os.environ)

    filepath_list = lmap(lambda s:Jinja2Renderer.text2text(s.split(maxsplit=1)[1], data=h_env), l)

    # data = {"ENV": env, "REPO_DIR":repo_dir, "HOME_DIR":os.path.expanduser('~')}

    str_tmplt = "\n".join([Jinja2Renderer.textfile2text(fp, h_env)
                           for fp in filepath_list
                           if fp.endswith(".yaml") or fp.endswith(".yml")])

    envname_list = lfilter(bool, [h_env.get("ENV"), "__DEFAULT__"])
    json_yaml = yaml.load(str_tmplt, Loader=yaml.SafeLoader)
    kv_list = EnvTool.yaml_envnames2kv_list(json_yaml, h_env, envname_list)

    # logger.debug({"envname_list": envname_list})
    # logger.debug({"str_tmplt": str_tmplt})
    # logger.debug({"json_yaml": json_yaml})
    # logger.debug({"kv_list": kv_list})

    str_export_list = ['export {0}="{1}"'.format(k, v_yaml)
                       for k, v_yaml in kv_list]
    str_export = "\n".join(str_export_list)
    # logger.debug(pformat({
    #     'json_yaml':json_yaml,
    #     'kv_list':kv_list,
    #     "str_export_list": str_export_list
    # }))
    print(str_export)

if __name__== "__main__":
    FoxylibLogger.attach_stderr2loggers(logging.DEBUG)
    main()
