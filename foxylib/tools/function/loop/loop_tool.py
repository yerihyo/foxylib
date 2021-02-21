import time


class LoopTool:
    class ExitException(Exception):
        pass

    @classmethod
    def failcount2secs_default(cls, failcount):
        secs = min(2 ** failcount, 60)
        return secs

    @classmethod
    def func2loop(cls, func, failcount2secs=None):
        if failcount2secs is None:
            failcount2secs = cls.failcount2secs_default

        failcount = 0
        while True:
            try:
                succeeded = func()
            except cls.ExitException:
                return

            if succeeded:
                failcount = 0
                continue

            time.sleep(failcount2secs(failcount))
            failcount += 1



