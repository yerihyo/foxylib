from random import Random


class RandomTool:
    @classmethod
    def lasvegas(cls, func, cond):
        while True:
            v = func()
            if cond(v):
                return v

        raise NotImplementedError("Should not arrive here!")

    @classmethod
    def text2key(cls, seed: str, alphabet: str, digit: int):
        # alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-'
        # digit = 21

        r = Random(seed)
        return ''.join(r.choice(alphabet) for _ in range(digit))