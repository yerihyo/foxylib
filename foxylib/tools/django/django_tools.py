from foxylib.tools.env.env_tools import EnvToolkit


class DjangoToolkit:
    @classmethod
    def django2setup(cls, django):
        django.setup()

    @classmethod
    def envfile_django2setup(cls, env_yamlfile, django):
        EnvToolkit.yaml_filepath2env(env_yamlfile)
        DjangoToolkit.django2setup(django)
