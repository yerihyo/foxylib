import requests


class HttpToolkit:
    @classmethod
    def url2httpr(cls, url, config=None):
        k_Session = config.get("Session",{}) if config else {}
        s = requests.Session(**k_Session)

        k_HTTPAdapger = config.get("HttpAdapter",{}) if config else {}
        a = requests.adapters.HTTPAdapter(**k_HTTPAdapger)
        b = requests.adapters.HTTPAdapter(**k_HTTPAdapger)
        s.mount('http://', a)
        s.mount('https://', b)

        k_get= config.get("get",{}) if config else {}
        s.get(url, **k_get)

    @classmethod
    def url_retries2httpr(cls, url, max_retries):
        return cls.url2httpr(url, config={"HttpAdapter":{"max_retries":max_retries}})