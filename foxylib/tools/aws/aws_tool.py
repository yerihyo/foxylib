import socket
from requests.adapters import HTTPAdapter

from foxylib.tools.network.requests.requests_tool import SessionTool


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

        session = SessionTool.session_adapter2https_mounted(adapter=HTTPAdapter(max_retries=5))
        response = session.get("http://169.254.169.254/latest/meta-data/public-ipv4")

        # r = HttpTool.url_retries2response("http://169.254.169.254/latest/meta-data/public-ipv4", max_retries=5)
        if not response: return None

        return response.text
