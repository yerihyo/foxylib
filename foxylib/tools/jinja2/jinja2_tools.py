from jinja2 import Environment, BaseLoader

class Jinja2Toolkit:
    @classmethod
    def str_tmplt2render(cls, str_tmplt, data):
        rtemplate = Environment(loader=BaseLoader).from_string(str_tmplt)
        s_out = rtemplate.render(**data)
        return s_out