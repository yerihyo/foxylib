from jsonschema import Draft7Validator, validators

from foxylib.tools.collections.collections_tool import DictTool, merge_dicts, \
    vwrite_no_duplicate_key
from foxylib.tools.collections.traversile.traversile_tool import TraversileTool


class JsonschemaTool:
    BaseValidator = Draft7Validator

    @classmethod
    def jpath2checked(cls, schema, jpath):
        return True  # for now


    @classmethod
    def definitions2Validator(cls, definitions):
        BaseValidator = Draft7Validator

        if not definitions:
            return BaseValidator

        type_checker = BaseValidator.TYPE_CHECKER.redefine_many(definitions)
        return validators.extend(BaseValidator, type_checker=type_checker)

    @classmethod
    def schema2validator(cls, schema_in, definitions=None):
        Validator = cls.definitions2Validator(definitions)
        return Validator(schema=schema_in)

    # @classmethod
    # def typechecked(cls, data_in, schema_in, definitions=None):
    #     Validator = cls.definitions2Validator(definitions)
    #     validator = Validator(schema=schema_in)
    #     validator.validate(instance=data_in)
    #     return data_in

    @classmethod
    def typechecked(cls, validator, data_in,):
        validator.validate(instance=data_in)
        return data_in

    @classmethod
    def schema2required_added(cls, schema_in):
        def node2required_added(schema_in_):
            if not isinstance(schema_in_, dict):
                return schema_in_

            schema_tmp = {k: cls.schema2required_added(v)
                          for k, v in schema_in_.items()}

            if 'properties' not in schema_in_:
                return schema_tmp

            if 'required' in schema_in_:
                return schema_tmp

            properties = schema_tmp['properties']
            fields = list(properties.keys())

            schema_out_ = merge_dicts([
                schema_tmp,
                {'required': fields}
            ], vwrite=vwrite_no_duplicate_key)
            return schema_out_

        schema_out = TraversileTool.tree2traversed(
            schema_in, node2required_added, target_types={list, set, tuple})

        return schema_out

    @classmethod
    def schema2required_removed(cls, schema_in):
        def node2required_removed(schema_in_):
            if not isinstance(schema_in_, dict):
                return schema_in_

            schema_tmp = DictTool.keys2excluded(schema_in_, ['required'])
            schema_out_ = {k: cls.schema2required_removed(v)
                           for k, v in schema_tmp.items()}
            return schema_out_

        schema_out = TraversileTool.tree2traversed(
            schema_in, node2required_removed, target_types={list, set, tuple})

        return schema_out


    # @classmethod
    # def xson_partial2full(cls, data_in, schema_in, defaults_in, policy=None):
    #     if not cls.is_valid(defaults_in, schema,
    #                         policy=DicttreeTool.Policy.FULL):
    #         raise ValueError({'defaults_in': defaults_in})
    #
    #     policy = policy or DicttreeTool.Policy.PARTIAL_DATA
    #     if not DicttreeTool.Policy.is_partial_data_allowed(policy):
    #         raise ValueError({'policy': policy})
    #
    #     if policy == DicttreeTool.Policy.PARTIAL_DATA:
    #         cls.is_valid(x_in, schema, policy=policy)
    #
    #     x_out = merge_dicts([
    #         x_in,
    #         defaults_in,
    #     ], vwrite=f_vwrite2f_hvwrite(DictTool.VWrite.skip_if_existing))
    #     return x_out
