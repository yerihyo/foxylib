from uuid import UUID

from foxylib.tools.binary2text.base64_tools import Base64Toolkit
from foxylib.tools.function.function_tools import FunctionToolkit


class UUIDToolkit:

    @classmethod
    def uuid2hex(cls, uuid):
        return uuid.hex if uuid is not None else None

    #     @classmethod
    #     def j_get(cls, j, uuid): return j.get(cls.uuid2hex(uuid))

    class NotUUIDException(Exception):
        pass

    @classmethod
    def x2uuid(cls, x_UUID):
        if x_UUID is None: return None
        if x_UUID == "null": return None

        if isinstance(x_UUID, UUID): return x_UUID
        try:
            if len(x_UUID) <= 24: return Base64Toolkit.b642uuid(x_UUID)
            return UUID(x_UUID)
        except ValueError as e:
            raise cls.NotUUIDException(x_UUID)

    @classmethod
    def x2hex(cls, x_UUID):
        uuid = cls.x2uuid(x_UUID)
        s = cls.uuid2hex(uuid)
        return s

    @classmethod
    def x2b64(cls, x_UUID):
        uuid = cls.x2uuid(x_UUID)
        if not uuid: return None
        return Base64Toolkit.uuid2b64(uuid)

    @classmethod
    def equals(cls, x1, x2, ):
        return cls.x2uuid(x1) == cls.x2uuid(x2)

    @classmethod
    def contains(cls, l, x):
        x_uuid = cls.x2uuid(x)

        for y in l:
            if cls.x2uuid(y) == x_uuid:
                return True

        return False
    has = contains

    @classmethod
    def contained_by(cls, x, l, ): return cls.contains(l, x)

    #     @classmethod
    #     def h2j_OLD(cls,h):
    #         if isinstance(h,dict):
    #             return {k:cls.h2j(v) for k,v in h.items()}
    #
    #         try:
    #             return UUIDToolkit.x2hex(h)
    #         except UUIDToolkit.NotUUIDException as e:
    #             return h

    @classmethod
    def _collection2convert_uuid(cls, x, kv2is_uuid, uuid_converter):
        if isinstance(x, list):
            return [cls._collection2convert_uuid(y, kv2is_uuid, uuid_converter) for y in x]

        if isinstance(x, dict):
            h = {}
            for k, v_IN in x.items():
                if kv2is_uuid(k, v_IN):
                    v_OUT = uuid_converter(v_IN)
                else:
                    v_OUT = cls._collection2convert_uuid(v_IN, kv2is_uuid, uuid_converter)
                h[k] = v_OUT
            return h

        return x

    @classmethod
    def h2j(cls, h, kv2is_uuid):
        return cls._collection2convert_uuid(h, kv2is_uuid, cls.x2hex, )

    @classmethod
    def j2h(cls, j, kv2is_uuid):
        return cls._collection2convert_uuid(j, kv2is_uuid, cls.x2uuid, )

uuid_in = UUIDToolkit.contained_by
uuid_not_in = FunctionToolkit.wrap2negate(uuid_in)
