import csv

from nose.tools import assert_greater_equal

from foxylib.tools.collections.collections_tools import iter2singleton, merge_dicts, vwrite_no_duplicate_key


class CSVTool:
    @classmethod
    def filepath2str_ll(cls, filepath):

        with open(filepath, 'r', encoding='utf-8') as f:
            r = csv.reader(f) #, delimiter=',', quotechar='|')
            l = list(r)
        return l

    @classmethod
    def lines2str_ll(cls, lines):
        r = csv.reader(lines) # , delimiter=',', quotechar='|')
        l = list(r)
        return l

    @classmethod
    def str_ll2h_list(cls, str_ll):
        assert_greater_equal(len(str_ll), 1)
        m = iter2singleton(map(len, str_ll))
        key_list = str_ll[0]


        h_list = [merge_dicts([{key_list[j]:l[j]} for j in range(m)],
                        vwrite=vwrite_no_duplicate_key)
                  for l in str_ll[1:]]
        return h_list
    @classmethod
    def strs_iter2fileptr(cls, str_list_iter, file_pointer):
        writer = csv.writer(file_pointer, quoting=csv.QUOTE_MINIMAL)
        for l in str_list_iter:
            writer.writerow(l)

    """ https://docs.python.org/3/library/csv.html#id3 (newline='') """
    @classmethod
    def strs_iter2file(cls, str_list_iter, filepath):
        with open(filepath, 'w', newline='') as f:
            cls.strs_iter2fileptr(str_list_iter, f)

    """ https://tobywf.com/2017/08/unicode-csv-excel/ (utf-8) """
    @classmethod
    def utf8s_iter2file(cls, utf8_list_iter, filepath):
        with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
            cls.strs_iter2fileptr(utf8_list_iter, f)

