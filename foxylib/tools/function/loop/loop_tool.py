import time


class LoopTool:
    class ExitException(Exception):
        pass

    @classmethod
    def failcount2sleep_default(cls, failcount):
        secs = max(2 ** failcount, 60)
        time.sleep(secs)

    @classmethod
    def func2loop(cls, callable, failcount2sleep=None):
        if failcount2sleep is None:
            failcount2sleep = cls.failcount2sleep_default

        failcount = 0

        while True:
            try:
                succeeded = callable()
            except cls.ExitException:
                break

            if succeeded:
                failcount = 0
                continue

            failcount2sleep(failcount)
            failcount += 1



