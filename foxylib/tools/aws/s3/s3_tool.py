import re
import unicodedata
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
    @lru_cache(maxsize=1)
    def patttern_invalid_tagvalue(cls):
        # return re.compile(r'[^\p{L}\p{Z}\p{N}_.:/=+\-@]')
        return re.compile(r'[^\w\s_.:/=+\-@]')

    @classmethod
    def tagvalue2escaped(cls, str_in: str) -> str:
        return cls.patttern_invalid_tagvalue().sub(str_in, ' ')
        # return cls.patttern_invalid_tagvalue().sub(unicodedata.normalize('NFC',str_in), ' ')

    @classmethod
    def bucketname_key2uri(cls, bucketname:str, key:str):
        return f's3://{bucketname}/{key}'

    @classmethod
    def object2readable(cls, obj):
        return obj.get()['Body']

    """
    https://stackoverflow.com/questions/33842944/check-if-a-key-exists-in-a-bucket-in-s3-using-boto3
    """
    @classmethod
    def s3uri2exists(cls, resource, s3uri:str) -> bool:
        bucketname, s3key = cls.uri2bucket_key(s3uri)
        return cls.bucket_s3key2exists(resource.Bucket(bucketname), s3key)

    @classmethod
    def bucket_s3key2exists(cls, bucket, s3key: str) -> bool:
        try:
            bucket.Object(s3key).load()
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

    @classmethod
    def upload(cls, resource, s3uri, bdata, ):
        bucketname, s3key = cls.uri2bucket_key(s3uri)
        return resource.Bucket(bucketname).put_object(Key=s3key, Body=bdata)

    @classmethod
    def upload_unless_exists(cls, resource, s3uri, bdata, ):
        if S3Tool.s3uri2exists(resource, s3uri):
            return

        cls.upload(resource, s3uri, bdata)

    # @classmethod
    # def put_object_or_skip(cls, bucket, s3key, bdata,):
    #     s3uri = S3Tool.bucketname_key2uri(bucket.name, s3key)
    #     if S3Tool.s3uri2exists(s3uri):
    #         return
    #
    #     bucket.put_object(Key=s3key, Body=bdata, )

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
    def objectSummary2uri(cls, objectSummary):
        return cls.bucketname_key2uri(objectSummary.bucket_name, objectSummary.key)

    @classmethod
    def objectSummary2is_folder(cls, objectSummary):
        return objectSummary.key.endswith('/') and (objectSummary.size == 0)

    @classmethod
    def objectSummary2is_file(cls, objectSummary):
        return not cls.objectSummary2is_folder(objectSummary)
