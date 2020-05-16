import asyncio
import concurrent.futures
import json
import logging
import os
import signal
import time
from datetime import datetime
from functools import lru_cache
from multiprocessing import Process
from unittest import TestCase, mock
from unittest.mock import Mock, ANY

from aiohttp import web, WSCloseCode
from slack.web.slack_response import SlackResponse

from foxylib.tools.collections.collections_tool import l_singleton2obj
from slack import RTMClient, WebClient

from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.messenger.slack.events.file_shared import FileSharedEvent
from foxylib.tools.messenger.slack.foxylib_slack import FoxylibSlack, FoxylibChannel
from foxylib.tools.messenger.slack.methods.files.upload import FilesUploadMethod
from foxylib.tools.messenger.slack.methods.response_tool import SlackResponseTool
from foxylib.tools.messenger.slack.slack_tool import SlackFiletype, SlackFile, SlackTool, FileUploadMethod
from foxylib.tools.file.file_tool import FileTool
from foxylib.tools.file.mimetype_tool import MimetypeTool
from foxylib.tools.process.process_tool import ProcessTool



FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)


class TestFoxylibSlackAsyncio:
    def test_02(self):
        logger = FoxylibLogger.func_level2logger(self.test_02, logging.DEBUG)

        loop = asyncio.get_event_loop()
        rtm_client = RTMClient(token=FoxylibSlack.xoxb_token(), run_async=True, loop=loop)
        async def inf_loop():
            logger = logging.getLogger()
            while 1:
                try:
                    logger.info("Ping Pong! I'm alive")
                    await asyncio.sleep(900)
                except asyncio.CancelledError:
                    break

        tasks = asyncio.gather(rtm_client.start(), inf_loop())

        def callback(signum, frame):
            tasks.cancel()
            logger.warning("Cancelling tasks...")

        # loop.add_signal_handler(signal.SIGINT, callback)
        signal.signal(signal.SIGINT, callback)
        signal.signal(signal.SIGTERM, callback)

        try:
            loop.run_until_complete(tasks)
        except asyncio.CancelledError as e:
            logger.error(e)
        finally:
            logger.info("Quitting... Bye!")
            loop.close()


    def test_03(self):
        loop = asyncio.get_event_loop()
        rtm_client = RTMClient(token=FoxylibSlack.xoxb_token(), run_async=True, loop=loop)

        @RTMClient.run_on(event="open")
        async def typing_message(**payload):
            for i in range(5):
                time.sleep(2)
                print("Hi there @ {} : {}".format(i+1, datetime.now()))

            rtm_client = payload["rtm_client"]
            rtm_client.stop()
            # channel = FoxylibChannel.V.FOXYLIB
            # filepath = os.path.join(FILE_DIR, "test_01.txt")
            #
            # await FilesUploadMethod.invoke(web_client, channel, filepath)
            # await rtm_client.typing(channel="C01234567")

        @RTMClient.run_on(event='message')
        async def say_hello(**payload):
            data = payload['data']
            print(data.get('text'))

        def sync_loop():
            for i in range(5):
                time.sleep(2)
                print("Hi there @ {} : {}".format(i+1, datetime.now()))


        async def slack_main():
            # executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            await asyncio.gather(
                # loop.run_in_executor(executor, sync_loop),
                rtm_client.start()
            )

        asyncio.run(slack_main())

def mock_rtm_response():
    coro = Mock(name="RTMResponse")
    data = {
        "client": ANY,
        "http_verb": ANY,
        "api_url": ANY,
        "req_args": ANY,
        "data": {
            "ok": True,
            "url": "ws://localhost:8765",
            "self": {"id": "U01234ABC", "name": "robotoverlord"},
            "team": {
                "domain": "exampledomain",
                "id": "T123450FP",
                "name": "ExampleName",
            },
        },
        "headers": ANY,
        "status_code": 200,
    }
    coro.return_value = SlackResponse(**data)
    corofunc = Mock(name="mock_rtm_response", side_effect=asyncio.coroutine(coro))
    corofunc.coro = coro
    return corofunc

# @mock.patch("slack.WebClient._send", new_callable=mock_rtm_response)
class TestFoxylibSlackFunction:
    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    async def mock_server(self):
        app = web.Application()
        app["websockets"] = []
        app.router.add_get("/", self.websocket_handler)
        app.on_shutdown.append(self.on_shutdown)
        runner = web.AppRunner(app)
        await runner.setup()
        self.site = web.TCPSite(runner, "localhost", 8765)
        await self.site.start()

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        request.app["websockets"].append(ws)
        try:
            async for msg in ws:
                await ws.send_json({"type": "message", "message_sent": msg.json()})
        finally:
            request.app["websockets"].remove(ws)
        return ws

    async def on_shutdown(self, app):
        for ws in set(app["websockets"]):
            await ws.close(code=WSCloseCode.GOING_AWAY, message="Server shutdown")

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        task = asyncio.ensure_future(self.mock_server(), loop=self.loop)
        self.loop.run_until_complete(asyncio.wait_for(task, 0.1))

        self.client = RTMClient(
            token=FoxylibSlack.xoxb_token(), loop=self.loop, auto_reconnect=False
        )

    def test_01(self):
        channel = FoxylibChannel.V.FOXYLIB

        @RTMClient.run_on(event="open")
        async def typing_message(**payload):
            rtm_client = payload["rtm_client"]
            await rtm_client.typing(channel=channel)

        @RTMClient.run_on(event="message")
        def check_message(**payload):
            message = {"id": 1, "type": "typing", "channel": channel}
            rtm_client = payload["rtm_client"]
            self.assertDictEqual(payload["data"]["message_sent"], message)
            rtm_client.stop()

        self.client.start()



    def test_04(self):
        @RTMClient.run_on(event="open")
        async def typing_message(**payload):
            web_client = payload["web_client"]
            channel = FoxylibChannel.V.FOXYLIB
            filepath = os.path.join(FILE_DIR, "test_01.txt")

            await FilesUploadMethod.invoke(web_client, channel, filepath)
            await rtm_client.typing(channel="C01234567")

        @RTMClient.run_on(event=FileSharedEvent.NAME)
        def on_file_shared(**payload):
            message = {"id": 1, "type": "typing", "channel": "C01234567"}
            rtm_client = payload["rtm_client"]
            self.assertDictEqual(payload["data"]["message_sent"], message)
            rtm_client.stop()

        FoxylibSlack.rtm_client().start()
        raise Exception()


    def test_05(self):
        def on_file_shared(**kwargs):
            j_event = kwargs.get("data")
            j_file_list = FileSharedEvent.j_event2j_file_list(j_event)
            self.assertEqual(len(j_file_list), 1)

            j_file = l_singleton2obj(j_file_list)
            filename = SlackFile.j_file2filename(j_file)
            self.assertEqual(filename, "test_01.txt")

            raise Exception()


        RTMClient.on(event="file_shared",
                     callback=on_file_shared
                     )

        rtm_client = FoxylibSlack.rtm_client()
        rtm_client.start()

        # p = Process(target=rtm_client.start)
        # p.start()


        web_client = FoxylibSlack.web_client()
        channel = FoxylibChannel.V.FOXYLIB
        filepath = os.path.join(FILE_DIR, "test_01.txt")
        response = FilesUploadMethod.invoke(web_client, channel, filepath)
