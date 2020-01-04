import logging
import time
from concurrent.futures.process import ProcessPoolExecutor
from functools import partial
from multiprocessing.pool import Pool

import dill
from future.utils import lmap, lfilter
from nose.tools import assert_equal

from foxylib.tools.collections.collections_tool import l_singleton2obj, IterTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.string.string_tool import format_str


class ProcessTool:
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


    # @classmethod
    # def _pool_fak_list2parallel_list(cls, pool, fak_list):
    #     logger = FoxylibLogger.func2logger(cls._pool_fak_list2parallel_list)
    #     # dillstr_list = lmap(cls.func2dillstr, func_list)
    #
    #     ar_list = [pool.apply_async(f, args=a, kwds=k)
    #                for f,a,k in fak_list]
    #     # logger.debug({"result_list": result_list})
    #
    #     output_list = [ar.get() for ar in ar_list]
    #
    #     return output_list

    @classmethod
    def _pool_fak_iter2ar_iter(cls, pool, fak_iter):
        # logger = FoxylibLogger.func2logger(cls._pool_fak_iter2ar_iter)

        for f,a,k in fak_iter:
            # logger.debug({"i":i})
            ar = pool.apply_async(partial(f), args=a, kwds=k) # partial makes it visible anywhere
            yield ar


    @classmethod
    def pool_func_iter2ar_iter(cls, pool, f_iter):
        fak_iter = ((f,[],{}) for f in f_iter)
        yield from cls._pool_fak_iter2ar_iter(pool, fak_iter)

    # @classmethod
    # def func_iter2ar_iter(cls, func_iter):
    #     # be careful because Pool() object should be able to see the target function definition
    #     # https://stackoverflow.com/questions/2782961/yet-another-confusion-with-multiprocessing-error-module-object-has-no-attribu
    #     with Pool() as p:
    #         ar_iter = cls._pool_func_iter2ar_iter(p, func_iter)
    #         yield from ar_iter

    @classmethod
    def ar_iter2buffered_result_iter(cls, ar_iter, buffer_size):
        logger = FoxylibLogger.func2logger(cls.ar_iter2buffered_result_iter)

        ar_iter_buffered = IterTool.iter2buffered(ar_iter, buffer_size)
        for ar in ar_iter_buffered:
            yield ar.get()

    @classmethod
    def pool_func_iter2buffered_result_iter(cls, pool, func_iter, buffer_size):
        ar_iter = cls.pool_func_iter2ar_iter(pool, func_iter)
        yield from cls.ar_iter2buffered_result_iter(ar_iter, buffer_size)

    @classmethod
    def func_iter2buffered_result_iter(cls, func_iter, buffer_size):
        logger = FoxylibLogger.func2logger(cls.func_iter2buffered_result_iter)

        # be careful because Pool() object should be able to see the target function definition
        # https://stackoverflow.com/questions/2782961/yet-another-confusion-with-multiprocessing-error-module-object-has-no-attribu
        with Pool() as pool:
            yield from cls.pool_func_iter2buffered_result_iter(pool, func_iter, buffer_size)


    @classmethod
    def func_list2buffered_result_iter(cls, func_list, buffer_size):
        if len(func_list) == 1:
            f = l_singleton2obj(func_list)
            yield f()
        else:
            result_iter = cls.func_iter2buffered_result_iter(func_list, buffer_size)
            yield from result_iter

    @classmethod
    def func_list2result_list_OLD(cls, func_list):
        logger = FoxylibLogger.func2logger(cls.func_list2result_list)

        with Pool() as pool:
            ar_list = [pool.apply_async(f) for f in func_list]
            output_list = [ar.get() for ar in ar_list]

        return output_list

    @classmethod
    def func_list2result_list(cls, func_list):
        logger = FoxylibLogger.func2logger(cls.func_list2result_list)
        logger.debug({"# func_list": len(func_list)})

        output_iter = cls.func_list2buffered_result_iter(func_list, len(func_list))
        result_list = list(output_iter)
        logger.debug({"# result_list":len(result_list)})
        return result_list

    @classmethod
    def func_list2run_parallel(cls, func_list):
        output_iter = cls.func_list2buffered_result_iter(func_list, len(func_list))
        IterTool.consume(output_iter)

    @classmethod
    def wait(cls, f, *_, **__):
        status_list = cls.wait_all([f], *_, **__)
        assert_equal(len(status_list), 1)
        return status_list[0]

    @classmethod
    def wait_all(cls, f_list, sec_timeout, sec_interval):
        logger = FoxylibLogger.func_level2logger(cls.wait_all, logging.DEBUG)
        time_end = time.time() + sec_timeout if sec_timeout is not None else None

        n = len(f_list)
        status_list = [None] * n

        logger.debug(format_str("waiting for {} process for {} secs", len(f_list), sec_timeout))

        while (time_end is None) or (time.time() < time_end):
            for i in range(n):
                if status_list[i] is True:
                    continue
                status_list[i] = f_list[i]()

            if all(status_list):
                break

            logger.debug(format_str("waiting for {}/{} processes for {} secs with {} sec interval",
                                    len(lfilter(lambda x: not x, status_list)),
                                    len(f_list),
                                    "{:.3f}".format(time_end - time.time()),
                                    sec_interval,
                                    ))
            time.sleep(sec_interval)

        return status_list

    # @classmethod
    # @VersionTool.inactive
    # def executor_func_list2parallel_list(cls, executor, func_list):
    #     logger = FoxylibLogger.func2logger(cls.executor_func_list2parallel_list)
    #     func_count = len(func_list)
    #
    #
    #     # Start the load operations and mark each future with its URL
    #
    #     h_future2index = {executor.submit(cls.dillstr2run, cls.func2dillstr(func)):i
    #                       for i,func in enumerate(func_list)}
    #     for future in as_completed(h_future2index):
    #         index = h_future2index[future]
    #         logger.info('Func #{0}/{1} completed'.format(index, func_count))
    #
    #     wait(h_future2index)
    #
    #     result_list = [future.result() for future in h_future2index]
    #     return result_list

    # @classmethod
    # def process2mem_rss(cls):
    #     import psutil
    #     process = psutil.Process(os.getpid())
    #     return process.memory_info().rss
