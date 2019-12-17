class FlowcontrolTool:
    @classmethod
    def ternary(cls, v,
                f_cond=lambda x: x,
                f_null=None,
                f_true=lambda x: x,
                f_false=lambda x: x,
                ):

        c = f_cond(v)

        if c is None:
            if f_null is not None:
                return f_null(v)

        return f_true(v) if c else f_false(v)

ternary = FlowcontrolTool.ternary