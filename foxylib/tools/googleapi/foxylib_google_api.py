import os
from functools import reduce

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
REPO_DIR = reduce(lambda x,f:f(x), [os.path.dirname]*3, FILE_DIR)

class FoxylibGoogleApi:
    @classmethod
    def filepath_credentials(cls):
        return os.path.join(REPO_DIR,"env","googleapi","foxytrixy.bot.credential.json")
