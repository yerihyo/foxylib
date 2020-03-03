from requests import Session
from requests.adapters import HTTPAdapter


# class RequestsTool:
#     @classmethod
#     def max_retries2http_adapter(cls, max_retries):
#         return HTTPAdapter(max_retries=max_retries)

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
    def response2status_code(cls, response):
        return response.status_code

    @classmethod
    def response2is_ok(cls, response):
        return response.ok

    @classmethod
    def request2curl(cls, request):
        command = "curl -X {method} -H {headers} -d '{data}' '{uri}'"
        method = request.method
        uri = request.url
        data = request.body
        headers = ['"{0}: {1}"'.format(k, v) for k, v in request.headers.items()]
        headers = " -H ".join(headers)
        return command.format(method=method, headers=headers, data=data, uri=uri)

# class PhantomjsToolkit:
#     @classmethod
#     def url2utf8(cls, url, phantomjs_dir, wait_sec=None, ):
#         PHANTOM_JS = os.path.join(phantomjs_dir, "bin", "phantomjs")
#
#         with Display(visible=0, size=(1024, 768)) as display:
#             browser = webdriver.PhantomJS(executable_path=PHANTOM_JS, service_args=['--load-images=no'])
#             browser.get(url)
#             if wait_sec:
#                 time.sleep(wait_sec)
#
#             element = browser.find_element_by_xpath('/html/body')
#             html = element.get_attribute("innerHTML")
#             browser.quit()
#
#             return str(Markup('<html><body>{0}</body></html>').format(html))
