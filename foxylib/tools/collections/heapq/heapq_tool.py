from heapq import heappush


class HeapqTool:
    @classmethod
    def push_all(cls, q, items):
        for item in items:
            heappush(q, item)

        return q
