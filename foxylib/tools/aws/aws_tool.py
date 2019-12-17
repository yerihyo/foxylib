import socket

from foxylib.tools.http.http_tool import HttpTool


class AWSTool:
    @classmethod
    def hostname2is_aws(cls, hostname):
        if hostname.startswith('domU-'): return True
        if hostname.startswith('ip-'): return True

        return False

    @classmethod
    def aws2ip(cls):
        hostname = socket.gethostname()
        if not cls.hostname2is_aws(hostname):
            return None # not AWS

        r = HttpTool.url_retries2httpr("http://169.254.169.254/latest/meta-data/public-ipv4", max_retries=5)
        if not r: return None

        return r.text
