class CompareTool:
    cmp_sign_str_pair = [(">", "gt"),
                         ("<", "lt"),
                         (">=", "gte"),
                         ("<=", "lte"),
                         ("==", "eq"),
                         ("!=", "ne"),
                         ]
    cmp_s_all = [x for kv in cmp_sign_str_pair for x in kv]

    @classmethod
    def h_cmp_s2str(cls):
        return dict([(x, y)
                        for k, v in cls.cmp_sign_str_pair
                        for x, y in [(k, v), (v, v)]])
    @classmethod
    def h_cmp_s2sign(cls):
        return dict([(x, y)
                         for k, v in cls.cmp_sign_str_pair
                         for x, y in [(v, k), (k, k)]])

    @classmethod
    def cmp_s2str(cls, s):
        return cls.h_cmp_s2str()[s]

    @classmethod
    def cmp_s2sign(cls, s):
        return cls.h_cmp_s2sign()[s]

    @classmethod
    def v_pair2is_cmp_satisfied(cls, v1, v2,
                         cmp_s=None,
                         ):
        if cmp_s is None: cmp_s = "=="
        s = cls.cmp_s2sign(cmp_s)

        invalid_null_as_False = True
        if invalid_null_as_False:
            if all([(v1 is None) or (v2 is None),
                    cmp_s not in ["==", "!="],  # trivial, but for later safety from copy&paste
                    ]):
                return False

        if s == "==": return v1 == v2
        if s == "!=": return v1 != v2
        if s == ">": return v1 > v2
        if s == ">=": return v1 >= v2
        if s == "<": return v1 < v2
        if s == "<=": return v1 <= v2

        raise NotImplementedError("Invalid cmp_s: {0}".format(cmp_s))

v_pair2is_cmp_satisfied = CompareTool.v_pair2is_cmp_satisfied