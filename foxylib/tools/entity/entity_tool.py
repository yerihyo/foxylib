class EntityConfig:
    class Field:
        LOCALE = "locale"
    F = Field

    @classmethod
    def j2locale(cls, j):
        if not j:
            return None

        return j.get(cls.F.LOCALE)



class Entity:
    class Field:
        SPAN = "span"
        VALUE = "value"
        TEXT = "text"
    F = Field



    @classmethod
    def j2span(cls, j):
        # print({"j":j,}) # 'j["span"]':j["span"]})
        return j[cls.F.SPAN]

    @classmethod
    def j2value(cls, j):
        return j[cls.F.VALUE]


    @classmethod
    def j_pair2span(cls, j_pair):
        return (Entity.j2span(j_pair[0])[0], Entity.j2span(j_pair[1])[1])
