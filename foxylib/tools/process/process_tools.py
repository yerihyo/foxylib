import os
from concurrent.futures import as_completed, wait
from concurrent.futures.process import ProcessPoolExecutor
from multiprocessing.pool import Pool

import dill
from future.utils import lmap

from foxylib.tools.collections.collections_tools import l_singleton2obj
from foxylib.tools.log.logger_tools import FoxylibLogger
from foxylib.tools.version.version_tools import VersionToolkit


class ProcessToolkit:
    @classmethod
    def _func2dillstr(cls, f):
        # python only allows "real" function to parallelize
        # if we want to run partial(f,a,k) types, we need to serialize
        return dill.dumps(f)

    @classmethod
    def _dillstr2run(cls, str_dill):
        f = dill.loads(str_dill)
        return f()

    @classmethod
    def max_workers2executor(cls, max_workers):
        return ProcessPoolExecutor(max_workers=max_workers)

    @classmethod
    def _func_list2fak_list_filled(cls, func_list):
        dillstr_list = lmap(cls._func2dillstr, func_list)
        fak_list = [(cls._dillstr2run, [s],{})for s in dillstr_list]
        return fak_list

    @classmethod
    # @VersionToolkit.inactive
    def func_list2result_list(cls, func_list):
        # cannot do this because Pool() object should be able to see the target function definition
        # https://stackoverflow.com/questions/2782961/yet-another-confusion-with-multiprocessing-error-module-object-has-no-attribu

        if len(func_list) == 1:
            f = l_singleton2obj(func_list)
            return [f()]

        fak_list = cls._func_list2fak_list_filled(func_list)
        with Pool() as p:
            result_list = cls.pool_fak_list2result_list(p, fak_list)
        return result_list

    @classmethod
    def pool_fak_list2result_list(cls, pool, fak_list):
        logger = FoxylibLogger.func2logger(cls.pool_fak_list2result_list)
        # dillstr_list = lmap(cls.func2dillstr, func_list)

        ar_list = [pool.apply_async(f, args=a, kwds=k)
                   for f,a,k in fak_list]
        # logger.debug({"result_list": result_list})

        output_list = [ar.get() for ar in ar_list]

        return output_list

    @classmethod
    @VersionToolkit.inactive
    def executor_func_list2result_list(cls, executor, func_list):
        logger = FoxylibLogger.func2logger(cls.executor_func_list2result_list)
        func_count = len(func_list)


        # Start the load operations and mark each future with its URL

        h_future2index = {executor.submit(cls.dillstr2run, cls.func2dillstr(func)):i
                          for i,func in enumerate(func_list)}
        for future in as_completed(h_future2index):
            index = h_future2index[future]
            logger.info('Func #{0}/{1} completed'.format(index, func_count))

        wait(h_future2index)

        result_list = [future.result() for future in h_future2index]
        return result_list

    # @classmethod
    # def process2mem_rss(cls):
    #     import psutil
    #     process = psutil.Process(os.getpid())
    #     return process.memory_info().rss
