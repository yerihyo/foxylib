import base64
from uuid import UUID


class Base64Toolkit:
    @classmethod
    def uuid2b64(cls,uuid): return base64.urlsafe_b64encode(uuid.bytes).decode('utf8').rstrip('=\n') # return uuid.bytes.encode('base64').rstrip('=\n').replace('/', '_')

    @classmethod
    def b642uuid(cls,b64): return UUID(bytes=base64.urlsafe_b64decode(b64 + '=='))
