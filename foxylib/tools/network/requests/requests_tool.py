import requests
from requests import Session
from requests.adapters import HTTPAdapter


# class RequestsTool:
#     @classmethod
#     def max_retries2http_adapter(cls, max_retries):
#         return HTTPAdapter(max_retries=max_retries)
from foxylib.tools.file.file_tool import FileTool


class SessionTool:
    @classmethod
    def session_adapter2https_mounted(cls, session, adapter):
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        return session

    @classmethod
    def simple_https_session(cls):
        # adapter = HTTPAdapter(max_retries=max_retries)
        return cls.session_adapter2https_mounted(Session(), HTTPAdapter())



# class HttpTool:
    # def url2httpr(cls, url, config=None):
    #     k_Session = config.get("Session",{}) if config else {}
    #     s = requests.Session(**k_Session)
    #
    #     k_HTTPAdapger = config.get("HttpAdapter",{}) if config else {}
    #     a = requests.adapters.HTTPAdapter(**k_HTTPAdapger)
    #     b = requests.adapters.HTTPAdapter(**k_HTTPAdapger)
    #     s.mount('http://', a)
    #     s.mount('https://', b)
    #
    #     k_get= config.get("get",{}) if config else {}
    #     return s.get(url, **k_get)

class RequestsTool:
    @classmethod
    def url2bytes(cls, url):
        return requests.get(url).content

    # @classmethod
    # def url2file(cls, url, filepath):
    #     bytes = requests.get(url).content
    #     FileTool.bytes2file(bytes, filepath)

    @classmethod
    def response2status_code(cls, response):
        return response.status_code

    @classmethod
    def response2is_ok(cls, response):
        return response.ok

    @classmethod
    def token2header_bearer(cls, token):
        return {"Authorization": f"Bearer {token}"}

    @classmethod
    def request2curl(cls, request):
        command = "curl -X {method} -H {headers} -d '{data}' '{uri}'"
        method = request.method
        uri = request.url
        data = request.body
        headers = ['"{0}: {1}"'.format(k, v) for k, v in request.headers.items()]
        headers = " -H ".join(headers)
        return command.format(method=method, headers=headers, data=data, uri=uri)


class FailedRequest(Exception):
    def __init__(self, response):
        self.response = response
