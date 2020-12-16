import logging
from pprint import pformat
from typing import Type, _SpecialForm, Union

from nose.tools import assert_is_none, assert_is, assert_true
from typing_extensions import get_origin

from foxylib.tools.collections.collections_tool import l_singleton2obj, \
    merge_dicts, f_vwrite2f_hvwrite, DictTool
from foxylib.tools.collections.iter_tool import IterTool
from foxylib.tools.function.decorator_tool import DecoratorTool
from foxylib.tools.json.json_tool import JsonTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.native.typing.typing_tool import TypingTool


class JsonTypecheckTool:
    class Policy:
        FULL = 'full'
        PARTIAL_SCHEMA = 'partial_schema'
        PARTIAL_DATA = 'partial_data',
        EXISTING_KEYS_ONLY = 'existing_keys_only'

        @classmethod
        def values(cls):
            return {
                cls.FULL, cls.PARTIAL_SCHEMA,
                cls.PARTIAL_DATA, cls.EXISTING_KEYS_ONLY
            }

        @classmethod
        def policy2checked(cls, v):
            if v is None:
                return None

            if v not in cls.values():
                raise NotImplementedError({'policy':v})

            return v

        @classmethod
        def is_partial_data_allowed(cls, policy_in):
            cls.policy2checked(policy_in)

            return policy_in in {cls.PARTIAL_DATA, cls.EXISTING_KEYS_ONLY}

        @classmethod
        def is_partial_schema_allowed(cls, policy_in):
            cls.policy2checked(policy_in)

            return policy_in in {cls.PARTIAL_SCHEMA, cls.EXISTING_KEYS_ONLY}

    @classmethod
    def jpath2get(cls, j_in, schema, jpath):
        JsonTool.down_or_error(schema, jpath)
        return JsonTool.down(j_in, jpath)

    @classmethod
    def jpaths2filtered(cls, j_in, schema, jpaths):
        for jpath in jpaths:
            JsonTool.down_or_error(schema, jpath)

        j_out = JsonTool.jpaths2filtered(j_in, jpaths)
        return j_out

    @classmethod
    def jpath2filtered(cls, j_in, schema, jpath):
        return cls.jpaths2filtered(j_in, schema, [jpath])

    @classmethod
    def has_jpath(cls, j_in, schema, jpath):
        JsonTool.down_or_error(schema, jpath)
        return JsonTool.has_jpath(j_in, jpath)

    @classmethod
    def schema2is_terminal(cls, schema):
        if schema is None:
            return True

        if isinstance(schema, (dict, list)):
            return False

        if TypingTool.is_annotation(schema):
            return True

        if IterTool.is_iterable(schema):
            raise NotImplementedError({'schema':schema})

        if callable(schema):
            return True

        return True

    class TypecheckFailError(Exception):
        pass

    @classmethod
    def schema2keys_required(cls, schema):
        if not isinstance(schema, dict):
            raise ValueError({'schema':schema})

        for k,v in schema.items():
            if TypingTool.is_optional(v):
                continue

            yield k

    @classmethod
    def typecheck_terminal_converter(cls, value, type_):
        if not isinstance(value, callable):
            raise ValueError({'value':value})

    @classmethod
    def typecheck_terminal_value(cls, value, type_):
        # logger.debug({'value_':value_, 'type_':type_})
        if type_ is None:
            return

        if TypingTool.is_annotation(type_):
            if not TypingTool.is_instance(value, type_):
                raise cls.TypecheckFailError({
                    'type_': type_, 'value_': value
                })
            return

        if callable(type_):
            if not type_(value):
                raise cls.TypecheckFailError({
                    'type_': type_, 'value_': value
                })
            return

        raise ValueError({'type_': type_})



    @classmethod
    @DecoratorTool.override_result(
        func_override=lambda clazz, x_in, *_, **__: x_in)
    def xson2typechecked(cls, x_in, schema_in,
                         typecheck_terminal=None, policy=None):
        logger = FoxylibLogger.func_level2logger(
            cls.xson2is_valid, logging.DEBUG)

        # logger.debug(pformat({'x_in':x_in, 'schema_in':schema_in,}))

        typecheck_terminal = typecheck_terminal or cls.typecheck_terminal_value
        policy = cls.Policy.policy2checked(policy) or cls.Policy.FULL

        if cls.schema2is_terminal(schema_in):
            typecheck_terminal(x_in, schema_in)
            return

        # list
        def check_list(values_, type_):
            assert_true(isinstance(values_, list))

            if not isinstance(values_, list):
                raise cls.TypecheckFailError()

            for value_ in values_:
                cls.xson2typechecked(value_, type_, policy=policy)

        if isinstance(schema_in, (list,)):
            check_list(x_in, l_singleton2obj(schema_in))
            return

        def check_dict(value_, type_):
            assert_true(isinstance(value_, dict))

            keys_value_ = set(value_.keys())
            keys_type_ = set(type_.keys())
            keys_type_req_ = set(cls.schema2keys_required(type_))

            if not cls.Policy.is_partial_schema_allowed(policy):
                keys_undefined = keys_value_ - keys_type_
                if keys_undefined:
                    raise cls.TypecheckFailError()

            if not cls.Policy.is_partial_data_allowed(policy):
                keys_missing = keys_type_req_ - keys_value_
                if keys_missing:
                    raise cls.TypecheckFailError({
                        'keys_type_req_': keys_type_req_,
                        'keys_value_': keys_value_,
                    })

            keys_common = keys_value_ & keys_type_req_

            for k in keys_common:
                # logger.debug(pformat({'k': k, }))
                cls.xson2typechecked(value_[k], type_[k])

        # dict
        if isinstance(schema_in, (dict,)):
            check_dict(x_in, schema_in)
            return

        logger.exception({'x_in': x_in, 'schema_in': schema_in})
        raise NotImplementedError()

    @classmethod
    def converter2typechecked(cls, converter_tree, schema,):
        return cls.xson2typechecked(
            converter_tree,
            schema,
            typecheck_terminal=cls.typecheck_terminal_converter,
            policy=cls.Policy.PARTIAL_DATA,
        )

    @classmethod
    def xson2is_valid(cls, x_in, schema, policy=None):
        try:
            v = cls.xson2typechecked(x_in, schema, policy=policy)
            assert_is(x_in, v)
            return True
        except cls.TypecheckFailError:
            return False

    @classmethod
    def xson_partial2full(cls, x_in, schema, defaults_in, policy=None):
        if not cls.xson2is_valid(defaults_in, schema, policy=cls.Policy.FULL):
            raise ValueError({'defaults_in':defaults_in})

        def policy2cleaned(policy_):
            if policy_ is None:
                return cls.Policy.PARTIAL_DATA

            policies_valid = {cls.Policy.PARTIAL_DATA,
                              cls.Policy.EXISTING_KEYS_ONLY
                              }
            if policy_ not in policies_valid:
                raise ValueError({'policy_': policy_})

            return policy_
        policy = policy2cleaned(policy)

        if policy == cls.Policy.PARTIAL_DATA:
            cls.xson2is_valid(x_in, schema, policy=policy)

        x_out = merge_dicts([
            x_in,
            defaults_in,
        ], vwrite=f_vwrite2f_hvwrite(DictTool.VWrite.skip_if_existing))
        return x_out

