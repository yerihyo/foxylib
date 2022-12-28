import logging
from dataclasses import dataclass, asdict
from typing import List, Optional

from botocore.exceptions import ClientError
from dacite import from_dict

from foxylib.tools.dataclass.dataclass_tool import DataclassTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger


class SQSCreateQueue:
    @dataclass
    class Response:
        Messages: List[dict]
        HTTPStatusCode: int

    @classmethod
    def response2is_success(cls, response):
        code = response.get('HTTPStatusCode')
        return code == 200


class SQSSend:
    @dataclass
    class Message:
        Id: Optional[str]
        MessageBody: dict


class SQSReceive:
    @dataclass
    class Message:
        Body: dict
        MessageId: str
        ReceiptHandler: str

    @dataclass
    class Response:
        Messages: List


class SQSTool:
    @dataclass
    class Param:
        QueueName: str

    @classmethod
    def max_entrycount_per_request(cls):
        return 10

    @classmethod
    def name2url(cls, client, name):
        response = client.get_queue_url(
            QueueName=name,
        )
        url = response.get('QueueUrl')
        return url

    @classmethod
    def error2code(cls, error):
        return error.response['Error']['Code']

    @classmethod
    def param2get_or_create_url(cls, client, param: Param):
        logger = FoxylibLogger.func_level2logger(
                     cls.param2get_or_create_url, logging.DEBUG)

        name = param.QueueName

        try:
            url = cls.name2url(client, name)
            return url
        except ClientError as error:
            error_code = cls.error2code(error)
            logger.debug({'error_code':error_code})

            if error_code != 'AWS.SimpleQueueService.NonExistentQueue':
                raise error

        response = client.create_queue(**asdict(param))
        return response.get('QueueUrl')

    @classmethod
    def params2messages(cls, client, params):
        j_response = client.receive_message(**params)
        response = from_dict(SQSReceive.Response, j_response)
        return response.Messages


