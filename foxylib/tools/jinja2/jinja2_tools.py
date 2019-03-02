from jinja2 import Environment, BaseLoader

class Jinja2Toolkit:
    @classmethod
    def str_tmplt2str(cls, str_tmplt, data):
        rtemplate = Environment(loader=BaseLoader).from_string(str_tmplt)
        s_out = rtemplate.render(**data)
        return s_out

    @classmethod
    def file_tmplt2str(cls, filepath, data):
        rtemplate = Environment(loader=BaseLoader).get_template(filepath)
        s_out = rtemplate.render(**data)
        return s_out

str_tmplt2str = Jinja2Toolkit.str_tmplt2str