from typing import Callable


class LoopTool:
    class ExitException(Exception):
        pass

    @classmethod
    def func2loop(cls, func: Callable):
        failcount = 0

        while True:
            try:
                succeeded = func(failcount=failcount)
            except cls.ExitException:
                break

            if succeeded:
                failcount = 0
                continue

            failcount += 1


