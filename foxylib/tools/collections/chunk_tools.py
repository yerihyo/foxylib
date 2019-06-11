from nose.tools import assert_true

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
