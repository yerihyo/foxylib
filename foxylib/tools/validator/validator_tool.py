from future.utils import lmap

from foxylib.tools.collections.iter_tool import IterTool


class ValidatorTool:
    @classmethod
    def validate_funcs2errors_func(cls, validate_funcs, error_classes):
        @IterTool.f_iter2f_list
        def errors_func(*_, **__):
            for validate_func in validate_funcs:
                try:
                    validate_func(*_, **__)
                except error_classes as e:
                    yield e
        return errors_func

