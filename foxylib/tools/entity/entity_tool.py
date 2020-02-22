class EntityConfig:
    class Field:
        LOCALE = "locale"


    @classmethod
    def j2locale(cls, j):
        if not j:
            return None

        return j.get(cls.Field.LOCALE)



class Entity:
    class Field:
        SPAN = "span"
        VALUE = "value"
        TEXT = "text"




    @classmethod
    def j2span(cls, j):
        # print({"j":j,}) # 'j["span"]':j["span"]})
        return j[cls.Field.SPAN]

    @classmethod
    def j2value(cls, j):
        return j[cls.Field.VALUE]


    @classmethod
    def j_pair2span(cls, j_pair):
        return (Entity.j2span(j_pair[0])[0], Entity.j2span(j_pair[1])[1])
