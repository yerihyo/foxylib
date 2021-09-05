from functools import lru_cache
from operator import itemgetter as ig

import wtforms_json
from future.utils import lmap
from wtforms import Form, FormField, FieldList, Field
from wtforms.i18n import DummyTranslations

from foxylib.tools.collections.collections_tool import DictTool, l_singleton2obj
from foxylib.tools.function.function_tool import FunctionTool


class WTFormsTool:
    @classmethod
    @lru_cache(maxsize=1)
    def dummy_translation(cls):
        return DummyTranslations()

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=1))
    def json_init(cls):
        wtforms_json.init()

    @classmethod
    def h_gettext2translations(cls, h_gettext):
        class Translations(DummyTranslations):
            def gettext(self, str_in):
                if str_in in h_gettext:
                    return h_gettext[str_in]

                return super(Translations).gettext(str_in)
        return Translations()

    @classmethod
    def form2j_form(cls, form):
        if not form:
            return form

        return DictTool.filter(lambda k, v: v, form.patch_data)


    @classmethod
    def boundfield2name(cls, boundfield):
        return boundfield.short_name

    @classmethod
    def form2data_jinja2(cls, form):
        if not form:
            return None

        j_form = cls.form2j_form(form)
        if not j_form:
            return None

        h_jinja2 = {k: {"value": v}
                    for k, v in j_form.items()
                    if v
                    }
        return h_jinja2

    @classmethod
    def field2name(cls, field):
        return field.short_name

    @classmethod
    def field_label_list2formclass_dummy(cls, field_label_list, ):
        class ThisForm(Form):
            pass

        for label, field in field_label_list:
            setattr(ThisForm, label, field)

        return ThisForm

    @classmethod
    def field_label_value_list2form_dummy(cls, field_label_value_list):
        formclass = cls.field_label_list2formclass_dummy(lmap(ig(0,1), field_label_value_list))
        data = dict(map(ig(0,2), field_label_value_list))
        return formclass.from_json(data)

    # @classmethod
    # def field2boundfield_dummy(cls, field,):
    #     _Form = cls.field2Form_dummy(field)
    #     form = _Form()
    #
    #     field_list = list(form.fields)
    #     return l_singleton2obj(field_list)
