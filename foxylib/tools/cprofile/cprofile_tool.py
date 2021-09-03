import cProfile
import os
import pstats
from datetime import datetime
from functools import wraps

import pytz

from foxylib.tools.datetime.datetime_tool import DatetimeTool
from foxylib.tools.file.file_tool import DirTool
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.native.module.module_tool import ModuleTool

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)


class CprofileTool:
    @classmethod
    def func2datetimed_filepath(cls, func):
        dirpath = os.path.dirname(ModuleTool.func2filepath(func))

        now_utc = datetime.now(tz=pytz.utc)

        filename = f'{FunctionTool.func2fullpath(func)}.{now_utc.isoformat()}.cprofile'
        filepath = os.path.join(dirpath, 'cprofile', filename, )
        return filepath

    @classmethod
    def func2datetimed_filepath(cls, func):
        dirpath = os.path.dirname(ModuleTool.func2filepath(func))

        now_utc = datetime.now(tz=pytz.utc)

        filename = f'{FunctionTool.func2fullpath(func)}.{now_utc.isoformat()}.cprofile'
        filepath = os.path.join(dirpath, 'cprofile', filename, )
        return filepath

    @classmethod
    def analyze_dmp(cls, myinfilepath='stats.dmp', myoutfilepath='stats.log'):
        with open(myoutfilepath, 'w') as out_stream:
            ps = pstats.Stats(myinfilepath, stream=out_stream)
            sortby = 'cumulative'

            ps.strip_dirs().sort_stats(sortby).print_stats(1)  # plink around with this to get the results you need

    # @classmethod
    # def cprofile2file(cls, cprofile, ofilepath):
    #     DirTool.makedirs_if_empty(os.path.dirname(ofilepath))
    #     cprofile.dump_stats(ofilepath)

    @classmethod
    def func2wrapped_with_profile(cls, func, func2ofilepath=None):
        # https://stackoverflow.com/a/29631996/1902064

        @wraps(func)
        def wrapped(*args, **kwargs):
            nonlocal func2ofilepath
            if func2ofilepath is None:
                func2ofilepath = cls.func2filepath_default
            ofilepath = func2ofilepath(func)

            cprofile = cProfile.Profile()
            retval = cprofile.runcall(func, *args, **kwargs)
            # Note use of name from outer scope

            DirTool.makedirs_if_empty(os.path.dirname(ofilepath))
            cprofile.dump_stats(ofilepath)

            return retval

        return wrapped

