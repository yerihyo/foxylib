import os

from jinja2 import Environment, BaseLoader, FileSystemLoader


class Jinja2Toolkit:
    @classmethod
    def tmplt_str2str(cls, str_tmplt, data):
        rtemplate = Environment(loader=BaseLoader).from_string(str_tmplt)
        s_out = rtemplate.render(**data)
        return s_out

    @classmethod
    def tmplt_file2str(cls, filepath, data):
        file_dir, base_name = os.path.split(filepath)
        loader = FileSystemLoader(file_dir)
        rtemplate = Environment(loader=loader).get_template(base_name)
        s_out = rtemplate.render(**data)
        return s_out

tmplt_str2str = Jinja2Toolkit.tmplt_str2str
tmplt_file2str = Jinja2Toolkit.tmplt_file2str