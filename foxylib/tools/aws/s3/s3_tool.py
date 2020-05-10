from future.utils import lfilter

from foxylib.tools.file.file_tool import FileTool

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
    def s3path2exploded(cls, s3_path):

    @classmethod
    def list_bucket_objects(cls, client, bucket: str) -> [dict]:
        paginator = client.get_paginator('list_objects_v2')
        response_iterator = paginator.paginate(
            Bucket='string',
            Delimiter='string',
            EncodingType='url',
            Prefix='string',
            PaginationConfig={
                'MaxItems': 123,
                'PageSize': 123,
                'StartingToken': 'string'
            }
        )

        try:
            contents = client.list_objects_v2(Bucket=bucket)['Contents']
        except KeyError:
            # No Contents Key, empty bucket.
            return []
        else:
            return contents

    @classmethod
    def local2s3(cls, local_dir, s3_dir):
        """
        Sync source to dest, this means that all elements existing in
        source that not exists in dest will be copied to dest.

        No element will be deleted.

        :param source: Source folder.
        :param dest: Destination folder.

        :return: None
        """

        path_list_local = lfilter(lambda path: not path.is_dir(), local_dir.rglob("*"))


        objects = self.list_bucket_objects(dest)

        # Getting the keys and ordering to perform binary search
        # each time we want to check if any paths is already there.
        object_keys = [obj['Key'] for obj in objects]
        object_keys.sort()
        object_keys_length = len(object_keys)

        for path in paths:
            # Binary search.
            index = bisect_left(object_keys, path)
            if index == object_keys_length:
                # If path not found in object_keys, it has to be sync-ed.
                self._s3.upload_file(str(Path(source).joinpath(path)), Bucket=dest, Key=path)