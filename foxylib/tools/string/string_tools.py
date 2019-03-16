import ast


def str2strip(s): return s.strip() if s else s
def str2rstrip(s): return s.rstrip() if s else s
def str2split(s,*args,**kwargs): return s.split(*args,**kwargs) if s else s
def str2splitlines(s): return s.splitlines() if s else s
def str2lower(s): return s.lower() if s else s
def format_str(s, *args, **kwargs): return s.format(*args, **kwargs) if s else s
def join_str(s, *args, **kwargs): return s.join(*args, **kwargs) if s else s




class StringToolkit:
    @classmethod
    def quoted2stripped(cls, s_IN, ):
        try:
            module = ast.parse(s_IN)
        except SyntaxError:
            return s_IN

        node_list = module.body
        if len(node_list) != 1: return s_IN

        node_Expr = node_list[0]
        if not isinstance(node_Expr, ast.Expr): return s_IN

        node_Str = node_Expr.value
        if not isinstance(node_Str, ast.Str): return s_IN

        return node_Str.s

