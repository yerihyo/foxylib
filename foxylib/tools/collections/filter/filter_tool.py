from typing import TypeVar, Callable, List

T = TypeVar('T')


class FilterTool:
    @classmethod
    def f_conds2f_cond_and(cls, filters: List[Callable[[T], bool]]) -> Callable[[T], bool]:
        def f_cond_and(x):
            return all(map(lambda f: f(x), filters))

        return f_cond_and

    @classmethod
    def f_conds2f_cond_or(cls, filters):
        def f_cond_or(x):
            return any(map(lambda f: f(x), filters))

        return f_cond_or
