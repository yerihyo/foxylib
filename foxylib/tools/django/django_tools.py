from future.utils import lmap

from foxylib.tools.env.env_tools import EnvToolkit


class DjangoToolkit:
    @classmethod
    def django2setup(cls, django):
        django.setup()

    @classmethod
    def envfile_django2setup(cls, env_yamlfile, django):
        EnvToolkit.yaml_filepath2env(env_yamlfile)
        DjangoToolkit.django2setup(django)

class ModelToolkit:
    @classmethod
    def model2field_list(cls, model):
        return list(model._meta.get_fields())

    @classmethod
    def field2name(cls, field): return field.name

    @classmethod
    def model2fieldname_list(cls, model):
        return lmap(cls.field2name, cls.model2field_list(model))


# class DjangoObjToolkit:
#
#
#     @classmethod
#     def obj2attr_names(cls, obj):
#         is_django_attr =
#         filter(obj.__dict__