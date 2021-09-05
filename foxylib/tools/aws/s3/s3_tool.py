import re
from functools import lru_cache

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
