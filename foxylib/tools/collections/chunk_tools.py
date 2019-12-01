import logging
from functools import reduce
from operator import itemgetter as ig

from future.utils import lmap, lfilter
from nose.tools import assert_true, assert_equal, assert_less, assert_not_in, assert_false, assert_not_equal, assert_in

from foxylib.tools.collections.collections_tools import zip_strict, IterToolkit, list2singleton
from foxylib.tools.log.logger_tools import FoxylibLogger
from foxylib.tools.version.version_tools import VersionToolkit


class ChunkToolkit:
    @classmethod
    def index_list2chunks(cls, l, index_list):
        assert_true(index_list)
        n = len(index_list)

        return [l[(index_list[i - 1] if i else 0):index_list[i]]
                for i in range(n)]

    @classmethod
    def chunk_size2index_list(cls, n, chunk_size):
        chunk_count = n // chunk_size + (1 if n % chunk_size else 0)
        index_list = [min((i + 1) * chunk_size, n) for i in range(chunk_count)]
        return index_list

    @classmethod
    @VersionToolkit.inactive
    def chunk_count2chunk_size_list(cls, n, chunk_count):
        cc = min(n, chunk_count)
        r = n % chunk_count
        return [n // chunk_count + int(i < r) for i in range(cc)]

    @classmethod
    def chunk_count2index_list(cls, n, chunk_count):
        cc = min(n, chunk_count)
        return [(i + 1) * n // cc for i in range(cc)]

    # @classmethod
    # def chunk_size2chunks(cls, l, chunk_size):
    #     index_list = cls.chunk_size2index_list(len(l), chunk_size)
    #     return cls.index_list2chunks(l, index_list)

    @classmethod
    def chunk_count2chunks(cls, l, chunk_count):
        index_list = cls.chunk_count2index_list(len(l), chunk_count)
        return cls.index_list2chunks(l, index_list)

    @classmethod
    def chunk_size2chunks(cls, iterable, chunk_size):
        l = []
        for i,v in enumerate(iterable):
            l.append(v)

            if (i+1) % chunk_size == 0:
                yield l
                l = []

        if l:
            yield l

    @classmethod
    def iter_batch2yoo(cls, iter, f_batch, chunk_size):
        logger = FoxylibLogger.func_level2logger(cls.iter_batch2yoo, logging.DEBUG)

        for x_list_chunk in cls.chunk_size2chunks(iter, chunk_size):
            f_batch(x_list_chunk)
            yield from x_list_chunk

        # Do not forget to consume the result!!

    @classmethod
    def iter_batch2yoo_consumed(cls, iter, f_batch, chunk_size):
        IterToolkit.consume(cls.iter_batch2yoo(iter, f_batch, chunk_size))

    @classmethod
    def iter_batches2yoo(cls, iter, batch_chunksize_list):
        logger = FoxylibLogger.func_level2logger(cls.iter_batches2yoo, logging.DEBUG)

        iter_out = reduce(lambda x_iter, fp: cls.iter_batch2yoo(x_iter, fp[0], fp[1]),
                          batch_chunksize_list,
                          iter)
        yield from iter_out

    @classmethod
    def iter_batches2yoo_consumed(cls, iter, batch_chunksize_list):
        IterToolkit.consume(cls.iter_batches2yoo(iter, batch_chunksize_list))





    @classmethod
    def f_batch2f_iter(cls, f_batch, chunk_size):
        return IterToolkit.f_batch2f_iter(f_batch, chunk_size)


    # """ conditionally run batch function """
    @classmethod
    def iter_batch_cond2processed(cls, x_iter, f_batch, f_cond, size_minimax,):
        logger = FoxylibLogger.func_level2logger(cls.iter_batch_cond2processed, logging.DEBUG)

        def inputs_indexes2y_list(x_list, i_list):
            x_list_target = lmap(lambda i: x_list[i], i_list)
            y_list_target = f_batch(x_list_target)

            h_i2k = {i: k for k, i in enumerate(i_list)}

            y_list = [x if i not in h_i2k else y_list_target[h_i2k[i]]
                      for i, x in enumerate(x_list)]
            return y_list

        size_min, size_max = size_minimax

        x_list_buffer = []
        i_list_target = []

        for x in x_iter:
            is_buffer_empty = list2singleton([not x_list_buffer, not i_list_target])

            is_target = (f_cond is None) or f_cond(x)
            if (not is_target) and is_buffer_empty:
                yield x
                continue

            if is_target:
                i_list_target.append(len(x_list_buffer))
            x_list_buffer.append(x)

            run_batch = len(x_list_buffer)>=size_max or len(i_list_target)>=size_min
            if not run_batch:
                continue

            if not is_buffer_empty:
                y_list_buffer = inputs_indexes2y_list(x_list_buffer, i_list_target)
                logger.debug({"# i_list_target": len(i_list_target),
                              "# y_list_buffer": len(y_list_buffer),})
                yield from y_list_buffer

                x_list_buffer = []
                i_list_target = []


        is_buffer_empty = list2singleton([not x_list_buffer, not i_list_target])
        if not is_buffer_empty:
            yield from inputs_indexes2y_list(x_list_buffer, i_list_target)


class BatchPoolTool:
    @classmethod
    @VersionToolkit.inactive
    def iter2richiter_init(cls, iter):
        for x in iter:
            yield (False, x, None)

    @classmethod
    @VersionToolkit.inactive
    def richiter_func_sizes2richiter(cls, rich_iter, f_batch, size_pair):
        buffer_size, chunk_size = size_pair

        def buffer2is_call_triggered(buffer):
            if len(buffer) >= buffer_size:
                return True

            if IterToolkit.count(filter(ig(0), buffer)) >= chunk_size:
                return True

            return False

        def buffer_chunksize2rich_iter(buffer, chunk_size):
            i_list_invalid = lfilter(lambda i: not buffer[i][0], range(len(buffer)))
            i_list_target = i_list_invalid[:chunk_size]
            p = i_list_target[-1] + 1

            x_list_part = lmap(lambda i: buffer[i][1], i_list_target)
            by_list_part = f_batch(x_list_part)

            h_i2by = {i: by_list_part[k] for k, i in enumerate(i_list_target)}

            l_out = []
            for i in range(p):
                if buffer[i][0]:
                    l_out.append( buffer[i] )
                else:
                    b, y = h_i2by[i]
                    x = buffer[i][1]
                    l_out.append( (b, x, y) )
            return p, l_out


        buffer = []
        for b,x,y in rich_iter:
            if b and not buffer:
                yield (b,x,y)

            buffer.append( (b, x, y) )

            while buffer2is_call_triggered(buffer):
                p, l_out = buffer_chunksize2rich_iter(buffer, chunk_size)
                yield from l_out

                buffer = buffer[p:]


    @classmethod
    @VersionToolkit.inactive
    def iter2backoff_batches(cls, iter, batch_chunksize_list, buffer_size):
        logger = FoxylibLogger.func_level2logger(cls.iter2backoff_batches, logging.DEBUG)

        n = buffer_size
        m = len(batch_chunksize_list)

        queue_list = [[] for _ in range(m)]
        h_i2j = {}
        h_i2out = {}
        buffer_in = [None] * (n+1)


        # f_batch_list = lmap(ig(0), batch_chunksize_list)
        # chunksize_list = lmap(ig(1), batch_chunksize_list)


        def i2next(i): return (i+1) % (n+1)

        def append2j(i,j):
            h_i2j[i] = j
            queue_list[j].append(i)

        def iy2out(i,y):
            h_i2out[i] = y
            h_i2j.pop(i)

        def i2j_new(i, j_old):
            j_new = j_old +1
            h_i2j[i] = j_new
            queue_list[j_new].append(i)

        def j2batch(j):

            if not queue_list[j]:
                return

            f_batch, chunksize = batch_chunksize_list[j]

            i_list = queue_list[j][:chunksize]
            queue_list[j] = queue_list[j][chunksize:]

            x_list = [buffer_in[i] for i in i_list]
            by_list = f_batch(x_list)

            if j == m-1:
                ix_list = [(i, buffer_in[i])
                           for i, (b, y) in zip_strict(i_list, by_list)
                           if not b]
                assert_false(ix_list)

            for i,(b,y) in zip_strict(i_list,by_list):
                if b:
                    iy2out(i,y)
                else:
                    i2j_new(i,j)

            logger.debug({"step": "j2batch", "j": j,  "h_i2out":h_i2out, "h_i2j":h_i2j,})

        def i2yield(i):


            assert_in(i, h_i2out)
            assert_not_in(i, h_i2j)

            y = h_i2out.pop(i)

            logger.debug({"step": "i2yield", "i": i, "y":y})
            return y


        i_head = -1
        i_tail = -1
        for x in iter:
            i_head = i2next(i_head)
            logger.debug({"i_head":i_head})

            assert_not_in(i_head, h_i2j)
            buffer_in[i_head] = x

            append2j(i_head, 0)

            if len(h_i2j) + len(h_i2out)<n:
                continue

            i_tail = i2next(i_tail)
            logger.debug({"i_tail": i_tail, "h_i2j":h_i2j, "h_i2out":h_i2out,})

            assert_not_equal(i_tail in h_i2j, i_tail in h_i2out)

            if i_tail in h_i2out:
                yield i2yield(i_tail)
                continue


            j_tail = h_i2j[i_tail]

            for j in range(j_tail,m):
                j2batch(j)
                if i_tail not in h_i2out: # not done
                    continue

                yield i2yield(i_tail)
                break

        for j in range(m):
            while queue_list[j]:
                j2batch(j)

        assert_false(h_i2j)

        while h_i2out:
            i_tail = i2next(i_tail)
            yield i2yield(i_tail)
