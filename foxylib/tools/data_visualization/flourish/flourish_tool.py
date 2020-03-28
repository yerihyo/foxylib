import logging
from itertools import chain
from operator import itemgetter as ig

from foxylib.tools.arithmetic.arithmetic_tools import ArithmeticTool
from future.utils import lmap, lfilter
from nose.tools import assert_false, assert_less, assert_equal, assert_greater_equal

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.collections.collections_tool import iter2singleton, AbsoluteOrder, ListTool, lchain, IterTool, \
    wrap_iterable2list
from foxylib.tools.collections.groupby_tool import gb_tree_global
from foxylib.tools.span.span_tool import SpanTool
from foxylib.tools.version.version_tool import VersionTool


class FlourishTool:
    @classmethod
    def col_count_limit(cls):
        return 120



class FlourishTable:
    COLINDEX_GROUP = 1
    COUNT_ROWHEAD = 1
    COUNT_COLHEAD = 3
    COL_COUNT_LIMIT = 120

    @classmethod
    @wrap_iterable2list
    def table_labels2repeat(cls, table, label_list):
        n = len(table)
        p = len(label_list)

        for i in range(cls.COUNT_ROWHEAD):
            yield table[i]

        for i in range(cls.COUNT_ROWHEAD,n):
            row_in = table[i]

            r = (i - cls.COUNT_ROWHEAD) % p
            row_out = lchain(row_in[:cls.COLINDEX_GROUP],[label_list[r]],row_in[cls.COLINDEX_GROUP+1:])
            yield row_out

    @classmethod
    def span2colspan(cls, span):
        return SpanTool.add_each(span, cls.COUNT_COLHEAD)

    @classmethod
    def colspan2span(cls, colspan):
        return SpanTool.add_each(colspan, -cls.COUNT_COLHEAD)


    @classmethod
    def table2value_max(cls, table):
        return max(int(v)
                   for l in table[1:]
                   for v in l[FlourishTable.COUNT_COLHEAD:]
                   if v)

    @classmethod
    def table2percentage(cls, table, v):
        logger = FoxylibLogger.func_level2logger(cls.table2percentage, logging.DEBUG)

        count_col = iter2singleton(map(len, table))
        h_j2col_sum = {j: sum(map(int, filter(bool, map(ig(j), table[1:]))))
                       for j in range(cls.COUNT_COLHEAD, count_col)}
        for i, l in enumerate(table):
            if i == 0:
                yield l
                continue

            # logger.debug({"l":l})
            l_head = l[:cls.COUNT_COLHEAD]
            l_right = ["{:.02f}".format(int(l[j])*100/h_j2col_sum[j]) if l[j] else l[j]
                       for j in range(cls.COUNT_COLHEAD, count_col)]
            yield lchain(l_head, l_right)



    @classmethod
    def value2is_zero(cls, value):
        if not value:
            return True
        if value == "0":
            return True
        if value == 0:
            return True

        return False

    @classmethod
    def table_i2colindex_first(cls, table, i):
        row = table[i]
        m = len(row)

        return next(filter(lambda j: not cls.value2is_zero(row[j]), range(cls.COUNT_COLHEAD,m)), None)

    @classmethod
    def table_i2colindex_last(cls, table, i):
        row = table[i]
        m = len(row)

        return next(filter(lambda j: not cls.value2is_zero(row[j]), reversed(range(cls.COUNT_COLHEAD,m))), None)

    @classmethod
    def table_colspan2rowindex_list_starting(cls, table, colspan):
        n = len(table)
        return lfilter(lambda i: SpanTool.covers_index(colspan, cls.table_i2colindex_first(table,i)), range(n))

    # @classmethod
    # @wrap_iterable2list
    # def table_colspan2filtered_starting(cls, table, colspan):
    #     rowindex_list = cls.table_colspan2rowindex_list_starting(table, colspan)
    #     colindex_last = max(cls.table_i2colindex_last(table, i) for i in rowindex_list)
    #     colspan_trim = (colspan[0], colindex_last + 1)
    #
    #
    #     table_trimmed = cls.table_rowindexes_colspan2trimmed(table, rowindex_list, colspan_trim)
    #     return table_trimmed

    @classmethod
    def table_rowindex2is_empty(cls, table, rowindex):
        if rowindex < cls.COUNT_ROWHEAD: return False
        return all(map(cls.value2is_zero, table[rowindex][cls.COUNT_COLHEAD:]))

    @classmethod
    def table_rowindexes2filtered(cls, table, roxindex_iter):
        return lchain([table[0]], lmap(lambda i:table[i], filter(lambda i:i!=0,roxindex_iter)))

    @classmethod
    def table2row_trimmed(cls, table, ):
        n = len(table)
        rowindex_list_valid = lfilter(lambda i: not cls.table_rowindex2is_empty(table, i), range(n))
        return cls.table_rowindexes2filtered(table, rowindex_list_valid)

    @classmethod
    def table_colindex2is_empty(cls, table, colindex):
        if colindex < cls.COUNT_COLHEAD: return False

        n = len(table)
        return all(cls.value2is_zero(table[i][colindex]) for i in range(cls.COUNT_ROWHEAD,n))

    @classmethod
    def table_colindexes2filtered(cls, table, colindex_iter):
        colindex_list = list(colindex_iter)
        return [cls.row_colindexes2filtered(l, colindex_list) for l in table]


    @classmethod
    def table2col_trimmed(cls, table):
        m = iter2singleton(map(len, table))

        colindex_list_valid = lfilter(lambda j: not cls.table_colindex2is_empty(table, j), range(cls.COUNT_COLHEAD,m))
        return cls.table_colindexes2filtered(table, colindex_list_valid)

    @classmethod
    def table2trimmed(cls, table,):
        table_02 = cls.table2row_trimmed(table)
        table_03 = cls.table2col_trimmed(table_02)
        return table_03



    @classmethod
    def table_titles2subbed(cls, table, title_list):
        n_col = iter2singleton(map(len, table))
        assert_equal(n_col, len(title_list) + cls.COUNT_COLHEAD)

        l_row_top = lchain(table[0][:cls.COUNT_COLHEAD], title_list, )
        return lchain([l_row_top], table[1:])

    @classmethod
    @wrap_iterable2list
    def table_func2group_subbed(cls, table, func):
        for i,l in enumerate(table):
            group = l[cls.COLINDEX_GROUP]
            l_new = lchain(l[:cls.COLINDEX_GROUP],[func(i,group)],l[cls.COLINDEX_GROUP+1:])
            yield l_new


    @classmethod
    def _index2is_data(cls, i):
        if i<cls.COUNT_COLHEAD: return False
        #if i==n-1: return False
        return True

    @classmethod
    def _colindex_extended2str_time(cls, str_list, k_col, multiple):
        if not cls._index2is_data(k_col):
            return str_list[k_col]

        j_col, offset = cls.col_index_extended2raw_offset(k_col, multiple)

        year = str_list[j_col] if not offset else str_list[j_col+1]
        if multiple == 12:
            return "{}.{:02d}".format(year, ArithmeticTool.modulo_d(offset,multiple))
        elif multiple == 4:
            return "{}.Q{}".format(year, ArithmeticTool.modulo_d(offset,multiple))
        # elif multiple == 24:
        #     return "{}.{:02d}.{}".format(year, modulo_d(offset//2,multiple), 1 if offset % 2 == 0 else 15)
        else:
            return year


    @classmethod
    def _str_list2title_interpolated(cls, str_list, multiple):
        n_in = len(str_list)

        for i in range(n_in):
            if not cls._index2is_data(i):
                yield str_list[i]
                continue

            for j in range(multiple):
                k_col = cls.col_count_raw2extended(i, multiple)+j
                yield cls._colindex_extended2str_time(str_list, k_col, multiple)

    @classmethod
    def _data_list2interpolated_iter(cls, str_list, multiple):
        n_in = len(str_list)

        # v_list_in = [ternary(str_list[i], f_true=float) for i in range(n_in)]
        for i in range(n_in):
            if i==n_in-1 or not cls._index2is_data(i):
                yield str_list[i]
                continue

            for j in range(multiple):
                if (not str_list[i]) or (not str_list[i+1]):
                    yield None
                    continue

                v0 = float(str_list[i])
                v1 = float(str_list[i+1])

                v_out = (v0*(multiple-j) + v1*j)/multiple
                yield v_out

    @classmethod
    def col_count_raw2extended(cls, col_count, multiple):
        return (col_count - cls.COUNT_COLHEAD - 1) * multiple + 1 + cls.COUNT_COLHEAD

    @classmethod
    def _col_index_extended2raw(cls, k_col, multiple):
        if k_col < cls.COUNT_COLHEAD:
            return k_col

        j_col = (k_col - cls.COUNT_COLHEAD) // multiple + cls.COUNT_COLHEAD
        return j_col

    @classmethod
    def _col_index_extended2offset(cls, k_col, multiple):
        assert_false(k_col < cls.COUNT_COLHEAD)

        return (k_col - cls.COUNT_COLHEAD) % multiple

    @classmethod
    def col_index_extended2raw_offset(cls, k_col, multiple):
        return (cls._col_index_extended2raw(k_col, multiple),
                cls._col_index_extended2offset(k_col, multiple),
                )

    @classmethod
    def str_ll_col_index_extended2interpolated_list(cls, str_ll, j_col, offset, multiple):
        n_row = len(str_ll)

        if offset == 0:
            return [float(str_ll[i][j_col]) for i in range(n_row)]

        return [(float(str_ll[i][j_col])*(multiple-offset) + float(str_ll[i][j_col+1])*(offset))/multiple
                for i in range(n_row)]

    @classmethod
    def _col_index_extended2str_list(cls, str_ll, k_col, i_pivot, multiple):
        logger = FoxylibLogger.func_level2logger(cls._col_index_extended2str_list, logging.DEBUG)

        n_row = len(str_ll)

        n_col_raw = iter2singleton(map(len, str_ll))
        j_col = cls._col_index_extended2raw(k_col, multiple)
        assert_less(j_col, n_col_raw)

        n_col_extended = cls.col_count_raw2extended(n_col_raw, multiple)
        assert_less(k_col, n_col_extended)

        if not cls._index2is_data(j_col):
            return [str_ll[i][j_col] for i in range(n_row)]

        offset = cls._col_index_extended2offset(k_col, multiple)

        def interpolate(str_ll, i, j_col, p):
            assert_less(j_col, n_col_extended)
            s1 = str_ll[i][j_col]
            if not s1: return s1

            v1 = float(s1)
            if not p: return v1

            # logger.debug({"n_col_raw":n_col_raw,
            #               "n_col_extended":n_col_extended,
            #               "multiple": multiple,
            #               "i":i,
            #               "j_col":j_col,
            #               "p":p,
            #               "k_col":k_col,
            #               "offset":offset,
            #               })

            s2 = str_ll[i][j_col + 1]
            if not s2: return s2

            v2 = float(s2)
            return v1 + (v2 - v1) * p

        p = offset / multiple
        v_list_col = [interpolate(str_ll, i, j_col, p) for i in range(1,n_row)]

        str_time = cls._colindex_extended2str_time(str_ll[0], k_col, multiple)

        v_pivot = v_list_col[i_pivot-1]

        count_before = IterTool.count(filter(lambda v: v and v>v_pivot, v_list_col))
        rank = count_before +1
        count_total = IterTool.count(filter(bool, v_list_col))
        str_title = "{} (#{}/{})".format(str_time, rank, count_total)

        return [str_title] + v_list_col


    @classmethod
    def str_ll2interpolated_list(cls, str_ll_in, i_pivot, multiple):
        logger = FoxylibLogger.func_level2logger(cls.str_ll2interpolated_list, logging.DEBUG)

        n_row = len(str_ll_in)
        n_col_raw = iter2singleton(map(len, str_ll_in))
        n_col_extended = cls.col_count_raw2extended(n_col_raw, multiple)

        logger.debug({"n_col_raw": n_col_raw,
                      "n_col_extended": n_col_extended,
                      "multiple": multiple,
                      })
        # raise Exception()

        ll_tr = [cls._col_index_extended2str_list(str_ll_in, k, i_pivot, multiple)
                 for k in range(n_col_extended)]

        ll_out = [[ll_tr[k][i]
                   for k in range(n_col_extended)]
                  for i in range(n_row)]

        return ll_out

    # @classmethod
    # def str_ll2interpolated_iter_OLD(cls, str_ll_in, multiple):
    #     p = multiple
    #     n_row = len(str_ll_in)
    #
    #     for i in range(n_row):
    #         if i==0:
    #             yield list(cls._str_list2title_interpolated(str_ll_in[i], p))
    #         else:
    #             yield list(cls._data_list2interpolated_iter(str_ll_in[i], p))


    @classmethod
    def _index_strs_beam2index_iter(cls, str_list_in, i_pivot_in, beam):
        logger = FoxylibLogger.func_level2logger(cls._index_strs_beam2index_iter, logging.DEBUG)
        offset = 1

        i_pivot = i_pivot_in - offset
        str_list = str_list_in[offset:]
        count_value = len(str_list)

        v_list = lmap(lambda i: (-float(str_list[i]) if str_list[i] else AbsoluteOrder.MAX,
                                 -1 if i == i_pivot_in else 0
                                 ),
                      range(count_value),)

        i_list = SpanTool.index_values_beam2neighbor_indexes(i_pivot, v_list, beam)
        # logger.debug({"i_list":i_list, "v_list":lmap(lambda i:v_list[i], i_list)})
        assert_equal(len(i_list), sum(beam) + 1)

        i_list_out = ListTool.value2front(i_list,i_pivot)
        for i in i_list_out:
            i_out = i + offset
            yield i_out


    @classmethod
    def _str_ll_i2ij_iter(cls, str_ll, i_pivot, beam):
        logger = FoxylibLogger.func_level2logger(cls._str_ll_i2ij_iter, logging.DEBUG)

        # raise Exception({"lmap(len, str_ll)":lmap(len, str_ll)})
        col_count = iter2singleton(map(len, str_ll))

        for j in range(cls.COUNT_COLHEAD, col_count):
            logger.debug({"j": j})

            if not str_ll[i_pivot][j]:  # empty column
                continue

            str_col_list = lmap(lambda l: l[j], str_ll)
            i_iter = cls._index_strs_beam2index_iter(str_col_list, i_pivot, beam)
            for i in i_iter:
                yield (i, j)


    @classmethod
    def _i2j_list2l_out(cls, row, j_list):
        col_count = len(row)

        l_prefix = row[:cls.COUNT_COLHEAD]
        l_data = lmap(lambda j: row[j] if j in j_list else "", range(cls.COUNT_COLHEAD, col_count))
        l_out = lchain(l_prefix, l_data)
        return l_out

    @classmethod
    def table2beamed(cls, table, i_pivot, beam):
        ij_list = list(cls._str_ll_i2ij_iter(table, i_pivot, beam))
        i2j_list = gb_tree_global(ij_list, [ig(0), ], leaf_func=lambda l: lmap(ig(1), l))

        table_filtered = lchain([table[0]],
                                [cls._i2j_list2l_out(table[i], j_list) for i, j_list in
                                 i2j_list],
                                )
        return table_filtered


    @classmethod
    @VersionTool.deprecated
    def table_pagesize2split_OLD(cls, table, ncol_per_page):
        buffer = cls.COUNT_COLHEAD
        ncol_overlap = 1 # overlapping column 1

        n_row = len(table)
        divider = ncol_per_page - buffer - ncol_overlap

        ncol_table = iter2singleton(map(len, table))
        ncol_data = ncol_table - buffer

        n_page = (ncol_data-ncol_overlap) // divider + (1 if (ncol_data-ncol_overlap) % divider else 0)

        cols_header = lmap(lambda l:l[:cls.COUNT_COLHEAD], table)
        for i in range(n_page):
            start = buffer + i*divider
            end = buffer + min((i+1)*divider+1, ncol_data)

            cols_body = lmap(lambda l:SpanTool.list_span2sublist(l, (start,end)), table)

            table_partial = [cols_header[i]+cols_body[i] for i in range(n_row) if any(cols_body[i])]
            yield table_partial

    @classmethod
    def page_size2span_iter(cls, page_size, count_total, count_overlap=1):
        n_header = cls.COUNT_COLHEAD
        n_total, n_overlap = count_total, count_overlap
        n_page = page_size

        n_body = n_total - n_header
        divider = n_page - n_header - n_overlap

        n_page = (n_body - n_overlap) // divider + (1 if (n_body - n_overlap) % divider else 0)
        for i in range(n_page):
            start = n_header + i*divider
            end = n_header + min((i+1)*divider+1, n_body)
            yield (start,end)


    # @classmethod
    # def table_pagesize2split(cls, table, page_size):
    #     col_count = iter2singleton(map(len, table))
    #     span_iter = cls.page_size2span_iter(page_size, col_count,)
    #     yield from cls.table_spans2split(table, span_iter)

    # @classmethod
    # def l_row_j2v_last(cls, l_row, j):
    #     if l_row[j]: return l_row[j]
    #
    #     j_last = max(filter(lambda j:l_row[j], range(cls.COUNT_COLHEAD,j)), default=None)
    #     if j_last is None: return None
    #     return l_row[j_last]
    #
    #
    # @classmethod
    # def table_acc_i_j2v_last(cls, table, i, j):
    #     return cls.l_row_j2v_last(table[i], j)


    # @classmethod
    # def table2colindex_rowindexes_sorted_iter(cls, table):
    #     logger = FoxylibLogger.func_level2logger(cls.table2colindex_rowindexes_sorted_iter, logging.DEBUG)
    #
    #     n_row = len(table)
    #     n_col = iter2singleton(map(len, table))
    #
    #     for j in range(cls.COUNT_COLHEAD, n_col):
    #
    #         l_col = lmap(lambda i:table[i][j], range(n_row))
    #         i_list_valid = lfilter(lambda i: l_col[i], range(1,n_row))
    #         # raise Exception({"j":j,"i_list_valid":i_list_valid,})
    #
    #         i_list_sorted = sorted(i_list_valid, key=lambda i:-int(l_col[i]))
    #         yield (j,i_list_sorted)

    @classmethod
    def table_colindex2rowindexes_sorted(cls, table, colindex):
        logger = FoxylibLogger.func_level2logger(cls.table_colindex2rowindexes_sorted, logging.DEBUG)

        n_row = len(table)
        l_col = lmap(lambda i: table[i][colindex], range(n_row))
        i_list_valid = lfilter(lambda i: l_col[i], range(1, n_row))
        i_list_sorted = sorted(i_list_valid, key=lambda i: -int(l_col[i]))

        return i_list_sorted

    # @classmethod
    # def table_colspan2rowindexes_sorted_iter(cls, table, colspan):
    #     s,e = colspan
    #     for j, i_list in cls.table2colindex_rowindexes_sorted_iter(table):
    #         if j<s:
    #             continue
    #         if j>=e:
    #             break
    #
    #         yield i_list

    @classmethod
    def _table_colspan_i2is_valid(cls, table, colspan, rowindex, fresh_start_req=True):
        i = rowindex

        if i == 0: return True

        s, e = colspan
        if not any(table[i][s:e]):
            return False

        if s == cls.COUNT_COLHEAD:
            return True

        if not fresh_start_req:
            return True

        assert_greater_equal(s - cls.COUNT_COLHEAD - 1, 0,
                             {"start": s,
                              "cls.COUNT_COLHEAD": cls.COUNT_COLHEAD,
                              })

        if table[i][s - cls.COUNT_COLHEAD - 1]:
            return False

        return True

    @classmethod
    def _table_colspan2rowindexes_valid(cls, table, colspan, fresh_start_req=True):
        n_row = len(table)
        return lfilter(lambda i: cls._table_colspan_i2is_valid(table, colspan, i, fresh_start_req=fresh_start_req),
                       range(n_row))

    @classmethod
    def row_colindexes2filtered(cls, l_row, colindex_iter):
        l_out = lmap(lambda j: l_row[j], chain(range(cls.COUNT_COLHEAD),colindex_iter))
        return l_out

    @classmethod
    def row_colspan2filtered(cls, l_row, colspan):
        return cls.row_colindexes2filtered(l_row, range(*colspan))

    @classmethod
    def table_colspan2fresh_rows_filtered(cls, table, colspan):
        logger = FoxylibLogger.func_level2logger(cls.table_colspan2fresh_rows_filtered, logging.DEBUG)

        i_list_starting = cls.table_colspan2rowindex_list_starting(table, colspan)
        table_row_filtered = cls.table_rowindexes2filtered(table, i_list_starting)


        logger.debug({"colspan":colspan,
                      "len(table)":len(table),
                      "iter2singleton(map(len,table))": iter2singleton(map(len,table)),
                      "len(i_list_starting)":len(i_list_starting),
                      "len(table_row_filtered)":len(table_row_filtered),
                      "iter2singleton(map(len,table_row_filtered))": iter2singleton(map(len,table_row_filtered)),
                      })
        return table_row_filtered


    @classmethod
    def table_colspan2filtered(cls, table, colspan):
        return [cls.row_colspan2filtered(l_row, colspan) for l_row in table]

    @classmethod
    def table_colspan2filtered_trimmed(cls, table, colspan):
        table_02 = cls.table_colspan2filtered(table, colspan)
        return cls.table2row_trimmed(table_02)


    @classmethod
    def table_rowindexes_colspan2trimmed(cls, table, rowindex_list, colspan, ):
        logger = FoxylibLogger.func_level2logger(cls.table_colspan2filtered, logging.DEBUG)

        table_02 = cls.table_rowindexes2filtered(table, rowindex_list)
        table_03 = cls.table_colspan2filtered(table_02, colspan)

        logger.debug({"colspan": colspan,
                      "# table": len(table),
                      "# table_02": len(table_02),
                      "# table_03": len(table_03),
                      })

        return table_03



    @classmethod
    def table_spans2summed_row_iter(cls, table, colspan_list):

        def row_span2str(row, span):
            s,e = span

            v = sum(map(lambda x: int(x) if x else 0, row[s:e]))
            str_out = "" if not v else str(v)
            return str_out

        # n_row = len(table)

        for l_row in table:
            # l_row = table[i]
            l_header = l_row[:cls.COUNT_COLHEAD]


            l_body = [row_span2str(l_row, colspan) for colspan in colspan_list]
            l_out = lchain(l_header, l_body)
            yield l_out




    @classmethod
    def table_i_k2v(cls, table, i, k):
        if not table[i][k]:
            return None
        return float(table[i][k])