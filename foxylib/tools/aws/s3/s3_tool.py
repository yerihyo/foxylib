import re
from functools import lru_cache
from typing import Tuple
from urllib.parse import urlparse

import botocore.exceptions

from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.version.version_tool import VersionTool


class S3Content:
    """
    List all objects for the given bucket.

    :param bucket: Bucket name.
    :return: A [dict] containing the elements in the bucket.

    Example of a single object.

    {
        'Key': 'example/example.txt',
        'LastModified': datetime.datetime(2019, 7, 4, 13, 50, 34, 893000, tzinfo=tzutc()),
        'ETag': '"b11564415be7f58435013b414a59ae5c"',
        'Size': 115280,
        'StorageClass': 'STANDARD',
        'Owner': {
            'DisplayName': 'webfile',
            'ID': '75aa57f09aa0c8caeab4f8c24e99d10f8e7faeebf76c078efc7c6caea54ba06a'
        }
    }

    """

    @classmethod
    def content2key(cls, content):
        return content


class S3Tool:
    @classmethod
    def bucketname_key2uri(cls, bucketname:str, key:str):
        return f's3://{bucketname}/{key}'

    @classmethod
    def bucket_key2exists(cls, bucket, key:str) -> bool:
        try:
            bucket.Object(key).load()
            # s3.Object('my-bucket', 'dootdoot.jpg').load()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                # The object does not exist.
                return False
            else:
                # Something else has gone wrong.
                raise
        else:
            # The object does exist.
            return True

    """
    https://stackoverflow.com/a/42641363/1902064
    """
    @classmethod
    def uri2bucket_key(cls, uri:str) -> Tuple[str,str]:
        o = urlparse(uri, allow_fragments=False)
        return o.netloc, o.path.lstrip('/')

    @classmethod
    def uri2bucket(cls, uri: str) -> str:
        return cls.uri2bucket_key(uri)[0]

    @classmethod
    def uri2key(cls, uri: str) -> str:
        return cls.uri2bucket_key(uri)[1]

    # @classmethod
    # def uri2key(cls, uri: str) -> str:
    #     o = urlparse(uri, allow_fragments=False)
    #     return o.netloc, o.path.lstrip('/')

    # @classmethod
    # def objectSummary2obj(cls, resource, objectSummary):
    #     return resource.Object(objectSummary.bucket_name, objectSummary.key)

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=1))
    def pattern_prefix(cls):
        return re.compile(r"s3://")

    @classmethod
    def path2exploded(cls, path):
        m = cls.pattern_prefix().match(path)
        body = path if not m else path[m.span()[1]:]

        bucket, prefix = body.split("/", maxsplit=1)
        return bucket, prefix


    @classmethod
    def path2contents(cls, client, s3_path: str) -> [dict]:
        paginator = client.get_paginator('list_objects_v2')
        bucket, prefix = cls.path2exploded(s3_path)

        pages = paginator.paginate(Bucket=bucket, Prefix=prefix,)
        for page in pages:
            contents = page['Contents']
            yield from contents

    @classmethod
    @VersionTool.incomplete(reason="not needed")
    def local2s3(cls, local_dir, s3_path):
        # https://stackoverflow.com/a/56892500
        pass

    @classmethod
    def objectSummary2is_folder(cls, objectSummary):
        return objectSummary.key.endswith('/') and (objectSummary.size == 0)

    @classmethod
    def objectSummary2is_file(cls, objectSummary):
        return not cls.objectSummary2is_folder(objectSummary)
