import pstats
import time
from cProfile import Profile
from unittest import TestCase

from foxylib.tools.cprofile.cprofile_tool import CprofileTool


class ProfileToolTest(TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_1(self):
        def g():
            time.sleep(2)
            return 2

        def f():
            time.sleep(3)
            g()
            return 1

        # profiler = Profile()
        # profiler.enable()
        # f()
        # profiler.disable()
        # stats = pstats.Stats(profiler) #.sort_stats('tottime')
        # stats.strip_dirs().sort_stats('cumulative').print_stats()

        # Print the stats report
        # stats.print_stats()

        wrapped = CprofileTool.func2wrapped_with_profile(
            f,
            func2ofilepath=CprofileTool.func2datetimed_filepath,
        )
        hyp = wrapped()
        #
        self.assertEqual(hyp, 1)
