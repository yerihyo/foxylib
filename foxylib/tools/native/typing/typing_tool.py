from collections import Hashable
from typing import Union, Any, TypeVar, Optional

from foxylib.tools.native.typing._typing_tool_helper import is_instance, \
    is_subtype, is_generic


class TypingTool:
    class NotAnnotationError(Exception):
        pass

    @classmethod
    def is_annotation(cls, annotation):
        try:
            annotation.mro()
            return True
        except AttributeError:
            pass

        special_annotations = {Any,}
        if isinstance(annotation, Hashable):
            if annotation in special_annotations:
                return True

        if is_generic(annotation):
            return True

        if isinstance(annotation, TypeVar):
            return True

        return False

    @classmethod
    def is_instance(cls, obj, annotation):
        if not cls.is_annotation(annotation):
            raise cls.NotAnnotationError(annotation)

        return is_instance(obj, annotation)

    @classmethod
    def is_subtype(cls, sub_type, super_type):
        if not cls.is_annotation(sub_type):
            raise cls.NotAnnotationError(sub_type)

        if not cls.is_annotation(super_type):
            raise cls.NotAnnotationError(super_type)

        return is_subtype(sub_type, super_type)

    @classmethod
    def get_origin(cls, annotation):
        """
        https://docs.python.org/3/library/typing.html#typing.get_args

        typing.get_origin() doesn't exists for old version python
        alternative - https://stackoverflow.com/a/49471187

        :param type_in:
        :return:
        """

        if not cls.is_annotation(annotation):
            raise cls.NotAnnotationError(annotation)

        try:
            return getattr(annotation, '__origin__')
        except AttributeError:
            return None

    @classmethod
    def get_args(cls, type_in):
        """
        https://docs.python.org/3/library/typing.html#typing.get_args
        :param type_in:
        :return:
        """
        return getattr(type_in, '__args__', tuple([]),)

    @classmethod
    def is_optional(cls, type_in):
        if isinstance(type_in, dict):
            return False

        if type_in is None:
            return True

        if type_in is Optional:
            return True

        if cls.get_origin(type_in) is not Union:
            return False

        return isinstance(None, cls.get_args(type_in))


