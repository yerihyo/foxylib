import os
from functools import reduce

import time

import requests
from markupsafe import Markup
# from pyvirtualdisplay import Display
# from selenium import webdriver

class HttpTool:
    # @classmethod
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

    @classmethod
    def url2httpr(cls, url, args=None, kwargs=None, session=None, adapter=None, ):
        _a = args or []
        __k = kwargs or {}

        s = session or requests.Session()
        a = adapter or requests.adapters.HTTPAdapter()

        s.mount('http://', a)
        s.mount('https://', a)

        # k_get = config.get("get", {}) if config else {}
        return s.get(url, *_a, **__k)

    @classmethod
    def url_retries2httpr(cls, url, max_retries):
        adapter = requests.adapters.HTTPAdapter(max_retries=max_retries)
        return cls.url2httpr(url, adapter=adapter)

class HttprTool:
    @classmethod
    def httpr2status_code(cls, httpr): return httpr.status_code

    @classmethod
    def httpr2is_ok(cls, httpr): return httpr.ok

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
