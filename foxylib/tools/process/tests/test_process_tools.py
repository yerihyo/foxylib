import logging
from unittest import TestCase

from functools import partial
from time import sleep

from foxylib.tools.process.process_tools import ProcessToolkit

logger = logging.getLogger(__name__)

class PP:
    @classmethod
    def f(cls, proc_name, secs):
        print("{0}: waiting {1} secs".format(proc_name, secs))
        sleep(secs)
        print("{0}: done after {1} secs".format(proc_name, secs))
        return proc_name

class ProcessToolkitTest(TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    def test_01(self):
        def func(proc_name, secs):
            print("{0}: waiting {1} secs".format(proc_name, secs))
            sleep(secs)
            print("{0}: done after {1} secs".format(proc_name, secs))
            return proc_name

        f = PP.f
        # f = func

        func_list = [partial(f, "proc 00", 5),
                     partial(f, "proc 01", 10),
                     partial(f, "proc 02", 1),
                     partial(f, "proc 03", 3),
                     partial(f, "proc 04", 9),
                     partial(f, "proc 05", 2),
                     partial(f, "proc 06", 4),
                     partial(f, "proc 07", 7),
                     partial(f, "proc 08", 8),
                     partial(f, "proc 09", 6),
                     ]
        hyp = ProcessToolkit.func_list2result_list(func_list)
        ref = ["proc 00",
               "proc 01",
               "proc 02",
               "proc 03",
               "proc 04",
               "proc 05",
               "proc 06",
               "proc 07",
               "proc 08",
               "proc 09",
               ]
        self.assertEqual(hyp,ref)

