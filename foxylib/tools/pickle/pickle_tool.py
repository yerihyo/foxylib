import os
import pickle


class PickleTool:
    @classmethod
    def file2obj(cls, filepath):
        if not os.path.exists(filepath):
            return None

        with open(filepath, 'rb') as f:
            return pickle.load(f)

    @classmethod
    def obj2file(cls, filepath, obj):
        with open(filepath, 'wb') as f:
            pickle.dump(obj, f)
